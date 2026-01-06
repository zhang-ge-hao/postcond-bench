https://github.com/devnied/Bit-lib4j/blob/d0c1eff1da901a9022536240347ba7b4bf2e5106/./src/main/java/fr/devnied/bitlib/BitUtils.java#L303-L344
```
//@ ensures getCurrentBitIndex() == \old(getCurrentBitIndex()) + pLength;
//@ ensures \result >= 0;
//@ ensures pLength >= 64 || \result < (1L << pLength);
//@ ensures Arrays.equals(getData(), \old(getData()));
//@ ensures getSize() == \old(getSize());
```
```
hallucination on semantics

result can be negative
the comment says "doesn't handle signed values"
```
jml_fail
```
//@ ensures pLength >= 0 && pLength <= Long.SIZE;
//@ ensures pLength == 0 ==> \result == 0L;
//@ ensures currentBitIndex == \old(currentBitIndex) + pLength;
//@ ensures pLength < Long.SIZE ==> (\result >= 0 && \result < (1L << pLength));
//@ ensures pLength > 0 ==> (((\result >>> 0) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 0)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 0)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 1 ==> (((\result >>> 1) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 1)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 1)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 2 ==> (((\result >>> 2) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 2)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 2)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 3 ==> (((\result >>> 3) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 3)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 3)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 4 ==> (((\result >>> 4) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 4)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 4)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 5 ==> (((\result >>> 5) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 5)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 5)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 6 ==> (((\result >>> 6) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 6)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 6)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 7 ==> (((\result >>> 7) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 7)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 7)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 8 ==> (((\result >>> 8) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 8)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 8)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 9 ==> (((\result >>> 9) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 9)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 9)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 10 ==> (((\result >>> 10) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 10)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 10)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 11 ==> (((\result >>> 11) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 11)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 11)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 12 ==> (((\result >>> 12) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 12)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 12)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 13 ==> (((\result >>> 13) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 13)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 13)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 14 ==> (((\result >>> 14) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 14)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 14)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 15 ==> (((\result >>> 15) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 15)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 15)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 16 ==> (((\result >>> 16) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 16)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 16)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 17 ==> (((\result >>> 17) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 17)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 17)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 18 ==> (((\result >>> 18) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 18)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 18)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 19 ==> (((\result >>> 19) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 19)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 19)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 20 ==> (((\result >>> 20) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 20)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 20)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 21 ==> (((\result >>> 21) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 21)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 21)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 22 ==> (((\result >>> 22) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 22)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 22)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 23 ==> (((\result >>> 23) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 23)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 23)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 24 ==> (((\result >>> 24) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 24)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 24)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 25 ==> (((\result >>> 25) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 25)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 25)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 26 ==> (((\result >>> 26) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 26)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 26)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 27 ==> (((\result >>> 27) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 27)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 27)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 28 ==> (((\result >>> 28) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 28)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 28)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 29 ==> (((\result >>> 29) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 29)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 29)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 30 ==> (((\result >>> 30) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 30)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 30)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 31 ==> (((\result >>> 31) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 31)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 31)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 32 ==> (((\result >>> 32) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 32)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 32)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 33 ==> (((\result >>> 33) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 33)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 33)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 34 ==> (((\result >>> 34) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 34)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 34)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 35 ==> (((\result >>> 35) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 35)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 35)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 36 ==> (((\result >>> 36) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 36)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 36)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 37 ==> (((\result >>> 37) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 37)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 37)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 38 ==> (((\result >>> 38) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 38)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 38)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 39 ==> (((\result >>> 39) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 39)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 39)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 40 ==> (((\result >>> 40) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 40)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 40)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 41 ==> (((\result >>> 41) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 41)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 41)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 42 ==> (((\result >>> 42) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 42)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 42)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 43 ==> (((\result >>> 43) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 43)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 43)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 44 ==> (((\result >>> 44) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 44)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 44)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 45 ==> (((\result >>> 45) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 45)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 45)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 46 ==> (((\result >>> 46) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 46)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 46)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 47 ==> (((\result >>> 47) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 47)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 47)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 48 ==> (((\result >>> 48) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 48)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 48)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 49 ==> (((\result >>> 49) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 49)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 49)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 50 ==> (((\result >>> 50) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 50)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 50)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 51 ==> (((\result >>> 51) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 51)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 51)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 52 ==> (((\result >>> 52) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 52)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 52)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 53 ==> (((\result >>> 53) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 53)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 53)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 54 ==> (((\result >>> 54) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 54)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 54)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 55 ==> (((\result >>> 55) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 55)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 55)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 56 ==> (((\result >>> 56) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 56)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 56)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 57 ==> (((\result >>> 57) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 57)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 57)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 58 ==> (((\result >>> 58) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 58)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 58)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 59 ==> (((\result >>> 59) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 59)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 59)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 60 ==> (((\result >>> 60) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 60)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 60)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 61 ==> (((\result >>> 61) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 61)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 61)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 62 ==> (((\result >>> 62) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 62)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 62)) % BYTE_SIZE))) & 1L));
//@ ensures pLength > 63 ==> (((\result >>> 63) & 1L) == (((\old(byteTab)[(\old(currentBitIndex) + (pLength - 1 - 63)) / BYTE_SIZE] & DEFAULT_VALUE) >>> (BYTE_SIZE - 1 - ((\old(currentBitIndex) + (pLength - 1 - 63)) % BYTE_SIZE))) & 1L));
```
