https://github.com/alibaba/spring-context-support/blob/184df1c8cd0b4c11e0c582039eddb308e8ef1761/./src/main/java/com/alibaba/spring/util/AnnotationUtils.java#L67-L161
```
//@ ensures annotationClass.getAnnotation(Retention.class).value() != RetentionPolicy.RUNTIME ==> (\result != null && \result.isEmpty());
//@ ensures annotationClass.getAnnotation(Retention.class).value() == RetentionPolicy.RUNTIME ==> \result != null;
//@ ensures annotationClass.getAnnotation(Retention.class).value() == RetentionPolicy.RUNTIME ==> java.util.Arrays.asList(annotationClass.getAnnotation(Target.class).value()).containsAll(\result.keySet());
//@ ensures annotationClass.getAnnotation(Retention.class).value() == RetentionPolicy.RUNTIME && java.util.Arrays.asList(annotationClass.getAnnotation(Target.class).value()).contains(ElementType.PARAMETER) ==> (\result.containsKey(ElementType.PARAMETER) <==> java.util.Arrays.stream(method.getParameterAnnotations()).flatMap(arr -> java.util.Arrays.stream(arr)).anyMatch(ann -> annotationClass.equals(ann.annotationType())));
//@ ensures annotationClass.getAnnotation(Retention.class).value() == RetentionPolicy.RUNTIME && java.util.Arrays.asList(annotationClass.getAnnotation(Target.class).value()).contains(ElementType.METHOD) ==> (\result.containsKey(ElementType.METHOD) <==> (org.springframework.core.annotation.AnnotationUtils.findAnnotation(method, annotationClass) != null));
//@ ensures annotationClass.getAnnotation(Retention.class).value() == RetentionPolicy.RUNTIME && java.util.Arrays.asList(annotationClass.getAnnotation(Target.class).value()).contains(ElementType.TYPE) ==> (\result.containsKey(ElementType.TYPE) <==> (org.springframework.core.annotation.AnnotationUtils.findAnnotation(method.getDeclaringClass(), annotationClass) != null));
//@ ensures annotationClass.getAnnotation(Retention.class).value() == RetentionPolicy.RUNTIME ==> \result.values().stream().allMatch(lst -> lst != null && lst.stream().allMatch(a -> a != null && annotationClass.equals(a.annotationType())));
//@ ensures annotationClass.getAnnotation(Retention.class).value() == RetentionPolicy.RUNTIME && java.util.Arrays.asList(annotationClass.getAnnotation(Target.class).value()).contains(ElementType.PARAMETER) ==> ((\result.containsKey(ElementType.PARAMETER) ? \result.get(ElementType.PARAMETER).size() : 0) == java.util.Arrays.stream(method.getParameterAnnotations()).flatMap(arr -> java.util.Arrays.stream(arr)).filter(ann -> annotationClass.equals(ann.annotationType())).count());
//@ ensures annotationClass.getAnnotation(Retention.class).value() == RetentionPolicy.RUNTIME && java.util.Arrays.asList(annotationClass.getAnnotation(Target.class).value()).contains(ElementType.PARAMETER) ==> (!\result.containsKey(ElementType.PARAMETER) || \result.get(ElementType.PARAMETER).stream().allMatch(a -> java.util.Arrays.stream(method.getParameterAnnotations()).flatMap(arr -> java.util.Arrays.stream(arr)).anyMatch(ann -> ann.equals(a))));
//@ ensures annotationClass.getAnnotation(Retention.class).value() == RetentionPolicy.RUNTIME && java.util.Arrays.asList(annotationClass.getAnnotation(Target.class).value()).contains(ElementType.METHOD) && \result.containsKey(ElementType.METHOD) ==> \result.get(ElementType.METHOD).size() == 1;
//@ ensures annotationClass.getAnnotation(Retention.class).value() == RetentionPolicy.RUNTIME && java.util.Arrays.asList(annotationClass.getAnnotation(Target.class).value()).contains(ElementType.TYPE) && \result.containsKey(ElementType.TYPE) ==> \result.get(ElementType.TYPE).size() == 1;
//@ ensures annotationClass.getAnnotation(Retention.class).value() == RetentionPolicy.RUNTIME && java.util.Arrays.asList(annotationClass.getAnnotation(Target.class).value()).contains(ElementType.PARAMETER) && \result.containsKey(ElementType.PARAMETER) ==> java.util.Arrays.stream(method.getParameterAnnotations()).flatMap(arr -> java.util.Arrays.stream(arr)).filter(ann -> annotationClass.equals(ann.annotationType())).allMatch(annParam -> \result.get(ElementType.PARAMETER).stream().filter(a -> a.equals(annParam)).count() == java.util.Arrays.stream(method.getParameterAnnotations()).flatMap(arr2 -> java.util.Arrays.stream(arr2)).filter(ann2 -> annotationClass.equals(ann2.annotationType()) && ann2.equals(annParam)).count());
```
```
//@ ensures annotationClass.getAnnotation(Retention.class).value() != RetentionPolicy.RUNTIME ==> (\result != null && \result.isEmpty());
//@ ensures annotationClass.getAnnotation(Retention.class).value() == RetentionPolicy.RUNTIME ==> \result != null;
//@ ensures annotationClass.getAnnotation(Retention.class).value() == RetentionPolicy.RUNTIME ==> java.util.Arrays.asList(annotationClass.getAnnotation(Target.class).value()).containsAll(\result.keySet());
//@ ensures annotationClass.getAnnotation(Retention.class).value() == RetentionPolicy.RUNTIME && java.util.Arrays.asList(annotationClass.getAnnotation(Target.class).value()).contains(ElementType.PARAMETER) ==> (\result.containsKey(ElementType.PARAMETER) <==> java.util.Arrays.stream(method.getParameterAnnotations()).flatMap(arr -> java.util.Arrays.stream(arr)).anyMatch(ann -> annotationClass.equals(ann.annotationType())));
//@ ensures annotationClass.getAnnotation(Retention.class).value() == RetentionPolicy.RUNTIME && java.util.Arrays.asList(annotationClass.getAnnotation(Target.class).value()).contains(ElementType.METHOD) ==> (\result.containsKey(ElementType.METHOD) <==> (org.springframework.core.annotation.AnnotationUtils.findAnnotation(method, annotationClass) != null));
//@ ensures annotationClass.getAnnotation(Retention.class).value() == RetentionPolicy.RUNTIME && java.util.Arrays.asList(annotationClass.getAnnotation(Target.class).value()).contains(ElementType.TYPE) ==> (\result.containsKey(ElementType.TYPE) <==> (org.springframework.core.annotation.AnnotationUtils.findAnnotation(method.getDeclaringClass(), annotationClass) != null));
//@ ensures annotationClass.getAnnotation(Retention.class).value() == RetentionPolicy.RUNTIME ==> \result.values().stream().allMatch(lst -> lst != null && lst.stream().allMatch(a -> a != null && annotationClass.equals(a.annotationType())));
```
[15, 17, 18, 38, 46, 47, 48]
===== 15 =====
```
 
                     for (Annotation[] annotations : parameterAnnotations) {
 
-                        for (Annotation annotation : annotations) {
+                        for (Annotation annotation : method.getAnnotations()) {
 
                             if (annotationClass.equals(annotation.annotationType())) {
```
```
    /**
     * Find specified {@link Annotation} type maps from {@link Method}
     *
     * @param method          {@link Method}
     * @param annotationClass {@link Annotation} type
     * @param <A>             {@link Annotation} type
     * @return {@link Annotation} type maps , the {@link ElementType} as key ,
     * the list of {@link Annotation} as value.
     * If {@link Annotation} was annotated on {@link Method}'s parameters{@link ElementType#PARAMETER} ,
     * the associated {@link Annotation} list may contain multiple elements.
     */
    public static <A extends Annotation> Map<ElementType, List<A>> findAnnotations(Method method,
                                                                                   Class<A> annotationClass) {

        Retention retention = annotationClass.getAnnotation(Retention.class);

        RetentionPolicy retentionPolicy = retention.value();

        if (!RetentionPolicy.RUNTIME.equals(retentionPolicy)) {
            return Collections.emptyMap();
        }

        Map<ElementType, List<A>> annotationsMap = new LinkedHashMap<ElementType, List<A>>();

        Target target = annotationClass.getAnnotation(Target.class);

        ElementType[] elementTypes = target.value();


        for (ElementType elementType : elementTypes) {

            List<A> annotationsList = new LinkedList<A>();

            switch (elementType) {

                case PARAMETER:

                    Annotation[][] parameterAnnotations = method.getParameterAnnotations();

                    for (Annotation[] annotations : parameterAnnotations) {

                        for (Annotation annotation : method.getAnnotations()) {

                            if (annotationClass.equals(annotation.annotationType())) {

                                annotationsList.add((A) annotation);

                            }

                        }

                    }

                    break;

                case METHOD:

                    A annotation = findAnnotation(method, annotationClass);

                    if (annotation != null) {

                        annotationsList.add(annotation);

                    }

                    break;

                case TYPE:

                    Class<?> beanType = method.getDeclaringClass();

                    A annotation2 = findAnnotation(beanType, annotationClass);

                    if (annotation2 != null) {

                        annotationsList.add(annotation2);

                    }

                    break;

            }

            if (!annotationsList.isEmpty()) {

                annotationsMap.put(elementType, annotationsList);

            }


        }

        return Collections.unmodifiableMap(annotationsMap);

    }
```
===== 17 =====
```
 
                     for (Annotation[] annotations : parameterAnnotations) {
 
-                        for (Annotation annotation : annotations) {
+                        for (Annotation annotation : parameterAnnotations[0]) {
 
                             if (annotationClass.equals(annotation.annotationType())) {
```
```
    /**
     * Find specified {@link Annotation} type maps from {@link Method}
     *
     * @param method          {@link Method}
     * @param annotationClass {@link Annotation} type
     * @param <A>             {@link Annotation} type
     * @return {@link Annotation} type maps , the {@link ElementType} as key ,
     * the list of {@link Annotation} as value.
     * If {@link Annotation} was annotated on {@link Method}'s parameters{@link ElementType#PARAMETER} ,
     * the associated {@link Annotation} list may contain multiple elements.
     */
    public static <A extends Annotation> Map<ElementType, List<A>> findAnnotations(Method method,
                                                                                   Class<A> annotationClass) {

        Retention retention = annotationClass.getAnnotation(Retention.class);

        RetentionPolicy retentionPolicy = retention.value();

        if (!RetentionPolicy.RUNTIME.equals(retentionPolicy)) {
            return Collections.emptyMap();
        }

        Map<ElementType, List<A>> annotationsMap = new LinkedHashMap<ElementType, List<A>>();

        Target target = annotationClass.getAnnotation(Target.class);

        ElementType[] elementTypes = target.value();


        for (ElementType elementType : elementTypes) {

            List<A> annotationsList = new LinkedList<A>();

            switch (elementType) {

                case PARAMETER:

                    Annotation[][] parameterAnnotations = method.getParameterAnnotations();

                    for (Annotation[] annotations : parameterAnnotations) {

                        for (Annotation annotation : parameterAnnotations[0]) {

                            if (annotationClass.equals(annotation.annotationType())) {

                                annotationsList.add((A) annotation);

                            }

                        }

                    }

                    break;

                case METHOD:

                    A annotation = findAnnotation(method, annotationClass);

                    if (annotation != null) {

                        annotationsList.add(annotation);

                    }

                    break;

                case TYPE:

                    Class<?> beanType = method.getDeclaringClass();

                    A annotation2 = findAnnotation(beanType, annotationClass);

                    if (annotation2 != null) {

                        annotationsList.add(annotation2);

                    }

                    break;

            }

            if (!annotationsList.isEmpty()) {

                annotationsMap.put(elementType, annotationsList);

            }


        }

        return Collections.unmodifiableMap(annotationsMap);

    }
```
===== 18 =====
```
 
                     for (Annotation[] annotations : parameterAnnotations) {
 
-                        for (Annotation annotation : annotations) {
+                        for (int i = 0; i < parameterAnnotations.length; i++) { Annotation annotation = parameterAnnotations[i][0];
 
                             if (annotationClass.equals(annotation.annotationType())) {
```
```
    /**
     * Find specified {@link Annotation} type maps from {@link Method}
     *
     * @param method          {@link Method}
     * @param annotationClass {@link Annotation} type
     * @param <A>             {@link Annotation} type
     * @return {@link Annotation} type maps , the {@link ElementType} as key ,
     * the list of {@link Annotation} as value.
     * If {@link Annotation} was annotated on {@link Method}'s parameters{@link ElementType#PARAMETER} ,
     * the associated {@link Annotation} list may contain multiple elements.
     */
    public static <A extends Annotation> Map<ElementType, List<A>> findAnnotations(Method method,
                                                                                   Class<A> annotationClass) {

        Retention retention = annotationClass.getAnnotation(Retention.class);

        RetentionPolicy retentionPolicy = retention.value();

        if (!RetentionPolicy.RUNTIME.equals(retentionPolicy)) {
            return Collections.emptyMap();
        }

        Map<ElementType, List<A>> annotationsMap = new LinkedHashMap<ElementType, List<A>>();

        Target target = annotationClass.getAnnotation(Target.class);

        ElementType[] elementTypes = target.value();


        for (ElementType elementType : elementTypes) {

            List<A> annotationsList = new LinkedList<A>();

            switch (elementType) {

                case PARAMETER:

                    Annotation[][] parameterAnnotations = method.getParameterAnnotations();

                    for (Annotation[] annotations : parameterAnnotations) {

                        for (int i = 0; i < parameterAnnotations.length; i++) { Annotation annotation = parameterAnnotations[i][0];

                            if (annotationClass.equals(annotation.annotationType())) {

                                annotationsList.add((A) annotation);

                            }

                        }

                    }

                    break;

                case METHOD:

                    A annotation = findAnnotation(method, annotationClass);

                    if (annotation != null) {

                        annotationsList.add(annotation);

                    }

                    break;

                case TYPE:

                    Class<?> beanType = method.getDeclaringClass();

                    A annotation2 = findAnnotation(beanType, annotationClass);

                    if (annotation2 != null) {

                        annotationsList.add(annotation2);

                    }

                    break;

            }

            if (!annotationsList.isEmpty()) {

                annotationsMap.put(elementType, annotationsList);

            }


        }

        return Collections.unmodifiableMap(annotationsMap);

    }
```
===== 38 =====
```
 
                     if (annotation2 != null) {
 
-                        annotationsList.add(annotation2);
+                        annotationsList.add(annotation2); annotationsList.add(annotation2);
 
                     }
```
```
    /**
     * Find specified {@link Annotation} type maps from {@link Method}
     *
     * @param method          {@link Method}
     * @param annotationClass {@link Annotation} type
     * @param <A>             {@link Annotation} type
     * @return {@link Annotation} type maps , the {@link ElementType} as key ,
     * the list of {@link Annotation} as value.
     * If {@link Annotation} was annotated on {@link Method}'s parameters{@link ElementType#PARAMETER} ,
     * the associated {@link Annotation} list may contain multiple elements.
     */
    public static <A extends Annotation> Map<ElementType, List<A>> findAnnotations(Method method,
                                                                                   Class<A> annotationClass) {

        Retention retention = annotationClass.getAnnotation(Retention.class);

        RetentionPolicy retentionPolicy = retention.value();

        if (!RetentionPolicy.RUNTIME.equals(retentionPolicy)) {
            return Collections.emptyMap();
        }

        Map<ElementType, List<A>> annotationsMap = new LinkedHashMap<ElementType, List<A>>();

        Target target = annotationClass.getAnnotation(Target.class);

        ElementType[] elementTypes = target.value();


        for (ElementType elementType : elementTypes) {

            List<A> annotationsList = new LinkedList<A>();

            switch (elementType) {

                case PARAMETER:

                    Annotation[][] parameterAnnotations = method.getParameterAnnotations();

                    for (Annotation[] annotations : parameterAnnotations) {

                        for (Annotation annotation : annotations) {

                            if (annotationClass.equals(annotation.annotationType())) {

                                annotationsList.add((A) annotation);

                            }

                        }

                    }

                    break;

                case METHOD:

                    A annotation = findAnnotation(method, annotationClass);

                    if (annotation != null) {

                        annotationsList.add(annotation);

                    }

                    break;

                case TYPE:

                    Class<?> beanType = method.getDeclaringClass();

                    A annotation2 = findAnnotation(beanType, annotationClass);

                    if (annotation2 != null) {

                        annotationsList.add(annotation2); annotationsList.add(annotation2);

                    }

                    break;

            }

            if (!annotationsList.isEmpty()) {

                annotationsMap.put(elementType, annotationsList);

            }


        }

        return Collections.unmodifiableMap(annotationsMap);

    }
```
===== 46 =====
```
 
             if (!annotationsList.isEmpty()) {
 
-                annotationsMap.put(elementType, annotationsList);
+                annotationsMap.put(elementType, Collections.emptyList());
 
             }
```
```
    /**
     * Find specified {@link Annotation} type maps from {@link Method}
     *
     * @param method          {@link Method}
     * @param annotationClass {@link Annotation} type
     * @param <A>             {@link Annotation} type
     * @return {@link Annotation} type maps , the {@link ElementType} as key ,
     * the list of {@link Annotation} as value.
     * If {@link Annotation} was annotated on {@link Method}'s parameters{@link ElementType#PARAMETER} ,
     * the associated {@link Annotation} list may contain multiple elements.
     */
    public static <A extends Annotation> Map<ElementType, List<A>> findAnnotations(Method method,
                                                                                   Class<A> annotationClass) {

        Retention retention = annotationClass.getAnnotation(Retention.class);

        RetentionPolicy retentionPolicy = retention.value();

        if (!RetentionPolicy.RUNTIME.equals(retentionPolicy)) {
            return Collections.emptyMap();
        }

        Map<ElementType, List<A>> annotationsMap = new LinkedHashMap<ElementType, List<A>>();

        Target target = annotationClass.getAnnotation(Target.class);

        ElementType[] elementTypes = target.value();


        for (ElementType elementType : elementTypes) {

            List<A> annotationsList = new LinkedList<A>();

            switch (elementType) {

                case PARAMETER:

                    Annotation[][] parameterAnnotations = method.getParameterAnnotations();

                    for (Annotation[] annotations : parameterAnnotations) {

                        for (Annotation annotation : annotations) {

                            if (annotationClass.equals(annotation.annotationType())) {

                                annotationsList.add((A) annotation);

                            }

                        }

                    }

                    break;

                case METHOD:

                    A annotation = findAnnotation(method, annotationClass);

                    if (annotation != null) {

                        annotationsList.add(annotation);

                    }

                    break;

                case TYPE:

                    Class<?> beanType = method.getDeclaringClass();

                    A annotation2 = findAnnotation(beanType, annotationClass);

                    if (annotation2 != null) {

                        annotationsList.add(annotation2);

                    }

                    break;

            }

            if (!annotationsList.isEmpty()) {

                annotationsMap.put(elementType, Collections.emptyList());

            }


        }

        return Collections.unmodifiableMap(annotationsMap);

    }
```
===== 47 =====
```
 
             if (!annotationsList.isEmpty()) {
 
-                annotationsMap.put(elementType, annotationsList);
+                annotationsMap.put(elementType, annotationsList.subList(0, 1)); // only adds the first annotation, if any
 
             }
```
```
    /**
     * Find specified {@link Annotation} type maps from {@link Method}
     *
     * @param method          {@link Method}
     * @param annotationClass {@link Annotation} type
     * @param <A>             {@link Annotation} type
     * @return {@link Annotation} type maps , the {@link ElementType} as key ,
     * the list of {@link Annotation} as value.
     * If {@link Annotation} was annotated on {@link Method}'s parameters{@link ElementType#PARAMETER} ,
     * the associated {@link Annotation} list may contain multiple elements.
     */
    public static <A extends Annotation> Map<ElementType, List<A>> findAnnotations(Method method,
                                                                                   Class<A> annotationClass) {

        Retention retention = annotationClass.getAnnotation(Retention.class);

        RetentionPolicy retentionPolicy = retention.value();

        if (!RetentionPolicy.RUNTIME.equals(retentionPolicy)) {
            return Collections.emptyMap();
        }

        Map<ElementType, List<A>> annotationsMap = new LinkedHashMap<ElementType, List<A>>();

        Target target = annotationClass.getAnnotation(Target.class);

        ElementType[] elementTypes = target.value();


        for (ElementType elementType : elementTypes) {

            List<A> annotationsList = new LinkedList<A>();

            switch (elementType) {

                case PARAMETER:

                    Annotation[][] parameterAnnotations = method.getParameterAnnotations();

                    for (Annotation[] annotations : parameterAnnotations) {

                        for (Annotation annotation : annotations) {

                            if (annotationClass.equals(annotation.annotationType())) {

                                annotationsList.add((A) annotation);

                            }

                        }

                    }

                    break;

                case METHOD:

                    A annotation = findAnnotation(method, annotationClass);

                    if (annotation != null) {

                        annotationsList.add(annotation);

                    }

                    break;

                case TYPE:

                    Class<?> beanType = method.getDeclaringClass();

                    A annotation2 = findAnnotation(beanType, annotationClass);

                    if (annotation2 != null) {

                        annotationsList.add(annotation2);

                    }

                    break;

            }

            if (!annotationsList.isEmpty()) {

                annotationsMap.put(elementType, annotationsList.subList(0, 1)); // only adds the first annotation, if any

            }


        }

        return Collections.unmodifiableMap(annotationsMap);

    }
```
===== 48 =====
```
 
             if (!annotationsList.isEmpty()) {
 
-                annotationsMap.put(elementType, annotationsList);
+                annotationsMap.put(elementType, new LinkedList<A>()); // creates a new empty list instead of using annotationsList
 
             }
```
```
    /**
     * Find specified {@link Annotation} type maps from {@link Method}
     *
     * @param method          {@link Method}
     * @param annotationClass {@link Annotation} type
     * @param <A>             {@link Annotation} type
     * @return {@link Annotation} type maps , the {@link ElementType} as key ,
     * the list of {@link Annotation} as value.
     * If {@link Annotation} was annotated on {@link Method}'s parameters{@link ElementType#PARAMETER} ,
     * the associated {@link Annotation} list may contain multiple elements.
     */
    public static <A extends Annotation> Map<ElementType, List<A>> findAnnotations(Method method,
                                                                                   Class<A> annotationClass) {

        Retention retention = annotationClass.getAnnotation(Retention.class);

        RetentionPolicy retentionPolicy = retention.value();

        if (!RetentionPolicy.RUNTIME.equals(retentionPolicy)) {
            return Collections.emptyMap();
        }

        Map<ElementType, List<A>> annotationsMap = new LinkedHashMap<ElementType, List<A>>();

        Target target = annotationClass.getAnnotation(Target.class);

        ElementType[] elementTypes = target.value();


        for (ElementType elementType : elementTypes) {

            List<A> annotationsList = new LinkedList<A>();

            switch (elementType) {

                case PARAMETER:

                    Annotation[][] parameterAnnotations = method.getParameterAnnotations();

                    for (Annotation[] annotations : parameterAnnotations) {

                        for (Annotation annotation : annotations) {

                            if (annotationClass.equals(annotation.annotationType())) {

                                annotationsList.add((A) annotation);

                            }

                        }

                    }

                    break;

                case METHOD:

                    A annotation = findAnnotation(method, annotationClass);

                    if (annotation != null) {

                        annotationsList.add(annotation);

                    }

                    break;

                case TYPE:

                    Class<?> beanType = method.getDeclaringClass();

                    A annotation2 = findAnnotation(beanType, annotationClass);

                    if (annotation2 != null) {

                        annotationsList.add(annotation2);

                    }

                    break;

            }

            if (!annotationsList.isEmpty()) {

                annotationsMap.put(elementType, new LinkedList<A>()); // creates a new empty list instead of using annotationsList

            }


        }

        return Collections.unmodifiableMap(annotationsMap);

    }
```
