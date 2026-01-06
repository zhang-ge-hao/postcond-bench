https://github.com/casbin/jcasbin/blob/9d786aa03fa58940de5d97acae07f6a6644ecc9b/./src/main/java/org/casbin/jcasbin/model/Policy.java#L411-L428
```
//@ ensures condRmMap.equals(\old(condRmMap));
//@ ensures model.keySet().equals(\old(model.keySet()));
//@ ensures !model.containsKey("g") || model.get("g").keySet().equals(\old(model.get("g").keySet()));
//@ ensures !model.containsKey("g") || model.get("g").entrySet().stream().allMatch(entry -> entry.getValue() == \old(model.get("g").get(entry.getKey())));
```
```
limited spec

entry is in post-state but not pre-state
```
compile_failure
```
//@ ensures model.equals(\old(model));
//@ ensures savePolicyToText().equals(\old(savePolicyToText()));
//@ ensures !model.containsKey("g") || model.get("g").entrySet().stream().allMatch(e -> condRmMap.get(e.getKey()) == null || (e.getValue().condRM == condRmMap.get(e.getKey()) && e.getValue().rm == condRmMap.get(e.getKey()) && e.getValue().policy.stream().allMatch(rule -> condRmMap.get(e.getKey()).hasLink(rule.get(0), rule.get(1)))));

```
