https://github.com/ralscha/extdirectspring/blob/2ff60f87631de56c27badca1ff9a173990832296/./src/main/java/ch/ralscha/extdirectspring/util/ExtDirectSpringUtil.java#L67-L78
```
//@ ensures \result == (\old(request.getMethod().toLowerCase().equals("post")) && \old(request.getContentType()) != null && \old(request.getContentType().toLowerCase().startsWith("multipart/")));
//@ ensures !\old(request.getMethod().toLowerCase().equals("post")) ==> !\result;
//@ ensures \old(request.getContentType()) == null ==> !\result;
//@ ensures \old(request.getMethod().toLowerCase().equals("post")) && \old(request.getContentType()) != null && \old(request.getContentType().toLowerCase().startsWith("multipart/")) ==> \result;
```
```
null pointer exception

=> java.lang.NullPointerException: Cannot invoke "String.toLowerCase()" because the return value of "jakarta.servlet.http.HttpServletRequest.getContentType()" is null
```
failed
```
//@ ensures !request.getMethod().toLowerCase().equals("post") ==> \result == false
//@ ensures request.getMethod().toLowerCase().equals("post") && request.getContentType() != null && request.getContentType().toLowerCase().startsWith("multipart/") ==> \result == true
//@ ensures request.getMethod().toLowerCase().equals("post") && (request.getContentType() == null || !request.getContentType().toLowerCase().startsWith("multipart/")) ==> \result == false
```
