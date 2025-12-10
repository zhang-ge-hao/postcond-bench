https://github.com/americanexpress/unify-jdocs/blob/325af27be93ae4a1df784cf683cdff61e1bb7ac3/./src/main/java/com/americanexpress/unify/jdocs/JDocument.java#L3491-L3538
```
//@ ensures \result != null;
//@ ensures \result.stream().allMatch(di -> di != null);
//@ ensures \result.stream().allMatch(di -> di.getDiffResult() != null);
//@ ensures \result.stream().noneMatch(di -> di.getLeft() == null && di.getRight() == null);
//@ ensures \result.stream().filter(di -> di.getLeft() != null).allMatch(di -> \old(flattenWithValues()).stream().anyMatch(lp -> lp.getPath().equals(di.getLeft().getPath())));
//@ ensures \result.stream().filter(di -> di.getRight() != null).allMatch(di -> \old(right.flattenWithValues()).stream().anyMatch(rp -> rp.getPath().equals(di.getRight().getPath())));
//@ ensures \result.stream().filter(di -> di.getLeft() != null && di.getRight() == null).allMatch(di -> \old(right.flattenWithValues()).stream().noneMatch(rp -> rp.getPath().equals(di.getLeft().getPath())));
//@ ensures \result.stream().filter(di -> di.getLeft() == null && di.getRight() != null).allMatch(di -> \old(flattenWithValues()).stream().noneMatch(lp -> lp.getPath().equals(di.getRight().getPath())));
//@ ensures !onlyDifferences ==> (\old(flattenWithValues()).stream().allMatch(lp -> \result.stream().filter(di -> di.getLeft() != null).anyMatch(di -> di.getLeft().getPath().equals(lp.getPath()) && ((lp.getValue() == null && di.getLeft().getValue() == null) || (lp.getValue() != null && di.getLeft().getValue() != null && lp.getValue().equals(di.getLeft().getValue()))))));
//@ ensures !onlyDifferences ==> (\old(right.flattenWithValues()).stream().filter(rp -> \old(flattenWithValues()).stream().noneMatch(lp -> lp.getPath().equals(rp.getPath()))).allMatch(rp -> \result.stream().anyMatch(di -> di.getLeft() == null && di.getRight() != null && di.getRight().getPath().equals(rp.getPath()) && ((rp.getValue() == null && di.getRight().getValue() == null) || (rp.getValue() != null && di.getRight().getValue() != null && rp.getValue().equals(di.getRight().getValue()))))));
//@ ensures !onlyDifferences ==> ((long)\result.size() == (long)\old(flattenWithValues()).size() + \old(right.flattenWithValues()).stream().filter(rp -> \old(flattenWithValues()).stream().noneMatch(lp -> lp.getPath().equals(rp.getPath()))).count());
//@ ensures onlyDifferences ==> (\result.stream().noneMatch(di -> di.getDiffResult() == PathDiffResult.EQUAL));
//@ ensures onlyDifferences ==> (\old(flattenWithValues()).stream().filter(lp -> \old(right.flattenWithValues()).stream().anyMatch(rp -> rp.getPath().equals(lp.getPath()) && ((lp.getValue() == null && rp.getValue() == null) || (lp.getValue() != null && rp.getValue() != null && lp.getValue().equals(rp.getValue()))))).allMatch(lp -> \result.stream().noneMatch(di -> (di.getLeft() != null && di.getLeft().getPath().equals(lp.getPath())) || (di.getRight() != null && di.getRight().getPath().equals(lp.getPath())))));
//@ ensures onlyDifferences ==> (\old(flattenWithValues()).stream().filter(lp -> (lp.getValue() != null && \old(right.flattenWithValues()).stream().noneMatch(rp -> rp.getPath().equals(lp.getPath()))) || \old(right.flattenWithValues()).stream().anyMatch(rp -> rp.getPath().equals(lp.getPath()) && !(((lp.getValue() == null) && (rp.getValue() == null)) || (lp.getValue() != null && rp.getValue() != null && lp.getValue().equals(rp.getValue()))))).allMatch(lp -> \result.stream().filter(di -> di.getLeft() != null).anyMatch(di -> di.getLeft().getPath().equals(lp.getPath()) && ((lp.getValue() == null && di.getLeft().getValue() == null) || (lp.getValue() != null && di.getLeft().getValue() != null && lp.getValue().equals(di.getLeft().getValue()))))));
//@ ensures onlyDifferences ==> (\old(right.flattenWithValues()).stream().filter(rp -> rp.getValue() != null && \old(flattenWithValues()).stream().noneMatch(lp -> lp.getPath().equals(rp.getPath()))).allMatch(rp -> \result.stream().anyMatch(di -> di.getLeft() == null && di.getRight() != null && di.getRight().getPath().equals(rp.getPath()) && ((rp.getValue() == null && di.getRight().getValue() == null) || (rp.getValue() != null && di.getRight().getValue() != null && rp.getValue().equals(di.getRight().getValue()))))));
//@ ensures onlyDifferences ==> ((long)\result.size() == \old(flattenWithValues()).stream().filter(lp -> (lp.getValue() != null && \old(right.flattenWithValues()).stream().noneMatch(rp -> rp.getPath().equals(lp.getPath()))) || \old(right.flattenWithValues()).stream().anyMatch(rp -> rp.getPath().equals(lp.getPath()) && !(((lp.getValue() == null) && (rp.getValue() == null)) || (lp.getValue() != null && rp.getValue() != null && lp.getValue().equals(rp.getValue()))))).count() + \old(right.flattenWithValues()).stream().filter(rp -> rp.getValue() != null && \old(flattenWithValues()).stream().noneMatch(lp -> lp.getPath().equals(rp.getPath()))).count());
```
```
//@ ensures \result != null;
//@ ensures \result.stream().allMatch(di -> ((di.getLeft() != null && \old(flattenWithValues()).stream().anyMatch(lp -> lp.getPath().equals(di.getLeft().getPath()))) || (di.getRight() != null && \old(right.flattenWithValues()).stream().anyMatch(rp -> rp.getPath().equals(di.getRight().getPath())))));
//@ ensures (onlyDifferences) ==> (\result.stream().noneMatch(di -> di.getDiffResult() == PathDiffResult.EQUAL));
//@ ensures (!onlyDifferences) ==> (\old(flattenWithValues()).stream().allMatch(lp -> \result.stream().filter(di -> di.getLeft() != null).anyMatch(di -> di.getLeft().getPath().equals(lp.getPath()))));
//@ ensures (!onlyDifferences) ==> (\old(right.flattenWithValues()).stream().filter(rp -> \old(flattenWithValues()).stream().noneMatch(lp -> lp.getPath().equals(rp.getPath()))).allMatch(rp -> \result.stream().anyMatch(di -> di.getRight() != null && di.getRight().getPath().equals(rp.getPath()) && di.getLeft() == null)));
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 21, 23, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34, 35, 36, 38, 39, 40, 41, 42, 43, 44, 45]
===== 0 =====
```
    */
   public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
     List<DiffInfo> diffInfoList = new LinkedList<>();
