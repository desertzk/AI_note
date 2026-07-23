# Occupancy Profiling Counter Summary

This note summarizes the rocprofv3 counters collected for `occupancy_kernel`, explains which results are valid, and defines how to evaluate the new eightfold-oversubscribed workload.

## Plain-Language Walkthrough

This document is trying to answer one main question:

> While `occupancy_kernel` was running, how much of the GPU's capacity for
> resident wavefronts was actually occupied?

It distinguishes **theoretical occupancy**, **achieved occupancy**, and **GPU
utilization**. These sound similar, but they measure different things.

### 1. Essential HIP Terms

- **Work item/thread**: One execution of the kernel.
- **Wavefront**: A group of 32 work items executed together on this GPU.
- **Block/workgroup**: A group of 256 work items.
- **CU (Compute Unit)**: Hardware that holds and executes wavefronts.
- **Resident wave**: A wavefront currently loaded into a CU. It may be executing
  or waiting.
- **Occupancy**: The fraction of available resident-wave slots that are
  occupied, averaged over time.

Because the block size is 256 and the wave size is 32:

$$
\text{waves per block} = \frac{256}{32} = 8
$$

Therefore, every block creates eight wavefronts.

### 2. Theoretical Occupancy

The HIP occupancy API says that each HIP-visible CU can hold eight blocks of
this kernel. Each block has eight waves, so one CU can hold:

$$
8\ \text{blocks} \times 8\ \text{waves per block}
= 64\ \text{waves}
$$

The reported hardware maximum is also 64 waves per HIP-visible CU.
Consequently, the kernel is **eligible** for 100% occupancy.

This does not mean it will maintain 100% occupancy throughout execution. It
only means resources such as registers, LDS, and scratch memory do not prevent
it.

A useful analogy is a theater:

- Theoretical occupancy says all seats *can* be filled.
- Achieved occupancy measures how many seats were occupied on average.
- It does not assume that all seats were full for the entire performance.

### 3. Why the GPU Appears to Have Both 32 and 64 CUs

HIP reports:

$$
32\ \text{units} \times 64\ \text{wave slots}
= 2048\ \text{wave slots}
$$

rocprof and `amd-smi` report:

$$
64\ \text{physical CUs} \times 32\ \text{wave slots}
= 2048\ \text{wave slots}
$$

Because WGP have 2 CU inside.These are two different ways of grouping the same hardware capacity. The total
capacity remains 2,048 resident wave slots.

This distinction is important because the HIP program calculates its grid
using the 32-unit view, while rocprof calculates occupancy using the 64-CU
view.

### 4. The Original Grid

With multiplier 1, the program launches 256 blocks:

$$
32\ \text{HIP CUs} \times 8\ \text{blocks per CU}
= 256\ \text{blocks}
$$

The total number of waves is:

$$
256\ \text{blocks} \times 8\ \text{waves per block}
= 2048\ \text{waves}
$$

This is exactly one complete theoretical resident set: enough work to fill the
GPU once.

GPU work does not start and finish perfectly simultaneously:

1. Waves are gradually dispatched.
2. CUs become full after a ramp-up period.
3. Some blocks finish before others.
4. Near the end, no replacement blocks remain.
5. Occupancy declines while the final blocks drain.

Thus, the GPU might reach high occupancy in the middle but have lower
**time-averaged occupancy**.

### 5. Why the Grid Was Increased Eightfold

The current grid multiplier is 8:

$$
256\ \text{resident-grid blocks} \times 8
= 2048\ \text{blocks}
$$

That produces:

$$
2048\ \text{blocks} \times 8\ \text{waves per block}
= 16384\ \text{waves}
$$

Only 2,048 wave slots can be occupied simultaneously. The other waves wait in
the queue.

As resident blocks finish, waiting blocks replace them. This should keep the
GPU full for longer and reduce the relative impact of startup and shutdown.

The eightfold grid therefore does **not** increase maximum simultaneous
occupancy. It increases the amount of queued work, allowing high occupancy to
be sustained longer.

### 6. Why the First Profiling Result Was Invalid

The initial profiling run used automatic GPU power management, `AUTO`.

On gfx11 and gfx12 GPUs, rocprofiler requires a stable power state for reliable
counter collection. In `AUTO`, the result included:

```text
SQ_WAVE_CYCLES = 0
OccupancyPercent = 0
```

