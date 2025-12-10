https://github.com/logfellow/logstash-logback-encoder/blob/c2a913a5220b0b8c3623bdc357d312c3e6681894/./src/main/java/net/logstash/logback/stacktrace/ShortenedThrowableConverter.java#L412-L439
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
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
===== 0 =====
```
             IThrowableProxy throwableProxy,
             Deque<String> stackHashes) {
 
-        if (throwableProxy == null || builder.length() > this.maxLength) {
+        if (builder.length() < this.maxLength) {
             return;
         }
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (builder.length() < this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 1 =====
```
             IThrowableProxy throwableProxy,
             Deque<String> stackHashes) {
 
-        if (throwableProxy == null || builder.length() > this.maxLength) {
+        if (throwableProxy != null || builder.length() <= this.maxLength) {
             return;
         }
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy != null || builder.length() <= this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 2 =====
```
             IThrowableProxy throwableProxy,
             Deque<String> stackHashes) {
 
-        if (throwableProxy == null || builder.length() > this.maxLength) {
+        if (throwableProxy != null || builder.length() > this.maxLength) {
             return;
         }
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy != null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 3 =====
```
             IThrowableProxy throwableProxy,
             Deque<String> stackHashes) {
 
-        if (throwableProxy == null || builder.length() > this.maxLength) {
+        if (throwableProxy == null || builder.length() < this.maxLength) {
             return;
         }
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() < this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 4 =====
```
             IThrowableProxy throwableProxy,
             Deque<String> stackHashes) {
 
-        if (throwableProxy == null || builder.length() > this.maxLength) {
+        if (throwableProxy == null || builder.length() <= this.maxLength) {
             return;
         }
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() <= this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 5 =====
```
             return;
         }
 
-        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
+        String hash = stackHashes == null || stackHashes.isEmpty() ? "defaultHash" : stackHashes.removeFirst();
         appendFirstLine(builder, prefix, indent, throwableProxy, hash);
         appendStackTraceElements(builder, indent, throwableProxy);
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? "defaultHash" : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 6 =====
```
             return;
         }
 
-        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
+        String hash = stackHashes == null || stackHashes.isEmpty() ? "emptyHash" : stackHashes.removeFirst();
         appendFirstLine(builder, prefix, indent, throwableProxy, hash);
         appendStackTraceElements(builder, indent, throwableProxy);
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? "emptyHash" : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 7 =====
```
             return;
         }
 
-        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
+        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.peekFirst();
         appendFirstLine(builder, prefix, indent, throwableProxy, hash);
         appendStackTraceElements(builder, indent, throwableProxy);
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.peekFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 8 =====
```
             return;
         }
 
-        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
+        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeLast();
         appendFirstLine(builder, prefix, indent, throwableProxy, hash);
         appendStackTraceElements(builder, indent, throwableProxy);
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeLast();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 9 =====
```
         }
 
         String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
-        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
+        
         appendStackTraceElements(builder, indent, throwableProxy);
 
         IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 10 =====
```
         }
 
         String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
-        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
+        appendFirstLine(builder, prefix, indent, throwableProxy, null); // Passing null for hash instead of the computed value
         appendStackTraceElements(builder, indent, throwableProxy);
 
         IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, null); // Passing null for hash instead of the computed value
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 11 =====
```
         }
 
         String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
-        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
+        appendStackTraceElements(builder, indent, throwableProxy); // Missing the first line with prefix and hash
         appendStackTraceElements(builder, indent, throwableProxy);
 
         IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendStackTraceElements(builder, indent, throwableProxy); // Missing the first line with prefix and hash
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 12 =====
```
         }
 
         String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
-        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
+        builder.append("An error occurred: ").append(throwableProxy.getMessage()).append(getLineSeparator());
         appendStackTraceElements(builder, indent, throwableProxy);
 
         IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        builder.append("An error occurred: ").append(throwableProxy.getMessage()).append(getLineSeparator());
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 13 =====
```
         }
 
         String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
-        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
+        builder.append("Error: ").append(abbreviator.abbreviate(throwableProxy.getClassName())).append(getLineSeparator());
         appendStackTraceElements(builder, indent, throwableProxy);
 
         IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        builder.append("Error: ").append(abbreviator.abbreviate(throwableProxy.getClassName())).append(getLineSeparator());
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 14 =====
```
         }
 
         String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
-        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
+        builder.append(prefix).append(" ").append(throwableProxy.getMessage()).append(getLineSeparator()); // Missing class name abbreviation
         appendStackTraceElements(builder, indent, throwableProxy);
 
         IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        builder.append(prefix).append(" ").append(throwableProxy.getMessage()).append(getLineSeparator()); // Missing class name abbreviation
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 15 =====
```
 
         String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
         appendFirstLine(builder, prefix, indent, throwableProxy, hash);
