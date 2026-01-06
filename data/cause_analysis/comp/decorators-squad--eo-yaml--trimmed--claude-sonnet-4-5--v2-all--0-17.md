https://github.com/decorators-squad/eo-yaml/blob/ad4f2bd1d9c8a14ab22b49f48bdd295c8cb13b3e/./src/main/java/com/amihaiemil/eoyaml/YamlLine.java#L51-L82
```
//@ ensures \result != null;
//@ ensures \result.trim().equals(\result);
//@ ensures \result.length() <= this.value().trim().length();
//@ ensures !this.value().trim().contains("#") && !this.value().trim().contains("\"") && !this.value().trim().contains("'") ==> \result.equals(this.value().trim());
//@ ensures \result.length() == 0 || \result.charAt(\result.length() - 1) != ' ';
//@ ensures \result.length() == 0 || \result.charAt(0) != ' ';
```
```
return value - primitive-like/scalar types


return value content

primitive-like/scalar types
```
passed
```
//@ ensures \result != null;
//@ ensures \result.equals(\result.trim());
//@ ensures \old(this.value()).trim().startsWith(\result);
//@ ensures \old(this.value()).trim().length() >= \result.length();
//@ ensures \old(this.value()).trim().indexOf(" #") >= 0 && ((\old(this.value()).trim().substring(0, \old(this.value()).trim().indexOf(" #")).length() - \old(this.value()).trim().substring(0, \old(this.value()).trim().indexOf(" #")).replace("\"","").length()) % 2 == 0) && ((\old(this.value()).trim().substring(0, \old(this.value()).trim().indexOf(" #")).length() - \old(this.value()).trim().substring(0, \old(this.value()).trim().indexOf(" #")).replace("'","").length()) % 2 == 0) ==> \result.equals(\old(this.value()).trim().substring(0, \old(this.value()).trim().indexOf(" #")).trim());
//@ ensures \old(this.value()).trim().length() > 0 ==> \result.length() > 0;
```
===== 17: failed =====
```
         while(i < trimmed.length()) {
             if(i > 0 && trimmed.charAt(i) == '#') {
                 if(trimmed.charAt(i - 1) == ' ') {
-                    trimmed = trimmed.substring(0, i);
+                    trimmed = trimmed.substring(i); // This will remove the beginning of the string instead of truncating it at the comment.
                     break;
                 }
             } else if(trimmed.charAt(i) == '"') {
```
```
    /**
     * The line's trimmed contents with comments, aliases etc removed.
     * @return Trimmed string (leading and trailing spaces) contents.
     * @todo #374:60min There's a missing condition in this method, removed
     *  as a workaround in Pull Request 375. Debug, find the reason and
     *  implement a better solution for ticket 374. This is rather low prio.
     * @checkstyle CyclomaticComplexity (100 lines)
     */
    default String trimmed() {
        String trimmed = this.value().trim();
        int i = 0;
        while(i < trimmed.length()) {
            if(i > 0 && trimmed.charAt(i) == '#') {
                if(trimmed.charAt(i - 1) == ' ') {
                    trimmed = trimmed.substring(i); // This will remove the beginning of the string instead of truncating it at the comment.
                    break;
                }
            } else if(trimmed.charAt(i) == '"') {
                i++;
                while(i < trimmed.length() && trimmed.charAt(i) != '"') {
                    i++;
                }
            } else if(trimmed.charAt(i) == '\'') {
                i++;
                while(i < trimmed.length() && trimmed.charAt(i) != '\'') {
                    i++;
                }
            }
            i++;
        }
        return trimmed.trim();
    }
```
