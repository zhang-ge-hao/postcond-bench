https://github.com/logfellow/logstash-logback-encoder/blob/c2a913a5220b0b8c3623bdc357d312c3e6681894/./src/main/java/net/logstash/logback/stacktrace/ShortenedThrowableConverter.java#L652-L666
```
//@ ensures \result == (step.getClassPackagingData() != null && (previousStep == null || previousStep.getClassPackagingData() == null || !step.getClassPackagingData().equals(previousStep.getClassPackagingData())));
```
```
//@ ensures \result == (step.getClassPackagingData() != null && (previousStep == null || previousStep.getClassPackagingData() == null || !step.getClassPackagingData().equals(previousStep.getClassPackagingData())));
```
[7]
===== 7 =====
```
         if (previousStep == null || previousStep.getClassPackagingData() == null) {
             return true;
         }
-        return !step.getClassPackagingData().equals(previousStep.getClassPackagingData());
+        return step.getClassPackagingData().hashCode() != previousStep.getClassPackagingData().hashCode();
     }
```
```
    /**
     * Return true if packaging data should be appended for the current step.
     *
     * Packaging data for the current step is only appended if it differs
     * from the packaging data from the previous step.
     */
    private boolean shouldAppendPackagingData(StackTraceElementProxy step, StackTraceElementProxy previousStep) {
        if (step.getClassPackagingData() == null) {
            return false;
        }
        if (previousStep == null || previousStep.getClassPackagingData() == null) {
            return true;
        }
        return step.getClassPackagingData().hashCode() != previousStep.getClassPackagingData().hashCode();
    }
```
