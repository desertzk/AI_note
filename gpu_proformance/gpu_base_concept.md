---Architecture and formulas

The agent trace identifies **AMD Radeon AI PRO R9700 / gfx1201**, 64 physical CUs, 128 SIMD32s, wave size 32, and 16 wave slots/SIMD. gfx1201 LLVM target features select WGP mode: 4 SIMD32s (two physical CUs) per WGP, hence **32 WGPs**, 64 wave slots/WGP, or 32 slots/physical CU.

gfx1201 operates in WGP mode for this LLVM calculation:

```
1 WGP = 2 physical CUs = 4 SIMD32 units
32 WGPs in the GPU
64 wave slots per WGP
```

Therefore the whole GPU has:

```
32 WGPs × 64 wave slots = 2048 wave slots
```

total VGPR number 1536

For each dispatch:

- waves/workgroup = `ceil(block threads / 32)`;
- allocated VGPRs/wave = `align_up(VGPR_Count, 24)`; VGPR waves/SIMD = `min(16, floor(1536 / allocated VGPRs))`;
- VGPR group bound/WGP = `floor(4 * VGPR waves/SIMD / waves/workgroup)`;
- LDS group bound/WGP = `floor(131072 / LDS bytes/workgroup)`;
- wave/barrier group bound is `64 / waves/workgroup`, capped at 32 for multi-wave groups;
- active-WGP slot ceiling = resident waves/WGP divided by 64;
- grid-only GPU-wide ceiling = `total grid waves / (32 WGPs * 64 slots)`; the reported GPU-wide ceiling is the smaller of grid and residency ceilings.

LLVM models SGPR count as non-limiting for gfx10+, and every target dispatch has zero scratch/private segment bytes in this capture. The trace reports 64 KiB addressable LDS per physical CU; LLVM `getLocalMemorySize()` doubles it in WGP mode, giving the 128 KiB effective WGP residency pool used above.

## How to read each column

| Column               | Meaning                                                 |
| -------------------- | ------------------------------------------------------- |
| `Infer ord`          | Position among all 187 dispatches in one inference      |
| `Target ord`         | Position among the 73 launches with this exact symbol   |
| `Kernel ID`          | Capture-specific ID for the exact generated code object |
| `Median us`          | Median duration across 20 inference iterations          |
| `Grid`               | Total launched work-items in X/Y/Z                      |
| `Block`              | Workgroup size in X/Y/Z                                 |
| `Groups`             | Number of workgroups, calculated from grid/block        |
| `Waves/WG`           | Wavefronts in one workgroup                             |
| `VGPR (alloc)`       | Reported VGPR count and allocation-rounded count        |
| `SGPR`               | Reported scalar register count                          |
| `Group/LDS B`        | LDS/group-segment bytes per workgroup                   |
| `Private B`          | Private/scratch bytes; zero for these kernels           |
| `Resident waves/WGP` | Maximum theoretical resident waves on an active WGP     |
| `Active-WGP ceiling` | Resident waves divided by 64 WGP wave slots             |
| `Residency limiter`  | VGPR, LDS, wave/barrier capacity, or a tie              |
| `GPU-wide ceiling`   | Ceiling after accounting for the total grid size        |
| `GPU limiter`        | Whether grid or resources establish the final ceiling   |

`Kernel ID` is useful inside this capture, but may change after recompiling or starting a different process. Use the complete combination of symbol, shapes, grid/block, resources, and tuning configuration when identifying a compiler problem.

## Hottest grid-limited configurations

