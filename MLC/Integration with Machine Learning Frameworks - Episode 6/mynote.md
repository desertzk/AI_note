

```python
bb = relax.BlockBuilder()

with bb.function("main"):
 with bb.dataflow():
 C = bb.emit_te(te_matmul, A, B)
 D = bb.emit_te(te_relu, C)
 R = bb.emit_output(D)
 bb.emit_func_output(R, params=[A, B])

MyModule = bb.get()
MyModule.show()

/tmp/ipykernel_1374352/305398868.py:10: DeprecationWarning: tvm.relax.BlockBuilder.get is deprecated, use tvm.relax.BlockBuilder.finalize instead
 MyModule = bb.get()

# from tvm.script import ir as I

# from tvm.script import tir as T

# from tvm.script import relax as R

@I.ir_module
class Module:
 @T.prim_func(private=True)
 def te_matmul(A: T.Buffer((T.int64(128), T.int64(128)), "float32"), B: T.Buffer((T.int64(128), T.int64(128)), "float32"), matmul: T.Buffer((T.int64(128), T.int64(128)), "float32")):
 T.func_attr({"tir.noalias": T.bool(True)})
 # with T.block("root"):
 for i, j, k in T.grid(T.int64(128), T.int64(128), T.int64(128)):
 with T.block("matmul"):
 v_i, v_j, v_k = T.axis.remap("SSR", [i, j, k])
 T.reads(A[v_i, v_k], B[v_k, v_j])
 T.writes(matmul[v_i, v_j])
 with T.init():
 matmul[v_i, v_j] = T.float32(0)
 matmul[v_i, v_j] = matmul[v_i, v_j] + A[v_i, v_k] * B[v_k, v_j]
 @T.prim_func(private=True)
 def te_relu(A: T.Buffer((T.int64(128), T.int64(128)), "float32"), relu: T.Buffer((T.int64(128), T.int64(128)), "float32")):
 T.func_attr({"tir.noalias": T.bool(True)})
 # with T.block("root"):
 for i0, i1 in T.grid(T.int64(128), T.int64(128)):
 with T.block("relu"):
 v_i0, v_i1 = T.axis.remap("SS", [i0, i1])
 T.reads(A[v_i0, v_i1])
 T.writes(relu[v_i0, v_i1])
 relu[v_i0, v_i1] = T.max(A[v_i0, v_i1], T.float32(0))
 @R.function
 def main(A: R.Tensor((128, 128), dtype="float32"), B: R.Tensor((128, 128), dtype="float32")) -> R.Tensor((128, 128), dtype="float32"):
 cls = Module
 with R.dataflow():
 lv = R.call_tir(cls.te_matmul, (A, B), out_sinfo=R.Tensor((128, 128), dtype="float32"))
 lv1 = R.call_tir(cls.te_relu, (lv,), out_sinfo=R.Tensor((128, 128), dtype="float32"))
 gv: R.Tensor((128, 128), dtype="float32") = lv1
 R.output(gv)
 return gv
```

Perfect—that actually makes this easier. We'll build the concepts from the bottom up instead of jumping into the code.

Think of TVM as having **three levels**:

```
Python code
    │
    ▼
Relax (graph level)
    │
    ▼
TIR (TensorIR, loop level)
    │
    ▼
Machine code (GPU/CPU)
```

Another way to think about it:

| Level        | What it describes                  | Similar to                |
| ------------ | ---------------------------------- | ------------------------- |
| Relax        | **What operations** to perform     | PyTorch computation graph |
| TIR          | **How each operation is computed** | CUDA/OpenCL kernel        |
| Machine code | Instructions executed on hardware  | GPU ISA                   |

---

## Step 1. What are `te_matmul` and `te_relu`?

Correct! ✅

If you remove

```python
D = bb.emit_te(te_relu, C)
```

then the graph becomes

```
A      B
 \    /
  MatMul
     |
   Output
```

Exactly right.

---

Now let's answer your question:

> **What is TE?**

TE stands for **Tensor Expression**.

It is an API in TVM for describing **what computation should be performed on tensors**, without writing explicit loops.

For example, suppose you want to compute

[
C[i,j] = A[i,j] + B[i,j]
]

### In plain Python

You might write

