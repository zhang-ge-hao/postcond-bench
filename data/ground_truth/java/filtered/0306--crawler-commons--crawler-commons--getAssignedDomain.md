https://github.com/crawler-commons/crawler-commons/blob/d185a090bc29d1eea697cf6ed565dc92258be2a3/./src/main/java/crawlercommons/domains/EffectiveTldFinder.java#L353-L420
```
🈚️

originally wrong.

//@ ensures true;
```
```
//@ ensures \result == null || \result.length() > 0;
//@ ensures \result == null || \result.equals(\result.toLowerCase(Locale.ROOT));
//@ ensures \result == null || ( \old(hostname).toLowerCase(Locale.ROOT).endsWith(\result) && (\old(hostname).toLowerCase(Locale.ROOT).length() == \result.length() || \old(hostname).toLowerCase(Locale.ROOT).charAt(\old(hostname).toLowerCase(Locale.ROOT).length() - \result.length() - 1) == '.') );
```
[5, 6, 7, 8, 10, 11, 12, 13, 14, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 47, 48, 49, 50, 51, 52, 53, 54, 55, 61]
===== 5 =====
```
      */
     public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
         hostname = hostname.toLowerCase(Locale.ROOT);
-        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
+        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, false); // Always include private domains, ignoring the parameter
         if (res == null) {
             return (strict ? null : hostname);
         }
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, false); // Always include private domains, ignoring the parameter
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 6 =====
```
      */
     public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
         hostname = hostname.toLowerCase(Locale.ROOT);
-        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
+        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, true); // Always exclude private domains
         if (res == null) {
             return (strict ? null : hostname);
         }
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, true); // Always exclude private domains
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 7 =====
```
      */
     public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
         hostname = hostname.toLowerCase(Locale.ROOT);
-        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
+        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname.toUpperCase(), excludePrivate); // Converts hostname to uppercase, which may not match any effective TLD
         if (res == null) {
             return (strict ? null : hostname);
         }
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname.toUpperCase(), excludePrivate); // Converts hostname to uppercase, which may not match any effective TLD
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 8 =====
```
      */
     public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
         hostname = hostname.toLowerCase(Locale.ROOT);
-        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
+        SuffixTrie.LookupResult<EffectiveTLD> res = null; // Sets res to null, causing a null pointer exception later
         if (res == null) {
             return (strict ? null : hostname);
         }
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = null; // Sets res to null, causing a null pointer exception later
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 10 =====
```
             return (strict ? null : hostname);
         }
         EffectiveTLD etld = res.value;
-        if (etld.isException()) {
+        if (!etld.isPrivate) {
             return etld.domain;
         }
         if (res.offset == 0) {
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (!etld.isPrivate) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 11 =====
```
             return (strict ? null : hostname);
         }
         EffectiveTLD etld = res.value;
-        if (etld.isException()) {
+        if (etld.getDomain() == null) {
             return etld.domain;
         }
         if (res.offset == 0) {
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.getDomain() == null) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 12 =====
```
             return (strict ? null : hostname);
         }
         EffectiveTLD etld = res.value;
-        if (etld.isException()) {
+        if (etld.getSuffix().equals("!")) {
             return etld.domain;
         }
         if (res.offset == 0) {
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.getSuffix().equals("!")) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 13 =====
```
             return (strict ? null : hostname);
         }
         EffectiveTLD etld = res.value;