`SQ_WAVE_CYCLES` is the total number of cycles accumulated by resident waves. A
real kernel dispatch containing 2,048 waves should not normally produce zero
resident-wave cycles.

Therefore, the zero occupancy does not mean the GPU had no occupancy. It means
the required raw counter was not collected correctly.

Some values from that run are still meaningful:

```text
Wavefronts = 2048
GPU_UTIL = 100%
```

These say:

- 2,048 waves were dispatched.
- The GPU was active throughout the collection interval.

They do not establish how many waves were resident simultaneously.

### 7. The Valid Stable Baseline

The GPU was then set to `STABLE_STD`, and multiplier 1 was measured again:

```text
SQ_WAVE_CYCLES = 51,703,788,945
GRBM_GUI_ACTIVE = 37,421,018
MeanOccupancyPerCU = 21.588715
OccupancyPercent = 67.464735%
```

rocprof calculates the average resident waves per physical CU as:

$$
\frac{\text{SQ\_WAVE\_CYCLES}}
{\text{GRBM\_GUI\_ACTIVE} \times \text{physical CUs}}
$$

Substituting the values:

$$
\frac{51{,}703{,}788{,}945}
{37{,}421{,}018 \times 64}
= 21.588715
$$

Each physical CU supports 32 waves, so:

$$
\frac{21.588715}{32} \times 100
= 67.464735\%
$$

In plain language:

> During the measured GPU-active interval, each physical CU contained about
> 21.59 of its possible 32 resident waves on average.

This is a valid achieved-occupancy result because `SQ_WAVE_CYCLES` is nonzero.

### 8. Active-CU Occupancy Versus All-CU Occupancy

The baseline reports:

```text
MeanOccupancyPerActiveCU = 44.200200
MeanOccupancyPerCU       = 21.588715
```

These use different averaging rules:

- `MeanOccupancyPerActiveCU` considers CUs during periods when they were active.
- `MeanOccupancyPerCU` averages across all physical CUs, including CUs that were
  inactive during parts of the interval.

This is why the active-CU number can be much larger. For overall GPU occupancy,
the document uses `MeanOccupancyPerCU` and `OccupancyPercent`.

### 9. What Each Important Counter Means

`SQ_WAVES` or `Wavefronts` is the total number of waves dispatched:

$$
\text{blocks} \times \text{waves per block}
$$

For the new grid, it should equal 16,384. It verifies launch geometry but says
nothing about simultaneous residency.

`SQ_WAVE_CYCLES` is the sum of cycles during which waves were resident. This is
the key numerator for occupancy calculations. If it is zero, the occupancy
results are invalid.

`GRBM_GUI_ACTIVE` is the number of cycles for which the GPU was considered
active. rocprof uses this to calculate occupancy averaged across all CUs.

`SQ_BUSY_CYCLES` counts cycles during which shader sequencers were busy. It is
used for active-CU occupancy calculations.

`OccupancyPercent` is time-averaged resident waves divided by maximum
resident-wave capacity. This is the principal final result.

`GPU_UTIL` is the percentage of the collection interval during which the GPU
was active. A value of 100% does not mean all CUs were full.

`VALUBusy` describes how much GPU time involved vector arithmetic processing.
It measures execution-unit activity, not resident-wave occupancy.

### 10. Occupancy Is Not the Same as Performance

A high occupancy percentage does not automatically mean that the kernel runs
efficiently.

For example, many waves can be resident while they all wait for memory. That
would give:

- high occupancy;
- potentially low instruction throughput;
- potentially poor performance.

Conversely, a kernel may have lower occupancy but fully saturate memory
bandwidth or an arithmetic pipeline. Adding more waves would not necessarily
make it faster.

Occupancy should therefore be treated as a scheduling and resource-residency
metric, not a direct speed score.

### 11. What the Profiling Script Does

Run:

```bash
cd /home/amd/zk/hip_programming_examples/hip_occupancy_demo
./profile_stable_occupancy.sh
```

The script performs this sequence:

1. Uses `sudo` to put GPU 0 into `stable_std`.
2. Runs rocprofv3 against `occupancy_kernel`.
3. Collects the listed counters in one execution.
4. Restores the power mode to `auto`, even if profiling fails.
5. Displays the report.
6. Rejects results where `SQ_WAVE_CYCLES` or `OccupancyPercent` is zero.

