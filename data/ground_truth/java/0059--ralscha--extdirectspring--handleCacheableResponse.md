https://github.com/ralscha/extdirectspring/blob/2ff60f87631de56c27badca1ff9a173990832296/./src/main/java/ch/ralscha/extdirectspring/util/ExtDirectSpringUtil.java#L155-L186
```
//@ ensures response.getHeader("ETag") != null && response.getHeader("ETag").equals("\"0" + DigestUtils.md5DigestAsHex(data) + "\"");
//@ ensures response.getHeader("Cache-Control") != null && response.getHeader("Cache-Control").equals("public, max-age=" + (6L * 30L * 24L * 60L * 60L));
//@ ensures (request.getHeader("If-None-Match") != null && request.getHeader("If-None-Match").equals("\"0" + DigestUtils.md5DigestAsHex(data) + "\"")) ==> (response.getStatus() == HttpServletResponse.SC_NOT_MODIFIED && (!(response instanceof org.springframework.mock.web.MockHttpServletResponse) || ((org.springframework.mock.web.MockHttpServletResponse)response).getContentAsByteArray().length == 0));
//@ ensures !(request.getHeader("If-None-Match") != null && request.getHeader("If-None-Match").equals("\"0" + DigestUtils.md5DigestAsHex(data) + "\"")) ==> (response.getStatus() != HttpServletResponse.SC_NOT_MODIFIED && response.getContentType() == contentType && (!(response instanceof org.springframework.mock.web.MockHttpServletResponse) || java.util.Arrays.equals(((org.springframework.mock.web.MockHttpServletResponse)response).getContentAsByteArray(), data)));
//@ ensures !(request.getHeader("If-None-Match") != null && request.getHeader("If-None-Match").equals("\"0" + DigestUtils.md5DigestAsHex(data) + "\"")) ==> (!(response instanceof org.springframework.mock.web.MockHttpServletResponse) || ((org.springframework.mock.web.MockHttpServletResponse)response).getContentLength() == data.length);
```
```
//@ ensures response.getHeader("ETag") != null && response.getHeader("ETag").equals("\"0" + DigestUtils.md5DigestAsHex(data) + "\"");
//@ ensures (request.getHeader("If-None-Match") != null && request.getHeader("If-None-Match").equals("\"0" + DigestUtils.md5DigestAsHex(data) + "\"")) ==> (response.getStatus() == HttpServletResponse.SC_NOT_MODIFIED && ( !(response instanceof org.springframework.mock.web.MockHttpServletResponse) || ((org.springframework.mock.web.MockHttpServletResponse)response).getContentAsByteArray().length == 0 ) );
//@ ensures !(request.getHeader("If-None-Match") != null && request.getHeader("If-None-Match").equals("\"0" + DigestUtils.md5DigestAsHex(data) + "\"")) ==> (response.getStatus() != HttpServletResponse.SC_NOT_MODIFIED && response.getContentType() == contentType && ( !(response instanceof org.springframework.mock.web.MockHttpServletResponse) || java.util.Arrays.equals(((org.springframework.mock.web.MockHttpServletResponse)response).getContentAsByteArray(), data) ));
```
[7, 8, 9, 23, 24, 25, 26, 27]
===== 7 =====
```
 		String ifNoneMatch = request.getHeader("If-None-Match");
 		String etag = "\"0" + DigestUtils.md5DigestAsHex(data) + "\"";
 
-		addCacheHeaders(response, etag, 6);
+		addCacheHeaders(response, etag, -1); // Passing a negative month value, which is invalid
 
 		if (etag.equals(ifNoneMatch)) {
 			response.setStatus(HttpServletResponse.SC_NOT_MODIFIED);
```
```
	/**
	 * Checks etag and sends back HTTP status 304 if not modified. If modified sets
	 * content type and content length, adds cache headers (
	 * {@link #addCacheHeaders(HttpServletResponse, String, Integer)}), writes the data
	 * into the {@link HttpServletResponse#getOutputStream()} and flushes it.
	 * @param request the HTTP servlet request
	 * @param response the HTTP servlet response
	 * @param data the response data
	 * @param contentType the content type of the data (i.e.
	 * "application/javascript;charset=utf-8")
	 * @throws IOException
	 */
	public static void handleCacheableResponse(HttpServletRequest request, HttpServletResponse response, byte[] data,
			String contentType) throws IOException {
		String ifNoneMatch = request.getHeader("If-None-Match");
		String etag = "\"0" + DigestUtils.md5DigestAsHex(data) + "\"";

		addCacheHeaders(response, etag, -1); // Passing a negative month value, which is invalid

		if (etag.equals(ifNoneMatch)) {
			response.setStatus(HttpServletResponse.SC_NOT_MODIFIED);
			return;
		}

		response.setContentType(contentType);
		response.setContentLength(data.length);

		@SuppressWarnings("resource")
		ServletOutputStream out = response.getOutputStream();
		out.write(data);
		out.flush();
	}
```
===== 8 =====
```
 		String ifNoneMatch = request.getHeader("If-None-Match");
 		String etag = "\"0" + DigestUtils.md5DigestAsHex(data) + "\"";
 
-		addCacheHeaders(response, etag, 6);
+		addCacheHeaders(response, etag, 0); // Passing 0 months, which may lead to unexpected caching behavior
 
 		if (etag.equals(ifNoneMatch)) {
 			response.setStatus(HttpServletResponse.SC_NOT_MODIFIED);
```
```
	/**
	 * Checks etag and sends back HTTP status 304 if not modified. If modified sets
	 * content type and content length, adds cache headers (
	 * {@link #addCacheHeaders(HttpServletResponse, String, Integer)}), writes the data
	 * into the {@link HttpServletResponse#getOutputStream()} and flushes it.
	 * @param request the HTTP servlet request
	 * @param response the HTTP servlet response
	 * @param data the response data
	 * @param contentType the content type of the data (i.e.
	 * "application/javascript;charset=utf-8")
	 * @throws IOException
	 */
	public static void handleCacheableResponse(HttpServletRequest request, HttpServletResponse response, byte[] data,
			String contentType) throws IOException {
		String ifNoneMatch = request.getHeader("If-None-Match");
		String etag = "\"0" + DigestUtils.md5DigestAsHex(data) + "\"";

		addCacheHeaders(response, etag, 0); // Passing 0 months, which may lead to unexpected caching behavior

		if (etag.equals(ifNoneMatch)) {
			response.setStatus(HttpServletResponse.SC_NOT_MODIFIED);
			return;
		}

		response.setContentType(contentType);
		response.setContentLength(data.length);

		@SuppressWarnings("resource")
		ServletOutputStream out = response.getOutputStream();
		out.write(data);
		out.flush();
	}
```
===== 9 =====
```
 		String ifNoneMatch = request.getHeader("If-None-Match");
 		String etag = "\"0" + DigestUtils.md5DigestAsHex(data) + "\"";
 
-		addCacheHeaders(response, etag, 6);
+		addCacheHeaders(response, etag, 12); // Passing 12 months, which could lead to overly long caching
 
 		if (etag.equals(ifNoneMatch)) {
 			response.setStatus(HttpServletResponse.SC_NOT_MODIFIED);
```
```
	/**
	 * Checks etag and sends back HTTP status 304 if not modified. If modified sets
	 * content type and content length, adds cache headers (
	 * {@link #addCacheHeaders(HttpServletResponse, String, Integer)}), writes the data
	 * into the {@link HttpServletResponse#getOutputStream()} and flushes it.
	 * @param request the HTTP servlet request
	 * @param response the HTTP servlet response
	 * @param data the response data
	 * @param contentType the content type of the data (i.e.
	 * "application/javascript;charset=utf-8")
	 * @throws IOException
	 */
	public static void handleCacheableResponse(HttpServletRequest request, HttpServletResponse response, byte[] data,
			String contentType) throws IOException {
		String ifNoneMatch = request.getHeader("If-None-Match");
		String etag = "\"0" + DigestUtils.md5DigestAsHex(data) + "\"";

		addCacheHeaders(response, etag, 12); // Passing 12 months, which could lead to overly long caching

		if (etag.equals(ifNoneMatch)) {
			response.setStatus(HttpServletResponse.SC_NOT_MODIFIED);
			return;
		}

		response.setContentType(contentType);
		response.setContentLength(data.length);

		@SuppressWarnings("resource")
		ServletOutputStream out = response.getOutputStream();
		out.write(data);
		out.flush();
	}
```
===== 23 =====
```
 		}
 
 		response.setContentType(contentType);
-		response.setContentLength(data.length);
+		
 
 		@SuppressWarnings("resource")
 		ServletOutputStream out = response.getOutputStream();
```
```
	/**
	 * Checks etag and sends back HTTP status 304 if not modified. If modified sets
	 * content type and content length, adds cache headers (
	 * {@link #addCacheHeaders(HttpServletResponse, String, Integer)}), writes the data
	 * into the {@link HttpServletResponse#getOutputStream()} and flushes it.
	 * @param request the HTTP servlet request
	 * @param response the HTTP servlet response
	 * @param data the response data
	 * @param contentType the content type of the data (i.e.
	 * "application/javascript;charset=utf-8")
	 * @throws IOException
	 */
	public static void handleCacheableResponse(HttpServletRequest request, HttpServletResponse response, byte[] data,
			String contentType) throws IOException {
		String ifNoneMatch = request.getHeader("If-None-Match");
		String etag = "\"0" + DigestUtils.md5DigestAsHex(data) + "\"";

		addCacheHeaders(response, etag, 6);

		if (etag.equals(ifNoneMatch)) {
			response.setStatus(HttpServletResponse.SC_NOT_MODIFIED);
			return;
		}

		response.setContentType(contentType);
		

		@SuppressWarnings("resource")
		ServletOutputStream out = response.getOutputStream();
		out.write(data);
		out.flush();
	}
```
===== 24 =====
```
 		}
 
 		response.setContentType(contentType);
-		response.setContentLength(data.length);
+		response.setContentLength(-1); // Sets content length to an invalid negative value
 
 		@SuppressWarnings("resource")
 		ServletOutputStream out = response.getOutputStream();
```
```
	/**
	 * Checks etag and sends back HTTP status 304 if not modified. If modified sets
	 * content type and content length, adds cache headers (
	 * {@link #addCacheHeaders(HttpServletResponse, String, Integer)}), writes the data
	 * into the {@link HttpServletResponse#getOutputStream()} and flushes it.
	 * @param request the HTTP servlet request
	 * @param response the HTTP servlet response
	 * @param data the response data
	 * @param contentType the content type of the data (i.e.
	 * "application/javascript;charset=utf-8")
	 * @throws IOException
	 */
	public static void handleCacheableResponse(HttpServletRequest request, HttpServletResponse response, byte[] data,
			String contentType) throws IOException {
		String ifNoneMatch = request.getHeader("If-None-Match");
		String etag = "\"0" + DigestUtils.md5DigestAsHex(data) + "\"";

		addCacheHeaders(response, etag, 6);

		if (etag.equals(ifNoneMatch)) {
			response.setStatus(HttpServletResponse.SC_NOT_MODIFIED);
			return;
		}

		response.setContentType(contentType);
		response.setContentLength(-1); // Sets content length to an invalid negative value

		@SuppressWarnings("resource")
		ServletOutputStream out = response.getOutputStream();
		out.write(data);
		out.flush();
	}
```
===== 25 =====
```
 		}
 
 		response.setContentType(contentType);
-		response.setContentLength(data.length);
+		response.setContentLength(0); // Sets content length to 0, indicating no content
 
 		@SuppressWarnings("resource")
 		ServletOutputStream out = response.getOutputStream();
```
```
	/**
	 * Checks etag and sends back HTTP status 304 if not modified. If modified sets
	 * content type and content length, adds cache headers (
	 * {@link #addCacheHeaders(HttpServletResponse, String, Integer)}), writes the data
	 * into the {@link HttpServletResponse#getOutputStream()} and flushes it.
	 * @param request the HTTP servlet request
	 * @param response the HTTP servlet response
	 * @param data the response data
	 * @param contentType the content type of the data (i.e.
	 * "application/javascript;charset=utf-8")
	 * @throws IOException
	 */
	public static void handleCacheableResponse(HttpServletRequest request, HttpServletResponse response, byte[] data,
			String contentType) throws IOException {
		String ifNoneMatch = request.getHeader("If-None-Match");
		String etag = "\"0" + DigestUtils.md5DigestAsHex(data) + "\"";

		addCacheHeaders(response, etag, 6);

		if (etag.equals(ifNoneMatch)) {
			response.setStatus(HttpServletResponse.SC_NOT_MODIFIED);
			return;
		}

		response.setContentType(contentType);
		response.setContentLength(0); // Sets content length to 0, indicating no content

		@SuppressWarnings("resource")
		ServletOutputStream out = response.getOutputStream();
		out.write(data);
		out.flush();
	}
```
===== 26 =====
```
 		}
 
 		response.setContentType(contentType);
-		response.setContentLength(data.length);
+		response.setContentLength(data.length + 100); // Incorrectly adds 100 to the content length
 
 		@SuppressWarnings("resource")
 		ServletOutputStream out = response.getOutputStream();
```
```
	/**
	 * Checks etag and sends back HTTP status 304 if not modified. If modified sets
	 * content type and content length, adds cache headers (
	 * {@link #addCacheHeaders(HttpServletResponse, String, Integer)}), writes the data
	 * into the {@link HttpServletResponse#getOutputStream()} and flushes it.
	 * @param request the HTTP servlet request
	 * @param response the HTTP servlet response
	 * @param data the response data
	 * @param contentType the content type of the data (i.e.
	 * "application/javascript;charset=utf-8")
	 * @throws IOException
	 */
	public static void handleCacheableResponse(HttpServletRequest request, HttpServletResponse response, byte[] data,
			String contentType) throws IOException {
		String ifNoneMatch = request.getHeader("If-None-Match");
		String etag = "\"0" + DigestUtils.md5DigestAsHex(data) + "\"";

		addCacheHeaders(response, etag, 6);

		if (etag.equals(ifNoneMatch)) {
			response.setStatus(HttpServletResponse.SC_NOT_MODIFIED);
			return;
		}

		response.setContentType(contentType);
		response.setContentLength(data.length + 100); // Incorrectly adds 100 to the content length

		@SuppressWarnings("resource")
		ServletOutputStream out = response.getOutputStream();
		out.write(data);
		out.flush();
	}
```
===== 27 =====
```
 		}
 
 		response.setContentType(contentType);
-		response.setContentLength(data.length);
+		response.setContentLength(data.length / 2); // Incorrectly sets content length to half of the actual length
 
 		@SuppressWarnings("resource")
 		ServletOutputStream out = response.getOutputStream();
```
```
	/**
	 * Checks etag and sends back HTTP status 304 if not modified. If modified sets
	 * content type and content length, adds cache headers (
	 * {@link #addCacheHeaders(HttpServletResponse, String, Integer)}), writes the data
	 * into the {@link HttpServletResponse#getOutputStream()} and flushes it.
	 * @param request the HTTP servlet request
	 * @param response the HTTP servlet response
	 * @param data the response data
	 * @param contentType the content type of the data (i.e.
	 * "application/javascript;charset=utf-8")
	 * @throws IOException
	 */
	public static void handleCacheableResponse(HttpServletRequest request, HttpServletResponse response, byte[] data,
			String contentType) throws IOException {
		String ifNoneMatch = request.getHeader("If-None-Match");
		String etag = "\"0" + DigestUtils.md5DigestAsHex(data) + "\"";

		addCacheHeaders(response, etag, 6);

		if (etag.equals(ifNoneMatch)) {
			response.setStatus(HttpServletResponse.SC_NOT_MODIFIED);
			return;
		}

		response.setContentType(contentType);
		response.setContentLength(data.length / 2); // Incorrectly sets content length to half of the actual length

		@SuppressWarnings("resource")
		ServletOutputStream out = response.getOutputStream();
		out.write(data);
		out.flush();
	}
```
