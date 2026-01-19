https://github.com/glytching/junit-extensions/blob/5c498fd7a7a628e4d5f1c272c6bda24c8669d470/./src/main/java/io/github/glytching/junit/extension/system/SystemPropertyExtension.java#L162-L188
```
🈚️

No API.

//@ ensures java.util.Arrays.stream(extensionContext.getRequiredTestMethod().getAnnotationsByType(SystemProperty.class)).allMatch(sp -> java.util.Objects.equals(System.getProperty(sp.name()), sp.value()));
//@ ensures extensionContext.getRequiredTestMethod().getAnnotationsByType(SystemProperty.class).length == 0 ==> getStore(extensionContext, this.getClass()).get(KEY) == \old(getStore(extensionContext, this.getClass()).get(KEY));
//@ ensures extensionContext.getRequiredTestMethod().getAnnotationsByType(SystemProperty.class).length > 0 ==> getStore(extensionContext, this.getClass()).get(KEY) != null;
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
===== 0 =====
```
   public void beforeEach(ExtensionContext extensionContext) throws Exception {
     List<SystemProperty> systemProperties =
         getSystemProperties(extensionContext.getRequiredTestMethod());
-    if (!systemProperties.isEmpty()) {
+    if (systemProperties.contains(null)) {
       RestoreContext.Builder builder = RestoreContext.createBuilder();
       for (SystemProperty systemProperty : systemProperties) {
         builder.addPropertyName(systemProperty.name());
```
```
  /**
   * If the current test method has a system property annotation(s) then create a {@link
   * RestoreContext} representing the annotation(s). This causes the requested system properties to
   * be set and retains a copy of pre-set values for reinstatement after test execution.
   *
   * @param extensionContext the <em>context</em> in which the current test or container is being
   *     executed
   * @throws Exception
   */
  @Override
  public void beforeEach(ExtensionContext extensionContext) throws Exception {
    List<SystemProperty> systemProperties =
        getSystemProperties(extensionContext.getRequiredTestMethod());
    if (systemProperties.contains(null)) {
      RestoreContext.Builder builder = RestoreContext.createBuilder();
      for (SystemProperty systemProperty : systemProperties) {
        builder.addPropertyName(systemProperty.name());
        if (System.getProperty(systemProperty.name()) != null) {
          builder.addRestoreProperty(
              systemProperty.name(), System.getProperty(systemProperty.name()));
        }

        set(systemProperty);
      }
      writeRestoreContext(extensionContext, builder.build());
    }
  }
```
===== 1 =====
```
   public void beforeEach(ExtensionContext extensionContext) throws Exception {
     List<SystemProperty> systemProperties =
         getSystemProperties(extensionContext.getRequiredTestMethod());
-    if (!systemProperties.isEmpty()) {
+    if (systemProperties.isEmpty()) {
       RestoreContext.Builder builder = RestoreContext.createBuilder();
       for (SystemProperty systemProperty : systemProperties) {
         builder.addPropertyName(systemProperty.name());
```
```
  /**
   * If the current test method has a system property annotation(s) then create a {@link
   * RestoreContext} representing the annotation(s). This causes the requested system properties to
   * be set and retains a copy of pre-set values for reinstatement after test execution.
   *
   * @param extensionContext the <em>context</em> in which the current test or container is being
   *     executed
   * @throws Exception
   */
  @Override
  public void beforeEach(ExtensionContext extensionContext) throws Exception {
    List<SystemProperty> systemProperties =
        getSystemProperties(extensionContext.getRequiredTestMethod());
    if (systemProperties.isEmpty()) {
      RestoreContext.Builder builder = RestoreContext.createBuilder();
      for (SystemProperty systemProperty : systemProperties) {
        builder.addPropertyName(systemProperty.name());
        if (System.getProperty(systemProperty.name()) != null) {
          builder.addRestoreProperty(
              systemProperty.name(), System.getProperty(systemProperty.name()));
        }

        set(systemProperty);
      }
      writeRestoreContext(extensionContext, builder.build());
    }
  }
```
===== 2 =====
```
   public void beforeEach(ExtensionContext extensionContext) throws Exception {
     List<SystemProperty> systemProperties =
         getSystemProperties(extensionContext.getRequiredTestMethod());
-    if (!systemProperties.isEmpty()) {
+    if (systemProperties.size() < 1) {
       RestoreContext.Builder builder = RestoreContext.createBuilder();
       for (SystemProperty systemProperty : systemProperties) {
         builder.addPropertyName(systemProperty.name());
```
```
  /**
   * If the current test method has a system property annotation(s) then create a {@link
   * RestoreContext} representing the annotation(s). This causes the requested system properties to
   * be set and retains a copy of pre-set values for reinstatement after test execution.
   *
   * @param extensionContext the <em>context</em> in which the current test or container is being
   *     executed
   * @throws Exception
   */
  @Override
  public void beforeEach(ExtensionContext extensionContext) throws Exception {
    List<SystemProperty> systemProperties =
        getSystemProperties(extensionContext.getRequiredTestMethod());
    if (systemProperties.size() < 1) {
      RestoreContext.Builder builder = RestoreContext.createBuilder();
      for (SystemProperty systemProperty : systemProperties) {
        builder.addPropertyName(systemProperty.name());
        if (System.getProperty(systemProperty.name()) != null) {
          builder.addRestoreProperty(
              systemProperty.name(), System.getProperty(systemProperty.name()));
        }

        set(systemProperty);
      }
      writeRestoreContext(extensionContext, builder.build());
    }
  }
```
===== 3 =====
```
   public void beforeEach(ExtensionContext extensionContext) throws Exception {
     List<SystemProperty> systemProperties =
         getSystemProperties(extensionContext.getRequiredTestMethod());
-    if (!systemProperties.isEmpty()) {
+    if (systemProperties.size() == 0) {
       RestoreContext.Builder builder = RestoreContext.createBuilder();
       for (SystemProperty systemProperty : systemProperties) {
         builder.addPropertyName(systemProperty.name());
```
```
  /**
   * If the current test method has a system property annotation(s) then create a {@link
   * RestoreContext} representing the annotation(s). This causes the requested system properties to
   * be set and retains a copy of pre-set values for reinstatement after test execution.
   *
   * @param extensionContext the <em>context</em> in which the current test or container is being
   *     executed
   * @throws Exception
   */
  @Override
  public void beforeEach(ExtensionContext extensionContext) throws Exception {
    List<SystemProperty> systemProperties =
        getSystemProperties(extensionContext.getRequiredTestMethod());
    if (systemProperties.size() == 0) {
      RestoreContext.Builder builder = RestoreContext.createBuilder();
      for (SystemProperty systemProperty : systemProperties) {
        builder.addPropertyName(systemProperty.name());
        if (System.getProperty(systemProperty.name()) != null) {
          builder.addRestoreProperty(
              systemProperty.name(), System.getProperty(systemProperty.name()));
        }

        set(systemProperty);
      }
      writeRestoreContext(extensionContext, builder.build());
    }
  }
```
===== 4 =====
```
   public void beforeEach(ExtensionContext extensionContext) throws Exception {
     List<SystemProperty> systemProperties =
         getSystemProperties(extensionContext.getRequiredTestMethod());
-    if (!systemProperties.isEmpty()) {
+    if (systemProperties.size() > 1) {
       RestoreContext.Builder builder = RestoreContext.createBuilder();
       for (SystemProperty systemProperty : systemProperties) {
         builder.addPropertyName(systemProperty.name());
```
```
  /**
   * If the current test method has a system property annotation(s) then create a {@link
   * RestoreContext} representing the annotation(s). This causes the requested system properties to
   * be set and retains a copy of pre-set values for reinstatement after test execution.
   *
   * @param extensionContext the <em>context</em> in which the current test or container is being
   *     executed
   * @throws Exception
   */
  @Override
  public void beforeEach(ExtensionContext extensionContext) throws Exception {
    List<SystemProperty> systemProperties =
        getSystemProperties(extensionContext.getRequiredTestMethod());
    if (systemProperties.size() > 1) {
      RestoreContext.Builder builder = RestoreContext.createBuilder();
      for (SystemProperty systemProperty : systemProperties) {
        builder.addPropertyName(systemProperty.name());
        if (System.getProperty(systemProperty.name()) != null) {
          builder.addRestoreProperty(
              systemProperty.name(), System.getProperty(systemProperty.name()));
        }

        set(systemProperty);
      }
      writeRestoreContext(extensionContext, builder.build());
    }
  }
```
===== 5 =====
```
       RestoreContext.Builder builder = RestoreContext.createBuilder();
       for (SystemProperty systemProperty : systemProperties) {
         builder.addPropertyName(systemProperty.name());
-        if (System.getProperty(systemProperty.name()) != null) {
+        if (System.getProperty(systemProperty.name()) == null) {
           builder.addRestoreProperty(
               systemProperty.name(), System.getProperty(systemProperty.name()));
         }
```
```
  /**
   * If the current test method has a system property annotation(s) then create a {@link
   * RestoreContext} representing the annotation(s). This causes the requested system properties to
   * be set and retains a copy of pre-set values for reinstatement after test execution.
   *
   * @param extensionContext the <em>context</em> in which the current test or container is being
   *     executed
   * @throws Exception
   */
  @Override
  public void beforeEach(ExtensionContext extensionContext) throws Exception {
    List<SystemProperty> systemProperties =
        getSystemProperties(extensionContext.getRequiredTestMethod());
    if (!systemProperties.isEmpty()) {
      RestoreContext.Builder builder = RestoreContext.createBuilder();
      for (SystemProperty systemProperty : systemProperties) {
        builder.addPropertyName(systemProperty.name());
        if (System.getProperty(systemProperty.name()) == null) {
          builder.addRestoreProperty(
              systemProperty.name(), System.getProperty(systemProperty.name()));
        }

        set(systemProperty);
      }
      writeRestoreContext(extensionContext, builder.build());
    }
  }
```
===== 6 =====
```
               systemProperty.name(), System.getProperty(systemProperty.name()));
         }
 
-        set(systemProperty);
+        
       }
       writeRestoreContext(extensionContext, builder.build());
     }
```
```
  /**
   * If the current test method has a system property annotation(s) then create a {@link
   * RestoreContext} representing the annotation(s). This causes the requested system properties to
   * be set and retains a copy of pre-set values for reinstatement after test execution.
   *
   * @param extensionContext the <em>context</em> in which the current test or container is being
   *     executed
   * @throws Exception
   */
  @Override
  public void beforeEach(ExtensionContext extensionContext) throws Exception {
    List<SystemProperty> systemProperties =
        getSystemProperties(extensionContext.getRequiredTestMethod());
    if (!systemProperties.isEmpty()) {
      RestoreContext.Builder builder = RestoreContext.createBuilder();
      for (SystemProperty systemProperty : systemProperties) {
        builder.addPropertyName(systemProperty.name());
        if (System.getProperty(systemProperty.name()) != null) {
          builder.addRestoreProperty(
              systemProperty.name(), System.getProperty(systemProperty.name()));
        }

        
      }
      writeRestoreContext(extensionContext, builder.build());
    }
  }
```
===== 7 =====
```
               systemProperty.name(), System.getProperty(systemProperty.name()));
         }
 
-        set(systemProperty);
+        System.clearProperty(systemProperty.name());
       }
       writeRestoreContext(extensionContext, builder.build());
     }
```
```
  /**
   * If the current test method has a system property annotation(s) then create a {@link
   * RestoreContext} representing the annotation(s). This causes the requested system properties to
   * be set and retains a copy of pre-set values for reinstatement after test execution.
   *
   * @param extensionContext the <em>context</em> in which the current test or container is being
   *     executed
   * @throws Exception
   */
  @Override
  public void beforeEach(ExtensionContext extensionContext) throws Exception {
    List<SystemProperty> systemProperties =
        getSystemProperties(extensionContext.getRequiredTestMethod());
    if (!systemProperties.isEmpty()) {
      RestoreContext.Builder builder = RestoreContext.createBuilder();
      for (SystemProperty systemProperty : systemProperties) {
        builder.addPropertyName(systemProperty.name());
        if (System.getProperty(systemProperty.name()) != null) {
          builder.addRestoreProperty(
              systemProperty.name(), System.getProperty(systemProperty.name()));
        }

        System.clearProperty(systemProperty.name());
      }
      writeRestoreContext(extensionContext, builder.build());
    }
  }
```
===== 8 =====
```
               systemProperty.name(), System.getProperty(systemProperty.name()));
         }
 
-        set(systemProperty);
+        System.setProperty(systemProperty.name(), ""); // Setting to an empty string
       }
       writeRestoreContext(extensionContext, builder.build());
     }
```
```
  /**
   * If the current test method has a system property annotation(s) then create a {@link
   * RestoreContext} representing the annotation(s). This causes the requested system properties to
   * be set and retains a copy of pre-set values for reinstatement after test execution.
   *
   * @param extensionContext the <em>context</em> in which the current test or container is being
   *     executed
   * @throws Exception
   */
  @Override
  public void beforeEach(ExtensionContext extensionContext) throws Exception {
    List<SystemProperty> systemProperties =
        getSystemProperties(extensionContext.getRequiredTestMethod());
    if (!systemProperties.isEmpty()) {
      RestoreContext.Builder builder = RestoreContext.createBuilder();
      for (SystemProperty systemProperty : systemProperties) {
        builder.addPropertyName(systemProperty.name());
        if (System.getProperty(systemProperty.name()) != null) {
          builder.addRestoreProperty(
              systemProperty.name(), System.getProperty(systemProperty.name()));
        }

        System.setProperty(systemProperty.name(), ""); // Setting to an empty string
      }
      writeRestoreContext(extensionContext, builder.build());
    }
  }
```
===== 9 =====
```
               systemProperty.name(), System.getProperty(systemProperty.name()));
         }
 
-        set(systemProperty);
+        System.setProperty(systemProperty.name(), "defaultValue");
       }
       writeRestoreContext(extensionContext, builder.build());
     }
```
```
  /**
   * If the current test method has a system property annotation(s) then create a {@link
   * RestoreContext} representing the annotation(s). This causes the requested system properties to
   * be set and retains a copy of pre-set values for reinstatement after test execution.
   *
   * @param extensionContext the <em>context</em> in which the current test or container is being
   *     executed
   * @throws Exception
   */
  @Override
  public void beforeEach(ExtensionContext extensionContext) throws Exception {
    List<SystemProperty> systemProperties =
        getSystemProperties(extensionContext.getRequiredTestMethod());
    if (!systemProperties.isEmpty()) {
      RestoreContext.Builder builder = RestoreContext.createBuilder();
      for (SystemProperty systemProperty : systemProperties) {
        builder.addPropertyName(systemProperty.name());
        if (System.getProperty(systemProperty.name()) != null) {
          builder.addRestoreProperty(
              systemProperty.name(), System.getProperty(systemProperty.name()));
        }

        System.setProperty(systemProperty.name(), "defaultValue");
      }
      writeRestoreContext(extensionContext, builder.build());
    }
  }
```
===== 10 =====
```
               systemProperty.name(), System.getProperty(systemProperty.name()));
         }
 
-        set(systemProperty);
+        System.setProperty(systemProperty.name(), System.getProperty(systemProperty.name()) + "modified");
       }
       writeRestoreContext(extensionContext, builder.build());
     }
```
```
  /**
   * If the current test method has a system property annotation(s) then create a {@link
   * RestoreContext} representing the annotation(s). This causes the requested system properties to
   * be set and retains a copy of pre-set values for reinstatement after test execution.
   *
   * @param extensionContext the <em>context</em> in which the current test or container is being
   *     executed
   * @throws Exception
   */
  @Override
  public void beforeEach(ExtensionContext extensionContext) throws Exception {
    List<SystemProperty> systemProperties =
        getSystemProperties(extensionContext.getRequiredTestMethod());
    if (!systemProperties.isEmpty()) {
      RestoreContext.Builder builder = RestoreContext.createBuilder();
      for (SystemProperty systemProperty : systemProperties) {
        builder.addPropertyName(systemProperty.name());
        if (System.getProperty(systemProperty.name()) != null) {
          builder.addRestoreProperty(
              systemProperty.name(), System.getProperty(systemProperty.name()));
        }

        System.setProperty(systemProperty.name(), System.getProperty(systemProperty.name()) + "modified");
      }
      writeRestoreContext(extensionContext, builder.build());
    }
  }
```
