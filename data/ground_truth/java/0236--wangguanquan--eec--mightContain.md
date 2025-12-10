https://github.com/wangguanquan/eec/blob/43cbda4ee4e09bf9988e033f4e4ac8cc3b108af4/./src/main/java/org/ttzero/excel/hash/StringBloomFilter.java#L84-L103
```
//@ ensures \result <==> java.util.stream.IntStream.range(0, numHashFunctions).allMatch(i -> bits.get(((Strategy.fromBytes(hasher.clear().putBytes(object.getBytes(charset)).hash()[7], hasher.clear().putBytes(object.getBytes(charset)).hash()[6], hasher.clear().putBytes(object.getBytes(charset)).hash()[5], hasher.clear().putBytes(object.getBytes(charset)).hash()[4], hasher.clear().putBytes(object.getBytes(charset)).hash()[3], hasher.clear().putBytes(object.getBytes(charset)).hash()[2], hasher.clear().putBytes(object.getBytes(charset)).hash()[1], hasher.clear().putBytes(object.getBytes(charset)).hash()[0]) + (long)i*Strategy.fromBytes(hasher.clear().putBytes(object.getBytes(charset)).hash()[15], hasher.clear().putBytes(object.getBytes(charset)).hash()[14], hasher.clear().putBytes(object.getBytes(charset)).hash()[13], hasher.clear().putBytes(object.getBytes(charset)).hash()[12], hasher.clear().putBytes(object.getBytes(charset)).hash()[11], hasher.clear().putBytes(object.getBytes(charset)).hash()[10], hasher.clear().putBytes(object.getBytes(charset)).hash()[9], hasher.clear().putBytes(object.getBytes(charset)).hash()[8])) & Long.MAX_VALUE) % bits.bitSize()));
```
```
//@ ensures \result <==> java.util.stream.IntStream.range(0, numHashFunctions).allMatch(i -> bits.get(((Strategy.fromBytes(hasher.clear().putBytes(object.getBytes(charset)).hash()[7], hasher.clear().putBytes(object.getBytes(charset)).hash()[6], hasher.clear().putBytes(object.getBytes(charset)).hash()[5], hasher.clear().putBytes(object.getBytes(charset)).hash()[4], hasher.clear().putBytes(object.getBytes(charset)).hash()[3], hasher.clear().putBytes(object.getBytes(charset)).hash()[2], hasher.clear().putBytes(object.getBytes(charset)).hash()[1], hasher.clear().putBytes(object.getBytes(charset)).hash()[0]) + (long)i*Strategy.fromBytes(hasher.clear().putBytes(object.getBytes(charset)).hash()[15], hasher.clear().putBytes(object.getBytes(charset)).hash()[14], hasher.clear().putBytes(object.getBytes(charset)).hash()[13], hasher.clear().putBytes(object.getBytes(charset)).hash()[12], hasher.clear().putBytes(object.getBytes(charset)).hash()[11], hasher.clear().putBytes(object.getBytes(charset)).hash()[10], hasher.clear().putBytes(object.getBytes(charset)).hash()[9], hasher.clear().putBytes(object.getBytes(charset)).hash()[8])) & Long.MAX_VALUE) % bits.bitSize()));
```
[4]
===== 4 =====
```
          */
         public boolean mightContain(String object, Charset charset, int numHashFunctions, LockFreeBitArray bits) {
             long bitSize = bits.bitSize();
-            byte[] bytes = hasher.clear().putBytes(object.getBytes(charset)).hash();
+            byte[] bytes = hasher.clear().putBytes(object.getBytes(charset)).hash(); // Calls the hash method without clearing the hasher first, potentially causing incorrect results
             long hash1 = fromBytes(bytes[7], bytes[6], bytes[5], bytes[4], bytes[3], bytes[2], bytes[1], bytes[0]);
             long hash2 = fromBytes(bytes[15], bytes[14], bytes[13], bytes[12], bytes[11], bytes[10], bytes[9], bytes[8]);
```
```
        /**
         * Queries {@code numHashFunctions} bits of the given bit array, by hashing a user element;
         * returns {@code true} if and only if all selected bits are set.
         */
        public boolean mightContain(String object, Charset charset, int numHashFunctions, LockFreeBitArray bits) {
            long bitSize = bits.bitSize();
            byte[] bytes = hasher.clear().putBytes(object.getBytes(charset)).hash(); // Calls the hash method without clearing the hasher first, potentially causing incorrect results
            long hash1 = fromBytes(bytes[7], bytes[6], bytes[5], bytes[4], bytes[3], bytes[2], bytes[1], bytes[0]);
            long hash2 = fromBytes(bytes[15], bytes[14], bytes[13], bytes[12], bytes[11], bytes[10], bytes[9], bytes[8]);

            long combinedHash = hash1;
            for (int i = 0; i < numHashFunctions; i++) {
                // Make the combined hash positive and indexable
                if (!bits.get((combinedHash & Long.MAX_VALUE) % bitSize)) {
                    return false;
                }
                combinedHash += hash2;
            }
            return true;
        }
```