The underlying profiler command has this form:

```bash
rocprofv3 [profiler options] -- ./hip_occupancy_demo
```

The `--` is important:

- Everything before `--` belongs to rocprofv3.
- Everything after `--` is the application and its arguments.

For example:

```bash
rocprofv3 [profiler options] -- ./hip_occupancy_demo 500000 8
```

This runs the application with arguments `500000` and `8`; they are not
profiler options.

### 12. What Result Is Expected Next

The multiplier-8 workload has not yet been measured according to this document.
The main expected checks are:

```text
SQ_WAVES = 16384
SQ_WAVE_CYCLES > 0
GRBM_GUI_ACTIVE > 0
SQ_BUSY_CYCLES > 0
0 < OccupancyPercent <= 100
```

Interpretation:

- **80-100%**: Queued replacement blocks successfully reduced ramp-up and
  tail-drain losses.
- **Around 67%**: Oversubscription did not materially help, so scheduling
  distribution or counter averaging may be responsible.
- **0% with `SQ_WAVE_CYCLES = 0`**: Invalid collection.
- **Above 100%**: Counter, formula, or hardware-topology mismatch.

The shortest summary is:

> The kernel can theoretically occupy every wave slot. The valid one-batch
> measurement averaged 67.46% because startup and shutdown periods were
> included. The eightfold grid queues more blocks so that completed blocks can
> be replaced, and the next stable-power profiling run will determine whether
> this raises achieved occupancy toward 80-100%.

## Result States

Three profiling states must not be mixed:

| State               | Power mode                  | Grid multiplier | Result status                                               |
| ------------------- | --------------------------- | ---------------:| ----------------------------------------------------------- |
| Initial counter run | `AUTO`                      | 1               | Occupancy counters invalid because `SQ_WAVE_CYCLES = 0`     |
| Stable baseline     | `STABLE_STD`                | 1               | Valid achieved occupancy: 67.464735%                        |
| Current workload    | Requires `STABLE_STD` rerun | 8               | Not measured yet; designed to reduce ramp-up and tail drain |

A long Perfetto kernel rectangle proves that the kernel remained in flight. It does not prove high occupancy. Achieved occupancy must come from valid, nonzero occupancy counters.

## Current Workload Geometry

The program calls `hipModuleOccupancyMaxActiveBlocksPerMultiprocessor` and currently reports:

```text
HIP-reported compute units:       32
Wave size:                        32
Block size:                       256 work items
Active blocks per reported CU:     8
Waves per block:                   8
Resident waves per reported CU:   64
Maximum waves per reported CU:    64
Resident grid:                   256 blocks
Grid multiplier:                   8
Actual grid:                    2048 blocks
Total work items:             524288
Expected dispatched waves:      16384
```

The resident-set calculation is:

$$
8\ \text{blocks per CU} \times 8\ \text{waves per block}
= 64\ \text{resident waves per CU}
$$

The runtime reports a maximum of 64 waves per HIP-visible CU, so the kernel is eligible for 100% theoretical resident-wave occupancy.

The current total wave count should be:

$$
2048\ \text{blocks} \times 8\ \text{waves per block}
= 16384\ \text{waves}
$$

The eightfold grid does not change the maximum simultaneous residency. It keeps replacement blocks queued after the first resident set retires, which should reduce average occupancy lost during dispatch ramp-up and tail drain.

## Counter Meanings

| Counter                    | Meaning                                                  | What it does not prove         |
| -------------------------- | -------------------------------------------------------- | ------------------------------ |
| `SQ_WAVES` / `Wavefronts`  | Total dispatched waves                                   | Simultaneous residency         |
| `SQ_WAVE_CYCLES`           | Sum of resident-wave cycles                              | Useful work or VALU throughput |
| `SQ_BUSY_CYCLES`           | Cycles in which shader sequencers were busy              | Full occupancy                 |
| `GRBM_GUI_ACTIVE`          | GPU-active cycles                                        | All CUs were full              |
| `MeanOccupancyPerActiveCU` | Average resident waves on CUs active during the interval | Average across inactive CUs    |
| `MeanOccupancyPerCU`       | Average resident waves across all physical CUs           | Peak occupancy                 |
| `OccupancyPercent`         | Time-averaged resident waves as percentage of maximum    | Performance efficiency         |
| `GPU_UTIL`                 | Percentage of collection interval with GPU activity      | CU saturation                  |
| `VALUBusy`                 | Percentage of GPU time processing VALU instructions      | Occupancy by itself            |