```python
for i in range(128):
    for j in range(128):
        C[i, j] = A[i, j] + B[i, j]
```

You manually write the loops.

---

### In TE

Instead, you write the mathematical expression:

```python
C = te.compute(
    (128, 128),
    lambda i, j: A[i, j] + B[i, j]
)
```

Notice there are **no loops**.

You're only saying

> "Each element of `C` is computed this way."

---

## Another example: ReLU

Instead of

```python
for i in range(128):
    for j in range(128):
        D[i, j] = max(C[i, j], 0)
```

TE writes

```python
D = te.compute(
    (128,128),
    lambda i,j: te.max(C[i,j], 0)
)
```

Again, **no loops**.

---

## Matrix multiplication

The mathematical formula is

[
C[i,j] = \sum_k A[i,k]B[k,j]
]

In TE, this becomes something like

```python
k = te.reduce_axis((0, 128), name="k")

C = te.compute(
    (128, 128),
    lambda i, j: te.sum(A[i, k] * B[k, j], axis=k)
)
```

You're describing **the math**, not the implementation.

---

## Then where do the loops come from?

This is the key idea.

You write

```
TE
```

↓

TVM automatically generates

```
TIR
```

↓

which contains the loops

```python
for i:
    for j:
        for k:
            ...
```

So the relationship is

```
TE
 │
 │ describes computation
 ▼
C[i,j] = Σ A[i,k]B[k,j]

        ↓ Lowering

TIR
 │
 ▼

for i:
    for j:
        for k:
            ...
```

You already see these in the generated module.

```python
@T.prim_func
def te_matmul(...):
```

This is **TensorIR (TIR)**.

It literally contains loops:

```python
for i, j, k:
```

and computes

```
C = A × B
```

Similarly,

```python
@T.prim_func
def te_relu(...):
```

contains loops computing

```
D = max(C, 0)
```

So these are **low-level kernels**.

Think of them as GPU kernels or C functions.

```
Kernel 1:
A,B
 │
 ▼
MatMul
 │
 ▼
C

Kernel 2:
C
 │
 ▼
ReLU
 │
 ▼
D
```

---

## Step 2. What is Relax?

Relax does **not** contain loops.

Instead, it describes

> **which kernels should run and in what order.**

For your example:

```
A,B
 │
 ▼
MatMul
 │
 ▼
ReLU
 │
 ▼
Output
```

Notice this is a graph, not nested loops.

---

## Step 3. Then what is `BlockBuilder`?

This line

```python
bb = relax.BlockBuilder()
```

creates an object that **builds a Relax program**.

Think of it like constructing an AST (Abstract Syntax Tree).

Instead of writing

```python
@R.function
def main(...):
    ...
```

yourself,

you tell the builder

> "Add a function."

> "Inside it, call this kernel."

> "Then call another kernel."

> "Return the result."

When you're finished,

```python
bb.get()
```

produces the complete IRModule.

---

## Step 4. Let's go through the code line by line

### ①

```python
bb = relax.BlockBuilder()
```

Create an **empty builder**.

At this point:

```
(empty)
```

No functions exist yet.

---

### ②

```python
with bb.function("main"):
```

Start creating

```
main(...)
```

Now the module looks like

```
Module

main(...)
{
    ...
}
```

The body is still empty.

---

### ③

```python
with bb.dataflow():
```

Begin a Relax **dataflow block**.

Inside this block,

variables are temporary values.

Think of it like

```
lv
lv1
lv2
```

that only exist inside the graph.

---

### ④

```python
C = bb.emit_te(te_matmul, A, B)
```

This is one of the most important lines.

It means

> "Insert a call to this TE computation."

Internally, BlockBuilder creates something like

```python
lv = R.call_tir(
    te_matmul,
    (A, B)
)
```

Notice the generated code:

```python
lv = R.call_tir(
    cls.te_matmul,
    (A, B),
    ...
)
```

So

```
bb.emit_te(...)
```

became

```
R.call_tir(...)
```

because TE has already been lowered into a TIR function.

Graph now becomes

```
A   B
 \ /
MatMul
 |
lv
```

---

### ⑤

```python
D = bb.emit_te(te_relu, C)
```

Same idea.

Builder adds

```
lv1 = call_tir(te_relu, lv)
```

