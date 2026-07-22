# Occupancy Profiling Counter Summary

This note summarizes the rocprofv3 counters collected for `occupancy_kernel`, explains which results are valid, and defines how to evaluate the new eightfold-oversubscribed workload.

## Result States

Three profiling states must not be mixed:

| State | Power mode | Grid multiplier | Result status |
|---|---|---:|---|
| Initial counter run | `AUTO` | 1 | Occupancy counters invalid because `SQ_WAVE_CYCLES = 0` |
| Stable baseline | `STABLE_STD` | 1 | Valid achieved occupancy: 67.464735% |
| Current workload | Requires `STABLE_STD` rerun | 8 | Not measured yet; designed to reduce ramp-up and tail drain |

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

| Counter | Meaning | What it does not prove |
|---|---|---|
| `SQ_WAVES` / `Wavefronts` | Total dispatched waves | Simultaneous residency |
| `SQ_WAVE_CYCLES` | Sum of resident-wave cycles | Useful work or VALU throughput |
| `SQ_BUSY_CYCLES` | Cycles in which shader sequencers were busy | Full occupancy |
| `GRBM_GUI_ACTIVE` | GPU-active cycles | All CUs were full |
| `MeanOccupancyPerActiveCU` | Average resident waves on CUs active during the interval | Average across inactive CUs |
| `MeanOccupancyPerCU` | Average resident waves across all physical CUs | Peak occupancy |
| `OccupancyPercent` | Time-averaged resident waves as percentage of maximum | Performance efficiency |
| `GPU_UTIL` | Percentage of collection interval with GPU activity | CU saturation |
| `VALUBusy` | Percentage of GPU time processing VALU instructions | Occupancy by itself |

High occupancy is not automatically high performance. A kernel can have many resident waves but spend most cycles waiting, or have lower occupancy while fully utilizing a bottlenecked execution unit.

## Invalid Auto-Power Run

The initial run used automatic power management. rocprofiler-sdk requires gfx11 and gfx12 GPUs to use a stable power state for counter collection.

The auto-power run reported:

| Counter | Value | Validity |
|---|---:|---|
| `Wavefronts` | 2048 | Valid dispatch count for multiplier 1 |
| `GPU_UTIL` | 100% | GPU remained active during collection |
| `SQ_WAVE_CYCLES` | 0 | Invalid |
| `OccupancyPercent` | 0 | Invalid because its numerator was zero |
| `MeanOccupancyPerActiveCU` | 0 | Invalid because its numerator was zero |
| `MeanOccupancyPerCU` | 0 | Invalid because its numerator was zero |
| `VALUBusy` | 0 | Invalid because its raw VALU-cycle input was zero |

Do not interpret those occupancy zeros as real 0% occupancy.

## Valid Stable Baseline

After setting GPU 0 to `STABLE_STD`, multiplier 1 produced:

| Counter | Value |
|---|---:|
| `GRBM_GUI_ACTIVE` | 37,421,018 |
| `SQ_BUSY_CYCLES` | 1,169,763,684 |
| `SQ_WAVE_CYCLES` | 51,703,788,945 |
| `SQ_WAVES` | 2,048 |
| `MeanOccupancyPerActiveCU` | 44.200200 waves |
| `MeanOccupancyPerCU` | 21.588715 waves |
| `OccupancyPercent` | 67.464735% |

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

| Option | Meaning in this command |
|---|---|
| `--pmc ...` | Collects the listed performance-monitor counters for each selected kernel dispatch |
| `--kernel-include-regex 'occupancy_kernel'` | Collects counters only for kernels whose name matches `occupancy_kernel`; runtime helper kernels are excluded |
| `--output-format csv` | Writes tabular counter records suitable for formulas and scripts |
| `--output-file stable_occupancy` | Uses `stable_occupancy` as the report-name prefix |
| `--output-directory rocprof_stable_occupancy` | Places reports in that directory instead of the default hostname/PID directory |
| `--` | Separates profiler arguments from the executable command |
| `./hip_occupancy_demo` | Runs the current executable, whose default grid multiplier is 8 |

Counter purposes:

| Counter | Why it is collected |
|---|---|
| `OccupancyPercent` | Final achieved occupancy as a percentage of maximum resident-wave capacity |
| `MeanOccupancyPerActiveCU` | Average resident waves over only CUs that were active |
| `MeanOccupancyPerCU` | Average resident waves over all physical CUs |
| `SQ_WAVE_CYCLES` | Numerator used by the derived occupancy formulas; must be nonzero |
| `SQ_BUSY_CYCLES` | Denominator for occupancy on active CUs |
| `GRBM_GUI_ACTIVE` | GPU-active cycle count used for occupancy averaged over all CUs |
| `SQ_WAVES` | Total dispatched waves; validates grid geometry but not simultaneous residency |

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

| `OccupancyPercent` | Interpretation |
|---:|---|
| 0 with zero `SQ_WAVE_CYCLES` | Invalid collection |
| Below 50% | Low achieved residency; investigate grid, resources, imbalance, or waits |
| 50-80% | Moderate achieved occupancy |
| 80-100% | High achieved occupancy |
| Above 100% | Invalid formula, topology mismatch, or counter issue |

For this kernel, an 80-100% result would confirm that oversubscription successfully amortized the one-batch ramp-up and tail effects. A result near 67% would suggest another limiting factor, such as scheduler distribution or the counter's averaging semantics.

## Output Files

| Path | Contents |
|---|---|
| `rocprof_stable_occupancy/stable_occupancy_counter_collection.csv` | Valid multiplier-1 stable baseline; overwritten by the next helper run |
| `rocprof_occupancy/pass_1/occupancy_counters_counter_collection.csv` | Invalid auto-power occupancy-derived metrics |
| `rocprof_occupancy/pass_2/occupancy_counters_counter_collection.csv` | Auto-power utilization metrics |
| `rocprof_raw/raw_counters_counter_collection.csv` | Raw counter diagnostic run |
| `rocprof_trace/occupancy_trace_kernel_stats.csv` | Kernel duration summary |
| `rocprof_trace/occupancy_trace_kernel_trace.csv` | Grid, block, register, scratch, stream, and timestamp data |
| `rocprof_trace/occupancy_trace_results.pftrace` | Perfetto timeline |

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