| Infer ord | Target ord | Kernel ID | Median us | Grid      | Block   | Groups | Waves/WG | VGPR (alloc) | SGPR | Group/LDS B | Private B | Resident waves/WGP | Active-WGP ceiling | Residency limiter | GPU-wide ceiling | GPU limiter |
| --------- | ---------- | --------- | --------- | --------- | ------- | ------ | -------- | ------------ | ---- | ----------- | --------- | ------------------ | ------------------ | ----------------- | ---------------- | ----------- |
| 14        | 8          | 4042      | 50.58     | 6400x1x1  | 128x1x1 | 50     | 4        | 128 (144)    | 128  | 10240       | 0         | 40                 | 62.5%              | VGPR              | 9.8%             | grid        |
| 8         | 5          | 4036      | 47.22     | 6400x1x1  | 64x1x1  | 100    | 2        | 176 (192)    | 128  | 8192        | 0         | 32                 | 50.0%              | VGPR+LDS          | 9.8%             | grid        |
| 162       | 59         | 4003      | 41.22     | 1664x1x1  | 128x1x1 | 13     | 4        | 96 (96)      | 128  | 4096        | 0         | 64                 | 100.0%             | VGPR+wave/barrier | 2.5%             | grid        |
| 114       | 46         | 4139      | 41.08     | 1664x1x1  | 128x1x1 | 13     | 4        | 96 (96)      | 128  | 4096        | 0         | 64                 | 100.0%             | VGPR+wave/barrier | 2.5%             | grid        |
| 25        | 13         | 4053      | 37.40     | 3328x1x1  | 128x1x1 | 26     | 4        | 128 (144)    | 128  | 10240       | 0         | 40                 | 62.5%              | VGPR              | 5.1%             | grid        |
| 2         | 2          | 4030      | 33.30     | 25600x1x1 | 64x1x1  | 400    | 2        | 104 (120)    | 128  | 2048        | 0         | 48                 | 75.0%              | VGPR              | 39.1%            | grid        |
| 13        | 7          | 4041      | 27.66     | 25600x1x1 | 128x1x1 | 200    | 4        | 104 (120)    | 128  | 4096        | 0         | 48                 | 75.0%              | VGPR              | 39.1%            | grid        |
| 115       | 47         | 4140      | 27.48     | 3200x1x1  | 64x1x1  | 50     | 2        | 120 (120)    | 128  | 6144        | 0         | 42                 | 65.6%              | LDS               | 4.9%             | grid        |
| 164       | 61         | 4005      | 27.04     | 3200x1x1  | 64x1x1  | 50     | 2        | 120 (120)    | 128  | 6144        | 0         | 42                 | 65.6%              | LDS               | 4.9%             | grid        |
| 89        | 34         | 4114      | 26.14     | 6656x1x1  | 128x1x1 | 52     | 4        | 96 (96)      | 128  | 4096        | 0         | 64                 | 100.0%             | VGPR+wave/barrier | 10.2%            | grid        |
| 158       | 56         | 3999      | 25.56     | 6400x1x1  | 64x1x1  | 100    | 2        | 192 (192)    | 128  | 8192        | 0         | 32                 | 50.0%              | VGPR+LDS          | 9.8%             | grid        |
| 118       | 49         | 4143      | 25.50     | 6400x1x1  | 64x1x1  | 100    | 2        | 192 (192)    | 128  | 8192        | 0         | 32                 | 50.0%              | VGPR+LDS          | 9.8%             | grid        |
| 67        | 25         | 4092      | 24.56     | 6400x1x1  | 64x1x1  | 100    | 2        | 176 (192)    | 128  | 8192        | 0         | 32                 | 50.0%              | VGPR+LDS          | 9.8%             | grid        |
| 3         | 3          | 4031      | 20.26     | 25600x1x1 | 64x1x1  | 400    | 2        | 104 (120)    | 128  | 3072        | 0         | 48                 | 75.0%              | VGPR              | 39.1%            | grid        |
| 77        | 29         | 4102      | 19.38     | 6400x1x1  | 64x1x1  | 100    | 2        | 120 (120)    | 128  | 2048        | 0         | 48                 | 75.0%              | VGPR              | 9.8%             | grid        |

These are the first tuning targets. Lowering VGPR or LDS cannot fix their GPU-wide ceiling while the grid remains smaller than the resident capacity. Increase independent workgroups (usually smaller output tiles, or safe spatial/channel splitting) and then re-check duration and resources.

## Grid, block, groups, and waves

Consider dispatch 114:

```
Grid:  1664 × 1 × 1
Block: 128 × 1 × 1
```

Number of workgroups:

```
1664 / 128 = 13 workgroups
```

gfx1201 uses wave32, so waves per workgroup are:

```
128 threads / 32 threads per wave = 4 waves/workgroup
```

The entire dispatch therefore contains:

```
13 workgroups × 4 waves = 52 total waves
```

The GPU has 2,048 wave slots, so even if all 52 waves were simultaneously resident:

```
52 / 2048 = 2.54%
```

That is why dispatch 114 has:

```
Active-WGP ceiling: 100%
GPU-wide ceiling:     2.5%
Residency limiter:    VGPR + wave/barrier
GPU limiter:          grid
```

