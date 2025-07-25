
<div align="center">

![Logo]
<br> <br>

# Septabin

</div>

Septabin is a compact, self-validating binary encoding system that represents characters using fixed-length 7-bit binary values. It includes message framing and checksum verification for integrity — ideal for lightweight, structured, and tamper-resistant communication.

---

## Features

- Fixed 7-bit binary encoding for all supported characters
- Start (`0000000`) and End (`1111111`) markers to define message boundaries
- Parity block for integrity checking using modulo 128 checksum
- Supports uppercase, lowercase, digits, space, and selected punctuation (`.,!?-`)
- Simple rule set that is both human-readable and verifiable

---

## How It Works

A Septabin message has the structure:

```
0000000 + [data blocks] + [checksum block] + 1111111
```

- Each block is exactly 7 bits.
- The checksum block is computed by summing the decimal values of all data blocks and taking modulo 128.

### Example

Plaintext:  
```
Hello!
```

Septabin binary:  
```
0000000 0100100 0010101 0110110 0110110 0111111 0110100 1111111
```

The last data block before the end marker is the checksum for integrity verification.

---

## Translator

A translator that translates from and to Septabin is available. 
This translator also has the added ability to check the integrity of Septabin strings using the checksum block.
The translator is available from me (Catana791) directly on Discord.

<!----------------------------------[ Links ]--------------------------------->
[Logo]: septabin-logo.png