### How `SQ_WAVE_CYCLES` and `GRBM_GUI_ACTIVE` Produce Mean Occupancy

`SQ_WAVE_CYCLES` is approximately the sum of resident-wave cycles across the
GPU. In one GPU cycle, each resident wave contributes one wave-cycle. For
example, 10 resident waves present for one cycle contribute 10 wave-cycles.
A resident wave normally contributes even when it is stalled or waiting, so
this counter measures residency rather than useful instruction throughput.

Conceptually:

$$
\text{SQ\_WAVE\_CYCLES}
= \sum_{\text{cycles}} \text{number of resident waves}
$$

`GRBM_GUI_ACTIVE` counts global GPU cycles during which the GPU was active
processing work. It is a time counter for the GPU as a whole, not a separate
counter for each CU. A nonzero value does not mean that every CU was active,
every wave slot was occupied, or every arithmetic unit was executing during
every counted cycle.

To obtain the total number of CU-cycle observations, multiply the global active
cycles by the number of physical CUs:

$$
\text{total CU-cycles}
= \text{GRBM\_GUI\_ACTIVE} \times \text{physical CUs}
$$

The units in the mean-occupancy formula are therefore:

$$
\frac{\text{SQ\_WAVE\_CYCLES}}
{\text{GRBM\_GUI\_ACTIVE} \times \text{physical CUs}}
= \frac{\text{wave-cycles}}{\text{CU-cycles}}
= \text{average resident waves per CU}
$$

For the stable multiplier-1 measurement:

$$
\text{total CU-cycles}
= 37{,}421{,}018 \times 64
= 2{,}394{,}945{,}152
$$

$$
\text{MeanOccupancyPerCU}
= \frac{51{,}703{,}788{,}945}{2{,}394{,}945{,}152}
= 21.588715\ \text{resident waves per physical CU}
$$

Because each physical CU supports at most 32 resident waves, the corresponding
occupancy percentage is:

$$
\text{OccupancyPercent}
= \frac{21.588715}{32} \times 100
= 67.464735\%
$$

As a small example, suppose a GPU has two CUs and is active for three cycles:

| Cycle | CU 0 resident waves | CU 1 resident waves |
| -----:| -------------------:| -------------------:|
| 1     | 4                   | 2                   |
| 2     | 4                   | 4                   |
| 3     | 2                   | 2                   |

The accumulated resident-wave cycles are:

$$
\text{SQ\_WAVE\_CYCLES} = 4+2+4+4+2+2 = 18
$$

The denominator contains six CU-cycles:

$$
\text{GRBM\_GUI\_ACTIVE} \times \text{physical CUs}
= 3 \times 2 = 6
$$

The mean occupancy is therefore $18/6=3$ resident waves per CU. In short,
`SQ_WAVE_CYCLES` is accumulated residency, while `GRBM_GUI_ACTIVE` times the
physical CU count is the accumulated CU time over which that residency is
averaged.

High occupancy is not automatically high performance. A kernel can have many resident waves but spend most cycles waiting, or have lower occupancy while fully utilizing a bottlenecked execution unit.

## Invalid Auto-Power Run

The initial run used automatic power management. rocprofiler-sdk requires gfx11 and gfx12 GPUs to use a stable power state for counter collection.

The auto-power run reported:

| Counter                    | Value | Validity                                          |
| -------------------------- | -----:| ------------------------------------------------- |
| `Wavefronts`               | 2048  | Valid dispatch count for multiplier 1             |
| `GPU_UTIL`                 | 100%  | GPU remained active during collection             |
| `SQ_WAVE_CYCLES`           | 0     | Invalid                                           |
| `OccupancyPercent`         | 0     | Invalid because its numerator was zero            |
| `MeanOccupancyPerActiveCU` | 0     | Invalid because its numerator was zero            |
| `MeanOccupancyPerCU`       | 0     | Invalid because its numerator was zero            |
| `VALUBusy`                 | 0     | Invalid because its raw VALU-cycle input was zero |

Do not interpret those occupancy zeros as real 0% occupancy.

## Valid Stable Baseline