There is no contradiction. A WGP that receives one of these workgroups has enough resources for full theoretical residency, but the dispatch contains only 13 workgroups for 32 WGPs and only 52 waves for 2,048 slots.

# Step 1. Think of a WGP as a factory

Imagine one GPU **WGP (Work Group Processor)** is a factory.

Inside the factory are **4 workers**.

Each worker is a **SIMD**.

```
One WGP
+------------------------------------------------+
|                                                |
|   SIMD0   SIMD1   SIMD2   SIMD3                |
|                                                |
+------------------------------------------------+
```

So

```
1 WGP
    ↓
4 SIMDs
```

---

# Step 2. What does one SIMD do?

A SIMD executes **one wave at a time**.

For RDNA (gfx12), a wave contains

```
32 threads
```

Imagine one wave is one class of students.

```
Wave 0
32 students

Wave 1
32 students

Wave 2
32 students
```

The SIMD teaches **one class each cycle**.

---

# Step 3. Then why can it "host 10 waves"?

This is the important distinction.

Hosting ≠ Executing.

Suppose you're cooking.

You have

```
10 dishes
```

on the kitchen counter.

But your stove can only cook

```
1 dish
```

at a time.

```
Counter
-------------
Dish 1
Dish 2
...
Dish10

↓

Stove

Cooking Dish 3
```

The other dishes wait.

Exactly the same idea.

A SIMD may **store many waves** that are ready to run.

Only one instruction is issued each cycle, but if one wave stalls (for example, waiting for memory), the scheduler quickly switches to another ready wave.

---

# Step 4. Why store many waves?

Memory is slow.

Suppose

```
Wave A

load global memory
```

The memory takes

```
200 cycles
```

Instead of waiting,

the SIMD immediately switches

```
Wave B

do math
```

then

```
Wave C

do math
```

then

```
Wave D
```

...

until Wave A's data arrives.

This is called **latency hiding**.

More resident waves give the scheduler more choices to keep the hardware busy.

---

# Step 5. What does "10 waves/SIMD" really mean?

Imagine this storage.

```
SIMD

+------------------------+
| Wave 1                 |
| Wave 2                 |
| Wave 3                 |
| Wave 4                 |
| Wave 5                 |
| Wave 6                 |
| Wave 7                 |
| Wave 8                 |
| Wave 9                 |
| Wave10                 |
+------------------------+
```

This SIMD has room for

```
10 resident waves.
```

Each wave has

```
32 threads
```

So the SIMD currently has

```
10 × 32 = 320 threads
```

ready to execute.

---

# Step 6. Why only 10?

Because every wave consumes VGPRs.

Suppose one wave needs

```
144 VGPR
```

The SIMD owns

```
1536 VGPR
```

Total.

So

```
1536
--------
144

=10
```

The register file is now full.

There isn't enough room for an 11th wave.

---

# Step 7. What happens with only 8 waves?

Now imagine the kernel uses more registers.

```
Allocated VGPR

192
```

Now

```
1536
-------
192

=8
```

The SIMD can only keep

```
8 waves
```

instead of

```
10 waves.
```

Think of the counter becoming smaller.

Before

```
Counter

Wave1
Wave2
...
Wave10
```

After

```
Counter

Wave1
Wave2
...
Wave8
```

Now the scheduler has fewer choices.

---

# Step 8. What does "lower residency" mean?

**Residency** simply means:

> **How many waves can stay on the hardware at the same time?**

Higher residency

```
16 waves resident
```

means

```
Wave1
Wave2
...
Wave16
```

Lower residency

```
8 waves resident
```

means

```
Wave1
...
Wave8
```

There are fewer waves available to execute while others wait.

---

# Step 9. Does lower residency always mean slower?

This is a common misconception.

**Not necessarily.**

Consider two kernels.

Kernel A

```
8 waves resident

Each wave performs lots of arithmetic.
```

Kernel B

```
16 waves resident

Each wave spends most of its time waiting for memory.
```

Kernel A can actually be **faster**, despite lower residency.

Occupancy helps only if the kernel benefits from having more ready work to hide stalls. If the kernel is already limited by arithmetic throughput or doesn't stall much, increasing residency may not improve performance.

That's why your profiling table has kernels with different occupancies but similar runtimes.