-    List<PathValue> leftPaths = flattenWithValues();
+    List<PathValue> leftPaths = flattenWithValues().stream().map(pv -> new PathValue(pv.getPath(), null, pv.getDataType())).collect(Collectors.toList()); // This creates new PathValue objects with null values, losing the original values for comparison.
     List<PathValue> rightPaths = right.flattenWithValues();
 
     Map<String, PathValue> rightMap = new HashMap<>();
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues().stream().map(pv -> new PathValue(pv.getPath(), null, pv.getDataType())).collect(Collectors.toList()); // This creates new PathValue objects with null values, losing the original values for comparison.
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 1 =====
```
    */
   public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
     List<DiffInfo> diffInfoList = new LinkedList<>();
-    List<PathValue> leftPaths = flattenWithValues();
+    List<PathValue> leftPaths = flattenWithValues().subList(0, 1); // This only takes the first path, ignoring all others and leading to incomplete comparisons.
     List<PathValue> rightPaths = right.flattenWithValues();
 
     Map<String, PathValue> rightMap = new HashMap<>();
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues().subList(0, 1); // This only takes the first path, ignoring all others and leading to incomplete comparisons.
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 2 =====
```
    */
   public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
     List<DiffInfo> diffInfoList = new LinkedList<>();
-    List<PathValue> leftPaths = flattenWithValues();
+    List<PathValue> leftPaths = new ArrayList<>(); // This initializes an empty list, resulting in no paths being compared.
     List<PathValue> rightPaths = right.flattenWithValues();
 
     Map<String, PathValue> rightMap = new HashMap<>();
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = new ArrayList<>(); // This initializes an empty list, resulting in no paths being compared.
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 3 =====
```
   public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
     List<DiffInfo> diffInfoList = new LinkedList<>();
     List<PathValue> leftPaths = flattenWithValues();
-    List<PathValue> rightPaths = right.flattenWithValues();
+    List<PathValue> rightPaths = new ArrayList<>(); // This initializes an empty list, causing all comparisons to fail.
 
     Map<String, PathValue> rightMap = new HashMap<>();
     rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = new ArrayList<>(); // This initializes an empty list, causing all comparisons to fail.

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 4 =====
```
   public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
     List<DiffInfo> diffInfoList = new LinkedList<>();
     List<PathValue> leftPaths = flattenWithValues();
