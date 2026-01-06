https://github.com/logfellow/logstash-logback-encoder/blob/c2a913a5220b0b8c3623bdc357d312c3e6681894/./src/main/java/net/logstash/logback/stacktrace/ShortenedThrowableConverter.java#L412-L439
```
//@ ensures (throwableProxy == null || \old(builder.length()) > maxLength) ==> builder.length() == \old(builder.length());
//@ ensures (throwableProxy != null && \old(builder.length()) <= maxLength) ==> builder.length() >= \old(builder.length());
//@ ensures (stackHashes != null && !\old(stackHashes.isEmpty()) && throwableProxy != null && \old(builder.length()) <= maxLength) ==> stackHashes.size() <= \old(stackHashes.size());
//@ ensures builder.length() <= Math.max(\old(builder.length()), maxLength + 1);
```
```
null pointer exception

=> java.lang.NullPointerException: Cannot invoke "java.util.Deque.isEmpty()" because "<parameter5>" is null
```
jml_fail
```
//@ ensures builder.toString().startsWith(\old(builder.toString()));
//@ ensures builder.length() >= \old(builder.length());
//@ ensures (throwableProxy == null || \old(builder.length()) > maxLength) ==> builder.length() == \old(builder.length());
//@ ensures throwableProxy != null && \old(builder.length()) <= maxLength ==> builder.length() > \old(builder.length());
//@ ensures builder.length() > \old(builder.length()) ==> builder.toString().endsWith(lineSeparator);
//@ ensures throwableProxy != null && throwableProxy.getMessage() != null && \old(builder.length()) <= maxLength && builder.length() > \old(builder.length()) ==> builder.toString().contains(abbreviator.abbreviate(throwableProxy.getClassName()) + ": " + throwableProxy.getMessage());
//@ ensures throwableProxy != null && throwableProxy.getStackTraceElementProxyArray() != null && throwableProxy.getStackTraceElementProxyArray().length > 0 && \old(builder.length()) <= maxLength ==> builder.toString().contains("at " + abbreviator.abbreviate(throwableProxy.getStackTraceElementProxyArray()[0].getStackTraceElement().getClassName()) + "." + throwableProxy.getStackTraceElementProxyArray()[0].getStackTraceElement().getMethodName());
//@ ensures throwableProxy != null && throwableProxy.getSuppressed() != null && throwableProxy.getSuppressed().length > 0 && \old(builder.length()) <= maxLength ==> builder.toString().contains(CoreConstants.SUPPRESSED);
//@ ensures throwableProxy != null && throwableProxy.getSuppressed() != null && throwableProxy.getSuppressed().length > 0 && \old(builder.length()) <= maxLength ==> java.util.Arrays.stream(throwableProxy.getSuppressed()).filter(sp -> sp != null && sp.getMessage() != null).allMatch(sp -> builder.toString().contains(sp.getMessage()));
//@ ensures throwableProxy != null && throwableProxy.getCause() != null && \old(builder.length()) <= maxLength ==> builder.toString().contains(CoreConstants.CAUSED_BY);
//@ ensures throwableProxy != null && throwableProxy.getCause() != null && throwableProxy.getCause().getMessage() != null && \old(builder.length()) <= maxLength ==> builder.toString().contains(throwableProxy.getCause().getMessage());
//@ ensures \old(stackHashes == null || stackHashes.isEmpty()) ==> builder.toString().indexOf("<#") == \old(builder.toString().indexOf("<#")) && builder.toString().lastIndexOf("<#") == \old(builder.toString().lastIndexOf("<#"));
//@ ensures inlineHash && stackHasher != null && prefix == null && throwableProxy instanceof ch.qos.logback.classic.spi.ThrowableProxy && stackHasher.hexHashes(((ch.qos.logback.classic.spi.ThrowableProxy) throwableProxy).getThrowable()).size() >= 1 && \old(builder.length()) <= maxLength ==> builder.toString().contains("<#" + stackHasher.hexHashes(((ch.qos.logback.classic.spi.ThrowableProxy) throwableProxy).getThrowable()).peekFirst() + ">");
//@ ensures inlineHash && stackHasher != null && prefix == null && throwableProxy instanceof ch.qos.logback.classic.spi.ThrowableProxy && stackHasher.hexHashes(((ch.qos.logback.classic.spi.ThrowableProxy) throwableProxy).getThrowable()).size() >= 2 && \old(builder.length()) <= maxLength ==> builder.toString().indexOf("<#" + stackHasher.hexHashes(((ch.qos.logback.classic.spi.ThrowableProxy) throwableProxy).getThrowable()).peekFirst() + ">") < builder.toString().indexOf("<#" + stackHasher.hexHashes(((ch.qos.logback.classic.spi.ThrowableProxy) throwableProxy).getThrowable()).stream().skip(1).findFirst().get() + ">");
//@ ensures inlineHash && throwableProxy != null && throwableProxy.getMessage() != null && \old(builder.length()) <= maxLength ==> ( \old(stackHashes == null || stackHashes.isEmpty()) || (builder.toString().indexOf("<#" + (\old(stackHashes == null ? null : stackHashes.peekFirst())) + ">") >= 0 && builder.toString().indexOf("<#" + (\old(stackHashes == null ? null : stackHashes.peekFirst())) + ">") < builder.toString().indexOf(throwableProxy.getMessage())));

```
