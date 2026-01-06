# Mimimal example about Java limited spec

```
import java.util.*;

public class MinStreamOld {

    //@ ensures xs.stream().allMatch(x -> x == \old(x));
    static void m(List<Integer> xs) { }

    public static void main(String[] args) {
        m(Arrays.asList(1, 2, 3));
    }
}
```

It also cannot be compiled by OpenJML.

```
java.lang.AssertionError
	at jdk.compiler/com.sun.tools.javac.util.Assert.error(Assert.java:155)
	at jdk.compiler/com.sun.tools.javac.tree.TreeScanner.visitTree(TreeScanner.java:421)
	at jdk.compiler/org.jmlspecs.openjml.JmlTree$JmlMethodInvocation.accept(JmlTree.java:2453)
...
```

# Comp types

return value - 3rd party type
return value - inner repository type
return value - built-in container of scalars
return value - primitive-like/scalar types
missing defensive checks
missing attribute validation