-    List<PathValue> rightPaths = right.flattenWithValues();
+    List<PathValue> rightPaths = right.flattenWithValues().stream().map(pv -> new PathValue(pv.getPath(), null, pv.getDataType())).collect(Collectors.toList()); // This creates new PathValue objects with null values, leading to incorrect comparisons.
 
     Map<String, PathValue> rightMap = new HashMap<>();
     rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues().stream().map(pv -> new PathValue(pv.getPath(), null, pv.getDataType())).collect(Collectors.toList()); // This creates new PathValue objects with null values, leading to incorrect comparisons.

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 5 =====
```
   public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
     List<DiffInfo> diffInfoList = new LinkedList<>();
     List<PathValue> leftPaths = flattenWithValues();
-    List<PathValue> rightPaths = right.flattenWithValues();
+    List<PathValue> rightPaths = right.flattenWithValues().subList(0, 1); // This only takes the first element, ignoring the rest and leading to incomplete comparisons.
 
     Map<String, PathValue> rightMap = new HashMap<>();
     rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues().subList(0, 1); // This only takes the first element, ignoring the rest and leading to incomplete comparisons.

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 6 =====
```
     List<PathValue> rightPaths = right.flattenWithValues();
 
     Map<String, PathValue> rightMap = new HashMap<>();
