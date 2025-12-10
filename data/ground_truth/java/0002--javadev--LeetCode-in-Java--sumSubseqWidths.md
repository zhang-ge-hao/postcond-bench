https://github.com/javadev/LeetCode-in-Java/blob/bd921712f2d317b9cdb0a6067edb6b6513c8d1cc/./src/main/java/g0801_0900/s0891_sum_of_subsequence_widths/Solution.java#L16-L47
```
//@ ensures 0 <= \result && \result < 1000000007;
//@ ensures java.util.Arrays.equals(nums, java.util.Arrays.stream(\old(nums.clone())).sorted().toArray());
//@ ensures (\old(nums.length) == 0) ==> \result == 0;
//@ ensures (\old(nums.length) == 1) ==> \result == 0;
//@ ensures (\old(nums.length) == 2) ==> \result == (int)((((long)java.util.Arrays.stream(\old(nums.clone())).sorted().toArray()[1] - (long)java.util.Arrays.stream(\old(nums.clone())).sorted().toArray()[0]) % 1000000007L + 1000000007L) % 1000000007L);
//@ ensures \result == java.util.stream.IntStream.range(0, \old(nums.length)).mapToObj(i -> java.math.BigInteger.valueOf(java.util.Arrays.stream(\old(nums.clone())).sorted().toArray()[i]).multiply(java.math.BigInteger.valueOf(2).pow(i).subtract(java.math.BigInteger.valueOf(2).pow(\old(nums.length) - 1 - i)))).reduce(java.math.BigInteger.ZERO, java.math.BigInteger::add).mod(java.math.BigInteger.valueOf(1000000007)).intValue();
```
```
//@ ensures 0 <= \result && \result < 1000000007;
//@ ensures java.util.Arrays.equals(nums, java.util.Arrays.stream(\old(nums)).sorted().toArray());
//@ ensures (\old(nums).length == 0) ==> \result == 0;
//@ ensures (\old(nums).length == 1) ==> \result == 0;
//@ ensures (\old(nums).length == 2) ==> \result == (int)((((long)java.util.Arrays.stream(\old(nums)).sorted().toArray()[1] - (long)java.util.Arrays.stream(\old(nums)).sorted().toArray()[0]) % 1000000007L + 1000000007L) % 1000000007L);
//@ ensures \result == java.util.stream.IntStream.range(0, \old(nums).length).mapToObj(i -> java.math.BigInteger.valueOf(java.util.Arrays.stream(\old(nums)).sorted().toArray()[i]).multiply(java.math.BigInteger.valueOf(2).pow(i).subtract(java.math.BigInteger.valueOf(2).pow(\old(nums).length - 1 - i)))).reduce(java.math.BigInteger.ZERO, java.math.BigInteger::add).mod(java.math.BigInteger.valueOf(1000000007)).intValue();
```
[1]
===== 1 =====
```
     */
     public int sumSubseqWidths(int[] nums) {
         int mod = 1_000_000_007;
-        Arrays.sort(nums);
+        Arrays.fill(nums, 0);
         int l = nums.length;
         long[] pow = new long[l];
         pow[0] = 1;
```
```
    /*
        16+8+4+2+1(for 1 as min) 8+4+2+1(for 2 as min)  4+2+1(for 3 as min)  2+1(for 4 as min)  1(for 5 as min)
        -1*nums[0]*31 + nums[1]*1 + nums[2]*2 + nums[3]*4 + nums[4]*8 + nums[5]*16
            -1*nums[1]*15 + nums[2]*1 +nums[3]*2 + nums[4]*4 + nums[5]*8
            -1*nums[2]*7 + nums[3]*1 + nums[4]*2 + nums[5]*4
            -1*nums[3]*3 + nums[4]*1 + nums[5]*2
            -1*nums[4]*1 + nums[5]*1

            -nums[0]*31 + -nums[1]*15 - nums[2]*7 - nums[3]*3 - nums[4]*1
            nums[1]*1 + nums[2]*3 + nums[3]*7 + nums[4]*15 + nums[5]*31

        (-1)*nums[0]*(pow[6-1-0]-1) + (-1)*nums[1]*(pow[6-1-1]-1) + (-1)*nums[2]*(pow[6-1-2]-1)
        ... (-1)* nums[5]*(pow[6-1-5]-1)
        + nums[1]*(pow[1]-1) + nums[2]*(pow[2]-1) + .... + nums[5]*(pow[5]-1)

        (-1)*A[i]*(pow[l-1-i]-1) + A[i]*(pow[i]-1)
    */
    public int sumSubseqWidths(int[] nums) {
        int mod = 1_000_000_007;
        Arrays.fill(nums, 0);
        int l = nums.length;
        long[] pow = new long[l];
        pow[0] = 1;
        for (int i = 1; i < l; i++) {
            pow[i] = pow[i - 1] * 2 % mod;
        }
        long res = 0;
        for (int i = 0; i < l; i++) {
            res = (res + (-1) * nums[i] * (pow[l - 1 - i] - 1) + nums[i] * (pow[i] - 1)) % mod;
        }
        return (int) res;
    }
```