After setting GPU 0 to `STABLE_STD`, multiplier 1 produced:

| Counter                    | Value           |
| -------------------------- | ---------------:|
| `GRBM_GUI_ACTIVE`          | 37,421,018      |
| `SQ_BUSY_CYCLES`           | 1,169,763,684   |
| `SQ_WAVE_CYCLES`           | 51,703,788,945  |
| `SQ_WAVES`                 | 2,048           |
| `MeanOccupancyPerActiveCU` | 44.200200 waves |
| `MeanOccupancyPerCU`       | 21.588715 waves |
| `OccupancyPercent`         | 67.464735%      |

These values are valid because `SQ_WAVE_CYCLES` is nonzero.

rocprof's gfx1201 occupancy formula uses 64 physical CUs and a maximum of 32 waves per physical CU. The measured average is:

$$
\frac{51{,}703{,}788{,}945}
{37{,}421{,}018 \times 64}
= 21.588715\ \text{waves per physical CU}
$$

The percentage is:

$$
\frac{21.588715}{32} \times 100
= 67.464735\%
$$

The HIP runtime reports 32 larger scheduling units with up to 64 waves each, while `amd-smi` and rocprof expose 64 physical CUs with up to 32 waves each. Both views describe the same total capacity:

$$
32 \times 64 = 64 \times 32 = 2048\ \text{resident wave slots}
$$

## Why The Baseline Was Below 80%

Multiplier 1 launched exactly one theoretical resident set: 256 blocks. Even when every block is eligible for full residency, time-averaged occupancy loses cycles during:

- command and wave launch ramp-up;
- block distribution across CUs;
- blocks finishing at slightly different times;
- tail drain when too few blocks remain to refill every CU.

The valid 67.46% result is therefore not contradictory to 100% theoretical occupancy. Theoretical occupancy is a resource limit; achieved occupancy is averaged over time.

## Profile The New Eightfold Grid

Run:

```bash
cd /home/amd/zk/hip_programming_examples/hip_occupancy_demo
./profile_stable_occupancy.sh
```

The script:

1. Sets GPU 0 to `stable_std` with `sudo`.
2. Runs the occupancy counters against the current multiplier-8 executable.
3. Restores GPU 0 to `auto`, including after failure.
4. Prints the counter report.
5. Rejects zero `SQ_WAVE_CYCLES` or zero `OccupancyPercent`.

### rocprofv3 Counter Command

The helper script runs this profiler command after entering `STABLE_STD` mode:

```bash
rocprofv3 \
  --pmc OccupancyPercent MeanOccupancyPerActiveCU MeanOccupancyPerCU \
        SQ_WAVE_CYCLES SQ_BUSY_CYCLES GRBM_GUI_ACTIVE SQ_WAVES \
  --kernel-include-regex 'occupancy_kernel' \
  --output-format csv \
  --output-file stable_occupancy \
  --output-directory rocprof_stable_occupancy \
  -- ./hip_occupancy_demo
```

The `--` separator ends rocprofv3 options. Everything after it is the application
command and its arguments. To test a different workload size, append arguments:

```bash
rocprofv3 [profiler options] -- ./hip_occupancy_demo 500000 8
```

Profiler options:

| Option                                        | Meaning in this command                                                                                       |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `--pmc ...`                                   | Collects the listed performance-monitor counters for each selected kernel dispatch                            |
| `--kernel-include-regex 'occupancy_kernel'`   | Collects counters only for kernels whose name matches `occupancy_kernel`; runtime helper kernels are excluded |
| `--output-format csv`                         | Writes tabular counter records suitable for formulas and scripts                                              |
| `--output-file stable_occupancy`              | Uses `stable_occupancy` as the report-name prefix                                                             |
| `--output-directory rocprof_stable_occupancy` | Places reports in that directory instead of the default hostname/PID directory                                |
| `--`                                          | Separates profiler arguments from the executable command                                                      |
| `./hip_occupancy_demo`                        | Runs the current executable, whose default grid multiplier is 8                                               |

Counter purposes:

