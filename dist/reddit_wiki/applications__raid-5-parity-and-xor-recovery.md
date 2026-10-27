# RAID-5: rebuilding a lost disk by solving one linear equation

### Start here

A storage array spreads data across several disks. Disks fail, and copying everything twice to survive
a failure would halve the usable space. [RAID](https://en.wikipedia.org/wiki/Standard_RAID_levels)-5 survives the loss of any one disk at the cost of just one
disk's worth of extra space.

The trick is a [checksum](https://en.wikipedia.org/wiki/Checksum) of the simplest possible kind. For each group of blocks stored at the same
position on the data disks, the array stores one extra block, built bit by bit: each bit records
whether the matching bits of the data blocks contain an even or an odd number of 1s. If one disk dies,
every one of its bits can be worked out from the others, because the count of 1s in each position has
to come out even again. The missing bit is whatever makes it so.

In algebra this is one equation, data plus check equals zero, in the arithmetic where 1 + 1 = 0, and
recovering a lost disk is solving that equation for its single unknown. Everything about what RAID-5
can and cannot do follows from it being one equation: one unknown can be found, but two cannot, and a
block that is wrong rather than missing can be noticed but not located.

**Field:** Storage systems, system administration, distributed storage  
**Tier:** 1 — one parity equation over [GF(2)](https://en.wikipedia.org/wiki/GF%282%29), the numbers 0 and 1 with arithmetic modulo 2 (addition is [XOR](https://en.wikipedia.org/wiki/Exclusive_or)), solved for one unknown. Surviving two failures needs a second independent equation over the larger field GF(2^8), which is Tier 3.  
**Scalar field:** GF(2), the numbers 0 and 1 with arithmetic modulo 2 (addition is XOR, and subtraction is the same as addition)  
**Vectors:** GF(2)^w for a block of w bits: every block of a stripe is a vector, and the parity equation holds coordinate by coordinate, one bit position at a time. A stripe across n disks is a point of (GF(2)^w)^n, and the valid stripes form the subspace cut out by the parity equation  
**Underlying equations:** One linear equation over GF(2) per stripe, applied to each bit position: the data blocks and the parity block add up to zero modulo 2

### The problem

Two words carry the whole subject. A **block** is a fixed-size piece of one disk: a run of consecutive
bits, typically 4 KiB to 1 MiB, and the unit that the array reads, writes and protects (storage
engineers also call it a chunk or stripe unit). The array divides every disk into blocks and lines them
up across the disks. A **stripe** is then the set of n blocks at the same position, one on each disk:
the first block of every disk forms stripe 1, the second block of every disk forms stripe 2, and so on.
In RAID-5, n − 1 blocks of each stripe hold data and the remaining one, the parity block, is computed
from them. Each stripe is protected on its own, so recovering a failed disk means recovering its block
in every stripe, one stripe at a time.

The problem is to store data on n disks so that the contents of any one failed disk can be
reconstructed from the other n − 1, using one block of redundancy per stripe (one disk's worth in
total), and to keep the parity correct as data change.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| n | number of disks | disks in the array, including parity | integer | — |
| w | block size | bits per block | integer | bits |
| d_1, …, d_(n−1) | data blocks | the data in one stripe | each a w × 1 vector over GF(2) | bits |
| p | parity block | the check block of the stripe | w × 1 over GF(2) | bits |
| d_old, d_new | one data block | before and after an update | w × 1 | bits |
| p_old, p_new | parity block | before and after the update | w × 1 | bits |

All arithmetic is in GF(2): 0 + 0 = 1 + 1 = 0 and 0 + 1 = 1, which on blocks is the bitwise exclusive
OR (XOR). Since 1 + 1 = 0, every block is its own negative, and subtracting is the same as adding.

### Formulation

**Where the equations come from.** The model is a design choice: the parity block of every stripe is
defined to make one linear equation hold.

**One bit position.** Look at bit position k of every block in a stripe. The [parity bit](https://en.wikipedia.org/wiki/Parity_bit) is defined by

```
p[k] = d_1[k] + d_2[k] + ⋯ + d_(n−1)[k]     (mod 2)
```

which is the even-or-odd count of 1s: p[k] is 1 exactly when the data bits in position k contain an odd
number of 1s. Moving p[k] to the left side, which costs nothing because subtraction is addition, gives
the equation that every stripe satisfies:

```
d_1[k] + d_2[k] + ⋯ + d_(n−1)[k] + p[k] = 0     (mod 2)
```

**All bit positions at once.** The same equation holds in every one of the w positions, so for whole
blocks it reads d_1 + ⋯ + d_(n−1) + p = 0 in GF(2)^w. In matrix terms each bit position is the 1 × n
system (1 1 ⋯ 1) v = 0, with v the n bits of that position across the disks. Its rank is 1, so the
valid stripes form a subspace of dimension n − 1: any n − 1 blocks can be chosen freely, and the last
is determined.

**Recovering a lost disk.** If disk j fails, its block is the only unknown in the equation. Solving
for it, and remembering that subtraction is addition,

```
d_j = (sum of all the other blocks of the stripe)     (mod 2)
```

so the lost block is the XOR of the survivors.

**Updating one block.** When block d_i changes from d_old to d_new, the equation still has to hold.
Because it is linear, the parity changes by the same amount as the data:

```
p_new = p_old + d_old + d_new
```

so a small write reads only the old data and old parity, not the rest of the stripe.

**Worked case: four disks, 4-bit blocks.** Data d_1 = 1011, d_2 = 0110, d_3 = 1100 give parity
p = 1011 + 0110 + 1100 = 0001. If disk 2 fails, d_2 = d_1 + d_3 + p = 1011 + 1100 + 0001 = 0110, as
stored. If d_2 is then rewritten as 0011, the new parity is 0001 + 0110 + 0011 = 0100, and indeed
1011 + 0011 + 1100 = 0100.

### Matrix structure

One row of 1s, 1 × n, applied independently to each of the w bit positions, so the whole stripe is a
w × nw system made of w identical copies. Real arrays also rotate which disk holds the parity from
stripe to stripe, so that parity updates do not all land on one disk. That changes which coordinate is
called p, not the equation.

### What is computed

Writing a full stripe: one XOR across the data blocks. Updating one block: read the old data and
parity, XOR in the change, write both back, which is four disk operations and the reason small writes
are slow on RAID-5. Reading in degraded mode or rebuilding: XOR the surviving blocks of each stripe.
Processors provide vector instructions that XOR many bytes at once, and the Linux md driver chooses the
fastest routine at boot.

### Why linear algebra is the right tool

Every capability and limit of RAID-5 is a statement about one linear equation. One unknown can be
solved for; two unknowns in one equation leave a one-dimensional solution set, so a second failure
during a rebuild loses data. Updating parity from the change alone works because the equation is
linear. The design generalizes exactly as linear algebra suggests: to survive two failures, add a second
equation independent of the first (RAID-6), and to survive r failures, use r independent equations,
which is an [erasure code](https://en.wikipedia.org/wiki/Erasure_code).

### Pitfall worth teaching

Parity corrects erasures, not errors. If a disk reports that it has failed, the unknown's position is
known and the equation can be solved. If instead a block is silently wrong, through a firmware bug, a
bit flip or the write hole (a crash after the data block was written but before its parity), the stripe
simply violates its equation. The array can detect that something is wrong, but one equation cannot say
which of the n blocks is the culprit: changing any one of them would restore it. Worse, if the mismatch
goes unnoticed and a disk later fails, the rebuild solves the equation using the wrong block and
reconstructs wrong data without any warning. This is the linear-algebra content of the advice that
RAID is not a backup, and the reason file systems such as [ZFS](https://en.wikipedia.org/wiki/ZFS) add checksums: a checksum locates the bad
block, turning the error back into an erasure.

### Extensions

RAID-6 adds a second check block, computed with coefficients from the 256-element field GF(2^8), so
that two erasures give two independent equations; the scheme is a [Reed–Solomon](https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction) code (the
[error-correcting](https://en.wikipedia.org/wiki/Error_correction_code) codes entry, Tier 3 for GF(2^m)). Distributed storage systems use the same idea with
more check blocks, and the error-correcting codes entry shows how several parity checks can locate an
error as well as fill an erasure. Shamir secret sharing is the same equations-from-redundancy idea over
GF(p), arranged so that too few shares reveal nothing. [CRC](https://en.wikipedia.org/wiki/Cyclic_redundancy_check) checksums, which detect errors in
transmitted data, are also linear over GF(2) (the CRC entry).

### Terminology

How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| stripe | one block from each disk at the same position, the unknowns of one parity equation |
| stripe unit (chunk) | one block of a stripe, a vector in GF(2)^w |
| parity block | the block chosen so that every stripe satisfies d_1 + ⋯ + d_(n−1) + p = 0 |
| XOR | addition in GF(2), applied bit by bit |
| degraded mode | one block of each stripe unknown, recovered on every read by solving the equation |
| rebuild (resilvering) | solving the equation for the failed disk's block in every stripe |
| read-modify-write (small write) | updating parity by p_new = p_old + d_old + d_new, which uses linearity |
| write hole | a crash between writing data and parity, which leaves a stripe that violates its equation |
| erasure vs error | a lost block at a known position (solvable) vs a wrong block at an unknown position (only detectable) |
| RAID-6 | a second, independent equation over GF(2^8), so two erasures can be solved |

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
