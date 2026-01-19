https://github.com/americanexpress/unify-jdocs/blob/325af27be93ae4a1df784cf683cdff61e1bb7ac3/./src/main/java/com/americanexpress/unify/base/BaseUtils.java#L726-L747
```
🈚️

originally wrong. `String... others`

//@ ensures (first == null || others == null) ==> \result == false;
//@ ensures (first != null && others != null && java.util.Arrays.stream(others).anyMatch(o -> o != null && first.equalsIgnoreCase(o))) ==> \result == true;
//@ ensures (first != null && others != null && java.util.Arrays.stream(others).noneMatch(o -> o != null && first.equalsIgnoreCase(o))) ==> \result == false;
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
===== 0 =====
```
    * False if first or others are null
    */
   public static boolean compareWithManyIgnoreCase(String first, String... others) {
-    if (first == null || others == null) {
+    if (first != null && others != null) {
       return false;
     }
```
```
  /**
   * Compares the given String with more than one Strings ignoring case
   *
   * @param first  The String to compare
   * @param others The Strings to compare against
   * @return True if first is matched to any of others else false
   * <p>
   * False if first or others are null
   */
  public static boolean compareWithManyIgnoreCase(String first, String... others) {
    if (first != null && others != null) {
      return false;
    }

    for (int i = 0; i < others.length; i++) {
      if (first.equalsIgnoreCase(others[i])) {
        return true;
      }
    }

    return false;
  }
```
===== 1 =====
```
    * False if first or others are null
    */
   public static boolean compareWithManyIgnoreCase(String first, String... others) {
-    if (first == null || others == null) {
+    if (first != null || others == null) {
       return false;
     }
```
```
  /**
   * Compares the given String with more than one Strings ignoring case
   *
   * @param first  The String to compare
   * @param others The Strings to compare against
   * @return True if first is matched to any of others else false
   * <p>
   * False if first or others are null
   */
  public static boolean compareWithManyIgnoreCase(String first, String... others) {
    if (first != null || others == null) {
      return false;
    }

    for (int i = 0; i < others.length; i++) {
      if (first.equalsIgnoreCase(others[i])) {
        return true;
      }
    }

    return false;
  }
```
===== 2 =====
```
    * False if first or others are null
    */
   public static boolean compareWithManyIgnoreCase(String first, String... others) {
-    if (first == null || others == null) {
+    if (first == null || others != null) {
       return false;
     }
```
```
  /**
   * Compares the given String with more than one Strings ignoring case
   *
   * @param first  The String to compare
   * @param others The Strings to compare against
   * @return True if first is matched to any of others else false
   * <p>
   * False if first or others are null
   */
  public static boolean compareWithManyIgnoreCase(String first, String... others) {
    if (first == null || others != null) {
      return false;
    }

    for (int i = 0; i < others.length; i++) {
      if (first.equalsIgnoreCase(others[i])) {
        return true;
      }
    }

    return false;
  }
```
===== 3 =====
```
    * False if first or others are null
    */
   public static boolean compareWithManyIgnoreCase(String first, String... others) {
-    if (first == null || others == null) {
+    if (first == null || others.length > 0) {
       return false;
     }
```
```
  /**
   * Compares the given String with more than one Strings ignoring case
   *
   * @param first  The String to compare
   * @param others The Strings to compare against
   * @return True if first is matched to any of others else false
   * <p>
   * False if first or others are null
   */
  public static boolean compareWithManyIgnoreCase(String first, String... others) {
    if (first == null || others.length > 0) {
      return false;
    }

    for (int i = 0; i < others.length; i++) {
      if (first.equalsIgnoreCase(others[i])) {
        return true;
      }
    }

    return false;
  }
```
===== 4 =====
```
    */
   public static boolean compareWithManyIgnoreCase(String first, String... others) {
     if (first == null || others == null) {
-      return false;
+      return true;
     }
 
     for (int i = 0; i < others.length; i++) {
```
```
  /**
   * Compares the given String with more than one Strings ignoring case
   *
   * @param first  The String to compare
   * @param others The Strings to compare against
   * @return True if first is matched to any of others else false
   * <p>
   * False if first or others are null
   */
  public static boolean compareWithManyIgnoreCase(String first, String... others) {
    if (first == null || others == null) {
      return true;
    }

    for (int i = 0; i < others.length; i++) {
      if (first.equalsIgnoreCase(others[i])) {
        return true;
      }
    }

    return false;
  }
```
===== 5 =====
```
       return false;
     }
 
-    for (int i = 0; i < others.length; i++) {
+    for (int i = 0; i < others.length - 1; i++) {
       if (first.equalsIgnoreCase(others[i])) {
         return true;
       }
```
```
  /**
   * Compares the given String with more than one Strings ignoring case
   *
   * @param first  The String to compare
   * @param others The Strings to compare against
   * @return True if first is matched to any of others else false
   * <p>
   * False if first or others are null
   */
  public static boolean compareWithManyIgnoreCase(String first, String... others) {
    if (first == null || others == null) {
      return false;
    }

    for (int i = 0; i < others.length - 1; i++) {
      if (first.equalsIgnoreCase(others[i])) {
        return true;
      }
    }

    return false;
  }
```
===== 6 =====
```
       return false;
     }
 
-    for (int i = 0; i < others.length; i++) {
+    for (int i = 0; i >= others.length; i++) {
       if (first.equalsIgnoreCase(others[i])) {
         return true;
       }
```
```
  /**
   * Compares the given String with more than one Strings ignoring case
   *
   * @param first  The String to compare
   * @param others The Strings to compare against
   * @return True if first is matched to any of others else false
   * <p>
   * False if first or others are null
   */
  public static boolean compareWithManyIgnoreCase(String first, String... others) {
    if (first == null || others == null) {
      return false;
    }

    for (int i = 0; i >= others.length; i++) {
      if (first.equalsIgnoreCase(others[i])) {
        return true;
      }
    }

    return false;
  }
```
===== 7 =====
```
     }
 
     for (int i = 0; i < others.length; i++) {
-      if (first.equalsIgnoreCase(others[i])) {
+      if (first == others[i]) {
         return true;
       }
     }
```
```
  /**
   * Compares the given String with more than one Strings ignoring case
   *
   * @param first  The String to compare
   * @param others The Strings to compare against
   * @return True if first is matched to any of others else false
   * <p>
   * False if first or others are null
   */
  public static boolean compareWithManyIgnoreCase(String first, String... others) {
    if (first == null || others == null) {
      return false;
    }

    for (int i = 0; i < others.length; i++) {
      if (first == others[i]) {
        return true;
      }
    }

    return false;
  }
```
===== 8 =====
```
     }
 
     for (int i = 0; i < others.length; i++) {
-      if (first.equalsIgnoreCase(others[i])) {
+      if (first.equals(others[i])) {
         return true;
       }
     }
```
```
  /**
   * Compares the given String with more than one Strings ignoring case
   *
   * @param first  The String to compare
   * @param others The Strings to compare against
   * @return True if first is matched to any of others else false
   * <p>
   * False if first or others are null
   */
  public static boolean compareWithManyIgnoreCase(String first, String... others) {
    if (first == null || others == null) {
      return false;
    }

    for (int i = 0; i < others.length; i++) {
      if (first.equals(others[i])) {
        return true;
      }
    }

    return false;
  }
```
===== 9 =====
```
 
     for (int i = 0; i < others.length; i++) {
       if (first.equalsIgnoreCase(others[i])) {
-        return true;
+        return false;
       }
     }
```
```
  /**
   * Compares the given String with more than one Strings ignoring case
   *
   * @param first  The String to compare
   * @param others The Strings to compare against
   * @return True if first is matched to any of others else false
   * <p>
   * False if first or others are null
   */
  public static boolean compareWithManyIgnoreCase(String first, String... others) {
    if (first == null || others == null) {
      return false;
    }

    for (int i = 0; i < others.length; i++) {
      if (first.equalsIgnoreCase(others[i])) {
        return false;
      }
    }

    return false;
  }
```
===== 10 =====
```
       }
     }
 
-    return false;
+    return true;
   }
```
```
  /**
   * Compares the given String with more than one Strings ignoring case
   *
   * @param first  The String to compare
   * @param others The Strings to compare against
   * @return True if first is matched to any of others else false
   * <p>
   * False if first or others are null
   */
  public static boolean compareWithManyIgnoreCase(String first, String... others) {
    if (first == null || others == null) {
      return false;
    }

    for (int i = 0; i < others.length; i++) {
      if (first.equalsIgnoreCase(others[i])) {
        return true;
      }
    }

    return true;
  }
```