-        appendStackTraceElements(builder, indent, throwableProxy);
+        
 
         IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
         if (suppressedThrowableProxies != null) {
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 16 =====
```
         appendFirstLine(builder, prefix, indent, throwableProxy, hash);
         appendStackTraceElements(builder, indent, throwableProxy);
 
-        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
+        IThrowableProxy[] suppressedThrowableProxies = new IThrowableProxy[0]; // Initializes with an empty array, ignoring any suppressed throwables
         if (suppressedThrowableProxies != null) {
             for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                 // stack hashes are not computed/inlined on suppressed errors
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = new IThrowableProxy[0]; // Initializes with an empty array, ignoring any suppressed throwables
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 17 =====
```
         appendFirstLine(builder, prefix, indent, throwableProxy, hash);
         appendStackTraceElements(builder, indent, throwableProxy);
 
-        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
+        IThrowableProxy[] suppressedThrowableProxies = new IThrowableProxy[1]; // Allocates an array but does not populate it, leading to potential null references
         if (suppressedThrowableProxies != null) {
             for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                 // stack hashes are not computed/inlined on suppressed errors
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = new IThrowableProxy[1]; // Allocates an array but does not populate it, leading to potential null references
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 18 =====
```
         appendFirstLine(builder, prefix, indent, throwableProxy, hash);
         appendStackTraceElements(builder, indent, throwableProxy);
 
-        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
+        IThrowableProxy[] suppressedThrowableProxies = null; // Suppresses all suppressed throwables
         if (suppressedThrowableProxies != null) {
             for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                 // stack hashes are not computed/inlined on suppressed errors
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = null; // Suppresses all suppressed throwables
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 19 =====
```
         appendStackTraceElements(builder, indent, throwableProxy);
 
         IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
-        if (suppressedThrowableProxies != null) {
+        if (suppressedThrowableProxies == null || suppressedThrowableProxies.length == 0) {
             for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                 // stack hashes are not computed/inlined on suppressed errors
                 appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies == null || suppressedThrowableProxies.length == 0) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 20 =====
```
         appendStackTraceElements(builder, indent, throwableProxy);
 
         IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
-        if (suppressedThrowableProxies != null) {
+        if (suppressedThrowableProxies == null) {
             for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                 // stack hashes are not computed/inlined on suppressed errors
                 appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies == null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 21 =====
```
 
         IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
         if (suppressedThrowableProxies != null) {
-            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
+            for (IThrowableProxy suppressedThrowableProxy : new IThrowableProxy[0]) {
                 // stack hashes are not computed/inlined on suppressed errors
                 appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
             }
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : new IThrowableProxy[0]) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 22 =====
```
         if (suppressedThrowableProxies != null) {
             for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                 // stack hashes are not computed/inlined on suppressed errors
-                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
+                
             }
         }
         appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 23 =====
```
         if (suppressedThrowableProxies != null) {
             for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                 // stack hashes are not computed/inlined on suppressed errors
-                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
+                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, null, null);
             }
         }
         appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, null, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 24 =====
```
         if (suppressedThrowableProxies != null) {
             for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                 // stack hashes are not computed/inlined on suppressed errors
-                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
+                appendRootCauseLast(builder, null, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
             }
         }
         appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, null, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
    }
```
===== 25 =====
```
                 appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
             }
         }
-        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
+        
     }
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        
    }
```
===== 26 =====
```
                 appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
             }
         }
-        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
+        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), null);
     }
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), null);
    }
```
===== 27 =====
```
                 appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
             }
         }
-        appendRootCauseLast(builder, CoreConstants.CAUSED_BY, indent, throwableProxy.getCause(), stackHashes);
+        appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent, throwableProxy.getCause(), stackHashes);
     }
```
```
    /**
     * Appends a throwable and recursively appends its causedby/suppressed throwables
     * in "normal" order (Root cause last).
     */
    private void appendRootCauseLast(
            StringBuilder builder,
            String prefix,
            int indent,
            IThrowableProxy throwableProxy,
            Deque<String> stackHashes) {

        if (throwableProxy == null || builder.length() > this.maxLength) {
            return;
        }

        String hash = stackHashes == null || stackHashes.isEmpty() ? null : stackHashes.removeFirst();
        appendFirstLine(builder, prefix, indent, throwableProxy, hash);
        appendStackTraceElements(builder, indent, throwableProxy);

        IThrowableProxy[] suppressedThrowableProxies = throwableProxy.getSuppressed();
        if (suppressedThrowableProxies != null) {
            for (IThrowableProxy suppressedThrowableProxy : suppressedThrowableProxies) {
                // stack hashes are not computed/inlined on suppressed errors
                appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent + ThrowableProxyUtil.SUPPRESSED_EXCEPTION_INDENT, suppressedThrowableProxy, null);
            }
        }
        appendRootCauseLast(builder, CoreConstants.SUPPRESSED, indent, throwableProxy.getCause(), stackHashes);
    }
```
