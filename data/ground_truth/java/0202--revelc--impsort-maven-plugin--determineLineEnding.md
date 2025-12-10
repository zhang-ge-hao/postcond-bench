https://github.com/revelc/impsort-maven-plugin/blob/c1910f7dab00f6f7cc654501459442658a74fdd7/./src/main/java/net/revelc/code/impsort/LineEnding.java#L35-L69
```
//@ ensures \result != null;
//@ ensures \result == LineEnding.LF || \result == LineEnding.CRLF || \result == LineEnding.CR || \result == LineEnding.UNKNOWN;
//@ ensures (\result == LineEnding.LF) == (java.util.stream.IntStream.range(0, fileDataString.length()).filter(i -> fileDataString.charAt(i) == '\n' && (i == 0 || fileDataString.charAt(i - 1) != '\r')).count() > java.util.stream.IntStream.range(0, fileDataString.length()).filter(i -> fileDataString.charAt(i) == '\r' && (i + 1 >= fileDataString.length() || fileDataString.charAt(i + 1) != '\n')).count() && java.util.stream.IntStream.range(0, fileDataString.length()).filter(i -> fileDataString.charAt(i) == '\n' && (i == 0 || fileDataString.charAt(i - 1) != '\r')).count() > java.util.stream.IntStream.range(0, fileDataString.length() - 1).filter(i -> fileDataString.charAt(i) == '\r' && fileDataString.charAt(i + 1) == '\n').count());
//@ ensures (\result == LineEnding.CRLF) == (java.util.stream.IntStream.range(0, fileDataString.length() - 1).filter(i -> fileDataString.charAt(i) == '\r' && fileDataString.charAt(i + 1) == '\n').count() > java.util.stream.IntStream.range(0, fileDataString.length()).filter(i -> fileDataString.charAt(i) == '\n' && (i == 0 || fileDataString.charAt(i - 1) != '\r')).count() && java.util.stream.IntStream.range(0, fileDataString.length() - 1).filter(i -> fileDataString.charAt(i) == '\r' && fileDataString.charAt(i + 1) == '\n').count() > java.util.stream.IntStream.range(0, fileDataString.length()).filter(i -> fileDataString.charAt(i) == '\r' && (i + 1 >= fileDataString.length() || fileDataString.charAt(i + 1) != '\n')).count());
//@ ensures (\result == LineEnding.CR) == (java.util.stream.IntStream.range(0, fileDataString.length()).filter(i -> fileDataString.charAt(i) == '\r' && (i + 1 >= fileDataString.length() || fileDataString.charAt(i + 1) != '\n')).count() > java.util.stream.IntStream.range(0, fileDataString.length()).filter(i -> fileDataString.charAt(i) == '\n' && (i == 0 || fileDataString.charAt(i - 1) != '\r')).count() && java.util.stream.IntStream.range(0, fileDataString.length()).filter(i -> fileDataString.charAt(i) == '\r' && (i + 1 >= fileDataString.length() || fileDataString.charAt(i + 1) != '\n')).count() > java.util.stream.IntStream.range(0, fileDataString.length() - 1).filter(i -> fileDataString.charAt(i) == '\r' && fileDataString.charAt(i + 1) == '\n').count());
//@ ensures (\result == LineEnding.UNKNOWN) == (!(java.util.stream.IntStream.range(0, fileDataString.length()).filter(i -> fileDataString.charAt(i) == '\n' && (i == 0 || fileDataString.charAt(i - 1) != '\r')).count() > java.util.stream.IntStream.range(0, fileDataString.length()).filter(i -> fileDataString.charAt(i) == '\r' && (i + 1 >= fileDataString.length() || fileDataString.charAt(i + 1) != '\n')).count() && java.util.stream.IntStream.range(0, fileDataString.length()).filter(i -> fileDataString.charAt(i) == '\n' && (i == 0 || fileDataString.charAt(i - 1) != '\r')).count() > java.util.stream.IntStream.range(0, fileDataString.length() - 1).filter(i -> fileDataString.charAt(i) == '\r' && fileDataString.charAt(i + 1) == '\n').count()) && !(java.util.stream.IntStream.range(0, fileDataString.length() - 1).filter(i -> fileDataString.charAt(i) == '\r' && fileDataString.charAt(i + 1) == '\n').count() > java.util.stream.IntStream.range(0, fileDataString.length()).filter(i -> fileDataString.charAt(i) == '\n' && (i == 0 || fileDataString.charAt(i - 1) != '\r')).count() && java.util.stream.IntStream.range(0, fileDataString.length() - 1).filter(i -> fileDataString.charAt(i) == '\r' && fileDataString.charAt(i + 1) == '\n').count() > java.util.stream.IntStream.range(0, fileDataString.length()).filter(i -> fileDataString.charAt(i) == '\r' && (i + 1 >= fileDataString.length() || fileDataString.charAt(i + 1) != '\n')).count()) && !(java.util.stream.IntStream.range(0, fileDataString.length()).filter(i -> fileDataString.charAt(i) == '\r' && (i + 1 >= fileDataString.length() || fileDataString.charAt(i + 1) != '\n')).count() > java.util.stream.IntStream.range(0, fileDataString.length()).filter(i -> fileDataString.charAt(i) == '\n' && (i == 0 || fileDataString.charAt(i - 1) != '\r')).count() && java.util.stream.IntStream.range(0, fileDataString.length()).filter(i -> fileDataString.charAt(i) == '\r' && (i + 1 >= fileDataString.length() || fileDataString.charAt(i + 1) != '\n')).count() > java.util.stream.IntStream.range(0, fileDataString.length() - 1).filter(i -> fileDataString.charAt(i) == '\r' && fileDataString.charAt(i + 1) == '\n').count()));
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45]
===== 0 =====
```
     int crCount = 0;
     int crlfCount = 0;
 
