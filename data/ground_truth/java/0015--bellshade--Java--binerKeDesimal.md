https://github.com/bellshade/Java/blob/d5387355d572170808e7ef5d014ec4343e6c3471/./src/main/java/algorithm/conversions/BinaryToDecimal.java#L10-L31
```
//@ ensures \old(angkaBiner) >= 0 ==> (((\old(angkaBiner) / 1L) % 10L == 0L) || ((\old(angkaBiner) / 1L) % 10L == 1L)) && (((\old(angkaBiner) / 10L) % 10L == 0L) || ((\old(angkaBiner) / 10L) % 10L == 1L)) && (((\old(angkaBiner) / 100L) % 10L == 0L) || ((\old(angkaBiner) / 100L) % 10L == 1L)) && (((\old(angkaBiner) / 1000L) % 10L == 0L) || ((\old(angkaBiner) / 1000L) % 10L == 1L)) && (((\old(angkaBiner) / 10000L) % 10L == 0L) || ((\old(angkaBiner) / 10000L) % 10L == 1L)) && (((\old(angkaBiner) / 100000L) % 10L == 0L) || ((\old(angkaBiner) / 100000L) % 10L == 1L)) && (((\old(angkaBiner) / 1000000L) % 10L == 0L) || ((\old(angkaBiner) / 1000000L) % 10L == 1L)) && (((\old(angkaBiner) / 10000000L) % 10L == 0L) || ((\old(angkaBiner) / 10000000L) % 10L == 1L)) && (((\old(angkaBiner) / 100000000L) % 10L == 0L) || ((\old(angkaBiner) / 100000000L) % 10L == 1L)) && (((\old(angkaBiner) / 1000000000L) % 10L == 0L) || ((\old(angkaBiner) / 1000000000L) % 10L == 1L)) && (((\old(angkaBiner) / 10000000000L) % 10L == 0L) || ((\old(angkaBiner) / 10000000000L) % 10L == 1L)) && (((\old(angkaBiner) / 100000000000L) % 10L == 0L) || ((\old(angkaBiner) / 100000000000L) % 10L == 1L)) && (((\old(angkaBiner) / 1000000000000L) % 10L == 0L) || ((\old(angkaBiner) / 1000000000000L) % 10L == 1L)) && (((\old(angkaBiner) / 10000000000000L) % 10L == 0L) || ((\old(angkaBiner) / 10000000000000L) % 10L == 1L)) && (((\old(angkaBiner) / 100000000000000L) % 10L == 0L) || ((\old(angkaBiner) / 100000000000000L) % 10L == 1L)) && (((\old(angkaBiner) / 1000000000000000L) % 10L == 0L) || ((\old(angkaBiner) / 1000000000000000L) % 10L == 1L)) && (((\old(angkaBiner) / 10000000000000000L) % 10L == 0L) || ((\old(angkaBiner) / 10000000000000000L) % 10L == 1L)) && (((\old(angkaBiner) / 100000000000000000L) % 10L == 0L) || ((\old(angkaBiner) / 100000000000000000L) % 10L == 1L)) && (((\old(angkaBiner) / 1000000000000000000L) % 10L == 0L) || ((\old(angkaBiner) / 1000000000000000000L) % 10L == 1L));
//@ ensures \old(angkaBiner) >= 0 ==> \result == (((\old(angkaBiner) / 1L) % 10L) * 1L) + (((\old(angkaBiner) / 10L) % 10L) * 2L) + (((\old(angkaBiner) / 100L) % 10L) * 4L) + (((\old(angkaBiner) / 1000L) % 10L) * 8L) + (((\old(angkaBiner) / 10000L) % 10L) * 16L) + (((\old(angkaBiner) / 100000L) % 10L) * 32L) + (((\old(angkaBiner) / 1000000L) % 10L) * 64L) + (((\old(angkaBiner) / 10000000L) % 10L) * 128L) + (((\old(angkaBiner) / 100000000L) % 10L) * 256L) + (((\old(angkaBiner) / 1000000000L) % 10L) * 512L) + (((\old(angkaBiner) / 10000000000L) % 10L) * 1024L) + (((\old(angkaBiner) / 100000000000L) % 10L) * 2048L) + (((\old(angkaBiner) / 1000000000000L) % 10L) * 4096L) + (((\old(angkaBiner) / 10000000000000L) % 10L) * 8192L) + (((\old(angkaBiner) / 100000000000000L) % 10L) * 16384L) + (((\old(angkaBiner) / 1000000000000000L) % 10L) * 32768L) + (((\old(angkaBiner) / 10000000000000000L) % 10L) * 65536L) + (((\old(angkaBiner) / 100000000000000000L) % 10L) * 131072L) + (((\old(angkaBiner) / 1000000000000000000L) % 10L) * 262144L);
//@ ensures \old(angkaBiner) < 0L ==> \result < 0L;
```
```
//@ ensures \old(angkaBiner) >= 0 ==> (((\old(angkaBiner) / 1L) % 10L == 0L) || ((\old(angkaBiner) / 1L) % 10L == 1L)) && (((\old(angkaBiner) / 10L) % 10L == 0L) || ((\old(angkaBiner) / 10L) % 10L == 1L)) && (((\old(angkaBiner) / 100L) % 10L == 0L) || ((\old(angkaBiner) / 100L) % 10L == 1L)) && (((\old(angkaBiner) / 1000L) % 10L == 0L) || ((\old(angkaBiner) / 1000L) % 10L == 1L)) && (((\old(angkaBiner) / 10000L) % 10L == 0L) || ((\old(angkaBiner) / 10000L) % 10L == 1L)) && (((\old(angkaBiner) / 100000L) % 10L == 0L) || ((\old(angkaBiner) / 100000L) % 10L == 1L)) && (((\old(angkaBiner) / 1000000L) % 10L == 0L) || ((\old(angkaBiner) / 1000000L) % 10L == 1L)) && (((\old(angkaBiner) / 10000000L) % 10L == 0L) || ((\old(angkaBiner) / 10000000L) % 10L == 1L)) && (((\old(angkaBiner) / 100000000L) % 10L == 0L) || ((\old(angkaBiner) / 100000000L) % 10L == 1L)) && (((\old(angkaBiner) / 1000000000L) % 10L == 0L) || ((\old(angkaBiner) / 1000000000L) % 10L == 1L)) && (((\old(angkaBiner) / 10000000000L) % 10L == 0L) || ((\old(angkaBiner) / 10000000000L) % 10L == 1L)) && (((\old(angkaBiner) / 100000000000L) % 10L == 0L) || ((\old(angkaBiner) / 100000000000L) % 10L == 1L)) && (((\old(angkaBiner) / 1000000000000L) % 10L == 0L) || ((\old(angkaBiner) / 1000000000000L) % 10L == 1L)) && (((\old(angkaBiner) / 10000000000000L) % 10L == 0L) || ((\old(angkaBiner) / 10000000000000L) % 10L == 1L)) && (((\old(angkaBiner) / 100000000000000L) % 10L == 0L) || ((\old(angkaBiner) / 100000000000000L) % 10L == 1L)) && (((\old(angkaBiner) / 1000000000000000L) % 10L == 0L) || ((\old(angkaBiner) / 1000000000000000L) % 10L == 1L)) && (((\old(angkaBiner) / 10000000000000000L) % 10L == 0L) || ((\old(angkaBiner) / 10000000000000000L) % 10L == 1L)) && (((\old(angkaBiner) / 100000000000000000L) % 10L == 0L) || ((\old(angkaBiner) / 100000000000000000L) % 10L == 1L)) && (((\old(angkaBiner) / 1000000000000000000L) % 10L == 0L) || ((\old(angkaBiner) / 1000000000000000000L) % 10L == 1L));
//@ ensures \old(angkaBiner) >= 0 ==> \result == (((\old(angkaBiner) / 1L) % 10L) * 1L) + (((\old(angkaBiner) / 10L) % 10L) * 2L) + (((\old(angkaBiner) / 100L) % 10L) * 4L) + (((\old(angkaBiner) / 1000L) % 10L) * 8L) + (((\old(angkaBiner) / 10000L) % 10L) * 16L) + (((\old(angkaBiner) / 100000L) % 10L) * 32L) + (((\old(angkaBiner) / 1000000L) % 10L) * 64L) + (((\old(angkaBiner) / 10000000L) % 10L) * 128L) + (((\old(angkaBiner) / 100000000L) % 10L) * 256L) + (((\old(angkaBiner) / 1000000000L) % 10L) * 512L) + (((\old(angkaBiner) / 10000000000L) % 10L) * 1024L) + (((\old(angkaBiner) / 100000000000L) % 10L) * 2048L) + (((\old(angkaBiner) / 1000000000000L) % 10L) * 4096L) + (((\old(angkaBiner) / 10000000000000L) % 10L) * 8192L) + (((\old(angkaBiner) / 100000000000000L) % 10L) * 16384L) + (((\old(angkaBiner) / 1000000000000000L) % 10L) * 32768L) + (((\old(angkaBiner) / 10000000000000000L) % 10L) * 65536L) + (((\old(angkaBiner) / 100000000000000000L) % 10L) * 131072L) + (((\old(angkaBiner) / 1000000000000000000L) % 10L) * 262144L);
```
[1]
===== 1 =====
```
     long valueDesimal = 0;
     long pangkat = 0;
     
-    while (angkaBiner != 0) {
+    while (angkaBiner > 0) {
       long digit = angkaBiner % 10;
       if (digit > 1) {
         throw new IllegalArgumentException("angka biner tidak benar: " + digit);
```
```
  /**
   * fungsi mengubah angka biner ke angka desimal
   * 
   * @param angkaBiner angka biner yang akan dikonversikan
   * @return hasil dari konversi angka biner ke angka desimal
   * @throws IllegalArgumentException ini terjadi jika angka biner tidak terdapat angka 0 atau 1
   */

   public static long binerKeDesimal(long angkaBiner) {
    long valueDesimal = 0;
    long pangkat = 0;
    
    while (angkaBiner > 0) {
      long digit = angkaBiner % 10;
      if (digit > 1) {
        throw new IllegalArgumentException("angka biner tidak benar: " + digit);
      }
      valueDesimal += (long) (digit * Math.pow(BASE_BINER, pangkat++));
      angkaBiner /= 10;
    }
    return valueDesimal;
   }
```
