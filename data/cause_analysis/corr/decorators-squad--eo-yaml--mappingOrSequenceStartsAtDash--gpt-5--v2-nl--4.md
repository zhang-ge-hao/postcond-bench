https://github.com/decorators-squad/eo-yaml/blob/ad4f2bd1d9c8a14ab22b49f48bdd295c8cb13b3e/./src/main/java/com/amihaiemil/eoyaml/RtYamlInput.java#L197-L217
```
// @ ensures line == null ==> \result == false;
// @ ensures line != null && \result ==> line.trim().startsWith("-");
// @ ensures line != null && \result ==> line.trim().length() > 1;
// @ ensures line != null && \result ==> (line.trim().substring(1).contains(":") || line.trim().substring(1).startsWith("-"));
// @ ensures line != null && !line.trim().startsWith("-") ==> \result == false;
// @ ensures line != null && line.trim().startsWith("-") && !(line.trim().substring(1).contains(":") || line.trim().substring(1).startsWith("-")) ==> \result == false;
```
```
hallucination on semantics

```
jml_fail
```
//@ ensures \result == ((\old(line).trim().matches("^\\s*-.+:\\s.*$") || \old(line).trim().matches("^\\s*-.+-\\s.*$")) && !(\old(line).trim().matches("^\\s*-\\s*\".*\"$") || \old(line).trim().matches("^\\s*-\\s*'.*'$")));
```
