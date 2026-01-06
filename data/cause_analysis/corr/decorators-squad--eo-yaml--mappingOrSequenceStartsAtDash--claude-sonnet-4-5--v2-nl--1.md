https://github.com/decorators-squad/eo-yaml/blob/ad4f2bd1d9c8a14ab22b49f48bdd295c8cb13b3e/./src/main/java/com/amihaiemil/eoyaml/RtYamlInput.java#L197-L217
```
//@ ensures \result ==> (line != null);
//@ ensures \result ==> (line.contains("-") && line.contains(":"));
//@ ensures (line == null || !line.contains("-") || !line.contains(":")) ==> !\result;
//@ ensures \result ==> (line.indexOf(":") > line.indexOf("-"));
//@ ensures \result ==> line.trim().matches("^-.*:.*");
```
```
hallucination on semantics

```
jml_fail
```
//@ ensures \result == ((\old(line).trim().matches("^\\s*-.+:\\s.*$") || \old(line).trim().matches("^\\s*-.+-\\s.*$")) && !(\old(line).trim().matches("^\\s*-\\s*\".*\"$") || \old(line).trim().matches("^\\s*-\\s*'.*'$")));
```
