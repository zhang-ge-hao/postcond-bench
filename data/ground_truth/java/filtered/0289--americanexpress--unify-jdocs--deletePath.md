https://github.com/americanexpress/unify-jdocs/blob/325af27be93ae4a1df784cf683cdff61e1bb7ac3/./src/main/java/com/americanexpress/unify/jdocs/JDocument.java#L2213-L2233
```
🈚️

originally wrong. `String... vargs`
```
```
None
```
[0, 1, 2, 3, 4, 5, 6]
===== 0 =====
```
 
     // we first check if the path exists in the document only then do we go ahead to delete it
     // we do this because pathExists handles out of bound indexes but deletePath does not
-    if (pathExists(path) == true) {
+    if (!pathExists(path)) {
       deletePath(path, tokenList);
     }
   }
```
```
  /**
   * Deletes the specified path
   *
   * @param path The path to be deleted
   * @param vargs Optional arguments for the path
   */
  @Override
  public void deletePath(String path, String... vargs) {
    path = getStaticPath(path, vargs);
    List<Token> tokenList = validatePath(path, CONSTS_JDOCS.API.DELETE_PATH, PathAccessType.OBJECT);
    if (isTyped()) {
      validateFilterNames(path, tokenList, docType);
      checkPathExistsInModel(getModelPath(path), docType);
    }

    // we first check if the path exists in the document only then do we go ahead to delete it
    // we do this because pathExists handles out of bound indexes but deletePath does not
    if (!pathExists(path)) {
      deletePath(path, tokenList);
    }
  }
```
===== 1 =====
```
 
     // we first check if the path exists in the document only then do we go ahead to delete it
     // we do this because pathExists handles out of bound indexes but deletePath does not
-    if (pathExists(path) == true) {
+    if (pathExists(path) != true) {
       deletePath(path, tokenList);
     }
   }
```
```
  /**
   * Deletes the specified path
   *
   * @param path The path to be deleted
   * @param vargs Optional arguments for the path
   */
  @Override
  public void deletePath(String path, String... vargs) {
    path = getStaticPath(path, vargs);
    List<Token> tokenList = validatePath(path, CONSTS_JDOCS.API.DELETE_PATH, PathAccessType.OBJECT);
    if (isTyped()) {
      validateFilterNames(path, tokenList, docType);
      checkPathExistsInModel(getModelPath(path), docType);
    }

    // we first check if the path exists in the document only then do we go ahead to delete it
    // we do this because pathExists handles out of bound indexes but deletePath does not
    if (pathExists(path) != true) {
      deletePath(path, tokenList);
    }
  }
```
===== 2 =====
```
 
     // we first check if the path exists in the document only then do we go ahead to delete it
     // we do this because pathExists handles out of bound indexes but deletePath does not
-    if (pathExists(path) == true) {
+    if (pathExists(path) && isTyped()) {
       deletePath(path, tokenList);
     }
   }
```
```
  /**
   * Deletes the specified path
   *
   * @param path The path to be deleted
   * @param vargs Optional arguments for the path
   */
  @Override
  public void deletePath(String path, String... vargs) {
    path = getStaticPath(path, vargs);
    List<Token> tokenList = validatePath(path, CONSTS_JDOCS.API.DELETE_PATH, PathAccessType.OBJECT);
    if (isTyped()) {
      validateFilterNames(path, tokenList, docType);
      checkPathExistsInModel(getModelPath(path), docType);
    }

    // we first check if the path exists in the document only then do we go ahead to delete it
    // we do this because pathExists handles out of bound indexes but deletePath does not
    if (pathExists(path) && isTyped()) {
      deletePath(path, tokenList);
    }
  }
```
===== 3 =====
```
 
     // we first check if the path exists in the document only then do we go ahead to delete it
     // we do this because pathExists handles out of bound indexes but deletePath does not
-    if (pathExists(path) == true) {
+    if (pathExists(path) == false) {
       deletePath(path, tokenList);
     }
   }
```
```
  /**
   * Deletes the specified path
   *
   * @param path The path to be deleted
   * @param vargs Optional arguments for the path
   */
  @Override
  public void deletePath(String path, String... vargs) {
    path = getStaticPath(path, vargs);
    List<Token> tokenList = validatePath(path, CONSTS_JDOCS.API.DELETE_PATH, PathAccessType.OBJECT);
    if (isTyped()) {
      validateFilterNames(path, tokenList, docType);
      checkPathExistsInModel(getModelPath(path), docType);
    }

    // we first check if the path exists in the document only then do we go ahead to delete it
    // we do this because pathExists handles out of bound indexes but deletePath does not
    if (pathExists(path) == false) {
      deletePath(path, tokenList);
    }
  }
```
===== 4 =====
```
     // we first check if the path exists in the document only then do we go ahead to delete it
     // we do this because pathExists handles out of bound indexes but deletePath does not
     if (pathExists(path) == true) {
-      deletePath(path, tokenList);
+      
     }
   }
```
```
  /**
   * Deletes the specified path
   *
   * @param path The path to be deleted
   * @param vargs Optional arguments for the path
   */
  @Override
  public void deletePath(String path, String... vargs) {
    path = getStaticPath(path, vargs);
    List<Token> tokenList = validatePath(path, CONSTS_JDOCS.API.DELETE_PATH, PathAccessType.OBJECT);
    if (isTyped()) {
      validateFilterNames(path, tokenList, docType);
      checkPathExistsInModel(getModelPath(path), docType);
    }

    // we first check if the path exists in the document only then do we go ahead to delete it
    // we do this because pathExists handles out of bound indexes but deletePath does not
    if (pathExists(path) == true) {
      
    }
  }
```
===== 5 =====
```
     // we first check if the path exists in the document only then do we go ahead to delete it
     // we do this because pathExists handles out of bound indexes but deletePath does not
     if (pathExists(path) == true) {
-      deletePath(path, tokenList);
+      deletePath(path, new ArrayList<>()); // passing an empty list
     }
   }
```
```
  /**
   * Deletes the specified path
   *
   * @param path The path to be deleted
   * @param vargs Optional arguments for the path
   */
  @Override
  public void deletePath(String path, String... vargs) {
    path = getStaticPath(path, vargs);
    List<Token> tokenList = validatePath(path, CONSTS_JDOCS.API.DELETE_PATH, PathAccessType.OBJECT);
    if (isTyped()) {
      validateFilterNames(path, tokenList, docType);
      checkPathExistsInModel(getModelPath(path), docType);
    }

    // we first check if the path exists in the document only then do we go ahead to delete it
    // we do this because pathExists handles out of bound indexes but deletePath does not
    if (pathExists(path) == true) {
      deletePath(path, new ArrayList<>()); // passing an empty list
    }
  }
```
===== 6 =====
```
     // we first check if the path exists in the document only then do we go ahead to delete it
     // we do this because pathExists handles out of bound indexes but deletePath does not
     if (pathExists(path) == true) {
-      deletePath(path, tokenList);
+      deletePath(path, tokenList.subList(0, tokenList.size() - 1)); // removing the last token
     }
   }
```
```
  /**
   * Deletes the specified path
   *
   * @param path The path to be deleted
   * @param vargs Optional arguments for the path
   */
  @Override
  public void deletePath(String path, String... vargs) {
    path = getStaticPath(path, vargs);
    List<Token> tokenList = validatePath(path, CONSTS_JDOCS.API.DELETE_PATH, PathAccessType.OBJECT);
    if (isTyped()) {
      validateFilterNames(path, tokenList, docType);
      checkPathExistsInModel(getModelPath(path), docType);
    }

    // we first check if the path exists in the document only then do we go ahead to delete it
    // we do this because pathExists handles out of bound indexes but deletePath does not
    if (pathExists(path) == true) {
      deletePath(path, tokenList.subList(0, tokenList.size() - 1)); // removing the last token
    }
  }
```