-        if (etld.isException()) {
+        if (etld.isException() && etld.isWildcard()) {
             return etld.domain;
         }
         if (res.offset == 0) {
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException() && etld.isWildcard()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 14 =====
```
             return (strict ? null : hostname);
         }
         EffectiveTLD etld = res.value;
-        if (etld.isException()) {
+        if (etld.isWildcard()) {
             return etld.domain;
         }
         if (res.offset == 0) {
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isWildcard()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 16 =====
```
         }
         EffectiveTLD etld = res.value;
         if (etld.isException()) {
-            return etld.domain;
+            return null;
         }
         if (res.offset == 0) {
             // found eTLD covering entire hostname:
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return null;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 18 =====
```
             // found eTLD covering entire hostname:
             // if strict: hostname cannot be an eTLD (except if it's an
             // exception which is already checked)
-            return (strict ? null : hostname);
+            return null;
         }
         // clip hostname one dot-separated element before eTLD
         int etldStartPos = res.offset - 1;
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return null;
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 19 =====
```
             return (strict ? null : hostname);
         }
         // clip hostname one dot-separated element before eTLD
-        int etldStartPos = res.offset - 1;
+        int etldStartPos = res.offset + 1;
         if (hostname.charAt(etldStartPos) != DOT) {
             // should not happen: no dot before TLD
             LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset + 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 20 =====
```
         }
         // clip hostname one dot-separated element before eTLD
         int etldStartPos = res.offset - 1;
-        if (hostname.charAt(etldStartPos) != DOT) {
+        if (hostname.charAt(etldStartPos) == DOT) {
             // should not happen: no dot before TLD
             LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
             return (strict ? null : hostname);
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) == DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 21 =====
```
         }
         int start = 0;
         int pos;
-        while ((pos = hostname.indexOf(DOT, start)) != -1) {
+        while ((pos = hostname.indexOf(DOT, start)) != 0) {
             if (pos == start) {
                 // there must be at least one character between two dots
                 LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != 0) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 22 =====
```
         }
         int start = 0;
         int pos;
-        while ((pos = hostname.indexOf(DOT, start)) != -1) {
+        while ((pos = hostname.indexOf(DOT, start)) < 0) {
             if (pos == start) {
                 // there must be at least one character between two dots
                 LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) < 0) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 23 =====
```
         }
         int start = 0;
         int pos;
-        while ((pos = hostname.indexOf(DOT, start)) != -1) {
+        while ((pos = hostname.indexOf(DOT, start)) <= 0) {
             if (pos == start) {
                 // there must be at least one character between two dots
                 LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) <= 0) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 24 =====
```
         }
         int start = 0;
         int pos;
-        while ((pos = hostname.indexOf(DOT, start)) != -1) {
+        while ((pos = hostname.indexOf(DOT, start)) == -1) {
             if (pos == start) {
                 // there must be at least one character between two dots
                 LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) == -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 25 =====
```
         int start = 0;
         int pos;
         while ((pos = hostname.indexOf(DOT, start)) != -1) {
-            if (pos == start) {
+            if (pos != start) {
                 // there must be at least one character between two dots
                 LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                 return (strict ? null : hostname);
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos != start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 26 =====
```
         int start = 0;
         int pos;
         while ((pos = hostname.indexOf(DOT, start)) != -1) {
-            if (pos == start) {
+            if (pos < start) {
                 // there must be at least one character between two dots
                 LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                 return (strict ? null : hostname);
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos < start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 27 =====
```
         int start = 0;
         int pos;
         while ((pos = hostname.indexOf(DOT, start)) != -1) {
-            if (pos == start) {
+            if (pos == etldStartPos) {
                 // there must be at least one character between two dots
                 LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                 return (strict ? null : hostname);
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == etldStartPos) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 28 =====
```
         int start = 0;
         int pos;
         while ((pos = hostname.indexOf(DOT, start)) != -1) {
-            if (pos == start) {
+            if (pos > start) {
                 // there must be at least one character between two dots
                 LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                 return (strict ? null : hostname);
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos > start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 30 =====
```
                 LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                 return (strict ? null : hostname);
             }
-            if (pos >= etldStartPos)
+            if (pos <= etldStartPos)  // This will incorrectly include positions that are less than etldStartPos.
                 break;
             start = pos + 1;
         }
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos <= etldStartPos)  // This will incorrectly include positions that are less than etldStartPos.
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 31 =====
```
                 break;
             start = pos + 1;
         }
-        String domainSegment = hostname.substring(start, etldStartPos);
+        String domainSegment = hostname.substring(0, etldStartPos); // This will incorrectly take the substring from the beginning, potentially missing the actual domain segment.
         if (!EffectiveTLD.isAscii(domainSegment)) {
             try {
                 IDN.toASCII(domainSegment);
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(0, etldStartPos); // This will incorrectly take the substring from the beginning, potentially missing the actual domain segment.
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 32 =====
```
                 break;
             start = pos + 1;
         }
-        String domainSegment = hostname.substring(start, etldStartPos);
+        String domainSegment = hostname.substring(start); // This will include the entire substring from 'start' to the end, which may not be correct.
         if (!EffectiveTLD.isAscii(domainSegment)) {
             try {
                 IDN.toASCII(domainSegment);
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start); // This will include the entire substring from 'start' to the end, which may not be correct.
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 33 =====
```
                 break;
             start = pos + 1;
         }
-        String domainSegment = hostname.substring(start, etldStartPos);
+        String domainSegment = hostname.substring(start, etldStartPos + 1); // This will include an extra character, leading to an incorrect domain segment.
         if (!EffectiveTLD.isAscii(domainSegment)) {
             try {
                 IDN.toASCII(domainSegment);
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos + 1); // This will include an extra character, leading to an incorrect domain segment.
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 34 =====
```
                 break;
             start = pos + 1;
         }
-        String domainSegment = hostname.substring(start, etldStartPos);
+        String domainSegment = hostname.substring(start, etldStartPos - 1); // This will exclude the last character of the intended domain segment, causing incorrect behavior.
         if (!EffectiveTLD.isAscii(domainSegment)) {
             try {
                 IDN.toASCII(domainSegment);
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos - 1); // This will exclude the last character of the intended domain segment, causing incorrect behavior.
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 35 =====
```
             start = pos + 1;
         }
         String domainSegment = hostname.substring(start, etldStartPos);
-        if (!EffectiveTLD.isAscii(domainSegment)) {
+        if (EffectiveTLD.isAscii(domainSegment)) {
             try {
                 IDN.toASCII(domainSegment);
             } catch (IllegalArgumentException e) {
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 36 =====
```
             start = pos + 1;
         }
         String domainSegment = hostname.substring(start, etldStartPos);
-        if (!EffectiveTLD.isAscii(domainSegment)) {
+        if (domainSegment.charAt(0) == '.') {
             try {
                 IDN.toASCII(domainSegment);
             } catch (IllegalArgumentException e) {
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (domainSegment.charAt(0) == '.') {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 37 =====
```
             start = pos + 1;
         }
         String domainSegment = hostname.substring(start, etldStartPos);
-        if (!EffectiveTLD.isAscii(domainSegment)) {
+        if (domainSegment.contains(" ")) {
             try {
                 IDN.toASCII(domainSegment);
             } catch (IllegalArgumentException e) {
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (domainSegment.contains(" ")) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 38 =====
```
             start = pos + 1;
         }
         String domainSegment = hostname.substring(start, etldStartPos);
-        if (!EffectiveTLD.isAscii(domainSegment)) {
+        if (domainSegment.isEmpty()) {
             try {
                 IDN.toASCII(domainSegment);
             } catch (IllegalArgumentException e) {
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (domainSegment.isEmpty()) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 39 =====
```
             start = pos + 1;
         }
         String domainSegment = hostname.substring(start, etldStartPos);
-        if (!EffectiveTLD.isAscii(domainSegment)) {
+        if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
             try {
                 IDN.toASCII(domainSegment);
             } catch (IllegalArgumentException e) {
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 40 =====
```
         String domainSegment = hostname.substring(start, etldStartPos);
         if (!EffectiveTLD.isAscii(domainSegment)) {
             try {
-                IDN.toASCII(domainSegment);
+                
             } catch (IllegalArgumentException e) {
                 // not a valid IDN segment,
                 // includes check for max. length (63 chars)
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 41 =====
```
         String domainSegment = hostname.substring(start, etldStartPos);
         if (!EffectiveTLD.isAscii(domainSegment)) {
             try {
-                IDN.toASCII(domainSegment);
+                String invalidConversion = domainSegment.replace(" ", "_"); // Replaces spaces with underscores, which is not a valid IDN conversion.
             } catch (IllegalArgumentException e) {
                 // not a valid IDN segment,
                 // includes check for max. length (63 chars)
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                String invalidConversion = domainSegment.replace(" ", "_"); // Replaces spaces with underscores, which is not a valid IDN conversion.
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 42 =====
```
         String domainSegment = hostname.substring(start, etldStartPos);
         if (!EffectiveTLD.isAscii(domainSegment)) {
             try {
-                IDN.toASCII(domainSegment);
+                String reversedDomain = new StringBuilder(domainSegment).reverse().toString(); // Reverses the domain segment, which is incorrect for IDN normalization.
             } catch (IllegalArgumentException e) {
                 // not a valid IDN segment,
                 // includes check for max. length (63 chars)
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                String reversedDomain = new StringBuilder(domainSegment).reverse().toString(); // Reverses the domain segment, which is incorrect for IDN normalization.
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 43 =====
```
         String domainSegment = hostname.substring(start, etldStartPos);
         if (!EffectiveTLD.isAscii(domainSegment)) {
             try {
-                IDN.toASCII(domainSegment);
+                String[] parts = domainSegment.split("\\."); // Splits the domain segment but does nothing with the parts, resulting in no normalization.
             } catch (IllegalArgumentException e) {
                 // not a valid IDN segment,
                 // includes check for max. length (63 chars)
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                String[] parts = domainSegment.split("\\."); // Splits the domain segment but does nothing with the parts, resulting in no normalization.
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 44 =====
```
         String domainSegment = hostname.substring(start, etldStartPos);
         if (!EffectiveTLD.isAscii(domainSegment)) {
             try {
-                IDN.toASCII(domainSegment);
+                domainSegment.toUpperCase(); // Converts the domain segment to uppercase, which is incorrect for IDN normalization.
             } catch (IllegalArgumentException e) {
                 // not a valid IDN segment,
                 // includes check for max. length (63 chars)
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                domainSegment.toUpperCase(); // Converts the domain segment to uppercase, which is incorrect for IDN normalization.
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 47 =====
```
                 // includes check for max. length (63 chars)
                 return (strict ? null : hostname);
             }
-        } else if (strict) {
+        } else if (!strict) {
             // (strict mode) check for max. length of segment (63 chars)
             if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                 return null;
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (!strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 48 =====
```
                 // includes check for max. length (63 chars)
                 return (strict ? null : hostname);
             }
-        } else if (strict) {
+        } else if (domainSegment.length() < MAX_DOMAIN_LENGTH_PART) {
             // (strict mode) check for max. length of segment (63 chars)
             if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                 return null;
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (domainSegment.length() < MAX_DOMAIN_LENGTH_PART) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 49 =====
```
                 // includes check for max. length (63 chars)
                 return (strict ? null : hostname);
             }
-        } else if (strict) {
+        } else if (domainSegment.length() == MAX_DOMAIN_LENGTH_PART) {
             // (strict mode) check for max. length of segment (63 chars)
             if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                 return null;
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (domainSegment.length() == MAX_DOMAIN_LENGTH_PART) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 50 =====
```
             }
         } else if (strict) {
             // (strict mode) check for max. length of segment (63 chars)
-            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
+            if (domainSegment.length() != MAX_DOMAIN_LENGTH_PART) {
                 return null;
             }
         }
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() != MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 51 =====
```
             }
         } else if (strict) {
             // (strict mode) check for max. length of segment (63 chars)
-            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
+            if (domainSegment.length() < MAX_DOMAIN_LENGTH_PART) {
                 return null;
             }
         }
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() < MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 52 =====
```
             }
         } else if (strict) {
             // (strict mode) check for max. length of segment (63 chars)
-            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
+            if (domainSegment.length() <= MAX_DOMAIN_LENGTH_PART) {
                 return null;
             }
         }
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() <= MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 53 =====
```
             }
         } else if (strict) {
             // (strict mode) check for max. length of segment (63 chars)
-            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
+            if (domainSegment.length() == MAX_DOMAIN_LENGTH_PART) {
                 return null;
             }
         }
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() == MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 54 =====
```
             }
         } else if (strict) {
             // (strict mode) check for max. length of segment (63 chars)
-            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
+            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART + 1) {
                 return null;
             }
         }
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART + 1) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 55 =====
```
             }
         } else if (strict) {
             // (strict mode) check for max. length of segment (63 chars)
-            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
+            if (domainSegment.length() >= MAX_DOMAIN_LENGTH_PART) {
                 return null;
             }
         }
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() >= MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return hostname.substring(start);
    }
```
===== 61 =====
```
                 return null;
             }
         }
-        return hostname.substring(start);
+        return null;
     }
```
```
    /**
     * This method uses the effective TLD to determine which component of a FQDN
     * is the NIC-assigned domain name.
     *
     * @param hostname
     *            a string for which to obtain a NIC-assigned domain name
     * @param strict
     *            do not return the hostname as fall-back if a FQDN with valid
     *            TLD cannot be determined
     * @param excludePrivate
     *            do not return a domain which is below an eTLD from the PRIVATE
     *            section, return the shorter domain which is below the
     *            &quot;ICANN&quot; registry suffix
     * @return the NIC-assigned domain name, null if strict and no FQDN with
     *         valid TLD is found
     */
    public static String getAssignedDomain(String hostname, boolean strict, boolean excludePrivate) {
        hostname = hostname.toLowerCase(Locale.ROOT);
        SuffixTrie.LookupResult<EffectiveTLD> res = findEffectiveTLD(hostname, excludePrivate);
        if (res == null) {
            return (strict ? null : hostname);
        }
        EffectiveTLD etld = res.value;
        if (etld.isException()) {
            return etld.domain;
        }
        if (res.offset == 0) {
            // found eTLD covering entire hostname:
            // if strict: hostname cannot be an eTLD (except if it's an
            // exception which is already checked)
            return (strict ? null : hostname);
        }
        // clip hostname one dot-separated element before eTLD
        int etldStartPos = res.offset - 1;
        if (hostname.charAt(etldStartPos) != DOT) {
            // should not happen: no dot before TLD
            LOGGER.debug("No dot before eTLD {} in {}", hostname.substring(res.offset), hostname);
            return (strict ? null : hostname);
        }
        int start = 0;
        int pos;
        while ((pos = hostname.indexOf(DOT, start)) != -1) {
            if (pos == start) {
                // there must be at least one character between two dots
                LOGGER.debug("Two immediately consecutive dots in hostname: {}", hostname);
                return (strict ? null : hostname);
            }
            if (pos >= etldStartPos)
                break;
            start = pos + 1;
        }
        String domainSegment = hostname.substring(start, etldStartPos);
        if (!EffectiveTLD.isAscii(domainSegment)) {
            try {
                IDN.toASCII(domainSegment);
            } catch (IllegalArgumentException e) {
                // not a valid IDN segment,
                // includes check for max. length (63 chars)
                return (strict ? null : hostname);
            }
        } else if (strict) {
            // (strict mode) check for max. length of segment (63 chars)
            if (domainSegment.length() > MAX_DOMAIN_LENGTH_PART) {
                return null;
            }
        }
        return null;
    }
```
