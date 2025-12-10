https://github.com/beanshell/beanshell/blob/eee36c81c35525fd771285e77b6fb8173db3f1dc/./src/main/java/bsh/classpath/BshClassPath.java#L520-L536
```
//@ ensures \result != null;
//@ ensures java.util.Arrays.stream(\result).noneMatch(s -> s == null || s.length() == 0);
//@ ensures java.util.Arrays.stream(\result).allMatch(s -> canonicalizeClassName(s).equals(s));
//@ ensures java.util.Arrays.stream(\result).allMatch(s -> !s.endsWith(".class"));
//@ ensures java.util.Arrays.equals(java.util.Arrays.stream(\result).sorted().toArray(String[]::new), java.util.Arrays.stream(searchJarFSForClasses(new java.net.URL("jar:"+url.toExternalForm()+"!/"))).sorted().toArray(String[]::new));
```
```
//@ ensures \result != null;
//@ ensures \result.length > 0;
//@ ensures java.util.Arrays.stream(\result).noneMatch(s -> s == null || s.length() == 0);
//@ ensures java.util.Arrays.stream(\result).allMatch(s -> canonicalizeClassName(s).equals(s));
//@ ensures java.util.Arrays.stream(\result).allMatch(s -> !s.endsWith(".class"));
```
[4, 6, 8]
===== 4 =====
```
         ZipEntry ze;
         while( zip.available() == 1 )
             if ( (ze = zip.getNextEntry()) != null
-                    && isClassFileName( ze.getName() ) )
+                    && !isClassFileName( ze.getName() ) )
                 list.add( canonicalizeClassName( ze.getName() ) );
         zip.close();
```
```
    /** Search Archive for classes.
     * @param url the archive file location
     * @return array of class names found
     * @throws IOException of any reading problems  */
    static String[] searchArchiveForClasses( URL url ) throws IOException {
        List<String> list = new ArrayList<>();
        ZipInputStream zip = new ZipInputStream(url.openStream());

        ZipEntry ze;
        while( zip.available() == 1 )
            if ( (ze = zip.getNextEntry()) != null
                    && !isClassFileName( ze.getName() ) )
                list.add( canonicalizeClassName( ze.getName() ) );
        zip.close();

        return list.toArray( new String[list.size()] );
    }
```
===== 6 =====
```
         ZipEntry ze;
         while( zip.available() == 1 )
             if ( (ze = zip.getNextEntry()) != null
-                    && isClassFileName( ze.getName() ) )
+                    && isClassFileName( ze.getName() ) && ze.getName().contains("Test") )
                 list.add( canonicalizeClassName( ze.getName() ) );
         zip.close();
```
```
    /** Search Archive for classes.
     * @param url the archive file location
     * @return array of class names found
     * @throws IOException of any reading problems  */
    static String[] searchArchiveForClasses( URL url ) throws IOException {
        List<String> list = new ArrayList<>();
        ZipInputStream zip = new ZipInputStream(url.openStream());

        ZipEntry ze;
        while( zip.available() == 1 )
            if ( (ze = zip.getNextEntry()) != null
                    && isClassFileName( ze.getName() ) && ze.getName().contains("Test") )
                list.add( canonicalizeClassName( ze.getName() ) );
        zip.close();

        return list.toArray( new String[list.size()] );
    }
```
===== 8 =====
```
         while( zip.available() == 1 )
             if ( (ze = zip.getNextEntry()) != null
                     && isClassFileName( ze.getName() ) )
-                list.add( canonicalizeClassName( ze.getName() ) );
+                list.add( canonicalizeClassName( ze.getName().toUpperCase() ) ); // Converts the class name to uppercase, which is incorrect
         zip.close();
 
         return list.toArray( new String[list.size()] );
```
```
    /** Search Archive for classes.
     * @param url the archive file location
     * @return array of class names found
     * @throws IOException of any reading problems  */
    static String[] searchArchiveForClasses( URL url ) throws IOException {
        List<String> list = new ArrayList<>();
        ZipInputStream zip = new ZipInputStream(url.openStream());

        ZipEntry ze;
        while( zip.available() == 1 )
            if ( (ze = zip.getNextEntry()) != null
                    && isClassFileName( ze.getName() ) )
                list.add( canonicalizeClassName( ze.getName().toUpperCase() ) ); // Converts the class name to uppercase, which is incorrect
        zip.close();

        return list.toArray( new String[list.size()] );
    }
```