-    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));
+    
 
     for (PathValue leftPv : leftPaths) {
       PathValue rightPv = rightMap.get(leftPv.getPath());
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 7 =====
```
     List<PathValue> rightPaths = right.flattenWithValues();
 
     Map<String, PathValue> rightMap = new HashMap<>();
-    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));
+    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath() + "_suffix", pv)); // This will change the keys in the map, leading to incorrect path references
 
     for (PathValue leftPv : leftPaths) {
       PathValue rightPv = rightMap.get(leftPv.getPath());
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath() + "_suffix", pv)); // This will change the keys in the map, leading to incorrect path references

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 8 =====
```
     List<PathValue> rightPaths = right.flattenWithValues();
 
     Map<String, PathValue> rightMap = new HashMap<>();
-    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));
+    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), new PathValue(pv.getPath(), null, null))); // This will create PathValue objects with null values
 
     for (PathValue leftPv : leftPaths) {
       PathValue rightPv = rightMap.get(leftPv.getPath());
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), new PathValue(pv.getPath(), null, null))); // This will create PathValue objects with null values

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 9 =====
```
     Map<String, PathValue> rightMap = new HashMap<>();
     rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));
 
-    for (PathValue leftPv : leftPaths) {
+    for (PathValue leftPv : rightPaths) {
       PathValue rightPv = rightMap.get(leftPv.getPath());
       DiffInfo di = comparePaths(leftPv, rightPv);
       if (onlyDifferences == true) {
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : rightPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 10 =====
```
     rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));
 
     for (PathValue leftPv : leftPaths) {
-      PathValue rightPv = rightMap.get(leftPv.getPath());
+      PathValue rightPv = rightMap.get(leftPv.getPath() + "[0]"); // Incorrectly appending an index to the path, which may not exist
       DiffInfo di = comparePaths(leftPv, rightPv);
       if (onlyDifferences == true) {
         if (di.getDiffResult() != PathDiffResult.EQUAL) {
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath() + "[0]"); // Incorrectly appending an index to the path, which may not exist
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 11 =====
```
     rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));
 
     for (PathValue leftPv : leftPaths) {
-      PathValue rightPv = rightMap.get(leftPv.getPath());
+      PathValue rightPv = rightMap.get(leftPv.getPath() + "extra"); // Incorrectly appending extra text to the path
       DiffInfo di = comparePaths(leftPv, rightPv);
       if (onlyDifferences == true) {
         if (di.getDiffResult() != PathDiffResult.EQUAL) {
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath() + "extra"); // Incorrectly appending extra text to the path
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 12 =====
```
     rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));
 
     for (PathValue leftPv : leftPaths) {
-      PathValue rightPv = rightMap.get(leftPv.getPath());
+      PathValue rightPv = rightMap.get(leftPv.getPath().replace(".", "_")); // Replacing dots with underscores, which will not match the original path
       DiffInfo di = comparePaths(leftPv, rightPv);
       if (onlyDifferences == true) {
         if (di.getDiffResult() != PathDiffResult.EQUAL) {
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath().replace(".", "_")); // Replacing dots with underscores, which will not match the original path
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 13 =====
```
     rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));
 
     for (PathValue leftPv : leftPaths) {
-      PathValue rightPv = rightMap.get(leftPv.getPath());
+      PathValue rightPv = rightMap.get(leftPv.getPath().substring(1)); // Removing the first character of the path, potentially causing a mismatch
       DiffInfo di = comparePaths(leftPv, rightPv);
       if (onlyDifferences == true) {
         if (di.getDiffResult() != PathDiffResult.EQUAL) {
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath().substring(1)); // Removing the first character of the path, potentially causing a mismatch
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 14 =====
```
     rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));
 
     for (PathValue leftPv : leftPaths) {
-      PathValue rightPv = rightMap.get(leftPv.getPath());
+      PathValue rightPv = rightMap.get(leftPv.getPath().toUpperCase()); // Converting the path to uppercase, which may not match
       DiffInfo di = comparePaths(leftPv, rightPv);
       if (onlyDifferences == true) {
         if (di.getDiffResult() != PathDiffResult.EQUAL) {
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath().toUpperCase()); // Converting the path to uppercase, which may not match
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 15 =====
```
 
     for (PathValue leftPv : leftPaths) {
       PathValue rightPv = rightMap.get(leftPv.getPath());
-      DiffInfo di = comparePaths(leftPv, rightPv);
+      DiffInfo di = comparePaths(leftPv, null);
       if (onlyDifferences == true) {
         if (di.getDiffResult() != PathDiffResult.EQUAL) {
           diffInfoList.add(di);
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, null);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 21 =====
```
       PathValue rightPv = rightMap.get(leftPv.getPath());
       DiffInfo di = comparePaths(leftPv, rightPv);
       if (onlyDifferences == true) {
-        if (di.getDiffResult() != PathDiffResult.EQUAL) {
+        if (di.getDiffResult() == PathDiffResult.DIFFERENT) {
           diffInfoList.add(di);
         }
       }
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() == PathDiffResult.DIFFERENT) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 23 =====
```
       PathValue rightPv = rightMap.get(leftPv.getPath());
       DiffInfo di = comparePaths(leftPv, rightPv);
       if (onlyDifferences == true) {
-        if (di.getDiffResult() != PathDiffResult.EQUAL) {
+        if (di.getDiffResult() == PathDiffResult.ONLY_IN_LEFT) {
           diffInfoList.add(di);
         }
       }
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() == PathDiffResult.ONLY_IN_LEFT) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 24 =====
```
       PathValue rightPv = rightMap.get(leftPv.getPath());
       DiffInfo di = comparePaths(leftPv, rightPv);
       if (onlyDifferences == true) {
-        if (di.getDiffResult() != PathDiffResult.EQUAL) {
+        if (di.getDiffResult() == null) {
           diffInfoList.add(di);
         }
       }
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() == null) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 25 =====
```
       DiffInfo di = comparePaths(leftPv, rightPv);
       if (onlyDifferences == true) {
         if (di.getDiffResult() != PathDiffResult.EQUAL) {
-          diffInfoList.add(di);
+          
         }
       }
       else {
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 26 =====
```
       DiffInfo di = comparePaths(leftPv, rightPv);
       if (onlyDifferences == true) {
         if (di.getDiffResult() != PathDiffResult.EQUAL) {
-          diffInfoList.add(di);
+          diffInfoList.add(null);
         }
       }
       else {
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(null);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 27 =====
```
       else {
         diffInfoList.add(di);
       }
-      rightMap.remove(leftPv.getPath());
+      
     }
 
     // now see if any right paths remain and process them if so
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 28 =====
```
       else {
         diffInfoList.add(di);
       }
-      rightMap.remove(leftPv.getPath());
+      rightMap.clear();
     }
 
     // now see if any right paths remain and process them if so
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.clear();
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 30 =====
```
       else {
         diffInfoList.add(di);
       }
-      rightMap.remove(leftPv.getPath());
+      rightMap.remove(leftPv.getPath() + "extra");
     }
 
     // now see if any right paths remain and process them if so
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath() + "extra");
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 31 =====
```
       else {
         diffInfoList.add(di);
       }
-      rightMap.remove(leftPv.getPath());
+      rightMap.remove(leftPv.getPath().toUpperCase());
     }
 
     // now see if any right paths remain and process them if so
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath().toUpperCase());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 32 =====
```
     }
 
     // now see if any right paths remain and process them if so
-    if (rightMap.size() > 0) {
+    if (rightMap.containsKey("nonexistentKey")) {
       rightPaths = rightMap.values().stream().collect(Collectors.toList());
       DiffInfo di = null;
       for (PathValue rightPv : rightPaths) {
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.containsKey("nonexistentKey")) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 33 =====
```
     }
 
     // now see if any right paths remain and process them if so
