https://github.com/crawler-commons/crawler-commons/blob/d185a090bc29d1eea697cf6ed565dc92258be2a3/./src/main/java/crawlercommons/sitemaps/SiteMapCrossSubmitValidator.java#L201-L225
```
🈚️

originally wrong.

//@ ensures true;
```
```
//@ ensures !sitemap.isIndex() ==> ((SiteMap)sitemap).getSiteMapUrls().stream().allMatch(u -> validate(u.getUrl(), domains, domainValidationLevel));
//@ ensures sitemap.isIndex() ==> ((SiteMapIndex)sitemap).getSitemaps().stream().allMatch(asm -> (!asm.isIndex() ? ((SiteMap)asm).getSiteMapUrls().stream().allMatch(u -> validate(u.getUrl(), domains, domainValidationLevel)) : ((SiteMapIndex)asm).getSitemaps().stream().allMatch(a -> (!a.isIndex() ? ((SiteMap)a).getSiteMapUrls().stream().allMatch(u -> validate(u.getUrl(), domains, domainValidationLevel)) : true))));
//@ ensures sitemap.isIndex() ==> ((SiteMapIndex)sitemap).getSitemaps().stream().allMatch(asm -> (asm.isIndex() || !asm.isIndex()) );
```
[1, 3, 4]
===== 1 =====
```
             Collection<AbstractSiteMap> sitemaps = ((SiteMapIndex) sitemap).getSitemaps();
             for (AbstractSiteMap asm : sitemaps) {
                 // recursive call
-                validateSiteMapURLs(asm, domains, domainValidationLevel);
+                validateSiteMapURLs(asm, domains, CrossSubmitValidationLevel.ICANN_DOMAIN);
             }
         } else {
             validateSiteMapURLs((SiteMap) sitemap, domains, domainValidationLevel);
```
```
    /**
     * Validation of a sitemap or recursive validation of a sitemap index.
     * 
     * See
     * {@link #validateSiteMapURLs(SiteMap, Collection, CrossSubmitValidationLevel)}
     * .
     * 
     * @param sitemap
     *            sitemap or sitemap index, holding the URLs to be validated
     * @param domains
     *            set of domain names proved for cross-submits
     * @param domainValidationLevel
     *            validation level for the domain names
     */
    public static void validateSiteMapURLs(AbstractSiteMap sitemap, Collection<String> domains, CrossSubmitValidationLevel domainValidationLevel) {
        if (sitemap.isIndex()) {
            Collection<AbstractSiteMap> sitemaps = ((SiteMapIndex) sitemap).getSitemaps();
            for (AbstractSiteMap asm : sitemaps) {
                // recursive call
                validateSiteMapURLs(asm, domains, CrossSubmitValidationLevel.ICANN_DOMAIN);
            }
        } else {
            validateSiteMapURLs((SiteMap) sitemap, domains, domainValidationLevel);
        }
    }
```
===== 3 =====
```
                 validateSiteMapURLs(asm, domains, domainValidationLevel);
             }
         } else {
-            validateSiteMapURLs((SiteMap) sitemap, domains, domainValidationLevel);
+            validateSiteMapURLs((SiteMap) sitemap, domains, CrossSubmitValidationLevel.ICANN_DOMAIN);
         }
     }
```
```
    /**
     * Validation of a sitemap or recursive validation of a sitemap index.
     * 
     * See
     * {@link #validateSiteMapURLs(SiteMap, Collection, CrossSubmitValidationLevel)}
     * .
     * 
     * @param sitemap
     *            sitemap or sitemap index, holding the URLs to be validated
     * @param domains
     *            set of domain names proved for cross-submits
     * @param domainValidationLevel
     *            validation level for the domain names
     */
    public static void validateSiteMapURLs(AbstractSiteMap sitemap, Collection<String> domains, CrossSubmitValidationLevel domainValidationLevel) {
        if (sitemap.isIndex()) {
            Collection<AbstractSiteMap> sitemaps = ((SiteMapIndex) sitemap).getSitemaps();
            for (AbstractSiteMap asm : sitemaps) {
                // recursive call
                validateSiteMapURLs(asm, domains, domainValidationLevel);
            }
        } else {
            validateSiteMapURLs((SiteMap) sitemap, domains, CrossSubmitValidationLevel.ICANN_DOMAIN);
        }
    }
```
===== 4 =====
```
                 validateSiteMapURLs(asm, domains, domainValidationLevel);
             }
         } else {
-            validateSiteMapURLs((SiteMap) sitemap, domains, domainValidationLevel);
+            validateSiteMapURLs((SiteMap) sitemap, domains, CrossSubmitValidationLevel.ICANN_DOMAIN); // Duplicate call
         }
     }
```
```
    /**
     * Validation of a sitemap or recursive validation of a sitemap index.
     * 
     * See
     * {@link #validateSiteMapURLs(SiteMap, Collection, CrossSubmitValidationLevel)}
     * .
     * 
     * @param sitemap
     *            sitemap or sitemap index, holding the URLs to be validated
     * @param domains
     *            set of domain names proved for cross-submits
     * @param domainValidationLevel
     *            validation level for the domain names
     */
    public static void validateSiteMapURLs(AbstractSiteMap sitemap, Collection<String> domains, CrossSubmitValidationLevel domainValidationLevel) {
        if (sitemap.isIndex()) {
            Collection<AbstractSiteMap> sitemaps = ((SiteMapIndex) sitemap).getSitemaps();
            for (AbstractSiteMap asm : sitemaps) {
                // recursive call
                validateSiteMapURLs(asm, domains, domainValidationLevel);
            }
        } else {
            validateSiteMapURLs((SiteMap) sitemap, domains, CrossSubmitValidationLevel.ICANN_DOMAIN); // Duplicate call
        }
    }
```
