123 0 0111 1011
456 1 1100 1000
 72 0 0100 1000


 #ip 4
_start_
0  seti 123 0 1       R1 <- 123 (0 0111 1011)
_loop_
1  bani 1 456 1       |
2  eqri 1 72 1        | IF R1 AND 456 (1 1100 1000) != 72 (0 0100 1000) GOTO _loop_
3  addr 1 4 4         |
4  seti 0 0 4         |
5  seti 0 3 1         R1 <- 0
_a_
6  bori 1 65536 2     R2 <- R1 OR 65536 (1 0000 0000 0000 0000)
                      // if R1 bit 16 is 1 R2 <- R1 ELSE R2 <- R1 + 65536 
7  seti 7902108 7 1   R1 <- 7902108 (0111 1000 1001 0011 1001 1100)
_b_
8  bani 2 255 5       R5 <- R2 AND 255 (1111 1111) // R5 is lowest byte of R2
9  addr 1 5 1         R1 += R5  // R1 += max(R2, 255)
10 bani 1 16777215 1  Truncate R1 to lowest 3 bytes i.e R1 = min(r1, 16777215)
11 muli 1 65899 1     R1 *= 65899
12 bani 1 16777215 1  Truncate R1 to lowest 3 bytes i.e R1 = min(r1, 16777215)
13 gtir 256 2 5       |
14 addr 5 4 4         | if R2 < 256 goto _e_ else goto _c_ // if R2 < 256 and R1 == input (R0) then DONE!
15 addi 4 1 4         |                                    // find first value of R1 when R2 < 256
16 seti 27 0 4        |
17 seti 0 0 5         R5 <- 0                 |
_c_                                           |
18 addi 5 1 3         R3 <- R5 + 1            |  r2 = 0..255 -> r2 = 0; then _b_
19 muli 3 256 3       R3 *= 256               |  r2 = 256..511 -> r2 = 1; then _b_
20 gtrr 3 2 3         |                       |
21 addr 3 4 4         | if R3 > R2 goto _d_   |  R2 = int(R2 / 256); then loop at _b_
22 addi 4 1 4         |                       |  Shift R2 8 bits to right (remove last byte)
23 seti 25 2 4        |                       |
24 addi 5 1 5         R5 += 1                 |
25 seti 17 2 4        GOTO _c_                |
_d_                                           |
26 setr 5 1 2         R2 <- R5                |
27 seti 7 2 4         GOTO _b_                |
_e_
28 eqrr 1 0 5         |
29 addr 5 4 4         | if R0 == R1 goto _done_ else GOTO _a_
30 seti 5 9 4         |
_done_