---

## One more connection to your table

The first row says:

```
Resident waves/WGP = 40
```

Now you can see where that comes from:

```
One SIMD
↓

10 resident waves

One WGP
↓

4 SIMDs

Total

10 × 4 = 40 resident waves
```

Similarly, when a kernel is limited to **8 waves/SIMD**:

```
8 waves/SIMD × 4 SIMDs/WGP = 32 resident waves/WGP
```

So "Resident waves/WGP" is just the sum of the resident waves across all four SIMDs in that WGP.

---

### Check your understanding

One small question (just one):

Suppose a wave is waiting 300 cycles for global memory. If the SIMD has **16 resident waves** instead of **8**, why might the GPU be able to keep doing useful work during those 300 cycles? Try explaining it in your own words.

A SIMD switches between ready waves. If one wave is stalled (for example, waiting for memory), it executes instructions from another ready wave instead. This hides memory latency.

Exactly! You're very close. There's just one small wording change that makes it technically accurate.

Instead of saying:

> "a SIMD will switch between 16 waves' computational part"

I'd say:

> **A SIMD switches between ready waves. If one wave is stalled (for example, waiting for memory), it executes instructions from another ready wave instead. This hides memory latency.**

The important point is that the SIMD is **not splitting one computation into pieces**. Each wave executes its own instruction stream, but the hardware scheduler rapidly switches which wave issues the next instruction.

Let's visualize it.

### Case 1: Only 2 resident waves

```
Cycle

Wave A : LOAD ---------------------- waiting -------------------- ADD
Wave B : MUL -> ADD -> LOAD -------- waiting -------------------- MUL

SIMD executes:

A
B
B
...
idle
idle
idle
...
A resumes
```

Once **both waves are waiting for memory**, the SIMD has nothing to do.

---

### Case 2: 16 resident waves

```
Wave A : waiting
Wave B : waiting
Wave C : ready
Wave D : ready
Wave E : ready
...
Wave P : ready
```

Now the scheduler can do something like:

```
Cycle 1 : Wave C
Cycle 2 : Wave D
Cycle 3 : Wave E
Cycle 4 : Wave F
...
Cycle12 : Wave M
```

By the time it comes back around, Wave A's memory request may have completed.

The SIMD stayed busy almost the entire time.

---

## Why does this reduce latency?

It **doesn't make memory itself faster**.

Suppose global memory still takes:

```
300 cycles
```

It is still **300 cycles**.

What changes is that instead of sitting idle for those 300 cycles, the SIMD performs useful work from other waves.

Think of a restaurant chef.

**One order:**

```
Put pizza in oven
↓
Wait 10 minutes
```

The chef wastes time.

**Sixteen orders:**

```
Pizza 1 in oven
→ prepare Pizza 2
→ prepare Pizza 3
→ prepare Pizza 4
...
```

The oven still needs **10 minutes**.

But the chef is productive instead of idle.

The GPU scheduler works in much the same way.

---

## One more subtle point

You said:

> "a SIMD will switch between 16 waves"

Yes—but it **doesn't necessarily switch every cycle**.

If the current wave is ready and has more instructions to execute, the scheduler may continue issuing instructions from that wave. It switches primarily when another wave is a better candidate (for example, because the current one is waiting on memory or another long-latency operation).

---

### Quick review

Can you answer this one?

If a kernel goes from **10 resident waves/SIMD** to **16 resident waves/SIMD**, does that mean the SIMD executes **16 instructions simultaneously**? Or does it still issue instructions from only one wave at a time while having more waves available to choose from?

A SIMD issues one instruction for one wave at a time. Because a wave on gfx12 contains 32 threads, that same instruction is executed by all 32 threads simultaneously (SIMD execution). The scheduler chooses which resident wave issues the next instruction.

Great question. Since you've been studying MIGraphX GPU kernels and occupancy, let's connect this table to what you already know about **waves, VGPRs, and occupancy**.

We'll build it one step at a time.

---

## Step 1. What is a VGPR?

Every GPU thread (work-item) has its own registers.

Suppose your kernel does

```cpp
float a, b, c, d;
```

These variables usually live in **VGPRs (Vector General Purpose Registers)**.

If a kernel needs

```
88 VGPR/thread
```

then every thread reserves 88 registers.

The more registers each thread uses, the fewer threads the GPU can keep active simultaneously.

