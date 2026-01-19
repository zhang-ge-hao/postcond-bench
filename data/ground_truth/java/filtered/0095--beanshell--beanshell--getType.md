https://github.com/beanshell/beanshell/blob/eee36c81c35525fd771285e77b6fb8173db3f1dc/./src/main/java/bsh/Primitive.java#L160-L176
```
🈚️

wrong originally.
No error message output for this repo.

//@ ensures (this == Primitive.VOID) ==> (\result == Void.TYPE);
//@ ensures (this == Primitive.NULL) ==> (\result == null);
//@ ensures (this != Primitive.VOID && this != Primitive.NULL) ==> (\result != Void.TYPE && \result != null);
//@ ensures (this != Primitive.VOID && this != Primitive.NULL && value instanceof Boolean) ==> (\result == Boolean.TYPE);
//@ ensures (this != Primitive.VOID && this != Primitive.NULL && value instanceof Byte) ==> (\result == Byte.TYPE);
//@ ensures (this != Primitive.VOID && this != Primitive.NULL && value instanceof Short) ==> (\result == Short.TYPE);
//@ ensures (this != Primitive.VOID && this != Primitive.NULL && value instanceof Character) ==> (\result == Character.TYPE);
//@ ensures (this != Primitive.VOID && this != Primitive.NULL && value instanceof Integer) ==> (\result == Integer.TYPE);
//@ ensures (this != Primitive.VOID && this != Primitive.NULL && value instanceof Long) ==> (\result == Long.TYPE);
//@ ensures (this != Primitive.VOID && this != Primitive.NULL && value instanceof Float) ==> (\result == Float.TYPE);
//@ ensures (this != Primitive.VOID && this != Primitive.NULL && value instanceof Double) ==> (\result == Double.TYPE);
//@ ensures (this != Primitive.VOID && this != Primitive.NULL && value instanceof BigInteger) ==> (\result == BigInteger.class);
//@ ensures (this != Primitive.VOID && this != Primitive.NULL && value instanceof BigDecimal) ==> (\result == BigDecimal.class);
```
```
//@ ensures (\result == Void.TYPE) <==> (this == Primitive.VOID);
//@ ensures (\result == null) <==> (this == Primitive.NULL);
//@ ensures (this != Primitive.VOID && this != Primitive.NULL) ==> (\result == unboxType(value.getClass()));
//@ ensures (this != Primitive.VOID && this != Primitive.NULL) ==> (\result != Void.TYPE && \result != null);
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
===== 0 =====
```
     */
     public Class<?> getType()
     {
-        if ( this == Primitive.VOID )
+        if ( this != Primitive.VOID )
             return Void.TYPE;
 
         // NULL return null as type... we currently use null type to indicate
```
```
    /**
        Get the corresponding Java primitive TYPE class for this Primitive.
        @return the primitive TYPE class type of the value or Void.TYPE for
        Primitive.VOID or null value for type of Primitive.NULL
    */
    public Class<?> getType()
    {
        if ( this != Primitive.VOID )
            return Void.TYPE;

        // NULL return null as type... we currently use null type to indicate
        // loose typing throughout bsh.
        if ( this == Primitive.NULL )
            return null;

        return unboxType( value.getClass() );
    }
```
===== 1 =====
```
     */
     public Class<?> getType()
     {
-        if ( this == Primitive.VOID )
+        if ( this == Primitive.NULL )
             return Void.TYPE;
 
         // NULL return null as type... we currently use null type to indicate
```
```
    /**
        Get the corresponding Java primitive TYPE class for this Primitive.
        @return the primitive TYPE class type of the value or Void.TYPE for
        Primitive.VOID or null value for type of Primitive.NULL
    */
    public Class<?> getType()
    {
        if ( this == Primitive.NULL )
            return Void.TYPE;

        // NULL return null as type... we currently use null type to indicate
        // loose typing throughout bsh.
        if ( this == Primitive.NULL )
            return null;

        return unboxType( value.getClass() );
    }
```
===== 2 =====
```
     */
     public Class<?> getType()
     {
-        if ( this == Primitive.VOID )
+        if ( this == Primitive.TRUE )
             return Void.TYPE;
 
         // NULL return null as type... we currently use null type to indicate
```
```
    /**
        Get the corresponding Java primitive TYPE class for this Primitive.
        @return the primitive TYPE class type of the value or Void.TYPE for
        Primitive.VOID or null value for type of Primitive.NULL
    */
    public Class<?> getType()
    {
        if ( this == Primitive.TRUE )
            return Void.TYPE;

        // NULL return null as type... we currently use null type to indicate
        // loose typing throughout bsh.
        if ( this == Primitive.NULL )
            return null;

        return unboxType( value.getClass() );
    }
```
===== 3 =====
```
     */
     public Class<?> getType()
     {
-        if ( this == Primitive.VOID )
+        if ( this.value instanceof Number )
             return Void.TYPE;
 
         // NULL return null as type... we currently use null type to indicate
```
```
    /**
        Get the corresponding Java primitive TYPE class for this Primitive.
        @return the primitive TYPE class type of the value or Void.TYPE for
        Primitive.VOID or null value for type of Primitive.NULL
    */
    public Class<?> getType()
    {
        if ( this.value instanceof Number )
            return Void.TYPE;

        // NULL return null as type... we currently use null type to indicate
        // loose typing throughout bsh.
        if ( this == Primitive.NULL )
            return null;

        return unboxType( value.getClass() );
    }
```
===== 4 =====
```
 
         // NULL return null as type... we currently use null type to indicate
         // loose typing throughout bsh.
-        if ( this == Primitive.NULL )
+        if ( this != Primitive.NULL )
             return null;
 
         return unboxType( value.getClass() );
```
```
    /**
        Get the corresponding Java primitive TYPE class for this Primitive.
        @return the primitive TYPE class type of the value or Void.TYPE for
        Primitive.VOID or null value for type of Primitive.NULL
    */
    public Class<?> getType()
    {
        if ( this == Primitive.VOID )
            return Void.TYPE;

        // NULL return null as type... we currently use null type to indicate
        // loose typing throughout bsh.
        if ( this != Primitive.NULL )
            return null;

        return unboxType( value.getClass() );
    }
```
===== 5 =====
```
 
         // NULL return null as type... we currently use null type to indicate
         // loose typing throughout bsh.
-        if ( this == Primitive.NULL )
+        if ( this == Primitive.FALSE )
             return null;
 
         return unboxType( value.getClass() );
```
```
    /**
        Get the corresponding Java primitive TYPE class for this Primitive.
        @return the primitive TYPE class type of the value or Void.TYPE for
        Primitive.VOID or null value for type of Primitive.NULL
    */
    public Class<?> getType()
    {
        if ( this == Primitive.VOID )
            return Void.TYPE;

        // NULL return null as type... we currently use null type to indicate
        // loose typing throughout bsh.
        if ( this == Primitive.FALSE )
            return null;

        return unboxType( value.getClass() );
    }
```
===== 6 =====
```
 
         // NULL return null as type... we currently use null type to indicate
         // loose typing throughout bsh.
-        if ( this == Primitive.NULL )
+        if ( this == Primitive.TRUE )
             return null;
 
         return unboxType( value.getClass() );
```
```
    /**
        Get the corresponding Java primitive TYPE class for this Primitive.
        @return the primitive TYPE class type of the value or Void.TYPE for
        Primitive.VOID or null value for type of Primitive.NULL
    */
    public Class<?> getType()
    {
        if ( this == Primitive.VOID )
            return Void.TYPE;

        // NULL return null as type... we currently use null type to indicate
        // loose typing throughout bsh.
        if ( this == Primitive.TRUE )
            return null;

        return unboxType( value.getClass() );
    }
```
===== 7 =====
```
 
         // NULL return null as type... we currently use null type to indicate
         // loose typing throughout bsh.
-        if ( this == Primitive.NULL )
+        if ( this == Primitive.VOID )
             return null;
 
         return unboxType( value.getClass() );
```
```
    /**
        Get the corresponding Java primitive TYPE class for this Primitive.
        @return the primitive TYPE class type of the value or Void.TYPE for
        Primitive.VOID or null value for type of Primitive.NULL
    */
    public Class<?> getType()
    {
        if ( this == Primitive.VOID )
            return Void.TYPE;

        // NULL return null as type... we currently use null type to indicate
        // loose typing throughout bsh.
        if ( this == Primitive.VOID )
            return null;

        return unboxType( value.getClass() );
    }
```
===== 8 =====
```
 
         // NULL return null as type... we currently use null type to indicate
         // loose typing throughout bsh.
-        if ( this == Primitive.NULL )
+        if ( this == Primitive.ZERO_DOUBLE )
             return null;
 
         return unboxType( value.getClass() );
```
```
    /**
        Get the corresponding Java primitive TYPE class for this Primitive.
        @return the primitive TYPE class type of the value or Void.TYPE for
        Primitive.VOID or null value for type of Primitive.NULL
    */
    public Class<?> getType()
    {
        if ( this == Primitive.VOID )
            return Void.TYPE;

        // NULL return null as type... we currently use null type to indicate
        // loose typing throughout bsh.
        if ( this == Primitive.ZERO_DOUBLE )
            return null;

        return unboxType( value.getClass() );
    }
```
===== 9 =====
```
 
         // NULL return null as type... we currently use null type to indicate
         // loose typing throughout bsh.
-        if ( this == Primitive.NULL )
+        if ( this == Primitive.ZERO_INT )
             return null;
 
         return unboxType( value.getClass() );
```
```
    /**
        Get the corresponding Java primitive TYPE class for this Primitive.
        @return the primitive TYPE class type of the value or Void.TYPE for
        Primitive.VOID or null value for type of Primitive.NULL
    */
    public Class<?> getType()
    {
        if ( this == Primitive.VOID )
            return Void.TYPE;

        // NULL return null as type... we currently use null type to indicate
        // loose typing throughout bsh.
        if ( this == Primitive.ZERO_INT )
            return null;

        return unboxType( value.getClass() );
    }
```
===== 10 =====
```
         if ( this == Primitive.NULL )
             return null;
 
-        return unboxType( value.getClass() );
+        return Boolean.class; // This will incorrectly assume all primitives are of type Boolean, leading to faulty behavior.
     }
```
```
    /**
        Get the corresponding Java primitive TYPE class for this Primitive.
        @return the primitive TYPE class type of the value or Void.TYPE for
        Primitive.VOID or null value for type of Primitive.NULL
    */
    public Class<?> getType()
    {
        if ( this == Primitive.VOID )
            return Void.TYPE;

        // NULL return null as type... we currently use null type to indicate
        // loose typing throughout bsh.
        if ( this == Primitive.NULL )
            return null;

        return Boolean.class; // This will incorrectly assume all primitives are of type Boolean, leading to faulty behavior.
    }
```
===== 11 =====
```
         if ( this == Primitive.NULL )
             return null;
 
-        return unboxType( value.getClass() );
+        return Object.class; // This will incorrectly indicate that the type is Object, causing type mismatches.
     }
```
```
    /**
        Get the corresponding Java primitive TYPE class for this Primitive.
        @return the primitive TYPE class type of the value or Void.TYPE for
        Primitive.VOID or null value for type of Primitive.NULL
    */
    public Class<?> getType()
    {
        if ( this == Primitive.VOID )
            return Void.TYPE;

        // NULL return null as type... we currently use null type to indicate
        // loose typing throughout bsh.
        if ( this == Primitive.NULL )
            return null;

        return Object.class; // This will incorrectly indicate that the type is Object, causing type mismatches.
    }
```
===== 12 =====
```
         if ( this == Primitive.NULL )
             return null;
 
-        return unboxType( value.getClass() );
+        return Primitive.class; // This will return the class of the Primitive wrapper itself, which is not useful for determining the primitive type.
     }
```
```
    /**
        Get the corresponding Java primitive TYPE class for this Primitive.
        @return the primitive TYPE class type of the value or Void.TYPE for
        Primitive.VOID or null value for type of Primitive.NULL
    */
    public Class<?> getType()
    {
        if ( this == Primitive.VOID )
            return Void.TYPE;

        // NULL return null as type... we currently use null type to indicate
        // loose typing throughout bsh.
        if ( this == Primitive.NULL )
            return null;

        return Primitive.class; // This will return the class of the Primitive wrapper itself, which is not useful for determining the primitive type.
    }
```
===== 13 =====
```
         if ( this == Primitive.NULL )
             return null;
 
-        return unboxType( value.getClass() );
+        return null;
     }
