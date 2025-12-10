https://github.com/wangguanquan/eec/blob/43cbda4ee4e09bf9988e033f4e4ac8cc3b108af4/./src/main/java/org/ttzero/excel/util/CSVUtil.java#L1147-L1206
```
//@ ensures this.offset >= 0 && this.offset <= this.cb.length;
//@ ensures this.i == \old(this.i) + 1;
//@ ensures (\old(this.offset) + 1 + size <= this.cb.length && java.util.stream.IntStream.range(offset, offset + size).noneMatch(k -> chars[k] == QUOTE || chars[k] == LF || chars[k] == HT || chars[k] == separator || chars[k] == COMMA)) ==> new String(this.cb, this.offset - size, size).equals(new String(chars, offset, size));
//@ ensures (\old(this.offset) + 1 + (size + 2) <= this.cb.length && java.util.stream.IntStream.range(offset, offset + size).noneMatch(k -> chars[k] == QUOTE) && java.util.stream.IntStream.range(offset, offset + size).anyMatch(k -> chars[k] == LF || chars[k] == HT || chars[k] == separator || chars[k] == COMMA)) ==> new String(this.cb, this.offset - (size + 2), size + 2).equals("\"" + new String(chars, offset, size) + "\"");
//@ ensures (\old(this.offset) + 1 + ("\"" + new String(chars, offset, size).replace("\"", "\"\"") + "\"").length() <= this.cb.length && java.util.stream.IntStream.range(offset, offset + size).anyMatch(k -> chars[k] == QUOTE)) ==> new String(this.cb, this.offset - ("\"" + new String(chars, offset, size).replace("\"", "\"\"") + "\"").length(), ("\"" + new String(chars, offset, size).replace("\"", "\"\"") + "\"").length()).equals("\"" + new String(chars, offset, size).replace("\"", "\"\"") + "\"");
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38]
===== 0 =====
```
          * @throws IOException If an I/O error occurs
          */
         public void write(char[] chars, int offset, int size) throws IOException {
-            test();
+            
             int i = 0;
             int last = offset;
             boolean quoted = false, shouldBeQuoted = false;
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 1 =====
```
          * @throws IOException If an I/O error occurs
          */
         public void write(char[] chars, int offset, int size) throws IOException {
-            test();
+            if (column > 0 && i >= column) { i++; }
             int i = 0;
             int last = offset;
             boolean quoted = false, shouldBeQuoted = false;
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            if (column > 0 && i >= column) { i++; }
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 2 =====
```
          * @throws IOException If an I/O error occurs
          */
         public void write(char[] chars, int offset, int size) throws IOException {
-            test();
+            if (i == 0) { column++; }
             int i = 0;
             int last = offset;
             boolean quoted = false, shouldBeQuoted = false;
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            if (i == 0) { column++; }
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 3 =====
```
          * @throws IOException If an I/O error occurs
          */
         public void write(char[] chars, int offset, int size) throws IOException {
-            test();
+            if (i == 0) { i++; }
             int i = 0;
             int last = offset;
             boolean quoted = false, shouldBeQuoted = false;
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            if (i == 0) { i++; }
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 4 =====
```
          * @throws IOException If an I/O error occurs
          */
         public void write(char[] chars, int offset, int size) throws IOException {
-            test();
+            if (i == 0) { return; }
             int i = 0;
             int last = offset;
             boolean quoted = false, shouldBeQuoted = false;
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            if (i == 0) { return; }
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 5 =====
```
          * @throws IOException If an I/O error occurs
          */
         public void write(char[] chars, int offset, int size) throws IOException {
-            test();
+            if (i > 0) { i--; }
             int i = 0;
             int last = offset;
             boolean quoted = false, shouldBeQuoted = false;
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            if (i > 0) { i--; }
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 6 =====
```
             int last = offset;
             boolean quoted = false, shouldBeQuoted = false;
 
-            for ( ; i < size; ) {
+            for ( ; i < size - 1; ) { // This will miss the last character in the array
                 char c = chars[i++];
 
                 // A (double) quote character in a field must be represented
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size - 1; ) { // This will miss the last character in the array
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 7 =====
```
             int last = offset;
             boolean quoted = false, shouldBeQuoted = false;
 
-            for ( ; i < size; ) {
+            for ( ; i < size; i += 2) { // This will skip every other character in the array
                 char c = chars[i++];
 
                 // A (double) quote character in a field must be represented
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; i += 2) { // This will skip every other character in the array
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 8 =====
```
             int last = offset;
             boolean quoted = false, shouldBeQuoted = false;
 
-            for ( ; i < size; ) {
+            for ( ; i < size; i++) { // This will skip the last character in the array
                 char c = chars[i++];
 
                 // A (double) quote character in a field must be represented
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; i++) { // This will skip the last character in the array
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 9 =====
```
             int last = offset;
             boolean quoted = false, shouldBeQuoted = false;
 
-            for ( ; i < size; ) {
+            for ( ; i >= size; ) {
                 char c = chars[i++];
 
                 // A (double) quote character in a field must be represented
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i >= size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 10 =====
```
 
                 // A (double) quote character in a field must be represented
                 // by two (double) quote characters.
-                if (c == QUOTE) {
+                if (c != QUOTE) {
                     quoted = true;
                     if (last == offset) {
                         checkBound(1);
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c != QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 11 =====
```
 
                 // A (double) quote character in a field must be represented
                 // by two (double) quote characters.
-                if (c == QUOTE) {
+                if (c == COMMA) {
                     quoted = true;
                     if (last == offset) {
                         checkBound(1);
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == COMMA) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 12 =====
```
 
                 // A (double) quote character in a field must be represented
                 // by two (double) quote characters.
-                if (c == QUOTE) {
+                if (c == HT) {
                     quoted = true;
                     if (last == offset) {
                         checkBound(1);
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == HT) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 13 =====
```
 
                 // A (double) quote character in a field must be represented
                 // by two (double) quote characters.
-                if (c == QUOTE) {
+                if (c == LF || c == CR) {
                     quoted = true;
                     if (last == offset) {
                         checkBound(1);
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == LF || c == CR) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 14 =====
```
                 // by two (double) quote characters.
                 if (c == QUOTE) {
                     quoted = true;
-                    if (last == offset) {
+                    if (last != offset) {
                         checkBound(1);
                         cb[this.offset++] = QUOTE;
                     }
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last != offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 15 =====
```
                 // by two (double) quote characters.
                 if (c == QUOTE) {
                     quoted = true;
-                    if (last == offset) {
+                    if (last < offset) {
                         checkBound(1);
                         cb[this.offset++] = QUOTE;
                     }
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last < offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 16 =====
```
                 // by two (double) quote characters.
                 if (c == QUOTE) {
                     quoted = true;
-                    if (last == offset) {
+                    if (last == offset + 1) {
                         checkBound(1);
                         cb[this.offset++] = QUOTE;
                     }
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset + 1) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 17 =====
```
                 // by two (double) quote characters.
                 if (c == QUOTE) {
                     quoted = true;
-                    if (last == offset) {
+                    if (last > offset) {
                         checkBound(1);
                         cb[this.offset++] = QUOTE;
                     }
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last > offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 18 =====
```
                         cb[this.offset++] = QUOTE;
                     }
                     checkBound(i - last + 1);
-                    System.arraycopy(chars, last, cb, this.offset, i - last);
+                    
                     this.offset += (i - last);
                     cb[this.offset++] = QUOTE;
                     last = i;
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 19 =====
```
                         cb[this.offset++] = QUOTE;
                     }
                     checkBound(i - last + 1);
-                    System.arraycopy(chars, last, cb, this.offset, i - last);
+                    System.arraycopy(chars, last, cb, this.offset, 0); // Copying zero characters, resulting in no data being transferred
                     this.offset += (i - last);
                     cb[this.offset++] = QUOTE;
                     last = i;
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, 0); // Copying zero characters, resulting in no data being transferred
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 20 =====
```
                         cb[this.offset++] = QUOTE;
                     }
                     checkBound(i - last + 1);
-                    System.arraycopy(chars, last, cb, this.offset, i - last);
+                    System.arraycopy(chars, last, cb, this.offset, i - last - 1); // Off-by-one error, missing the last character
                     this.offset += (i - last);
                     cb[this.offset++] = QUOTE;
                     last = i;
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last - 1); // Off-by-one error, missing the last character
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 21 =====
```
                         cb[this.offset++] = QUOTE;
                     }
                     checkBound(i - last + 1);
-                    System.arraycopy(chars, last, cb, this.offset, i - last);
+                    System.arraycopy(chars, last, cb, this.offset, i - last); this.offset++; // Incrementing offset incorrectly, causing data misalignment
                     this.offset += (i - last);
                     cb[this.offset++] = QUOTE;
                     last = i;
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last); this.offset++; // Incrementing offset incorrectly, causing data misalignment
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 22 =====
```
 
             }
 
-            if (quoted) {
+            if (!quoted) {
                 checkBound(i - last + 1);
                 System.arraycopy(chars, last, cb, this.offset, i - last);
                 this.offset += (i - last);
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (!quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 23 =====
```
 
             }
 
-            if (quoted) {
+            if (i == 0) {
                 checkBound(i - last + 1);
                 System.arraycopy(chars, last, cb, this.offset, i - last);
                 this.offset += (i - last);
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (i == 0) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 24 =====
```
 
             }
 
-            if (quoted) {
+            if (shouldBeQuoted) {
                 checkBound(i - last + 1);
                 System.arraycopy(chars, last, cb, this.offset, i - last);
                 this.offset += (i - last);
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (shouldBeQuoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 25 =====
```
 
             if (quoted) {
                 checkBound(i - last + 1);
-                System.arraycopy(chars, last, cb, this.offset, i - last);
+                
                 this.offset += (i - last);
                 cb[this.offset++] = QUOTE;
             }
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 26 =====
```
 
             if (quoted) {
                 checkBound(i - last + 1);
-                System.arraycopy(chars, last, cb, this.offset, i - last);
+                System.arraycopy(chars, last, cb, this.offset, 0); // Copying zero characters, resulting in no data being transferred
                 this.offset += (i - last);
                 cb[this.offset++] = QUOTE;
             }
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, 0); // Copying zero characters, resulting in no data being transferred
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 27 =====
```
 
             if (quoted) {
                 checkBound(i - last + 1);
-                System.arraycopy(chars, last, cb, this.offset, i - last);
+                System.arraycopy(chars, last, cb, this.offset, i - last - 1); // Off-by-one error, missing the last character
                 this.offset += (i - last);
                 cb[this.offset++] = QUOTE;
             }
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last - 1); // Off-by-one error, missing the last character
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 28 =====
```
 
             if (quoted) {
                 checkBound(i - last + 1);
-                System.arraycopy(chars, last, cb, this.offset, i - last);
+                System.arraycopy(chars, last, cb, this.offset, i - last); this.offset++; // Incrementing offset incorrectly, causing data misalignment
                 this.offset += (i - last);
                 cb[this.offset++] = QUOTE;
             }
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last); this.offset++; // Incrementing offset incorrectly, causing data misalignment
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 29 =====
```
             if (quoted) {
                 checkBound(i - last + 1);
                 System.arraycopy(chars, last, cb, this.offset, i - last);
-                this.offset += (i - last);
+                this.offset += (i + last);
                 cb[this.offset++] = QUOTE;
             }
             else if (shouldBeQuoted) {
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i + last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 30 =====
```
                 this.offset += (i - last);
                 cb[this.offset++] = QUOTE;
             }
-            else if (shouldBeQuoted) {
+            else if (i % 2 == 0) {
                 checkBound(size + 2);
                 cb[this.offset++] = QUOTE;
                 System.arraycopy(chars, offset, cb, this.offset, size);
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (i % 2 == 0) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 31 =====
```
                 this.offset += (i - last);
                 cb[this.offset++] = QUOTE;
             }
-            else if (shouldBeQuoted) {
+            else if (quoted) {
                 checkBound(size + 2);
                 cb[this.offset++] = QUOTE;
                 System.arraycopy(chars, offset, cb, this.offset, size);
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (quoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 32 =====
```
             else if (shouldBeQuoted) {
                 checkBound(size + 2);
                 cb[this.offset++] = QUOTE;
-                System.arraycopy(chars, offset, cb, this.offset, size);
+                
                 this.offset += size;
                 cb[this.offset++] = QUOTE;
             }
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 33 =====
```
             else if (shouldBeQuoted) {
                 checkBound(size + 2);
                 cb[this.offset++] = QUOTE;
-                System.arraycopy(chars, offset, cb, this.offset, size);
+                System.arraycopy(chars, offset, cb, this.offset + 1, size); // Writes data one position too far in the destination array
                 this.offset += size;
                 cb[this.offset++] = QUOTE;
             }
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset + 1, size); // Writes data one position too far in the destination array
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 34 =====
```
             else if (shouldBeQuoted) {
                 checkBound(size + 2);
                 cb[this.offset++] = QUOTE;
-                System.arraycopy(chars, offset, cb, this.offset, size);
+                System.arraycopy(chars, offset, cb, this.offset, 0); // Copies zero characters, resulting in no data being written
                 this.offset += size;
                 cb[this.offset++] = QUOTE;
             }
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, 0); // Copies zero characters, resulting in no data being written
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 35 =====
```
             else if (shouldBeQuoted) {
                 checkBound(size + 2);
                 cb[this.offset++] = QUOTE;
-                System.arraycopy(chars, offset, cb, this.offset, size);
+                System.arraycopy(chars, offset, cb, this.offset, size - 1); // Off-by-one error
                 this.offset += size;
                 cb[this.offset++] = QUOTE;
             }
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size - 1); // Off-by-one error
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
            }

        }
```
===== 36 =====
```
             }
             else {
                 checkBound(size);
-                System.arraycopy(chars, offset, cb, this.offset, size);
+                
                 this.offset += size;
             }
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                
                this.offset += size;
            }

        }
```
===== 37 =====
```
             }
             else {
                 checkBound(size);
-                System.arraycopy(chars, offset, cb, this.offset, size);
+                System.arraycopy(chars, offset, cb, this.offset, 0); // Copies zero characters, resulting in no data being written
                 this.offset += size;
             }
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, 0); // Copies zero characters, resulting in no data being written
                this.offset += size;
            }

        }
```
===== 38 =====
```
             }
             else {
                 checkBound(size);
-                System.arraycopy(chars, offset, cb, this.offset, size);
+                System.arraycopy(chars, offset, cb, this.offset, size - 1); // Off-by-one error
                 this.offset += size;
             }
```
```
        /**
         * Compression and escape char sequence
         * - line-break, double-quote or commas should be quoted.
         * - A (double) quote character in a field must be represented by two (double) quote characters.
         *
         * @param chars the char sequence to be written
         * @param offset the offset index
         * @param size size of characters
         * @throws IOException If an I/O error occurs
         */
        public void write(char[] chars, int offset, int size) throws IOException {
            test();
            int i = 0;
            int last = offset;
            boolean quoted = false, shouldBeQuoted = false;

            for ( ; i < size; ) {
                char c = chars[i++];

                // A (double) quote character in a field must be represented
                // by two (double) quote characters.
                if (c == QUOTE) {
                    quoted = true;
                    if (last == offset) {
                        checkBound(1);
                        cb[this.offset++] = QUOTE;
                    }
                    checkBound(i - last + 1);
                    System.arraycopy(chars, last, cb, this.offset, i - last);
                    this.offset += (i - last);
                    cb[this.offset++] = QUOTE;
                    last = i;
                }

                else if (c == LF || c == HT || c == separator || c == COMMA) {
                    shouldBeQuoted = true;
                }

            }

            if (quoted) {
                checkBound(i - last + 1);
                System.arraycopy(chars, last, cb, this.offset, i - last);
                this.offset += (i - last);
                cb[this.offset++] = QUOTE;
            }
            else if (shouldBeQuoted) {
                checkBound(size + 2);
                cb[this.offset++] = QUOTE;
                System.arraycopy(chars, offset, cb, this.offset, size);
                this.offset += size;
                cb[this.offset++] = QUOTE;
            }
            else {
                checkBound(size);
                System.arraycopy(chars, offset, cb, this.offset, size - 1); // Off-by-one error
                this.offset += size;
            }

        }
```
