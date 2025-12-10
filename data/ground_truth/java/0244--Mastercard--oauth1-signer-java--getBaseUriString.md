https://github.com/Mastercard/oauth1-signer-java/blob/8c84f7d0309f2de6a1a93ff5933d588fd861867c/./src/main/java/com/mastercard/developer/oauth/OAuth.java#L201-L228
```
//@ ensures \result != null;
//@ ensures \result.startsWith(uri.getScheme().toLowerCase() + "://");
//@ ensures !\result.contains("#") && !\result.contains("?");
//@ ensures \result.endsWith((uri.getRawPath() == null || uri.getRawPath().length() <= 0) ? "/" : uri.getRawPath());
//@ ensures \result.equals(uri.getScheme().toLowerCase() + "://" + ((((("http".equals(uri.getScheme().toLowerCase()) && uri.getPort() == 80) || ("https".equals(uri.getScheme().toLowerCase()) && uri.getPort() == 443)) && uri.getAuthority().toLowerCase().lastIndexOf(':') >= 0) ? uri.getAuthority().toLowerCase().substring(0, uri.getAuthority().toLowerCase().lastIndexOf(':')) : uri.getAuthority().toLowerCase()) + ((uri.getRawPath() == null || uri.getRawPath().length() <= 0) ? "/" : uri.getRawPath())));
//@ ensures (("http".equals(uri.getScheme().toLowerCase()) && uri.getPort() == 80) || ("https".equals(uri.getScheme().toLowerCase()) && uri.getPort() == 443)) ==> !\result.contains(":" + Integer.toString(uri.getPort()));
//@ ensures !(("http".equals(uri.getScheme().toLowerCase()) && uri.getPort() == 80) || ("https".equals(uri.getScheme().toLowerCase()) && uri.getPort() == 443)) ==> (\result.contains(":" + Integer.toString(uri.getPort())) || uri.getPort() == -1);
```
```
//@ ensures \result != null;
//@ ensures \result.startsWith(uri.getScheme().toLowerCase() + "://");
//@ ensures !\result.contains("#") && !\result.contains("?");
//@ ensures \result.endsWith((uri.getRawPath() == null || uri.getRawPath().length() <= 0) ? "/" : uri.getRawPath());
//@ ensures (!(("http".equals(uri.getScheme().toLowerCase()) && uri.getPort() == 80) || ("https".equals(uri.getScheme().toLowerCase()) && uri.getPort() == 443))) ==> \result.equals(uri.getScheme().toLowerCase() + "://" + uri.getAuthority().toLowerCase() + ((uri.getRawPath() == null || uri.getRawPath().length() <= 0) ? "/" : uri.getRawPath()));
//@ ensures (("http".equals(uri.getScheme().toLowerCase()) && uri.getPort() == 80) || ("https".equals(uri.getScheme().toLowerCase()) && uri.getPort() == 443)) ==> ( (uri.getAuthority().toLowerCase().lastIndexOf(':') >= 0 && \result.equals(uri.getScheme().toLowerCase() + "://" + uri.getAuthority().toLowerCase().substring(0, uri.getAuthority().toLowerCase().lastIndexOf(':')) + ((uri.getRawPath() == null || uri.getRawPath().length() <= 0) ? "/" : uri.getRawPath()))) || (uri.getAuthority().toLowerCase().lastIndexOf(':') < 0 && \result.equals(uri.getScheme().toLowerCase() + "://" + uri.getAuthority().toLowerCase() + ((uri.getRawPath() == null || uri.getRawPath().length() <= 0) ? "/" : uri.getRawPath())) ) );
//@ ensures (("http".equals(uri.getScheme().toLowerCase()) && uri.getPort() == 80) || ("https".equals(uri.getScheme().toLowerCase()) && uri.getPort() == 443)) ==> !\result.contains(":" + Integer.toString(uri.getPort()));
```
[10, 11]
===== 10 =====
```
 
     // Remove port if it matches the default for scheme
     if (("http".equals(scheme) && uri.getPort() == 80)
-        || ("https".equals(scheme) && uri.getPort() == 443)) {
+        || ("ftp".equals(scheme) && uri.getPort() == 21)) {
       int index = authority.lastIndexOf(':');
       if (index >= 0) {
         authority = authority.substring(0, index);
```
```
  /**
   * Normalizes the URL as per
   * https://tools.ietf.org/html/rfc5849#section-3.4.1.2
   *
   * @param uri URL that will be called as part of this request
   * @return Normalized URL
   */
  static String getBaseUriString(URI uri) {
    // Lowercase scheme and authority
    String scheme = uri.getScheme().toLowerCase();
    String authority = uri.getAuthority().toLowerCase();

    // Remove port if it matches the default for scheme
    if (("http".equals(scheme) && uri.getPort() == 80)
        || ("ftp".equals(scheme) && uri.getPort() == 21)) {
      int index = authority.lastIndexOf(':');
      if (index >= 0) {
        authority = authority.substring(0, index);
      }
    }

    String path = uri.getRawPath();
    if (path == null || path.length() <= 0) {
      path = "/";
    }

    return scheme + "://" + authority + path;
  }
```
===== 11 =====
```
 
     // Remove port if it matches the default for scheme
     if (("http".equals(scheme) && uri.getPort() == 80)
-        || ("https".equals(scheme) && uri.getPort() == 443)) {
+        || ("http".equals(scheme) && uri.getPort() == 80)) {
       int index = authority.lastIndexOf(':');
       if (index >= 0) {
         authority = authority.substring(0, index);
```
```
  /**
   * Normalizes the URL as per
   * https://tools.ietf.org/html/rfc5849#section-3.4.1.2
   *
   * @param uri URL that will be called as part of this request
   * @return Normalized URL
   */
  static String getBaseUriString(URI uri) {
    // Lowercase scheme and authority
    String scheme = uri.getScheme().toLowerCase();
    String authority = uri.getAuthority().toLowerCase();

    // Remove port if it matches the default for scheme
    if (("http".equals(scheme) && uri.getPort() == 80)
        || ("http".equals(scheme) && uri.getPort() == 80)) {
      int index = authority.lastIndexOf(':');
      if (index >= 0) {
        authority = authority.substring(0, index);
      }
    }

    String path = uri.getRawPath();
    if (path == null || path.length() <= 0) {
      path = "/";
    }

    return scheme + "://" + authority + path;
  }
```
