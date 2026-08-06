# YOLO26n MIGraphX Optimization: 2.0805 ms to 1.5023 ms

## Result

For YOLO26n FP32 inference at batch 1 and `640x640` on gfx1201, folding the
Ultralytics inference BatchNorm layers before `torch.compile` reduced steady-state
MIGraphX latency by **27.79%**.

| Graph | Paired run means (ms) | Mean (ms) | Dispatches | Compiled artifact |
|---|---|---:|---:|---:|
| Original model | 2.07855, 2.08182, 2.08113 | **2.08050** | 193 | 171,789,439 bytes |
| Model with BatchNorm folded | 1.49982, 1.50319, 1.50402 | **1.50234** | 152 | 12,128,721 bytes |

The optimized graph saves `0.57815 ms` per inference. The compiled artifact is
about **92.94% smaller**.

## Key optimization

The performance-changing code is one line executed after loading the inference
model and before calling `torch.compile`:

```python
model = YOLO("yolo26n.pt").model.to("cuda").eval()
model.fuse(verbose=False)
compiled = torch.compile(model, backend="migraphx", options=compile_options)
```

`model.fuse()` folds each inference `BatchNorm2d` into the preceding convolution's
weights and bias. It must run before MIGraphX traces or compiles the model. A
compiled cache made from the original graph must not be loaded for the fused
model; compile and save a new cache after fusion.

The benchmark implementation is in
[`performance/benchmark_yolo26_migraphx.py`](performance/benchmark_yolo26_migraphx.py).
Fusion is enabled by default and can be disabled with `--no-fuse-model`. The
independent direct PyTorch model is also fused so correctness and performance are
compared using equivalent inference graphs.

## How the trace identified it

Compilation and instruction tracing were enabled before starting Python:

```bash
export MIGRAPHX_TRACE_COMPILE=1
export MIGRAPHX_TRACE_EVAL=1
```

The original runtime contained 61 launches whose generated symbol family was:

```text
mlir_convolution_broadcast_mul_mul_add_sigmoid_mul
```

The operations after convolution represented inference BatchNorm arithmetic
followed by SiLU:

```text
convolution -> BatchNorm affine operations -> sigmoid -> multiply
```

MIGraphX already fused these operations into generated GPU launches, so adding
another backend fusion rule was not the main opportunity. Folding BatchNorm at
the model level removed those operations and constants before graph lowering.

After model fusion:

- the old 61-call family was completely eliminated;
- the main replacement family became 49 simpler
  `mlir_convolution_broadcast_add_sigmoid_mul` launches;
- total dispatches fell from 193 to 152;
- `BatchNorm2d` module count after fusion was zero.

`MIGRAPHX_TRACE_EVAL=1` synchronizes every instruction and changes timing. Use it
only to map instructions to generated kernel symbols. The reported 2.0805 ms and
1.5023 ms values came from normal steady-state GPU-event measurements with trace
timing disabled.

## Reproduce the optimized benchmark

Use the local MIGraphX/rocMLIR development build:

```bash
cd /home/amd/zk/yolo_model

PREFIX=/home/amd/zk/yolo_model/AMDMIGraphX/install-gpu-rocmlir-develop
ENV=/home/amd/miniconda3/envs/yolo26-migraphx-rocmlir-dev
export LD_LIBRARY_PATH="$PREFIX/lib:$PREFIX/lib/migraphx/lib:/opt/rocm/core-7.13/lib:/opt/rocm/lib"
export PYTHONPATH="$PREFIX/lib"
export PATH="$ENV/bin:$PREFIX/bin:/opt/rocm/core-7.13/bin:/opt/rocm/bin:/usr/local/bin:/usr/bin:/bin"
unset MIGRAPHX_TRACE_COMPILE MIGRAPHX_TRACE_EVAL

"$ENV/bin/python" performance/benchmark_yolo26_migraphx.py \
  --model yolo26n.pt \
  --image performance/assets/ultralytics_bus.jpg \
  --imgsz 640 \
  --fuse-model \
  --rounds 3 \
  --warmup 30 \
  --iterations 500 \
  --output-dir performance/model_fused_result
```

For an A/B run of the old graph, use the same command with `--no-fuse-model` and
a different output directory. Alternate old and fused runs to reduce clock and
thermal ordering bias.

## Correctness validation

Ultralytics changes the auxiliary output structure after model fusion: the fused
inference graph leaves `one2many` empty and retains `one2one`. Therefore, do not
compare flattened output leaves only by list position or tensor shape. Compare
semantic paths:

- final detections: `output[0]`;
- boxes: `output[1]["one2one"]["boxes"]`;
- scores: `output[1]["one2one"]["scores"]`;
- features: `output[1]["one2one"]["feats"]`.

The original and fused MIGraphX outputs passed `rtol=1e-3, atol=1e-4`:

| Output | Shape | Maximum absolute difference |
|---|---|---:|
| Final detections | `(1, 300, 6)` | 0.00131226 |
| One-to-one boxes | `(1, 4, 8400)` | 0.00009179 |
| One-to-one scores | `(1, 80, 8400)` | 0.00074959 |
| Feature level 0 | `(1, 64, 80, 80)` | 0.00003421 |
| Feature level 1 | `(1, 128, 40, 40)` | 0.00013405 |
| Feature level 2 | `(1, 256, 20, 20)` | 0.00009882 |

## Recorded artifacts

All paths are relative to `/home/amd/zk/yolo_model`.

| Artifact | Path |
|---|---|
| Original compiled graph | `performance/migraphx_trace/yolo26_640_rocmlir_fusedkey_quick_compiled.pt` |
| Fused compiled graph | `performance/migraphx_trace/yolo26_640_model_fused_rocmlir_quick_compiled.pt` |
| Fused compile log | `performance/migraphx_trace/yolo26_model_fused_rocmlir_quick_compile.log` |
| Fused tuning cache | `performance/migraphx_trace/yolo26_model_fused_rocmlir_quick_problem_cache.json` |
| Fused dispatch trace | `performance/migraphx_trace/model_fused_trace.log` |
| Original paired samples | `performance/migraphx_trace/baseline_modelfusepair{1,2,3}.json` |
| Fused paired samples | `performance/migraphx_trace/model_fused_modelfusepair{1,2,3}.json` |

## Attribution of the improvement

Two earlier backend changes remain useful but are not the direct cause of the
2.0805 ms to 1.5023 ms improvement:

1. The MIGraphX rocMLIR tuning key includes a fused-module MD5 so different
   post-operation graphs cannot alias the same cache entry.
2. rocMLIR Full and Exhaustive searches begin with known Quick candidates.

Those changes improve tuning correctness and candidate coverage. The measured
**27.79% latency reduction in this comparison came from model-level BatchNorm
folding with `model.fuse(verbose=False)`**.
