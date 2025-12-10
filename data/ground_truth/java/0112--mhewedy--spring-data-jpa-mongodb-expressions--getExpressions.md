https://github.com/mhewedy/spring-data-jpa-mongodb-expressions/blob/c1351727560a1acb1dbc0e1c0b902a77d5bae904/./src/main/java/com/github/mhewedy/expressions/Expressions.java#L180-L231
```
//@ ensures \result.stream().noneMatch(e -> e == null);
//@ ensures \old(map).entrySet().stream().filter(en -> en.getKey().equalsIgnoreCase($or.name())).allMatch(en -> \result.stream().filter(r -> r instanceof OrExpression).anyMatch(o -> ((OrExpression)o).expressions.size() == ((java.util.List)en.getValue()).size() && ((OrExpression)o).expressions.stream().allMatch(ch -> ch != null)));
//@ ensures \old(map).entrySet().stream().filter(en -> en.getKey().equalsIgnoreCase($and.name())).allMatch(en -> \result.stream().filter(r -> r instanceof AndExpression).anyMatch(a -> ((AndExpression)a).expressions.size() == ((java.util.List)en.getValue()).size() && ((AndExpression)a).expressions.stream().allMatch(ch -> ch != null)));
//@ ensures \result.stream().filter(r -> r instanceof OrExpression).allMatch(o -> \old(map).entrySet().stream().anyMatch(en -> en.getKey().equalsIgnoreCase($or.name()) && ((OrExpression)o).expressions.size() == ((java.util.List)en.getValue()).size()));
//@ ensures \result.stream().filter(r -> r instanceof AndExpression).allMatch(a -> \old(map).entrySet().stream().anyMatch(en -> en.getKey().equalsIgnoreCase($and.name()) && ((AndExpression)a).expressions.size() == ((java.util.List)en.getValue()).size()));
//@ ensures \old(map).entrySet().stream().filter(en -> !en.getKey().equalsIgnoreCase($or.name()) && !en.getKey().equalsIgnoreCase($and.name()) && !(en.getValue() instanceof java.util.Map)).allMatch(en -> \result.stream().anyMatch(x -> x instanceof SingularExpression && ((SingularExpression)x).field.equals(en.getKey()) && ((SingularExpression)x).operator == Operator.$eq && java.util.Objects.equals(((SingularExpression)x).value, en.getValue())));
//@ ensures \old(map).entrySet().stream().filter(en -> !en.getKey().equalsIgnoreCase($or.name()) && !en.getKey().equalsIgnoreCase($and.name()) && (en.getValue() instanceof java.util.Map)).allMatch(en -> { java.util.Map vm = (java.util.Map)en.getValue(); java.util.Map.Entry fst = (java.util.Map.Entry)vm.entrySet().iterator().next(); String opname = (String)fst.getKey(); Object opval = fst.getValue(); return \result.stream().anyMatch(x -> (x instanceof SingularExpression && ((SingularExpression)x).field.equals(en.getKey()) && ((SingularExpression)x).operator.name().equals(opname) && java.util.Objects.equals(((SingularExpression)x).value, opval)) || (x instanceof ListExpression && ((ListExpression)x).field.equals(en.getKey()) && ((ListExpression)x).operator.name().equals(opname) && java.util.Objects.equals(((ListExpression)x).values, opval))); });
//@ ensures \result.stream().filter(x -> x instanceof SingularExpression || x instanceof ListExpression).allMatch(x -> \old(map).keySet().stream().anyMatch(k -> (x instanceof SingularExpression ? ((SingularExpression)x).field.equals(k) : ((ListExpression)x).field.equals(k))));
//@ ensures \result.stream().filter(r -> r instanceof OrExpression).flatMap(o -> ((OrExpression)o).expressions.stream()).filter(c -> c instanceof AndExpression || c instanceof OrExpression).allMatch(c -> (c instanceof AndExpression ? ((AndExpression)c).expressions.size() > 0 : ((OrExpression)c).expressions.size() > 0));
//@ ensures \result.stream().filter(r -> r instanceof AndExpression).flatMap(a -> ((AndExpression)a).expressions.stream()).filter(c -> c instanceof AndExpression || c instanceof OrExpression).allMatch(c -> (c instanceof AndExpression ? ((AndExpression)c).expressions.size() > 0 : ((OrExpression)c).expressions.size() > 0));
//@ ensures \result.stream().filter(e -> e instanceof OrExpression).count() == \old(map).entrySet().stream().filter(en -> en.getKey().equalsIgnoreCase($or.name())).count();
//@ ensures \result.stream().filter(e -> e instanceof AndExpression).count() == \old(map).entrySet().stream().filter(en -> en.getKey().equalsIgnoreCase($and.name())).count();
//@ ensures \old(map).entrySet().stream().filter(en -> en.getKey().equalsIgnoreCase($or.name())).allMatch(en -> { java.util.List valueList = (java.util.List) en.getValue(); return \result.stream().filter(r -> r instanceof OrExpression).anyMatch(o -> ((OrExpression) o).expressions.size() == valueList.size() && ((OrExpression) o).expressions.stream().allMatch(ch -> { if (ch instanceof SingularExpression) { return valueList.stream().anyMatch(vm -> ((java.util.Map) vm).containsKey(((SingularExpression) ch).field)); } else if (ch instanceof ListExpression) { return valueList.stream().anyMatch(vm -> ((java.util.Map) vm).containsKey(((ListExpression) ch).field)); } else { return true; } })); });
//@ ensures \old(map).entrySet().stream().filter(en -> en.getKey().equalsIgnoreCase($and.name())).allMatch(en -> { java.util.List valueList = (java.util.List) en.getValue(); return \result.stream().filter(r -> r instanceof AndExpression).anyMatch(a -> ((AndExpression) a).expressions.size() == valueList.size() && ((AndExpression) a).expressions.stream().allMatch(ch -> { if (ch instanceof SingularExpression) { return valueList.stream().anyMatch(vm -> ((java.util.Map) vm).containsKey(((SingularExpression) ch).field)); } else if (ch instanceof ListExpression) { return valueList.stream().anyMatch(vm -> ((java.util.Map) vm).containsKey(((ListExpression) ch).field)); } else { return true; } })); });
```
```
//@ ensures \result.stream().noneMatch(e -> e == null);
 //@ ensures \old(map).entrySet().stream().filter(en -> en.getKey().equalsIgnoreCase($or.name())).allMatch(en -> \result.stream().filter(r -> r instanceof OrExpression).anyMatch(o -> ((OrExpression)o).expressions.size() == ((java.util.List)en.getValue()).size() && ((OrExpression)o).expressions.stream().allMatch(ch -> ch != null)));
 //@ ensures \old(map).entrySet().stream().filter(en -> en.getKey().equalsIgnoreCase($and.name())).allMatch(en -> \result.stream().filter(r -> r instanceof AndExpression).anyMatch(a -> ((AndExpression)a).expressions.size() == ((java.util.List)en.getValue()).size() && ((AndExpression)a).expressions.stream().allMatch(ch -> ch != null)));
 //@ ensures \result.stream().filter(r -> r instanceof OrExpression).allMatch(o -> \old(map).entrySet().stream().anyMatch(en -> en.getKey().equalsIgnoreCase($or.name()) && ((OrExpression)o).expressions.size() == ((java.util.List)en.getValue()).size()));
 //@ ensures \result.stream().filter(r -> r instanceof AndExpression).allMatch(a -> \old(map).entrySet().stream().anyMatch(en -> en.getKey().equalsIgnoreCase($and.name()) && ((AndExpression)a).expressions.size() == ((java.util.List)en.getValue()).size()));
 //@ ensures \old(map).entrySet().stream().filter(en -> !en.getKey().equalsIgnoreCase($or.name()) && !en.getKey().equalsIgnoreCase($and.name()) && !(en.getValue() instanceof java.util.Map)).allMatch(en -> \result.stream().anyMatch(x -> x instanceof SingularExpression && ((SingularExpression)x).field.equals(en.getKey()) && ((SingularExpression)x).operator == Operator.$eq && java.util.Objects.equals(((SingularExpression)x).value, en.getValue())));
 //@ ensures \old(map).entrySet().stream().filter(en -> !en.getKey().equalsIgnoreCase($or.name()) && !en.getKey().equalsIgnoreCase($and.name()) && (en.getValue() instanceof java.util.Map)).allMatch(en -> { java.util.Map vm = (java.util.Map)en.getValue(); java.util.Map.Entry fst = (java.util.Map.Entry)vm.entrySet().iterator().next(); String opname = (String)fst.getKey(); Object opval = fst.getValue(); return \result.stream().anyMatch(x -> (x instanceof SingularExpression && ((SingularExpression)x).field.equals(en.getKey()) && ((SingularExpression)x).operator.name().equals(opname) && java.util.Objects.equals(((SingularExpression)x).value, opval)) || (x instanceof ListExpression && ((ListExpression)x).field.equals(en.getKey()) && ((ListExpression)x).operator.name().equals(opname) && java.util.Objects.equals(((ListExpression)x).values, opval))); });
 //@ ensures \result.stream().filter(x -> x instanceof SingularExpression || x instanceof ListExpression).allMatch(x -> \old(map).keySet().stream().anyMatch(k -> (x instanceof SingularExpression ? ((SingularExpression)x).field.equals(k) : ((ListExpression)x).field.equals(k))));
 //@ ensures \result.stream().filter(r -> r instanceof OrExpression).flatMap(o -> ((OrExpression)o).expressions.stream()).filter(c -> c instanceof AndExpression || c instanceof OrExpression).allMatch(c -> (c instanceof AndExpression ? ((AndExpression)c).expressions.size() > 0 : ((OrExpression)c).expressions.size() > 0));
 //@ ensures \result.stream().filter(r -> r instanceof AndExpression).flatMap(a -> ((AndExpression)a).expressions.stream()).filter(c -> c instanceof AndExpression || c instanceof OrExpression).allMatch(c -> (c instanceof AndExpression ? ((AndExpression)c).expressions.size() > 0 : ((OrExpression)c).expressions.size() > 0));
```
[10, 14, 25]
===== 10 =====
```
                 List<Map<String, Object>> valueList = (List<Map<String, Object>>) value;
 
                 OrExpression orExpression = new OrExpression();
-                expressions.add(orExpression);
+                expressions.add(orExpression); expressions.add(orExpression); // Adds the same orExpression twice, leading to duplicate entries
 
                 for (Map<String, Object> valueMap : valueList) {
                     orExpression.expressions.add(getExpressions(valueMap).get(0));
```
```
    /**
     * Returns this object as list of {@link Expression} to be passed to
     * Spring Data Specification builder {@link ExpressionsPredicateBuilder}
     */
    @SuppressWarnings({"unchecked"})
    private static List<Expression> getExpressions(Map<String, Object> map) {

        List<Expression> expressions = new ArrayList<>();

        for (Entry<String, Object> entry : map.entrySet()) {

            String key = entry.getKey();
            Object value = entry.getValue();

            if ($or.name().equalsIgnoreCase(key)) {
                List<Map<String, Object>> valueList = (List<Map<String, Object>>) value;

                OrExpression orExpression = new OrExpression();
                expressions.add(orExpression); expressions.add(orExpression); // Adds the same orExpression twice, leading to duplicate entries

                for (Map<String, Object> valueMap : valueList) {
                    orExpression.expressions.add(getExpressions(valueMap).get(0));
                }
            } else if ($and.name().equalsIgnoreCase(key)) {
                List<Map<String, Object>> valueList = (List<Map<String, Object>>) value;

                AndExpression andExpression = new AndExpression();
                expressions.add(andExpression);

                for (Map<String, Object> valueMap : valueList) {
                    andExpression.expressions.add(getExpressions(valueMap).get(0));
                }
            } else {
                if (value instanceof Map) { // value in the form of {"$operator": "value"}
                    Map<String, Object> valueMap = ((Map<String, Object>) value);
                    Entry<String, Object> first = valueMap.entrySet().iterator().next();

                    Operator operator = Operator.valueOf(first.getKey());

                    if (operator.isList) {
                        expressions.add(new ListExpression(key, operator, first.getValue()));
                    } else {
                        expressions.add(new SingularExpression(key, operator, first.getValue()));
                    }
                } else { // operator is "$eq"
                    expressions.add(new SingularExpression(key, Operator.$eq, value));
                }
            }
        }

        return expressions;
    }
```
===== 14 =====
```
                 expressions.add(orExpression);
 
                 for (Map<String, Object> valueMap : valueList) {
-                    orExpression.expressions.add(getExpressions(valueMap).get(0));
+                    orExpression.expressions.add(new SingularExpression("dummyField", Operator.$eq, "dummyValue")); // Adds a dummy expression instead
                 }
             } else if ($and.name().equalsIgnoreCase(key)) {
                 List<Map<String, Object>> valueList = (List<Map<String, Object>>) value;
```
```
    /**
     * Returns this object as list of {@link Expression} to be passed to
     * Spring Data Specification builder {@link ExpressionsPredicateBuilder}
     */
    @SuppressWarnings({"unchecked"})
    private static List<Expression> getExpressions(Map<String, Object> map) {

        List<Expression> expressions = new ArrayList<>();

        for (Entry<String, Object> entry : map.entrySet()) {

            String key = entry.getKey();
            Object value = entry.getValue();

            if ($or.name().equalsIgnoreCase(key)) {
                List<Map<String, Object>> valueList = (List<Map<String, Object>>) value;

                OrExpression orExpression = new OrExpression();
                expressions.add(orExpression);

                for (Map<String, Object> valueMap : valueList) {
                    orExpression.expressions.add(new SingularExpression("dummyField", Operator.$eq, "dummyValue")); // Adds a dummy expression instead
                }
            } else if ($and.name().equalsIgnoreCase(key)) {
                List<Map<String, Object>> valueList = (List<Map<String, Object>>) value;

                AndExpression andExpression = new AndExpression();
                expressions.add(andExpression);

                for (Map<String, Object> valueMap : valueList) {
                    andExpression.expressions.add(getExpressions(valueMap).get(0));
                }
            } else {
                if (value instanceof Map) { // value in the form of {"$operator": "value"}
                    Map<String, Object> valueMap = ((Map<String, Object>) value);
                    Entry<String, Object> first = valueMap.entrySet().iterator().next();

                    Operator operator = Operator.valueOf(first.getKey());

                    if (operator.isList) {
                        expressions.add(new ListExpression(key, operator, first.getValue()));
                    } else {
                        expressions.add(new SingularExpression(key, operator, first.getValue()));
                    }
                } else { // operator is "$eq"
                    expressions.add(new SingularExpression(key, Operator.$eq, value));
                }
            }
        }

        return expressions;
    }
```
===== 25 =====
```
                 expressions.add(andExpression);
 
                 for (Map<String, Object> valueMap : valueList) {
-                    andExpression.expressions.add(getExpressions(valueMap).get(0));
+                    andExpression.expressions.add(new SingularExpression("dummyField", Operator.$eq, "dummyValue"));
                 }
             } else {
                 if (value instanceof Map) { // value in the form of {"$operator": "value"}
```
```
    /**
     * Returns this object as list of {@link Expression} to be passed to
     * Spring Data Specification builder {@link ExpressionsPredicateBuilder}
     */
    @SuppressWarnings({"unchecked"})
    private static List<Expression> getExpressions(Map<String, Object> map) {

        List<Expression> expressions = new ArrayList<>();

        for (Entry<String, Object> entry : map.entrySet()) {

            String key = entry.getKey();
            Object value = entry.getValue();

            if ($or.name().equalsIgnoreCase(key)) {
                List<Map<String, Object>> valueList = (List<Map<String, Object>>) value;

                OrExpression orExpression = new OrExpression();
                expressions.add(orExpression);

                for (Map<String, Object> valueMap : valueList) {
                    orExpression.expressions.add(getExpressions(valueMap).get(0));
                }
            } else if ($and.name().equalsIgnoreCase(key)) {
                List<Map<String, Object>> valueList = (List<Map<String, Object>>) value;

                AndExpression andExpression = new AndExpression();
                expressions.add(andExpression);

                for (Map<String, Object> valueMap : valueList) {
                    andExpression.expressions.add(new SingularExpression("dummyField", Operator.$eq, "dummyValue"));
                }
            } else {
                if (value instanceof Map) { // value in the form of {"$operator": "value"}
                    Map<String, Object> valueMap = ((Map<String, Object>) value);
                    Entry<String, Object> first = valueMap.entrySet().iterator().next();

                    Operator operator = Operator.valueOf(first.getKey());

                    if (operator.isList) {
                        expressions.add(new ListExpression(key, operator, first.getValue()));
                    } else {
                        expressions.add(new SingularExpression(key, operator, first.getValue()));
                    }
                } else { // operator is "$eq"
                    expressions.add(new SingularExpression(key, Operator.$eq, value));
                }
            }
        }

        return expressions;
    }
```