Think of it like this:

```
GPU register file
+----------------------------------+
|                                  |
| Registers for wave 1             |
| Registers for wave 2             |
| Registers for wave 3             |
| Registers for wave 4             |
| ...                              |
+----------------------------------+
```

The register file is fixed in size.

Large waves consume more space.

---

## Step 2. Why doesn't AMD allocate exactly 128 registers?

This is the confusing part.

AMD hardware doesn't allocate arbitrary numbers.

Instead it allocates in **chunks**.

On **gfx1201 (RDNA4, wave32)**

```
allocation granularity = 24 VGPR
```

So

```
Need 97 VGPR
```

doesn't allocate 97.

It allocates

```
120
```

because

```
align_up(97,24)=120
```

Likewise

```
Need 128
```

becomes

```
144
```

because

```
24 × 6 = 144
```

So the compiler reports

```
128 VGPR
```

but the hardware actually reserves

```
144 VGPR
```

for every thread.

That's why your table shows

```
VGPR (alloc)

128 (144)
```

meaning

```
reported : 128
allocated: 144
```

---

## Step 3. Why align to 24?

Imagine shelves in a warehouse.

Each shelf holds 24 boxes.

If you need

```
25 boxes
```

you cannot occupy

```
25/24 shelves.
```

You must reserve

```
48 spaces
```

Similarly,

```
Need 128 registers
```

must reserve

```
144
```

because registers are allocated in blocks.

---

## Step 4. Where does 1536 come from?

Each SIMD on gfx1201 owns

```
1536 VGPR
```

for active waves.

So the GPU computes

```
maximum waves
=
1536
--------------------
allocated VGPR
```

taking the floor.

For example,

Allocated VGPR = 96

```
1536 / 96 = 16
```

So

```
16 waves/SIMD
```

can fit.

---

## Step 5. Example: 128 reported VGPR

Compiler says

```
128 VGPR
```

Hardware rounds to

```
144
```

Now calculate

```
1536 / 144 = 10.66
```

Take the floor

```
10 waves/SIMD
```

So this kernel can only keep **10 waves active per SIMD**.

---

## Step 6. Why 176 VGPR becomes only 8 waves?

Reported

```
176
```

Hardware rounds

```
192
```

Now

```
1536 / 192 = 8
```

Exactly

```
8 waves/SIMD
```

This explains why the second kernel in your table has lower residency.

---

## Step 7. Why is 104 → 100 useless?

Let's compute it together.

Reported

```
104
```

Round up

```
120
```

Now imagine optimizing your kernel.

Reported becomes

```
100
```

Does it change the allocation?

No.

It is still

```
align_up(100,24)=120
```

The hardware still reserves

```
120
```

registers.

Occupancy stays

```
1536/120 = 12 waves
```

Nothing improved.

---

## Step 8. Why is 104 → 96 valuable?

Now suppose you reduce register pressure a little more.

Reported

```
96
```

Allocation

```
96
```

(no rounding needed)

Now

```
1536 / 96 = 16
```

Instead of

```
12 waves
```

you get

```
16 waves
```

So **removing just 8 reported VGPRs (104 → 96)** crosses an allocation boundary and increases the number of resident waves by **33% (12 → 16)**.

This is why compiler engineers often target **allocation thresholds**, not just "reduce VGPRs as much as possible."

---

## Step 9. Relating this to your profiling table

Look at the first kernel:

| Reported VGPR | Allocated | Waves/SIMD |
| ------------- | --------- | ---------- |
| 128           | 144       | 10         |

This is why the profiler reports

```
Resident waves/WGP = 40
```

because each SIMD can host only **10 waves**, and a WGP contains **4 SIMDs**:

```
10 waves/SIMD × 4 SIMDs = 40 waves/WGP
```

The third kernel is different:

| Reported VGPR | Allocated | Waves/SIMD |
| ------------- | --------- | ---------- |
| 96            | 96        | 16         |

Now

```
16 × 4 = 64 waves/WGP
```

which matches your table exactly:

```
Resident waves/WGP = 64
```

---

### Quick check

To make sure the idea has clicked, try this one calculation yourself:

A kernel reports **136 VGPR** on gfx1201.

1. What will the **allocated VGPR** be after rounding?
2. Using `floor(1536 / allocated VGPR)`, how many **waves per SIMD** can the hardware keep resident?

