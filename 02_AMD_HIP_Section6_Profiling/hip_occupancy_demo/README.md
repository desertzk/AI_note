# HIP Full-Occupancy Demo

This example creates a long-running, low-register arithmetic kernel and sizes its grid from HIP's runtime occupancy calculation. It is designed to fill every reported CU with the maximum number of resident blocks for a 256-thread block.

## What The Program Does

The program uses HIPRTC to compile `occupancy_kernel`, obtains the module function, and calls:

```cpp
hipModuleOccupancyMaxActiveBlocksPerMultiprocessor(
    &active_blocks_per_cu, function, block_size, 0);
```

It then calculates:

```cpp
waves_per_block = block_size / wave_size;
resident_waves_per_cu = active_blocks_per_cu * waves_per_block;
grid_blocks = cu_count * active_blocks_per_cu;
```

On the Radeon AI PRO R9700 runtime used for this test:

```text
Reported CUs:             32
Wave size:                32
Block size:               256 threads
Active blocks per CU:     8
Waves per block:          8
Resident waves per CU:   64
Maximum waves per CU:    64
Grid blocks:             256
Total work items:      65536
```

The predicted resident-wave occupancy is therefore:

```text
8 active blocks/CU * 8 waves/block = 64 waves/CU
64 predicted waves/CU / 64 maximum waves/CU = 100% theoretical occupancy
```

The kernel performs a dependent floating-point arithmetic loop for each work item. The default 500,000 iterations keep the dispatch active long enough for stable timeline and counter collection.

## Build

```bash
cd /home/amd/zk/hip_programming_examples/hip_occupancy_demo

/opt/rocm/llvm/bin/clang++ \
  -std=c++17 -g -O2 -fno-omit-frame-pointer \
  -D__HIP_PLATFORM_AMD__ \
  hip_occupancy_demo.cpp \
  -o hip_occupancy_demo \
  -I/home/amd/zk/rocm-systems-hip713/projects/clr/build-hip-debug/install/include \
  -I/home/amd/zk/rocm-systems-hip713/projects/rocr-runtime/build-debug/install/include \
  -L/home/amd/zk/rocm-systems-hip713/projects/clr/build-hip-debug/install/lib \
  -L/home/amd/zk/rocm-systems-hip713/projects/rocr-runtime/build-debug/install/lib \
  -Wl,-rpath,/home/amd/zk/rocm-systems-hip713/projects/clr/build-hip-debug/install/lib \
  -Wl,-rpath,/home/amd/zk/rocm-systems-hip713/projects/rocr-runtime/build-debug/install/lib \
  -lamdhip64 -lhiprtc -lhsa-runtime64 -ldl -pthread
```

## Run

```bash
export LD_LIBRARY_PATH=/home/amd/zk/rocm-systems-hip713/projects/rocr-runtime/build-debug/install/lib:\
/home/amd/zk/rocm-systems-hip713/projects/clr/build-hip-debug/install/lib:\
/opt/rocm/core-7.13/lib:/opt/rocm/lib

./hip_occupancy_demo
```

Pass a different arithmetic iteration count as the first argument:

```bash
./hip_occupancy_demo 1000000
```

The validated default run took approximately 21.6 ms without rocprof instrumentation.

## Timeline Profile

```bash
rocprofv3 \
  --runtime-trace \
  --stats \
  --output-format csv pftrace \
  --output-file occupancy_trace \
  --output-directory rocprof_trace \
  -- ./hip_occupancy_demo
```

Open `rocprof_trace/occupancy_trace_results.pftrace` at <https://ui.perfetto.dev>.

The traced dispatch reported:

```text
Kernel:          occupancy_kernel
Workgroup size:  256
Grid size:       65536 work items
VGPR count:      8
Scratch size:    0
Kernel duration: 21.70 ms
```

Low VGPR usage and no scratch allocation are consistent with the occupancy API allowing eight 256-thread blocks per reported CU.

## Occupancy And Utilization Counters

```bash
rocprofv3 \
  --pmc "OccupancyPercent MeanOccupancyPerActiveCU MeanOccupancyPerCU Wavefronts" \
  --pmc "GPU_UTIL VALUBusy WAVE_DEP_WAIT WAVE_ISSUE_WAIT" \
  --kernel-include-regex 'occupancy_kernel' \
  --output-format csv json \
  --output-file occupancy_counters \
  --output-directory rocprof_occupancy \
  -- ./hip_occupancy_demo
```

The two `--pmc` groups produce `pass_1` and `pass_2` directories. Verified results were:

| Metric | Value | Interpretation |
|---|---:|---|
| `Wavefronts` | 2048 | Exactly `256 blocks * 8 waves/block` |
| `GPU_UTIL` | 100% | GPU active for the full counter interval |
| `OccupancyPercent` | 0 | Invalid on this gfx1201 profiler build |
| `MeanOccupancyPerActiveCU` | 0 | Invalid because its raw wave-cycle input is zero |
| `MeanOccupancyPerCU` | 0 | Invalid because its raw wave-cycle input is zero |
| `VALUBusy` | 0 | Invalid because its raw VALU-cycle input is zero |

A raw-counter check showed:

```text
GRBM_GUI_ACTIVE:     nonzero
SQ_BUSY_CYCLES:      nonzero
SQ_WAVE_CYCLES:      0
SQ_INST_CYCLES_VALU: 0
```

Thus the zero derived occupancy and VALU values are a gfx1201 counter-mapping limitation in this rocprofiler build, not evidence that the kernel had zero occupancy or executed no VALU instructions.

## What Is Proven

The following facts are verified:

- The HIP occupancy API permits eight resident 256-thread blocks per reported CU.
- Eight blocks contain 64 wave32 wavefronts, equal to the runtime's maximum of 64 waves per CU.
- The grid contains enough blocks to place eight blocks on every reported CU.
- rocprof counted all expected 2,048 wavefronts.
- `GPU_UTIL` was 100% during the counter interval.
- The kernel used eight VGPRs, no LDS, and no scratch memory.

This establishes a workload designed for 100% theoretical resident-wave occupancy and verifies full GPU activity. Direct achieved-occupancy percentage cannot be confirmed with the broken gfx1201 wave-cycle counters in this profiler build.

High occupancy does not necessarily mean maximum performance. It measures resident waves, not VALU throughput, memory bandwidth, instruction issue efficiency, or useful work per cycle.
