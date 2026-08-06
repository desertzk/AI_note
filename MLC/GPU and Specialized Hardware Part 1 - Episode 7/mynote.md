Great example. Since you're in Study mode, let's build this up instead of just describing the code.

From our previous conversations, you already know:

* A GPU launches **blocks**.
* Each block contains many **threads**.
* TVM lowers a loop nest into CUDA by binding loops to `blockIdx.x` and `threadIdx.x`.

This example is the simplest CUDA kernel possible: **vector addition**.

---

## Step 1. The original TIR

```python
@T.prim_func
def main(A, B, C):
    for i in T.grid(1024):
        with T.block("C"):
            vi = T.axis.remap("S", [i])
            C[vi] = A[vi] + B[vi]
```

Think of this exactly like

```cpp
for (int i=0; i<1024; i++)
    C[i] = A[i] + B[i];
```

There is only **one loop**.

```
i
│
├──0
├──1
├──2
...
└──1023
```

No GPU yet.

---

## Step 2. Get the loop

```python
block_C = sch.get_block("C")
i, = sch.get_loops(block_C)
```

`get_loops()` returns the loops surrounding block `C`.

Here there is only one loop:

```
for i in range(1024):
    block C
```

so

```
i = 0..1023
```

---

## Step 3. Split the loop

```python
i0, i1 = sch.split(i, [None, 128])
```

This is the important transformation.

Instead of

```
for i in range(1024):
```

TVM rewrites it into

```
for i0 in range(8):
    for i1 in range(128):
```

because

```
8 × 128 = 1024
```

and

```
i = i0 * 128 + i1
```

---

Visualized:

Original

```
0
1
2
3
...
1023
```

Split

```
i0=0
    i1=0..127

i0=1
    i1=0..127

...

i0=7
    i1=0..127
```

---

### Quick check

Can you tell me **why `i0` has only 8 iterations** instead of 1024?

(Just answer that one question before reading further if you want to test yourself.)

---

## Step 4. Bind loops to CUDA

Although your snippet omits the scheduling calls, the generated TIR shows

```python
for i_0 in T.thread_binding(8, thread="blockIdx.x"):
    for i_1 in T.thread_binding(128, thread="threadIdx.x"):
```

which means TVM performed something equivalent to

```python
sch.bind(i0, "blockIdx.x")
sch.bind(i1, "threadIdx.x")
```

Now the loops are **no longer normal loops**.

Instead, CUDA executes them using hardware threads.

```
Grid
│
├── Block 0
├── Block 1
├── ...
└── Block 7
```

Each block contains

```
Thread 0
Thread 1
...
Thread 127
```

---

## Step 5. Each thread computes one element

Inside the kernel

```python
vi = i_0 * 128 + i_1
```

Suppose

```
blockIdx.x = 3
threadIdx.x = 20
```

Then

```
vi = 3*128 + 20
   = 404
```

That thread computes

```
C[404] = A[404] + B[404]
```

Another thread

```
blockIdx.x = 5
threadIdx.x = 7
```

computes

```
vi = 5*128 + 7
   = 647
```

Every thread has its own index.

---

## Step 6. Why exactly 128 threads?

You chose

```python
split(..., 128)
```

which means

```
threadIdx.x
```

has

```
0...127
```

So each CUDA block contains

```
128 threads
```

Since there are

```
1024 elements
```

the number of blocks is

```
1024 / 128 = 8
```

Hence

```
Grid
 ├─ Block 0 (128 threads)
 ├─ Block 1 (128 threads)
 ...
 └─ Block 7 (128 threads)
```

Total threads launched

```
8 × 128 = 1024
```

Exactly one thread per vector element.

---

## Step 7. Build

```python
rt_mod = tvm.build(sch.mod, target="cuda")
```

TVM now

* lowers TIR
* generates CUDA kernel code
* compiles it
* returns a runtime module.

Conceptually, it's similar to generating a CUDA kernel like:

```cpp
__global__
void vec_add(float* A, float* B, float* C)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    C[i] = A[i] + B[i];
}
```

---

## Step 8. Allocate GPU memory

```python
A_nd = tvm.nd.array(A_np, tvm.cuda(0))
```

This copies

```
NumPy (CPU)
```

↓

```
GPU memory
```

The same happens for

```
B_nd
```

For

```python
C_nd
```

TVM allocates GPU memory initialized to zeros.

---

## Step 9. Launch the kernel

```python
rt_mod["main"](A_nd, B_nd, C_nd)
```

TVM launches

```
8 blocks
```

Each block launches

```
128 threads
```

Each thread performs

```
C[i] = A[i] + B[i]
```

simultaneously.

---

## Step 10. Printing

When you do

```python
print(C_nd)
```

TVM prints the contents of the GPU array (internally synchronizing and reading the values for display), so you'll see the computed vector addition results.

---

### Big picture

The entire scheduling process transforms:

```
for i in range(1024)
```

↓

```
split
```

↓

```
for i0 in range(8):
    for i1 in range(128):
```

↓

```
bind
```

↓

```
blockIdx.x = i0
threadIdx.x = i1
```

↓

```
CUDA kernel launch

8 blocks
×
128 threads
=
1024 GPU threads
```

Each GPU thread computes one element:

```
global_index = blockIdx.x * 128 + threadIdx.x

C[global_index] = A[global_index] + B[global_index]
```

This "split + bind" pattern is one of the most fundamental scheduling techniques in TVM and is the basis for mapping computations onto CUDA's grid-and-block execution model.