```
```
    /**
        Get the corresponding Java primitive TYPE class for this Primitive.
        @return the primitive TYPE class type of the value or Void.TYPE for
        Primitive.VOID or null value for type of Primitive.NULL
    */
    public Class<?> getType()
    {
        if ( this == Primitive.VOID )
            return Void.TYPE;

        // NULL return null as type... we currently use null type to indicate
        // loose typing throughout bsh.
        if ( this == Primitive.NULL )
            return null;

        return null;
    }
```
===== 14 =====
```
         if ( this == Primitive.NULL )
             return null;
 
-        return unboxType( value.getClass() );
+        return null; // This will cause a NullPointerException when the type is accessed later.
     }
```
```
    /**
        Get the corresponding Java primitive TYPE class for this Primitive.
        @return the primitive TYPE class type of the value or Void.TYPE for
        Primitive.VOID or null value for type of Primitive.NULL
    */
    public Class<?> getType()
    {
        if ( this == Primitive.VOID )
            return Void.TYPE;

        // NULL return null as type... we currently use null type to indicate
        // loose typing throughout bsh.
        if ( this == Primitive.NULL )
            return null;

        return null; // This will cause a NullPointerException when the type is accessed later.
    }
```
===== 15 =====
```
         if ( this == Primitive.NULL )
             return null;
 
-        return unboxType( value.getClass() );
+        return value.getClass(); // This returns the actual class instead of the primitive type, leading to incorrect type handling.
     }
```
```
    /**
        Get the corresponding Java primitive TYPE class for this Primitive.
        @return the primitive TYPE class type of the value or Void.TYPE for
        Primitive.VOID or null value for type of Primitive.NULL
    */
    public Class<?> getType()
    {
        if ( this == Primitive.VOID )
            return Void.TYPE;

        // NULL return null as type... we currently use null type to indicate
        // loose typing throughout bsh.
        if ( this == Primitive.NULL )
            return null;

        return value.getClass(); // This returns the actual class instead of the primitive type, leading to incorrect type handling.
    }
```
