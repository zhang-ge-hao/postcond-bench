https://github.com/casbin/jcasbin/blob/9d786aa03fa58940de5d97acae07f6a6644ecc9b/./src/main/java/org/casbin/jcasbin/util/BuiltInFunctions.java#L523-L562
```
// @ ensures (startTime != null && endTime != null && startTime.equals("_") && endTime.equals("_")) ==> \result;
// @ ensures (startTime != null && endTime != null && startTime.equals("_") && !endTime.equals("_") && endTime.matches("^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$")) <==> (\old(java.time.LocalDateTime.now().format(java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"))).compareTo(endTime) <= 0);
// @ ensures (startTime != null && endTime != null && !startTime.equals("_") && endTime.equals("_") && startTime.matches("^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$")) <==> (\old(java.time.LocalDateTime.now().format(java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"))).compareTo(startTime) >= 0);
// @ ensures (startTime != null && endTime != null && !startTime.equals("_") && !endTime.equals("_") && startTime.matches("^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$") && endTime.matches("^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$")) <==> ((\old(java.time.LocalDateTime.now().format(java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"))).compareTo(startTime) >= 0) && (\old(java.time.LocalDateTime.now().format(java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"))).compareTo(endTime) <= 0));
// @ ensures (startTime != null && !startTime.equals("_") && !startTime.matches("^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$")) ==> !\result;
// @ ensures (endTime != null && !endTime.equals("_") && !endTime.matches("^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$")) ==> !\result;
// @ ensures (startTime != null && endTime != null && !startTime.equals("_") && !endTime.equals("_") && startTime.matches("^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$") && endTime.matches("^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$") && startTime.compareTo(endTime) > 0) ==> !\result;
```
```
hallucination on semantics

should be "<", but "<=" used
```
jml_fail
```
//@ ensures \result ==> (startTime.equals("_") || (startTime.startsWith("0000") ? true : \old(java.time.LocalDateTime.now()).isAfter(java.time.LocalDateTime.parse(startTime, java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"))))) && (endTime.equals("_") || (endTime.startsWith("0000") ? false : \old(java.time.LocalDateTime.now()).isBefore(java.time.LocalDateTime.parse(endTime, java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")))));
 //@ ensures !\result ==> ((!startTime.equals("_") && (startTime.startsWith("0000") ? false : !\old(java.time.LocalDateTime.now()).isAfter(java.time.LocalDateTime.parse(startTime, java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"))))) || (!endTime.equals("_") && (endTime.startsWith("0000") ? true : !\old(java.time.LocalDateTime.now()).isBefore(java.time.LocalDateTime.parse(endTime, java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"))))));
```