-    if (rightMap.size() > 0) {
+    if (rightMap.isEmpty()) {
       rightPaths = rightMap.values().stream().collect(Collectors.toList());
       DiffInfo di = null;
       for (PathValue rightPv : rightPaths) {
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.isEmpty()) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 34 =====
```
     }
 
     // now see if any right paths remain and process them if so
-    if (rightMap.size() > 0) {
+    if (rightMap.size() < 0) {
       rightPaths = rightMap.values().stream().collect(Collectors.toList());
       DiffInfo di = null;
       for (PathValue rightPv : rightPaths) {
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() < 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 35 =====
```
     }
 
     // now see if any right paths remain and process them if so
-    if (rightMap.size() > 0) {
+    if (rightMap.size() <= 0) {
       rightPaths = rightMap.values().stream().collect(Collectors.toList());
       DiffInfo di = null;
       for (PathValue rightPv : rightPaths) {
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() <= 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 36 =====
```
     }
 
     // now see if any right paths remain and process them if so
-    if (rightMap.size() > 0) {
+    if (rightMap.size() == 1) {
       rightPaths = rightMap.values().stream().collect(Collectors.toList());
       DiffInfo di = null;
       for (PathValue rightPv : rightPaths) {
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() == 1) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 38 =====
```
       for (PathValue rightPv : rightPaths) {
         di = comparePaths(null, rightPv);
         if (onlyDifferences == true) {
-          if (di.getDiffResult() != PathDiffResult.EQUAL) {
+          if (di.getDiffResult() != PathDiffResult.ONLY_IN_RIGHT) {
             diffInfoList.add(di);
           }
         }
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.ONLY_IN_RIGHT) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 39 =====
```
       for (PathValue rightPv : rightPaths) {
         di = comparePaths(null, rightPv);
         if (onlyDifferences == true) {
-          if (di.getDiffResult() != PathDiffResult.EQUAL) {
+          if (di.getDiffResult() == PathDiffResult.DIFFERENT) {
             diffInfoList.add(di);
           }
         }
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() == PathDiffResult.DIFFERENT) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 40 =====
```
       for (PathValue rightPv : rightPaths) {
         di = comparePaths(null, rightPv);
         if (onlyDifferences == true) {
-          if (di.getDiffResult() != PathDiffResult.EQUAL) {
+          if (di.getDiffResult() == PathDiffResult.EQUAL || di.getDiffResult() == PathDiffResult.DIFFERENT) {
             diffInfoList.add(di);
           }
         }
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() == PathDiffResult.EQUAL || di.getDiffResult() == PathDiffResult.DIFFERENT) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 41 =====
```
       for (PathValue rightPv : rightPaths) {
         di = comparePaths(null, rightPv);
         if (onlyDifferences == true) {
-          if (di.getDiffResult() != PathDiffResult.EQUAL) {
+          if (di.getDiffResult() == PathDiffResult.EQUAL) {
             diffInfoList.add(di);
           }
         }
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() == PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 42 =====
```
       for (PathValue rightPv : rightPaths) {
         di = comparePaths(null, rightPv);
         if (onlyDifferences == true) {
-          if (di.getDiffResult() != PathDiffResult.EQUAL) {
+          if (di.getDiffResult() == PathDiffResult.ONLY_IN_LEFT) {
             diffInfoList.add(di);
           }
         }
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() == PathDiffResult.ONLY_IN_LEFT) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 43 =====
```
         di = comparePaths(null, rightPv);
         if (onlyDifferences == true) {
           if (di.getDiffResult() != PathDiffResult.EQUAL) {
-            diffInfoList.add(di);
+            
           }
         }
         else {
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 44 =====
```
         di = comparePaths(null, rightPv);
         if (onlyDifferences == true) {
           if (di.getDiffResult() != PathDiffResult.EQUAL) {
-            diffInfoList.add(di);
+            diffInfoList.add(null);
           }
         }
         else {
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(null);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return diffInfoList;
  }
```
===== 45 =====
```
       }
     }
 
-    return diffInfoList;
+    return java.util.Collections.emptyList();
   }
```
```
  /**
   * Gets the differences
   *
   * @param right the right document to compare
   * @param onlyDifferences specifies if only difference results are to be returned or all
   * @return List of differences
   */
  public List<DiffInfo> getDifferences(Document right, boolean onlyDifferences) {
    List<DiffInfo> diffInfoList = new LinkedList<>();
    List<PathValue> leftPaths = flattenWithValues();
    List<PathValue> rightPaths = right.flattenWithValues();

    Map<String, PathValue> rightMap = new HashMap<>();
    rightPaths.stream().forEach(pv -> rightMap.put(pv.getPath(), pv));

    for (PathValue leftPv : leftPaths) {
      PathValue rightPv = rightMap.get(leftPv.getPath());
      DiffInfo di = comparePaths(leftPv, rightPv);
      if (onlyDifferences == true) {
        if (di.getDiffResult() != PathDiffResult.EQUAL) {
          diffInfoList.add(di);
        }
      }
      else {
        diffInfoList.add(di);
      }
      rightMap.remove(leftPv.getPath());
    }

    // now see if any right paths remain and process them if so
    if (rightMap.size() > 0) {
      rightPaths = rightMap.values().stream().collect(Collectors.toList());
      DiffInfo di = null;
      for (PathValue rightPv : rightPaths) {
        di = comparePaths(null, rightPv);
        if (onlyDifferences == true) {
          if (di.getDiffResult() != PathDiffResult.EQUAL) {
            diffInfoList.add(di);
          }
        }
        else {
          diffInfoList.add(di);
        }
      }
    }

    return java.util.Collections.emptyList();
  }
```