-    for (int i = 0; i < fileDataString.length(); i++) {
+    for (int i = 0; i < fileDataString.length() - 1; i++) {
       char c = fileDataString.charAt(i);
       if (c == '\r') {
         if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length() - 1; i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 1 =====
```
     int crCount = 0;
     int crlfCount = 0;
 
-    for (int i = 0; i < fileDataString.length(); i++) {
+    for (int i = 0; i < fileDataString.length(); i += 2) {
       char c = fileDataString.charAt(i);
       if (c == '\r') {
         if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i += 2) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 2 =====
```
     int crCount = 0;
     int crlfCount = 0;
 
-    for (int i = 0; i < fileDataString.length(); i++) {
+    for (int i = 0; i < fileDataString.length(); i++) { if (i % 2 == 0) continue;
       char c = fileDataString.charAt(i);
       if (c == '\r') {
         if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) { if (i % 2 == 0) continue;
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 3 =====
```
     int crCount = 0;
     int crlfCount = 0;
 
-    for (int i = 0; i < fileDataString.length(); i++) {
+    for (int i = 0; i >= fileDataString.length(); i++) {
       char c = fileDataString.charAt(i);
       if (c == '\r') {
         if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i >= fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 4 =====
```
     int crlfCount = 0;
 
     for (int i = 0; i < fileDataString.length(); i++) {
-      char c = fileDataString.charAt(i);
+      char c = ' ';
       if (c == '\r') {
         if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
           crlfCount++;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = ' ';
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 5 =====
```
     int crlfCount = 0;
 
     for (int i = 0; i < fileDataString.length(); i++) {
-      char c = fileDataString.charAt(i);
+      char c = fileDataString.charAt(i) == '\n' ? '\r' : fileDataString.charAt(i);
       if (c == '\r') {
         if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
           crlfCount++;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i) == '\n' ? '\r' : fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 6 =====
```
     int crlfCount = 0;
 
     for (int i = 0; i < fileDataString.length(); i++) {
-      char c = fileDataString.charAt(i);
+      char c = fileDataString.charAt(i) == '\r' ? '\n' : fileDataString.charAt(i);
       if (c == '\r') {
         if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
           crlfCount++;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i) == '\r' ? '\n' : fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 7 =====
```
 
     for (int i = 0; i < fileDataString.length(); i++) {
       char c = fileDataString.charAt(i);
-      if (c == '\r') {
+      if (c != '\r') {
         if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
           crlfCount++;
           i++;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c != '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 8 =====
```
 
     for (int i = 0; i < fileDataString.length(); i++) {
       char c = fileDataString.charAt(i);
-      if (c == '\r') {
+      if (c == ' ') {
         if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
           crlfCount++;
           i++;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == ' ') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 9 =====
```
 
     for (int i = 0; i < fileDataString.length(); i++) {
       char c = fileDataString.charAt(i);
-      if (c == '\r') {
+      if (c == '\b') {
         if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
           crlfCount++;
           i++;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\b') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 10 =====
```
 
     for (int i = 0; i < fileDataString.length(); i++) {
       char c = fileDataString.charAt(i);
-      if (c == '\r') {
+      if (c == '\f') {
         if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
           crlfCount++;
           i++;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\f') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 11 =====
```
 
     for (int i = 0; i < fileDataString.length(); i++) {
       char c = fileDataString.charAt(i);
-      if (c == '\r') {
+      if (c == '\t') {
         if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
           crlfCount++;
           i++;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\t') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 12 =====
```
 
     for (int i = 0; i < fileDataString.length(); i++) {
       char c = fileDataString.charAt(i);
-      if (c == '\r') {
+      if (c == '\u000C') {
         if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
           crlfCount++;
           i++;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\u000C') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 13 =====
```
     for (int i = 0; i < fileDataString.length(); i++) {
       char c = fileDataString.charAt(i);
       if (c == '\r') {
-        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
+        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) != '\n') {
           crlfCount++;
           i++;
         } else {
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) != '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 14 =====
```
     for (int i = 0; i < fileDataString.length(); i++) {
       char c = fileDataString.charAt(i);
       if (c == '\r') {
-        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
+        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i - 1) == '\n') {
           crlfCount++;
           i++;
         } else {
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i - 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 15 =====
```
       char c = fileDataString.charAt(i);
       if (c == '\r') {
         if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
-          crlfCount++;
+          crlfCount--;
           i++;
         } else {
           crCount++;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount--;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 16 =====
```
           crlfCount++;
           i++;
         } else {
-          crCount++;
+          crCount--;
         }
       } else if (c == '\n') {
         lfCount++;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount--;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 17 =====
```
         } else {
           crCount++;
         }
-      } else if (c == '\n') {
+      } else if (c != '\n') {
         lfCount++;
       }
     }
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c != '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 18 =====
```
         } else {
           crCount++;
         }
-      } else if (c == '\n') {
+      } else if (c == ' ') {
         lfCount++;
       }
     }
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == ' ') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 19 =====
```
         } else {
           crCount++;
         }
-      } else if (c == '\n') {
+      } else if (c == '\f') {
         lfCount++;
       }
     }
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\f') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 20 =====
```
         } else {
           crCount++;
         }
-      } else if (c == '\n') {
+      } else if (c == '\r') {
         lfCount++;
       }
     }
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\r') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 21 =====
```
         } else {
           crCount++;
         }
-      } else if (c == '\n') {
+      } else if (c == '\t') {
         lfCount++;
       }
     }
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\t') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 22 =====
```
         } else {
           crCount++;
         }
-      } else if (c == '\n') {
+      } else {
         lfCount++;
       }
     }
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 23 =====
```
           crCount++;
         }
       } else if (c == '\n') {
-        lfCount++;
+        lfCount--;
       }
     }
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount--;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 24 =====
```
       }
     }
 
-    if (lfCount > crCount && lfCount > crlfCount) {
+    if (lfCount < crCount && lfCount < crlfCount) {
       return LF;
     } else if (crlfCount > lfCount && crlfCount > crCount) {
       return CRLF;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount < crCount && lfCount < crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 25 =====
```
       }
     }
 
-    if (lfCount > crCount && lfCount > crlfCount) {
+    if (lfCount <= crCount && lfCount > crlfCount) {
       return LF;
     } else if (crlfCount > lfCount && crlfCount > crCount) {
       return CRLF;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount <= crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 26 =====
```
       }
     }
 
-    if (lfCount > crCount && lfCount > crlfCount) {
+    if (lfCount == crCount && lfCount == crlfCount) {
       return LF;
     } else if (crlfCount > lfCount && crlfCount > crCount) {
       return CRLF;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount == crCount && lfCount == crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 27 =====
```
       }
     }
 
-    if (lfCount > crCount && lfCount > crlfCount) {
+    if (lfCount == crCount && lfCount > crlfCount) {
       return LF;
     } else if (crlfCount > lfCount && crlfCount > crCount) {
       return CRLF;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount == crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 28 =====
```
       }
     }
 
-    if (lfCount > crCount && lfCount > crlfCount) {
+    if (lfCount > crCount && lfCount <= crlfCount) {
       return LF;
     } else if (crlfCount > lfCount && crlfCount > crCount) {
       return CRLF;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount <= crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 29 =====
```
       }
     }
 
-    if (lfCount > crCount && lfCount > crlfCount) {
+    if (lfCount > crCount && lfCount >= crlfCount) {
       return LF;
     } else if (crlfCount > lfCount && crlfCount > crCount) {
       return CRLF;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount >= crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 30 =====
```
       }
     }
 
-    if (lfCount > crCount && lfCount > crlfCount) {
+    if (lfCount > crCount || lfCount > crlfCount) {
       return LF;
     } else if (crlfCount > lfCount && crlfCount > crCount) {
       return CRLF;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount || lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 31 =====
```
       }
     }
 
-    if (lfCount > crCount && lfCount > crlfCount) {
+    if (lfCount >= crCount && lfCount >= crlfCount) {
       return LF;
     } else if (crlfCount > lfCount && crlfCount > crCount) {
       return CRLF;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount >= crCount && lfCount >= crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 32 =====
```
     }
 
     if (lfCount > crCount && lfCount > crlfCount) {
-      return LF;
+      return null;
     } else if (crlfCount > lfCount && crlfCount > crCount) {
       return CRLF;
     } else if (crCount > lfCount && crCount > crlfCount) {
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return null;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 33 =====
```
 
     if (lfCount > crCount && lfCount > crlfCount) {
       return LF;
-    } else if (crlfCount > lfCount && crlfCount > crCount) {
+    } else if (crlfCount < lfCount && crlfCount > crCount) {
       return CRLF;
     } else if (crCount > lfCount && crCount > crlfCount) {
       return CR;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount < lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 34 =====
```
 
     if (lfCount > crCount && lfCount > crlfCount) {
       return LF;
-    } else if (crlfCount > lfCount && crlfCount > crCount) {
+    } else if (crlfCount <= lfCount && crlfCount > crCount) {
       return CRLF;
     } else if (crCount > lfCount && crCount > crlfCount) {
       return CR;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount <= lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 35 =====
```
 
     if (lfCount > crCount && lfCount > crlfCount) {
       return LF;
-    } else if (crlfCount > lfCount && crlfCount > crCount) {
+    } else if (crlfCount == lfCount && crlfCount > crCount) {
       return CRLF;
     } else if (crCount > lfCount && crCount > crlfCount) {
       return CR;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount == lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 36 =====
```
 
     if (lfCount > crCount && lfCount > crlfCount) {
       return LF;
-    } else if (crlfCount > lfCount && crlfCount > crCount) {
+    } else if (crlfCount > lfCount && crlfCount <= crCount) {
       return CRLF;
     } else if (crCount > lfCount && crCount > crlfCount) {
       return CR;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount <= crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 37 =====
```
 
     if (lfCount > crCount && lfCount > crlfCount) {
       return LF;
-    } else if (crlfCount > lfCount && crlfCount > crCount) {
+    } else if (crlfCount >= lfCount && crlfCount > crCount) {
       return CRLF;
     } else if (crCount > lfCount && crCount > crlfCount) {
       return CR;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount >= lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 38 =====
```
     if (lfCount > crCount && lfCount > crlfCount) {
       return LF;
     } else if (crlfCount > lfCount && crlfCount > crCount) {
-      return CRLF;
+      return null;
     } else if (crCount > lfCount && crCount > crlfCount) {
       return CR;
     }
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return null;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 39 =====
```
       return LF;
     } else if (crlfCount > lfCount && crlfCount > crCount) {
       return CRLF;
-    } else if (crCount > lfCount && crCount > crlfCount) {
+    } else if (crCount < lfCount && crCount < crlfCount) {
       return CR;
     }
     return UNKNOWN;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount < lfCount && crCount < crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 40 =====
```
       return LF;
     } else if (crlfCount > lfCount && crlfCount > crCount) {
       return CRLF;
-    } else if (crCount > lfCount && crCount > crlfCount) {
+    } else if (crCount < lfCount || crCount < crlfCount) {
       return CR;
     }
     return UNKNOWN;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount < lfCount || crCount < crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 41 =====
```
       return LF;
     } else if (crlfCount > lfCount && crlfCount > crCount) {
       return CRLF;
-    } else if (crCount > lfCount && crCount > crlfCount) {
+    } else if (crCount <= lfCount && crCount > crlfCount) {
       return CR;
     }
     return UNKNOWN;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount <= lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 42 =====
```
       return LF;
     } else if (crlfCount > lfCount && crlfCount > crCount) {
       return CRLF;
-    } else if (crCount > lfCount && crCount > crlfCount) {
+    } else if (crCount == lfCount && crCount > crlfCount) {
       return CR;
     }
     return UNKNOWN;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount == lfCount && crCount > crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 43 =====
```
       return LF;
     } else if (crlfCount > lfCount && crlfCount > crCount) {
       return CRLF;
-    } else if (crCount > lfCount && crCount > crlfCount) {
+    } else if (crCount > lfCount && crCount <= crlfCount) {
       return CR;
     }
     return UNKNOWN;
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount <= crlfCount) {
      return CR;
    }
    return UNKNOWN;
  }
```
===== 44 =====
```
     } else if (crlfCount > lfCount && crlfCount > crCount) {
       return CRLF;
     } else if (crCount > lfCount && crCount > crlfCount) {
-      return CR;
+      return null;
     }
     return UNKNOWN;
   }
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return null;
    }
    return UNKNOWN;
  }
```
===== 45 =====
```
     } else if (crCount > lfCount && crCount > crlfCount) {
       return CR;
     }
-    return UNKNOWN;
+    return null;
   }
```
```
  /**
   * Returns the most occurring line-ending characters in the file text or null if no line-ending
   * occurs the most.
   *
   * @param fileDataString the raw file contents as a string
   * @return the determined line-ending
   */
  public static LineEnding determineLineEnding(String fileDataString) {
    int lfCount = 0;
    int crCount = 0;
    int crlfCount = 0;

    for (int i = 0; i < fileDataString.length(); i++) {
      char c = fileDataString.charAt(i);
      if (c == '\r') {
        if ((i + 1) < fileDataString.length() && fileDataString.charAt(i + 1) == '\n') {
          crlfCount++;
          i++;
        } else {
          crCount++;
        }
      } else if (c == '\n') {
        lfCount++;
      }
    }

    if (lfCount > crCount && lfCount > crlfCount) {
      return LF;
    } else if (crlfCount > lfCount && crlfCount > crCount) {
      return CRLF;
    } else if (crCount > lfCount && crCount > crlfCount) {
      return CR;
    }
    return null;
  }
```