Give those two numbers, and we'll verify them together before connecting this to why higher occupancy sometimes speeds up a convolution kernel.

Excellent—you got the calculation right:

- **136 → allocated 144 VGPR** ✅
- **1536 / 144 = 10.66 → floor = 10 waves/SIMD** ✅

The confusing part isn't the math—it's **what a wave, SIMD, and WGP actually are.** Let's build the hardware picture first.

Excellent! Your answer is essentially correct. I'll make one refinement:

> **A SIMD issues one instruction for one wave at a time.** Because a wave on gfx12 contains **32 threads**, that **same instruction** is executed by **all 32 threads simultaneously** (SIMD execution). The scheduler chooses **which resident wave** issues the next instruction.

Notice it's **one instruction**, not **32 different instructions**. It's one vector instruction broadcast to 32 lanes.

---

Now let's tackle the two profiler columns. These confuse almost everyone at first.

## First, think of two questions

The profiler is answering **two completely different questions**.

### Question 1: How busy *could one WGP* become?

This is **Active-WGP ceiling**.

It ignores whether the GPU has enough work overall.

It asks only:

> **If I continuously feed work to one WGP, what fraction of its hardware capacity can this kernel occupy?**

---

### Question 2: Does the GPU actually have enough work?

This is **GPU-wide ceiling**.

It asks:

> **Across the entire dispatch, are there enough waves to keep all 32 WGPs busy?**

This depends on the grid size.

---

# Step 1. Imagine a hotel

Suppose your GPU has

```
32 hotels
```

Each hotel is one WGP.

Each hotel has

```
64 rooms
```

Each room holds one resident wave.

So the entire GPU has

```
32 × 64 = 2048 rooms
```

These are the **2048 GPU wave slots**.

---

# Step 2. Active-WGP ceiling

Look at dispatch 14.

It says

```
Resident waves/WGP = 40
```

One hotel has

```
64 rooms
```

but this kernel can only occupy

```
40 rooms
```

because of VGPR usage.

So

```
40 / 64 = 62.5%
```

This means:

> **Even if you gave this WGP unlimited work, it could never exceed 62.5% occupancy.**

Notice we haven't talked about the grid yet.

We're only looking at **one WGP**.

---

# Step 3. Now look at the whole GPU

Now imagine the kernel launches

```
50 workgroups
```

Each workgroup has

```
4 waves
```

How many waves exist?

Instead of telling you directly, let's do it together.

Can you calculate:

```
50 workgroups × 4 waves/workgroup = ?
```

