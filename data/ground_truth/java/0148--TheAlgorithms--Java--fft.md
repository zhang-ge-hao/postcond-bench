https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/maths/FFT.java#L178-L220
```
//@ ensures \result != null;
//@ ensures \result.size() >= \old(x.size()) && ((\result.size() & (\result.size() - 1)) == 0);
//@ ensures (!inverse) ==> (\result.get(0).getReal() == \old(x).stream().mapToDouble(c -> c.getReal()).sum());
//@ ensures (!inverse) ==> (\result.get(0).getImaginary() == \old(x).stream().mapToDouble(c -> c.getImaginary()).sum());
//@ ensures (inverse) ==> (\result.get(0).getReal() == \old(x).stream().mapToDouble(c -> c.getReal()).sum() / \result.size());
//@ ensures (inverse) ==> (\result.get(0).getImaginary() == \old(x).stream().mapToDouble(c -> c.getImaginary()).sum() / \result.size());
//@ ensures (!inverse && \old(x.size()) == 4) ==> (\result.size() == 4);
//@ ensures (!inverse && \old(x.size()) == 4) ==> (\result.get(2).getReal() == \old(x.get(0).getReal() - x.get(1).getReal() + x.get(2).getReal() - x.get(3).getReal()));
//@ ensures (!inverse && \old(x.size()) == 4) ==> (\result.get(2).getImaginary() == \old(x.get(0).getImaginary() - x.get(1).getImaginary() + x.get(2).getImaginary() - x.get(3).getImaginary()));
```
```
//@ ensures \result != null;
//@ ensures \result.size() >= \old(x.size()) && ((\result.size() & (\result.size() - 1)) == 0);
//@ ensures (!inverse) ==> (\result.get(0).getReal() == \old(x).stream().mapToDouble(c -> c.getReal()).sum());
//@ ensures (!inverse) ==> (\result.get(0).getImaginary() == \old(x).stream().mapToDouble(c -> c.getImaginary()).sum());
//@ ensures (inverse) ==> (\result.get(0).getReal() == \old(x).stream().mapToDouble(c -> c.getReal()).sum() / \result.size());
//@ ensures (inverse) ==> (\result.get(0).getImaginary() == \old(x).stream().mapToDouble(c -> c.getImaginary()).sum() / \result.size());
```
[3, 4, 17, 21, 29, 34]
===== 3 =====
```
         /* Pad the signal with zeros if necessary */
         paddingPowerOfTwo(x);
         int n = x.size();
-        int log2n = findLog2(n);
+        int log2n = findLog2(n / 2); // Incorrectly calculates log2 of n / 2
         x = fftBitReversal(n, log2n, x);
         int direction = inverse ? -1 : 1;
```
```
    /**
     * Iterative In-Place Radix-2 Cooley-Tukey Fast Fourier Transform Algorithm
     * with Bit-Reversal. The size of the input signal must be a power of 2. If
     * it isn't then it is padded with zeros and the output FFT will be bigger
     * than the input signal.
     *
     * <p>
     * More info:
     * https://www.algorithm-archive.org/contents/cooley_tukey/cooley_tukey.html
     * https://www.geeksforgeeks.org/iterative-fast-fourier-transformation-polynomial-multiplication/
     * https://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm
     * https://cp-algorithms.com/algebra/fft.html
     *  @param x The discrete signal which is then converted to the FFT or the
     * IFFT of signal x.
     * @param inverse True if you want to find the inverse FFT.
     * @return
     */
    public static ArrayList<Complex> fft(ArrayList<Complex> x, boolean inverse) {
        /* Pad the signal with zeros if necessary */
        paddingPowerOfTwo(x);
        int n = x.size();
        int log2n = findLog2(n / 2); // Incorrectly calculates log2 of n / 2
        x = fftBitReversal(n, log2n, x);
        int direction = inverse ? -1 : 1;

        /* Main loop of the algorithm */
        for (int len = 2; len <= n; len *= 2) {
            double angle = -2 * Math.PI / len * direction;
            Complex wlen = new Complex(Math.cos(angle), Math.sin(angle));
            for (int i = 0; i < n; i += len) {
                Complex w = new Complex(1, 0);
                for (int j = 0; j < len / 2; j++) {
                    Complex u = x.get(i + j);
                    Complex v = w.multiply(x.get(i + j + len / 2));
                    x.set(i + j, u.add(v));
                    x.set(i + j + len / 2, u.subtract(v));
                    w = w.multiply(wlen);
                }
            }
        }
        x = inverseFFT(n, inverse, x);
        return x;
    }
```
===== 4 =====
```
         /* Pad the signal with zeros if necessary */
         paddingPowerOfTwo(x);
         int n = x.size();
-        int log2n = findLog2(n);
+        int log2n = findLog2(n) - 1; // Incorrectly decrements log2(n) by 1
         x = fftBitReversal(n, log2n, x);
         int direction = inverse ? -1 : 1;
```
```
    /**
     * Iterative In-Place Radix-2 Cooley-Tukey Fast Fourier Transform Algorithm
     * with Bit-Reversal. The size of the input signal must be a power of 2. If
     * it isn't then it is padded with zeros and the output FFT will be bigger
     * than the input signal.
     *
     * <p>
     * More info:
     * https://www.algorithm-archive.org/contents/cooley_tukey/cooley_tukey.html
     * https://www.geeksforgeeks.org/iterative-fast-fourier-transformation-polynomial-multiplication/
     * https://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm
     * https://cp-algorithms.com/algebra/fft.html
     *  @param x The discrete signal which is then converted to the FFT or the
     * IFFT of signal x.
     * @param inverse True if you want to find the inverse FFT.
     * @return
     */
    public static ArrayList<Complex> fft(ArrayList<Complex> x, boolean inverse) {
        /* Pad the signal with zeros if necessary */
        paddingPowerOfTwo(x);
        int n = x.size();
        int log2n = findLog2(n) - 1; // Incorrectly decrements log2(n) by 1
        x = fftBitReversal(n, log2n, x);
        int direction = inverse ? -1 : 1;

        /* Main loop of the algorithm */
        for (int len = 2; len <= n; len *= 2) {
            double angle = -2 * Math.PI / len * direction;
            Complex wlen = new Complex(Math.cos(angle), Math.sin(angle));
            for (int i = 0; i < n; i += len) {
                Complex w = new Complex(1, 0);
                for (int j = 0; j < len / 2; j++) {
                    Complex u = x.get(i + j);
                    Complex v = w.multiply(x.get(i + j + len / 2));
                    x.set(i + j, u.add(v));
                    x.set(i + j + len / 2, u.subtract(v));
                    w = w.multiply(wlen);
                }
            }
        }
        x = inverseFFT(n, inverse, x);
        return x;
    }
```
===== 17 =====
```
             for (int i = 0; i < n; i += len) {
                 Complex w = new Complex(1, 0);
                 for (int j = 0; j < len / 2; j++) {
-                    Complex u = x.get(i + j);
+                    Complex u = x.get(i + j + len / 2); // Incorrect index, accessing the second half
                     Complex v = w.multiply(x.get(i + j + len / 2));
                     x.set(i + j, u.add(v));
                     x.set(i + j + len / 2, u.subtract(v));
```
```
    /**
     * Iterative In-Place Radix-2 Cooley-Tukey Fast Fourier Transform Algorithm
     * with Bit-Reversal. The size of the input signal must be a power of 2. If
     * it isn't then it is padded with zeros and the output FFT will be bigger
     * than the input signal.
     *
     * <p>
     * More info:
     * https://www.algorithm-archive.org/contents/cooley_tukey/cooley_tukey.html
     * https://www.geeksforgeeks.org/iterative-fast-fourier-transformation-polynomial-multiplication/
     * https://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm
     * https://cp-algorithms.com/algebra/fft.html
     *  @param x The discrete signal which is then converted to the FFT or the
     * IFFT of signal x.
     * @param inverse True if you want to find the inverse FFT.
     * @return
     */
    public static ArrayList<Complex> fft(ArrayList<Complex> x, boolean inverse) {
        /* Pad the signal with zeros if necessary */
        paddingPowerOfTwo(x);
        int n = x.size();
        int log2n = findLog2(n);
        x = fftBitReversal(n, log2n, x);
        int direction = inverse ? -1 : 1;

        /* Main loop of the algorithm */
        for (int len = 2; len <= n; len *= 2) {
            double angle = -2 * Math.PI / len * direction;
            Complex wlen = new Complex(Math.cos(angle), Math.sin(angle));
            for (int i = 0; i < n; i += len) {
                Complex w = new Complex(1, 0);
                for (int j = 0; j < len / 2; j++) {
                    Complex u = x.get(i + j + len / 2); // Incorrect index, accessing the second half
                    Complex v = w.multiply(x.get(i + j + len / 2));
                    x.set(i + j, u.add(v));
                    x.set(i + j + len / 2, u.subtract(v));
                    w = w.multiply(wlen);
                }
            }
        }
        x = inverseFFT(n, inverse, x);
        return x;
    }
```
===== 21 =====
```
                 Complex w = new Complex(1, 0);
                 for (int j = 0; j < len / 2; j++) {
                     Complex u = x.get(i + j);
-                    Complex v = w.multiply(x.get(i + j + len / 2));
+                    Complex v = w.multiply(x.get(i + j)); // Incorrect index, should be len/2
                     x.set(i + j, u.add(v));
                     x.set(i + j + len / 2, u.subtract(v));
                     w = w.multiply(wlen);
```
```
    /**
     * Iterative In-Place Radix-2 Cooley-Tukey Fast Fourier Transform Algorithm
     * with Bit-Reversal. The size of the input signal must be a power of 2. If
     * it isn't then it is padded with zeros and the output FFT will be bigger
     * than the input signal.
     *
     * <p>
     * More info:
     * https://www.algorithm-archive.org/contents/cooley_tukey/cooley_tukey.html
     * https://www.geeksforgeeks.org/iterative-fast-fourier-transformation-polynomial-multiplication/
     * https://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm
     * https://cp-algorithms.com/algebra/fft.html
     *  @param x The discrete signal which is then converted to the FFT or the
     * IFFT of signal x.
     * @param inverse True if you want to find the inverse FFT.
     * @return
     */
    public static ArrayList<Complex> fft(ArrayList<Complex> x, boolean inverse) {
        /* Pad the signal with zeros if necessary */
        paddingPowerOfTwo(x);
        int n = x.size();
        int log2n = findLog2(n);
        x = fftBitReversal(n, log2n, x);
        int direction = inverse ? -1 : 1;

        /* Main loop of the algorithm */
        for (int len = 2; len <= n; len *= 2) {
            double angle = -2 * Math.PI / len * direction;
            Complex wlen = new Complex(Math.cos(angle), Math.sin(angle));
            for (int i = 0; i < n; i += len) {
                Complex w = new Complex(1, 0);
                for (int j = 0; j < len / 2; j++) {
                    Complex u = x.get(i + j);
                    Complex v = w.multiply(x.get(i + j)); // Incorrect index, should be len/2
                    x.set(i + j, u.add(v));
                    x.set(i + j + len / 2, u.subtract(v));
                    w = w.multiply(wlen);
                }
            }
        }
        x = inverseFFT(n, inverse, x);
        return x;
    }
```
===== 29 =====
```
                     Complex u = x.get(i + j);
                     Complex v = w.multiply(x.get(i + j + len / 2));
                     x.set(i + j, u.add(v));
-                    x.set(i + j + len / 2, u.subtract(v));
+                    x.set(i + j + len / 2, new Complex(0, 0)); // Sets the value to a new complex number (0,0), losing the intended calculation
                     w = w.multiply(wlen);
                 }
             }
```
```
    /**
     * Iterative In-Place Radix-2 Cooley-Tukey Fast Fourier Transform Algorithm
     * with Bit-Reversal. The size of the input signal must be a power of 2. If
     * it isn't then it is padded with zeros and the output FFT will be bigger
     * than the input signal.
     *
     * <p>
     * More info:
     * https://www.algorithm-archive.org/contents/cooley_tukey/cooley_tukey.html
     * https://www.geeksforgeeks.org/iterative-fast-fourier-transformation-polynomial-multiplication/
     * https://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm
     * https://cp-algorithms.com/algebra/fft.html
     *  @param x The discrete signal which is then converted to the FFT or the
     * IFFT of signal x.
     * @param inverse True if you want to find the inverse FFT.
     * @return
     */
    public static ArrayList<Complex> fft(ArrayList<Complex> x, boolean inverse) {
        /* Pad the signal with zeros if necessary */
        paddingPowerOfTwo(x);
        int n = x.size();
        int log2n = findLog2(n);
        x = fftBitReversal(n, log2n, x);
        int direction = inverse ? -1 : 1;

        /* Main loop of the algorithm */
        for (int len = 2; len <= n; len *= 2) {
            double angle = -2 * Math.PI / len * direction;
            Complex wlen = new Complex(Math.cos(angle), Math.sin(angle));
            for (int i = 0; i < n; i += len) {
                Complex w = new Complex(1, 0);
                for (int j = 0; j < len / 2; j++) {
                    Complex u = x.get(i + j);
                    Complex v = w.multiply(x.get(i + j + len / 2));
                    x.set(i + j, u.add(v));
                    x.set(i + j + len / 2, new Complex(0, 0)); // Sets the value to a new complex number (0,0), losing the intended calculation
                    w = w.multiply(wlen);
                }
            }
        }
        x = inverseFFT(n, inverse, x);
        return x;
    }
```
===== 34 =====
```
                 }
             }
         }
-        x = inverseFFT(n, inverse, x);
+        x = inverseFFT(n, !inverse, x);
         return x;
     }
```
```
    /**
     * Iterative In-Place Radix-2 Cooley-Tukey Fast Fourier Transform Algorithm
     * with Bit-Reversal. The size of the input signal must be a power of 2. If
     * it isn't then it is padded with zeros and the output FFT will be bigger
     * than the input signal.
     *
     * <p>
     * More info:
     * https://www.algorithm-archive.org/contents/cooley_tukey/cooley_tukey.html
     * https://www.geeksforgeeks.org/iterative-fast-fourier-transformation-polynomial-multiplication/
     * https://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm
     * https://cp-algorithms.com/algebra/fft.html
     *  @param x The discrete signal which is then converted to the FFT or the
     * IFFT of signal x.
     * @param inverse True if you want to find the inverse FFT.
     * @return
     */
    public static ArrayList<Complex> fft(ArrayList<Complex> x, boolean inverse) {
        /* Pad the signal with zeros if necessary */
        paddingPowerOfTwo(x);
        int n = x.size();
        int log2n = findLog2(n);
        x = fftBitReversal(n, log2n, x);
        int direction = inverse ? -1 : 1;

        /* Main loop of the algorithm */
        for (int len = 2; len <= n; len *= 2) {
            double angle = -2 * Math.PI / len * direction;
            Complex wlen = new Complex(Math.cos(angle), Math.sin(angle));
            for (int i = 0; i < n; i += len) {
                Complex w = new Complex(1, 0);
                for (int j = 0; j < len / 2; j++) {
                    Complex u = x.get(i + j);
                    Complex v = w.multiply(x.get(i + j + len / 2));
                    x.set(i + j, u.add(v));
                    x.set(i + j + len / 2, u.subtract(v));
                    w = w.multiply(wlen);
                }
            }
        }
        x = inverseFFT(n, !inverse, x);
        return x;
    }
```