| Counter                    | Why it is collected                                                            |
| -------------------------- | ------------------------------------------------------------------------------ |
| `OccupancyPercent`         | Final achieved occupancy as a percentage of maximum resident-wave capacity     |
| `MeanOccupancyPerActiveCU` | Average resident waves over only CUs that were active                          |
| `MeanOccupancyPerCU`       | Average resident waves over all physical CUs                                   |
| `SQ_WAVE_CYCLES`           | Numerator used by the derived occupancy formulas; must be nonzero              |
| `SQ_BUSY_CYCLES`           | Denominator for occupancy on active CUs                                        |
| `GRBM_GUI_ACTIVE`          | GPU-active cycle count used for occupancy averaged over all CUs                |
| `SQ_WAVES`                 | Total dispatched waves; validates grid geometry but not simultaneous residency |

All counters are requested with one `--pmc`, so rocprofv3 attempts to collect
them in one application pass. Keeping formula inputs and derived outputs in the
same pass avoids comparing different executions. If the hardware reports a
counter-group compatibility error, split the raw and derived metrics into
multiple quoted `--pmc` groups, but do not combine values from different passes
as though they came from one dispatch.

Expected output files include:

```text
rocprof_stable_occupancy/stable_occupancy_counter_collection.csv
rocprof_stable_occupancy/stable_occupancy_agent_info.csv
```

Each counter-collection row identifies the process, kernel, queue, grid size,
workgroup size, register usage, counter name, counter value, and dispatch start
and end timestamps. The helper's `awk` block reads columns 16 and 17, which are
`Counter_Name` and `Counter_Value`.

Expected structural checks:

```text
SQ_WAVES = 16384
SQ_WAVE_CYCLES > 0
GRBM_GUI_ACTIVE > 0
```

Interpret occupancy using these ranges:

| `OccupancyPercent`           | Interpretation                                                           |
| ----------------------------:| ------------------------------------------------------------------------ |
| 0 with zero `SQ_WAVE_CYCLES` | Invalid collection                                                       |
| Below 50%                    | Low achieved residency; investigate grid, resources, imbalance, or waits |
| 50-80%                       | Moderate achieved occupancy                                              |
| 80-100%                      | High achieved occupancy                                                  |
| Above 100%                   | Invalid formula, topology mismatch, or counter issue                     |

For this kernel, an 80-100% result would confirm that oversubscription successfully amortized the one-batch ramp-up and tail effects. A result near 67% would suggest another limiting factor, such as scheduler distribution or the counter's averaging semantics.

## Output Files

| Path                                                                 | Contents                                                               |
| -------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `rocprof_stable_occupancy/stable_occupancy_counter_collection.csv`   | Valid multiplier-1 stable baseline; overwritten by the next helper run |
| `rocprof_occupancy/pass_1/occupancy_counters_counter_collection.csv` | Invalid auto-power occupancy-derived metrics                           |
| `rocprof_occupancy/pass_2/occupancy_counters_counter_collection.csv` | Auto-power utilization metrics                                         |
| `rocprof_raw/raw_counters_counter_collection.csv`                    | Raw counter diagnostic run                                             |
| `rocprof_trace/occupancy_trace_kernel_stats.csv`                     | Kernel duration summary                                                |
| `rocprof_trace/occupancy_trace_kernel_trace.csv`                     | Grid, block, register, scratch, stream, and timestamp data             |
| `rocprof_trace/occupancy_trace_results.pftrace`                      | Perfetto timeline                                                      |

## Trace Results

The earlier multiplier-1 trace reported:

```text
Kernel:           occupancy_kernel
Duration:         21.702660 ms
Workgroup size:   256
Grid size:        65536 work items
VGPR count:       8
SGPR count:       128
LDS block size:   0
Scratch size:     0
Stream ID:        0
Queue ID:         1
```

Low VGPR use, no LDS, and no scratch are consistent with the occupancy API allowing eight blocks per HIP-visible CU. The trace establishes launch geometry and duration, but not achieved occupancy.

## Minimum Validity Checklist

Before trusting an occupancy result, verify all of the following:

- GPU 0 was set to `STABLE_STD` during collection.
- The script restored GPU 0 to `AUTO` afterward.
- `SQ_WAVE_CYCLES` is nonzero.
- `GRBM_GUI_ACTIVE` and `SQ_BUSY_CYCLES` are nonzero.
- `SQ_WAVES` equals the expected grid wave count.
- `OccupancyPercent` is between 0 and 100.
- The report row belongs to `occupancy_kernel` on `Agent 1`.
- Timing and counters are not compared across different grid multipliers without labeling them.
