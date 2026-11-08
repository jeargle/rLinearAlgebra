# CRC checksums: the remainder of a polynomial division is a linear map on bits

### Start here

Every [Ethernet](https://en.wikipedia.org/wiki/Ethernet) frame, every [ZIP archive](https://en.wikipedia.org/wiki/ZIP_%28file_format%29) and every [PNG](https://en.wikipedia.org/wiki/PNG) image carries a few extra bytes computed from
the rest: a cyclic redundancy check, or [CRC](https://en.wikipedia.org/wiki/Cyclic_redundancy_check). The receiver recomputes them from the data it got. If the
two disagree, something was corrupted on the way, and the data is sent again or rejected.

The CRC is defined as the remainder of a [long division](https://en.wikipedia.org/wiki/Polynomial_long_division), but of a special kind. The bits of the message
are treated as the coefficients of a polynomial, and all arithmetic on the coefficients is done
modulo 2, so 1 + 1 = 0 and there are no carries. Long division then needs nothing but [XOR](https://en.wikipedia.org/wiki/Exclusive_or), which is
why a CRC is cheap enough to compute in hardware on every packet.

The step from message to remainder is a linear map, and linear algebra explains the rest: how the fast
methods work, which errors slip through, and why a CRC protects against noise but not against an
attacker.

**Field:** Networking, storage, file formats, digital communications  
**Tier:** 1 — a CRC is the remainder after dividing by a fixed polynomial over [GF(2)](https://en.wikipedia.org/wiki/GF%282%29), the numbers 0 and 1 with arithmetic modulo 2, and taking that remainder is a linear map from message bits to check bits. Explaining which generators catch which errors, through the ring of polynomials modulo the generator, is Tier 3.  
**Scalar field:** GF(2), the numbers 0 and 1 with arithmetic modulo 2 (addition is XOR, and subtraction is the same as addition)  
**Vectors:** GF(2)^m for an m-bit message, read as the coefficients of a polynomial of degree below m, and GF(2)^r for the r check bits, the polynomials of degree below r. The CRC is a linear map from GF(2)^m to GF(2)^r, and the error patterns it cannot detect form a [null space](https://en.wikipedia.org/wiki/Kernel_%28linear_algebra%29)  
**Underlying equations:** Polynomial division over GF(2): M(x) x^r = Q(x) G(x) + R(x) with R of degree below r, and the check bits are the coefficients of R

### The problem

A **message** is a string of m bits, and it is read as a polynomial: the bits 1101 stand for
1·x³ + 1·x² + 0·x + 1 = x³ + x² + 1. The coefficients live in GF(2), the numbers 0 and 1 with
arithmetic modulo 2: 1 + 1 = 0, so adding two polynomials is XOR of their bit strings, and subtracting is
the same as adding. A **generator polynomial** G(x) of degree r is fixed in advance by the standard.
The sender appends r **check bits** so that the whole transmitted string, the **codeword**, is a
multiple of G(x). The receiver divides what arrives by G(x) and accepts only a zero remainder.

The motivating contrast is between **detecting** errors and **correcting** them. The [error-correcting](https://en.wikipedia.org/wiki/Error_correction_code)
codes entry repairs flipped bits; a CRC only notices them, and the fix is to send again. Detection is
much cheaper, and on networks and disks where errors are rare it is what is needed.

Compute the check bits for a message quickly, and say exactly which corruptions the receiver will
miss.

### Variables

| Symbol | Name | What it holds | Shape | Units |
|---|---|---|---|---|
| m | message length | number of message bits | integer | bits |
| r | CRC width | degree of the generator, number of check bits | integer | bits |
| u | message vector | the message bits as a vector | m × 1 over GF(2) | bits |
| M(x) | message polynomial | the same bits as polynomial coefficients | degree below m | — |
| G(x) | generator | the fixed divisor, of degree r | polynomial | — |
| Q(x) | quotient | the result of the division, discarded | polynomial | — |
| R(x) | remainder | of degree below r; its coefficients are the check bits | polynomial | — |
| c | check bits | the coefficients of R(x) as a vector | r × 1 over GF(2) | bits |
| H | CRC matrix | c = H u | r × m over GF(2) | — |
| E(x) | error pattern | the bits flipped in transit, as a polynomial | polynomial | — |
| s | register state | the r bits held in the shift register | r × 1 over GF(2) | bits |
| K | companion matrix | the register's update, s → K s | r × r over GF(2) | — |
| g | feedback vector | the coefficients of G(x) below x^r | r × 1 over GF(2) | — |

### Formulation

**Where the equations come from.** The defining equation is division with remainder, carried out on
polynomials whose coefficients are added modulo 2.

**The familiar formula.** The CRC is the remainder: shift the message up by r places and divide by the
generator,

```
M(x) · x^r  =  Q(x) · G(x)  +  R(x),        R of degree below r
```

The sender transmits M(x) x^r + R(x). Because subtraction is addition, that equals Q(x) G(x), a multiple
of the generator, and the receiver's division leaves remainder zero.

**Long division with XOR.** Take G(x) = x³ + x + 1, the bits 1011, so r = 3, and the message 1101.
Append three 0s and repeatedly XOR the generator under the leading 1:

```
  1101000     the message followed by three 0s
⊕ 1011
  0110000
⊕  1011
  0011100
⊕   1011
  0001010
⊕    1011
  0000001     remainder 001
```

The check bits are 001 and the codeword is 1101001.

**One column first.** Division by G(x) is linear. If A(x) leaves remainder R_1(x) and B(x) leaves R_2(x),
then A(x) + B(x) leaves R_1(x) + R_2(x), because the sum of the two quotients times G(x) accounts for the
rest and R_1 + R_2 still has degree below r. So the CRC of a message is the sum of the CRCs of its
individual 1-bits, and it is enough to know the remainder of each single power of x. For the generator
above, x³ = G(x) + x + 1 leaves x + 1, the bits 011. Multiplying by x and reducing again,

```
x⁴  =  x · x³   leaves   x · (x + 1)          =  x² + x            bits 110
x⁵  =  x · x⁴   leaves   x³ + x²  →  x² + x + 1                   bits 111
x⁶  =  x · x⁵   leaves   x³ + x² + x  →  x² + 1                   bits 101
```

where each arrow replaces x³ by x + 1.

**Stacking the columns.** The message bit that multiplies x³ in M(x) ends up multiplying x⁶ after the
shift, and so on down. Putting each bit's remainder in its column gives the CRC matrix, with message
bits in the order (coefficient of x³, x², x, 1) and check bits in the order (x², x, 1):

```
[ 1  1  1  0 ] [ 1 ]   [ 0 ]
[ 0  1  1  1 ] [ 1 ] = [ 0 ]
[ 1  1  0  1 ] [ 0 ]   [ 1 ]
               [ 1 ]
     H           u       c
```

Row by row, modulo 2: 1 + 1 + 0 + 0 = 0, 0 + 1 + 0 + 1 = 0, and 1 + 1 + 0 + 1 = 1. The matrix gives the same
check bits, 001, as the long division. The 7-bit codewords of this generator form a [Hamming(7,4)](https://en.wikipedia.org/wiki/Hamming%287,4%29) code, the
code of the error-correcting codes entry with its bit positions rearranged into cyclic form.

**The [shift register](https://en.wikipedia.org/wiki/Linear-feedback_shift_register).** Hardware processes one bit per clock tick with a register of r bits. Each tick
shifts the register, and if the bit leaving the top differs from the incoming message bit, it XORs in
the generator's lower coefficients. In matrix form, with the state s = (s_2, s_1, s_0) and
g = (0, 1, 1) from x + 1,

```
s  ←  K s  +  (incoming bit) · g,          [ 0  1  0 ]
                                       K = [ 1  0  1 ]
                                           [ 1  0  0 ]
```

For the message 1101, starting from 000, the states are 011, 101, 001 and 001, and the final state is
the remainder. K is the [companion matrix](https://en.wikipedia.org/wiki/Companion_matrix) of G(x): it multiplies the register's polynomial by x and
reduces.

**Worked case: CRC-8 of "Hi".** Take G(x) = x⁸ + x² + x + 1, the CRC-8 used by the [SMBus](https://en.wikipedia.org/wiki/System_Management_Bus) protocol, and the
two [ASCII](https://en.wikipedia.org/wiki/ASCII) bytes "Hi", 0x48 and 0x69, which are the 16 bits 0100 1000 0110 1001. Long division and the
shift register both give the remainder 0xEB, the bits 1110 1011. The matrix form gives it as a sum of
six columns of H, one for each 1-bit of the message:

| Message bit | Power after the shift | Its column (remainder) |
|---|---|---|
| 2nd | x²² | 0101 1011 |
| 5th | x¹⁹ | 1010 1000 |
| 10th | x¹⁴ | 1100 0111 |
| 11th | x¹³ | 1110 0000 |
| 13th | x¹¹ | 0011 1000 |
| 16th | x⁸ | 0000 0111 |
| sum (XOR) | | 1110 1011 = 0xEB |

Linearity can be checked directly. The CRC of "Ok" is 0x8E, and the CRC of the bytewise XOR of "Hi" and
"Ok" is 0x65, which is 0xEB ⊕ 0x8E.

### Matrix structure

H is a dense r × m matrix over GF(2). Its columns are not independent of each other: each is K times the
one before, since moving a bit one place earlier multiplies it by x. Software uses linearity on whole
bytes, with a lookup table of the CRCs of all 256 byte values, so that each byte costs a table lookup
and a few XORs instead of eight register steps. Hardware needs only r flip-flops and a few XOR gates.

### What is computed

The CRC-32 of Ethernet, ZIP, gzip and PNG uses the generator 0x04C11DB7. It processes bits in reversed
order, starts the register at all 1s and XORs the result with all 1s, so its check value for the ASCII
string "123456789" is 0xCBF43926. Libraries such as [zlib](https://en.wikipedia.org/wiki/Zlib) provide it. Modern processors have
instructions for CRCs: x86 has one for the CRC-32C variant, and carry-less multiplication instructions
let software process many bytes at once. Storage systems, the iSCSI and SCTP protocols and the ext4 and
Btrfs file systems use CRC-32C.

### Why linear algebra is the right tool

The remainder is a linear map from message bits to check bits, and every practical fact about CRCs is a
fact about that map. The table method works because the CRC of a message is the sum of the CRCs of its
parts. The shift register is a companion matrix applied once per bit. Error detection is a null-space
question. If the channel adds an error pattern E(x), the receiver's remainder is the remainder of E(x)
alone, so the error goes unnoticed exactly when E(x) is a multiple of G(x). Choosing a good generator
means choosing one whose multiples are unlike likely errors. When G(x) has a constant term, no [burst](https://en.wikipedia.org/wiki/Burst_error) of
r or fewer consecutive flipped bits is a multiple of it, so every such burst is detected.

### Pitfall worth teaching

A CRC protects against accidents, not against an attacker, and linearity is the reason. Anyone who
changes a message by a known pattern of bit flips can compute the matching change in the CRC, because
the CRC of the change is H times it, and fix the check bits without knowing anything secret. Standard
CRCs with an initial value and a final XOR are [affine](https://en.wikipedia.org/wiki/Affine_transformation) rather than linear: for messages of equal length,
CRC(a ⊕ b) = CRC(a) ⊕ CRC(b) ⊕ CRC(0). The attack works the same way.

This is how the [WEP](https://en.wikipedia.org/wiki/Wired_Equivalent_Privacy) encryption of early Wi-Fi was broken. WEP encrypted each packet by XOR with a key
stream and protected it with a CRC-32 inside the encryption. Both steps are linear in the message bits,
so an attacker could flip chosen bits of an encrypted packet and the matching bits of its encrypted CRC,
and the receiver would accept the altered packet. Integrity against an adversary needs a
[message authentication code](https://en.wikipedia.org/wiki/Message_authentication_code) such as [HMAC](https://en.wikipedia.org/wiki/HMAC), or an encryption mode with built-in authentication.

### Extensions

The polynomials modulo G(x) form a ring, and when G(x) is [irreducible](https://en.wikipedia.org/wiki/Irreducible_polynomial) they form a [finite field](https://en.wikipedia.org/wiki/Finite_field) with 2^r
elements (Tier 3). For a primitive G(x), the companion matrix K has order 2^r − 1, and the register
cycles through every nonzero state, producing the [maximal-length sequences](https://en.wikipedia.org/wiki/Maximum-length_sequence) used for scrambling and
spread-spectrum radio. [BCH](https://en.wikipedia.org/wiki/BCH_code) and [Reed–Solomon](https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction) codes are cyclic codes like the Hamming code above, built
over larger fields such as GF(2^8); they correct errors as well as detecting them, in [QR codes](https://en.wikipedia.org/wiki/QR_code), CDs and
deep-space links. The [RAID](https://en.wikipedia.org/wiki/Standard_RAID_levels)-5 entry uses a single parity equation over GF(2), and its RAID-6 extension
uses GF(2^8). The [Berlekamp–Massey](https://en.wikipedia.org/wiki/Berlekamp%E2%80%93Massey_algorithm) algorithm finds the shortest shift register that generates a given
sequence, which is solving a linear system for the register's feedback.

### Terminology

How this field's vocabulary reads as linear algebra.

| Domain term | In linear algebra |
|---|---|
| check bits (checksum) | the r bits appended to a message so the receiver can test it |
| generator polynomial G(x) | the fixed divisor of degree r that both ends agree on |
| codeword | a message with its check bits appended; always a multiple of G(x) |
| CRC-r | a cyclic redundancy check with r check bits, such as CRC-8 or CRC-32 |
| error detection vs error correction | noticing that bits changed, versus also knowing which ones |
| burst error | errors confined to a run of consecutive bits |
| shift register (LFSR) | the hardware that computes a CRC one bit per clock |
| lookup table | precomputed CRCs of all 256 byte values, for software that works a byte at a time |
| initial value and final XOR | constants added in standard CRCs, which make the map affine |
| message authentication code (MAC) | a keyed check that, unlike a CRC, an attacker cannot recompute |

---

[Back to the index](/r/LinearAlgebra/wiki/applications)