Graph becomes

```
A   B
 \ /
MatMul
 |
lv
 |
ReLU
 |
lv1
```

---

### ⑥

```python
R = bb.emit_output(D)
```

This marks

```
lv1
```

as the output of the dataflow block.

Equivalent generated code:

```python
gv = lv1
R.output(gv)
```

---

### ⑦

```python
bb.emit_func_output(R, params=[A, B])
```

Finish building

```python
main(A, B)
```

with

```
inputs:
    A
    B

output:
    R
```

---

### ⑧

```python
MyModule = bb.get()
```

Now BlockBuilder says

> "I'm done building."

and returns

```
IRModule
```

which contains

```
Module

te_matmul

te_relu

main
```

---

# Where did `call_tir` come from?

You never wrote

```python
R.call_tir(...)
```

Instead you wrote

```python
bb.emit_te(...)
```

The builder automatically lowered the TE computation into a TIR function and generated the corresponding `R.call_tir(...)` nodes in the Relax graph.

Conceptually:

```
You write

emit_te(matmul)

        │
        ▼

BlockBuilder creates

te_matmul()        <-- TIR kernel

        +
call_tir(te_matmul)
```

---

Excellent. This code is one of the core ideas behind TVM Relax: **automatically converting a PyTorch model into a Relax program**.

Instead of explaining each line individually, let's first understand the **big picture**.

---

# The goal

Suppose you have a PyTorch model:

```python
class MyModel(nn.Module):
    def forward(self, x):
        x = torch.matmul(x, self.weight)
        x = torch.relu(x)
        return x
```

Normally, PyTorch executes it directly.

```
PyTorch

input
  │
  ▼
matmul
  │
  ▼
relu
  │
  ▼
output
```

TVM cannot optimize a Python program directly.

Instead, it must convert it into its own IR.

The whole pipeline is

```
PyTorch Model
      │
      ▼
Torch FX Graph
      │
      ▼
Relax Graph
      │
      ▼
TensorIR
      │
      ▼
CPU/GPU code
```

Everything in your code is implementing **the middle arrow**:

```
Torch FX Graph
      │
      ▼
Relax Graph
```

---

# Step 1

```python
model = MyModel()
```

This creates a normal PyTorch model.

Nothing TVM-specific yet.

```
MyModel

forward()
```

---

# Step 2

```python
fx_module = fx.symbolic_trace(model)
```

This is where the magic begins.

`symbolic_trace` executes the model **using fake tensors**.

It does **not** perform real computation.

Instead it records every operation.

Suppose your model is

```python
y = torch.matmul(x, W)
z = torch.relu(y)
```

FX records

```
placeholder x

↓

get_attr weight

↓

matmul

↓

relu

↓

output
```

Notice

there are **no tensor values**

only operations.

This is exactly like drawing a computation graph.

---

## What is inside `fx_module`?

It contains nodes like

```
placeholder
```

means

```
Input tensor
```

---

```
get_attr
```

means

```
Load a parameter
```

---

```
call_function
```

means

```
Call torch.matmul
```

or

```
Call torch.relu
```

---

```
output
```

means

```
Return this value
```

So FX graph is

```
Input
   │
Weight
   │
   ▼
MatMul
   │
   ▼
ReLU
   │
   ▼
Output
```

---

# Step 3

Now we want to convert this FX graph into Relax.

This function does exactly that.

```python
from_fx(...)
```

Think of it as

```
FX Graph

↓

Walk every node

↓

Generate Relax IR
```

---

# Step 4

Inside `from_fx`

The most important loop is

```python
for node in fx_mod.graph.nodes:
```

Imagine FX graph contains

```
placeholder

↓

get_attr

↓

matmul

↓

relu

↓

output
```

This loop visits

```
placeholder
```

then

```
get_attr
```

then

```
matmul
```

then

```
relu
```

then

```
output
```

one by one.

---

# Step 5

## placeholder

Suppose node is

```
placeholder x
```

The code

```python
input_var = relax.Var(...)
```

creates a Relax input variable.

```
FX

placeholder x

↓

Relax

Var("x")
```

The mapping is saved

```python
node_map[node] = input_var
```

---

## Why do we need `node_map`?

This is extremely important.

FX node

```
matmul
```

needs