(Just this one number—we'll use it to understand why the GPU-wide ceiling becomes only **9.77%**.)

Exactly! ✅

```text
50 workgroups × 4 waves/workgroup = 200 total waves
```

Now let's see why **GPU-wide ceiling = 9.77%**.

---

## Step 2. How many wave slots exist on the whole GPU?

Earlier we said:

* 1 WGP = **64 wave slots**
* GPU has **32 WGPs**

So the entire GPU can hold

```text
32 × 64 = 2048 wave slots
```

Imagine a hotel chain.

```
GPU
│
├── WGP0  → 64 rooms
├── WGP1  → 64 rooms
├── WGP2  → 64 rooms
...
└── WGP31 → 64 rooms

Total = 2048 rooms
```

Each **room = one resident wave**.

---

## Step 3. But your dispatch only created 200 waves

Your kernel launches only

```text
200 waves
```

Even if the scheduler distributes them perfectly,

```
GPU capacity : 2048 rooms

Used         : 200 rooms

Empty         : 1848 rooms
```

So the GPU can never become fully occupied.

---

## Step 4. Calculate the GPU-wide ceiling

The profiler computes

[
\frac{200}{2048}=0.0977
]

which is

```text
9.77%
```

This is called the **grid-only ceiling** because it's limited purely by the **grid size** (the amount of work you launched).

---

## Step 5. Why take the minimum?

Now compare the two limits.

### Active-WGP ceiling

Resource limit:

```
40 resident waves/WGP

40 / 64 = 62.5%
```

This says:

> "If there were unlimited work, each WGP could reach **62.5% occupancy**."

---

### Grid-only ceiling

Amount of work:

```
Only 200 waves exist.

200 / 2048 = 9.77%
```

This says:

> "The entire GPU only has enough work to fill **9.77%** of all wave slots."

---

The GPU cannot exceed **either** limit.

It's like this:

```
Resource limit : 62.5%

Work available : 9.77%

Actual possible occupancy

= min(62.5%, 9.77%)

= 9.77%
```

That's why the profiler reports:

| Metric                 | Meaning                                                                          |
| ---------------------- | -------------------------------------------------------------------------------- |
| **Active-WGP ceiling** | If a WGP always has work, how full could it become?                              |
| **GPU-wide ceiling**   | Given the total amount of work launched, how full can the **entire GPU** become? |

---

## Why is the limiter "grid"?

Look at your table:

| Resident waves/WGP | Active-WGP ceiling | GPU-wide ceiling | GPU limiter |
| ------------------:| ------------------:| ----------------:| ----------- |
| 40                 | 62.5%              | 9.8%             | **grid**    |

The profiler is saying:

> "The kernel resources are **not** the biggest problem. The problem is that you launched too little work."

If instead you launched **thousands of workgroups**, the GPU-wide ceiling might become **62.5%**, and then the limiting factor would become **VGPRs** instead of the grid size.

---

### Quick check

Suppose you changed the kernel to launch **500 workgroups** instead of **50**, while keeping **4 waves/workgroup**.

Without using a calculator:

1. How many total waves would the dispatch have?
2. Would you expect the **GPU-wide ceiling** to become **larger** or **smaller** than 9.77%?

Just answer those two questions, and then we'll connect this to why small convolutions often show **`GPU limiter = grid`** in ROCm profiling.

Excellent! You got the key idea. ✅

Let's verify it carefully.

## Step 1. Total waves

```text
500 workgroups × 4 waves/workgroup = 2000 waves
```

Correct.

---

## Step 2. Grid-only ceiling

The GPU still has

```text
32 WGP × 64 wave slots = 2048 wave slots
```

So

[
\frac{2000}{2048}\approx0.977
]

or about **97.7%**.

So yes, the **grid-only ceiling becomes much larger** than before.

---

## Step 3. But is the GPU-wide ceiling 97.7%?

Here's the important part.

The profiler computes

```text
GPU-wide ceiling =
min(Active-WGP ceiling, Grid-only ceiling)
```

For dispatch 14:

* Active-WGP ceiling = **62.5%**
* Grid-only ceiling = **97.7%**

So

```text
min(62.5%, 97.7%) = 62.5%
```

**Not 97.7%.**

Why?

Because although you've launched enough work to fill almost the whole GPU, **each WGP is still limited to 40 resident waves (62.5%) by its VGPR usage**.

Think of it like this:

```
Before

Each hotel has 64 rooms.
Only 200 guests arrive.

Problem:
Not enough guests.

Occupancy = 9.8%
```

```
After

Each hotel still has 64 rooms.
2000 guests arrive.

Now there are plenty of guests.

But each hotel closes 24 rooms
because of a maintenance issue (VGPR limit).

Only 40 rooms are usable.

Occupancy = 40/64 = 62.5%
```

The bottleneck changed.

---

## Two completely different bottlenecks

### Case 1: Grid-limited

```
Resource capacity : 62.5%
Available work    : 9.8%

Result = 9.8%

Limiter = grid
```

---

### Case 2: Resource-limited

```
Resource capacity : 62.5%
Available work    : 97.7%

Result = 62.5%

Limiter = VGPR
```

Now the grid is no longer the problem.

The **VGPR allocation** becomes the limiting factor.

---

## A useful mental model

When you read ROCm profiler output, always ask these two questions **in order**:

1. **Did I launch enough work?**
   
   * If **no**, you'll often see **`GPU limiter = grid`**.
   * The GPU is underfed.

2. **If I launched enough work, what prevents each WGP from becoming full?**
   
   * VGPR?
   * LDS?
   * Barrier/workgroup limit?

That's exactly what the two columns are separating:

* **GPU-wide ceiling** answers **"Is there enough work?"**
* **Active-WGP ceiling** answers **"If there is enough work, how full can each WGP become?"**

---

### One last question

Suppose you keep **500 workgroups** (so plenty of work), but optimize the kernel from **128 reported VGPR (144 allocated)** down to **96 VGPR**.

Earlier we calculated:

* 144 allocated → **10 waves/SIMD**
* 96 allocated → **16 waves/SIMD**

Without doing detailed math, what do you think happens to the **Active-WGP ceiling**?

Will it **increase**, **decrease**, or **stay the same**? More importantly, **why?



你的思路很好，但这里有一个**关键误区**：

> 你把 **总 wave 数量 / waves per SIMD** 当成了 **每个 SIMD 实际驻留的 wave 数量**。

这个不对。我们慢慢拆开。

---

## 1. 先纠正你的计算

你写：

> 2000/10 = 200 each SIMD have 200 wave

这里错误在于：

**10 是每个 SIMD 能容纳的最大 resident waves，不是 GPU 执行分配比例。**

不是：

```
总waves ÷ 每个SIMD容量
```

而是：

```
每个SIMD最多能驻留多少waves 这个和VGPR有关
```

---

## 2. 128 VGPR 情况

你的 kernel:

```
reported VGPR = 128
allocated VGPR = 144
```

所以：

```
1536 / 144 = 10 waves/SIMD
```

意思：

```
一个 SIMD:

+----------------+
| Wave 0         |
| Wave 1         |
| Wave 2         |
| ...            |
| Wave 9         |
+----------------+

最多10个wave
```

一个 WGP 有4个SIMD：

```
WGP

SIMD0  10 waves
SIMD1  10 waves
SIMD2  10 waves
SIMD3  10 waves

total:

40 waves/WGP
```

所以：

```
Active-WGP ceiling

=40/64

=62.5%
```

---

## 3. 96 VGPR 情况

优化以后：

```
reported VGPR = 96
allocated VGPR = 96
```

计算：

```
1536 / 96 = 16 waves/SIMD
```

现在：

```
一个 SIMD:

+----------------+
| Wave 0         |
| Wave 1         |
| ...            |
| Wave15         |
+----------------+

最多16个wave
```

一个 WGP:

```
SIMD0 16 waves
SIMD1 16 waves
SIMD2 16 waves
SIMD3 16 waves
```

所以：

```
16 × 4 = 64 waves/WGP
```

---

## 4. Active-WGP ceiling 变化

以前：

```
40 waves/WGP

40 / 64

=62.5%
```

现在：

```
64 waves/WGP

64 / 64

=100%
```

所以答案：

> ❌ 不是 stay same  
> ✅ Active-WGP ceiling 从 62.5% 提升到 100%

---

## 5. 那你的 2000 waves 怎么理解？

你算：

```
2000/10
2000/16
```

这个不是 profiler 的计算方式。

正确方式：

GPU 有：

```
32 WGP
```

每个 WGP：

```
64 wave slots
```

所以：

```
GPU总容量:

32 × 64

=2048 waves
```

---

### 情况 A: 128 VGPR

资源限制：

```
每WGP只能40 waves
```

整个GPU：

```
32 × 40

=1280 resident waves
```

但是你的grid：

```
2000 waves
```

足够。

所以：

```
实际occupancy

=1280 / 2048

=62.5%
```

限制因素：

```
VGPR
```

---

### 情况 B: 96 VGPR

资源限制：

```
每WGP 64 waves
```

整个GPU：

```
32 ×64

=2048 resident waves
```

grid：

```
2000 waves
```

所以：

```
实际occupancy

=2000/2048

=97.7%
```

限制因素：

```
grid
```

---

## 6. 这也是为什么降低VGPR很重要

从：

```
128 VGPR
```

到：

```
96 VGPR
```

发生了：

```
144 allocated
        |
        v
96 allocated
```

导致：

```
10 waves/SIMD
        |
        v
16 waves/SIMD
```

WGP:

```
40 waves
        |
        v
64 waves
```

结果：

```
Active-WGP ceiling

62.5%
        |
        v
100%
```

这是一个非常大的变化。

---

## 最后总结一句

你可以这样记：

```
VGPR决定：
一个SIMD里面最多放几个wave

LDS决定：
一个WGP里面最多放几个workgroup

Grid决定：
整个GPU有没有足够wave填满它
```

所以：

- **Active-WGP ceiling** → "单个WGP最多能吃多少"

- **GPU-wide ceiling** → "整个dispatch有没有足够食物"

你已经掌握 occupancy 的核心逻辑了。下一步可以看为什么 **降低VGPR可能让kernel变慢（spill），而不是一定变快**，这也是GPU kernel优化最容易踩的坑。**

> 