```
x
```

and

```
weight
```

How do we find them?

`node_map` remembers

```
FX node

↓

Relax variable
```

For example

```
FX placeholder

↓

Relax Var(x)
```

Later,

when matmul asks for its input,

we simply look it up.

---

# Step 6

Suppose next node is

```
get_attr weight
```

That means

```
model.weight
```

The helper

```python
fetch_attr(...)
```

retrieves

```
model.weight
```

Then

```python
map_param(...)
```

converts it into

```python
relax.const(...)
```

Now

```
FX weight

↓

Relax constant
```

---

# Step 7

Now we reach

```
call_function
```

Suppose it is

```
torch.matmul
```

Instead of a huge

```python
if node.target == torch.matmul:
```

TVM uses a dictionary.

```
torch.matmul

↓

map_matmul
```

This dictionary is

```python
call_function_map
```

---

So

```python
call_function_map[node.target]
```

returns

```python
map_matmul
```

which is

```python
def map_matmul(bb, node_map, node):
    ...
```

---

Inside it

```python
A = node_map[node.args[0]]
```

means

```
Find Relax variable
corresponding to first FX input.
```

Similarly

```python
B = node_map[node.args[1]]
```

gets

```
weight
```

Then

```python
bb.emit_te(...)
```

creates

```
call_tir(te_matmul)
```

inside Relax.

---

Graph becomes

```
Relax

A
 \
  \
   MatMul
  /
W

↓

lv
```

---

# Step 8

Next node

```
torch.relu
```

Again

dictionary lookup

```
torch.relu

↓

map_relu
```

which does

```python
bb.emit_te(te_relu, A)
```

Now graph becomes

```
A
 \
  \
 MatMul
   │
   ▼
 ReLU
   │
   ▼
 lv1
```

---

# Step 9

Finally

```
output
```

becomes

```python
bb.emit_output(...)
```

and

```python
bb.emit_func_output(...)
```

finishes

```
main(...)
```

---

# What are `call_function_map` and `call_module_map`?

This design makes the converter **extensible**.

Instead of hardcoding every PyTorch operation, `from_fx` delegates translation to maps.

### `call_function_map`

Handles functional APIs like:

```python
torch.matmul(...)
torch.relu(...)
torch.add(...)
torch.sigmoid(...)
```

For example:

```
torch.matmul
        │
        ▼
 map_matmul()
        │
        ▼
bb.emit_te(te_matmul)
```

If you want to support a new function such as `torch.add`, you simply add:

```python
def map_add(bb, node_map, node):
    A = node_map[node.args[0]]
    B = node_map[node.args[1]]
    return bb.emit_te(te_add, A, B)

call_function_map = {
    torch.matmul: map_matmul,
    torch.relu: map_relu,
    torch.add: map_add,
}
```

No changes to `from_fx` are needed.

### `call_module_map`

Handles `nn.Module` objects such as:

```python
nn.Linear
nn.Conv2d
nn.BatchNorm2d
```

If your model contains:

```python
self.linear = nn.Linear(...)
```

FX produces a `call_module` node, and `from_fx` looks up the module type:

```
nn.Linear
      │
      ▼
map_linear()
      │
      ▼
Generate Relax IR
```

This separates the generic graph traversal from the operator-specific translation logic.

---

## The complete pipeline

```
PyTorch Model
      │
      ▼
fx.symbolic_trace()
      │
      ▼
FX Graph
(placeholder, get_attr,
 call_function, output)
      │
      ▼
from_fx()
      │
      ├── placeholder → Relax Var
      ├── get_attr    → Relax const
      ├── call_function → map_matmul/map_relu
      ├── output      → emit_output
      ▼
Relax Graph
      │
      ▼
call_tir(te_matmul)
      │
      ▼
call_tir(te_relu)
      │
      ▼
TensorIR kernels
```

---

### Check your understanding

Suppose the PyTorch model is:

```python
def forward(self, x):
    y = torch.relu(x)
    z = torch.sigmoid(y)
    return z
```

The FX graph will contain a `call_function` node for `torch.sigmoid`.

**Question:** If `call_function_map` only contains entries for `torch.relu` and `torch.matmul`, what do you think will happen when `from_fx()` encounters the `torch.sigmoid` node, and why?
