https://github.com/beanshell/beanshell/blob/eee36c81c35525fd771285e77b6fb8173db3f1dc/./src/main/java/bsh/Operators.java#L133-L177
```
🈚️

It's hard
```
```
//@ ensures \result != null;
//@ ensures (\old(obj1) instanceof bsh.Primitive && \old(obj2) instanceof bsh.Primitive) ==> (\result instanceof bsh.Primitive);
//@ ensures !(\old(obj1) instanceof bsh.Primitive && \old(obj2) instanceof bsh.Primitive) ==> (!(\result instanceof bsh.Primitive) || \result == bsh.Primitive.TRUE || \result == bsh.Primitive.FALSE)
```
[0, 1, 2, 3, 4, 5, 6, 16, 20, 21, 23, 25]
===== 0 =====
```
             throws UtilEvalError {
 
         // Unwrap primitives
-        Object lhs = Primitive.unwrap(obj1);
+        Object lhs = Primitive.unwrap(obj2); // Unwrapping the second argument instead of the first
         Object rhs = Primitive.unwrap(obj2);
 
         if ( Types.isNumeric(lhs) && Types.isNumeric(rhs) ) {
```
```
    /**
    Perform a binary operation on two Primitives or wrapper types.
    If both original args were Primitives return a Primitive result
    else it was mixed (wrapper/primitive) return the wrapper type.
    The exception is for boolean operations where we will return the
    primitive type either way.
    */
    public static Object binaryOperation(Object obj1, Object obj2, int kind)
            throws UtilEvalError {

        // Unwrap primitives
        Object lhs = Primitive.unwrap(obj2); // Unwrapping the second argument instead of the first
        Object rhs = Primitive.unwrap(obj2);

        if ( Types.isNumeric(lhs) && Types.isNumeric(rhs) ) {
            Object[] operands = promotePrimitives(lhs, rhs);
            lhs = operands[0];
            rhs = operands[1];
        }

        if ( lhs.getClass() != rhs.getClass() )
            throw new UtilEvalError("Type mismatch in operator.  "
                    + lhs.getClass() + " cannot be used with " + rhs.getClass());

        Object result;
        try {
            result = binaryOperationImpl( lhs, rhs, kind );
        } catch (ArithmeticException e) {
            throw new UtilTargetError("Arithemetic Exception in binary op", e);
        }

        if ( result instanceof Boolean )
            return ((Boolean) result).booleanValue() ? Primitive.TRUE : Primitive.FALSE;

        // If both original args were Primitives return a Primitive result
        // else it was mixed (wrapper/primitive) return the wrapper type
        // Exception is for boolean result, return the primitive
        if ( obj1 instanceof Primitive && obj2 instanceof Primitive )
            if ( Types.isFloatingpoint(result) && lhs.getClass() == BigDecimal.class )
                return Primitive.wrap(result, result.getClass());
            else
                return Primitive.shrinkWrap(result);

        return Primitive.shrinkWrap(result).getValue();
    }
```
===== 1 =====
```
 
         // Unwrap primitives
         Object lhs = Primitive.unwrap(obj1);
-        Object rhs = Primitive.unwrap(obj2);
+        Object rhs = Primitive.unwrap(obj1); // This mistakenly unwraps obj1 instead of obj2, potentially causing logic errors.
 
         if ( Types.isNumeric(lhs) && Types.isNumeric(rhs) ) {
             Object[] operands = promotePrimitives(lhs, rhs);
```
```
    /**
    Perform a binary operation on two Primitives or wrapper types.
    If both original args were Primitives return a Primitive result
    else it was mixed (wrapper/primitive) return the wrapper type.
    The exception is for boolean operations where we will return the
    primitive type either way.
    */
    public static Object binaryOperation(Object obj1, Object obj2, int kind)
            throws UtilEvalError {

        // Unwrap primitives
        Object lhs = Primitive.unwrap(obj1);
        Object rhs = Primitive.unwrap(obj1); // This mistakenly unwraps obj1 instead of obj2, potentially causing logic errors.

        if ( Types.isNumeric(lhs) && Types.isNumeric(rhs) ) {
            Object[] operands = promotePrimitives(lhs, rhs);
            lhs = operands[0];
            rhs = operands[1];
        }

        if ( lhs.getClass() != rhs.getClass() )
            throw new UtilEvalError("Type mismatch in operator.  "
                    + lhs.getClass() + " cannot be used with " + rhs.getClass());

        Object result;
        try {
            result = binaryOperationImpl( lhs, rhs, kind );
        } catch (ArithmeticException e) {
            throw new UtilTargetError("Arithemetic Exception in binary op", e);
        }

        if ( result instanceof Boolean )
            return ((Boolean) result).booleanValue() ? Primitive.TRUE : Primitive.FALSE;

        // If both original args were Primitives return a Primitive result
        // else it was mixed (wrapper/primitive) return the wrapper type
        // Exception is for boolean result, return the primitive
        if ( obj1 instanceof Primitive && obj2 instanceof Primitive )
            if ( Types.isFloatingpoint(result) && lhs.getClass() == BigDecimal.class )
                return Primitive.wrap(result, result.getClass());
            else
                return Primitive.shrinkWrap(result);

        return Primitive.shrinkWrap(result).getValue();
    }
```
===== 2 =====
```
         Object rhs = Primitive.unwrap(obj2);
 
         if ( Types.isNumeric(lhs) && Types.isNumeric(rhs) ) {
-            Object[] operands = promotePrimitives(lhs, rhs);
+            Object[] operands = promotePrimitives(lhs, lhs); // Incorrectly promotes lhs with itself instead of lhs and rhs
             lhs = operands[0];
             rhs = operands[1];
         }
```
```
    /**
    Perform a binary operation on two Primitives or wrapper types.
    If both original args were Primitives return a Primitive result
    else it was mixed (wrapper/primitive) return the wrapper type.
    The exception is for boolean operations where we will return the
    primitive type either way.
    */
    public static Object binaryOperation(Object obj1, Object obj2, int kind)
            throws UtilEvalError {

        // Unwrap primitives
        Object lhs = Primitive.unwrap(obj1);
        Object rhs = Primitive.unwrap(obj2);

        if ( Types.isNumeric(lhs) && Types.isNumeric(rhs) ) {
            Object[] operands = promotePrimitives(lhs, lhs); // Incorrectly promotes lhs with itself instead of lhs and rhs
            lhs = operands[0];
            rhs = operands[1];
        }

        if ( lhs.getClass() != rhs.getClass() )
            throw new UtilEvalError("Type mismatch in operator.  "
                    + lhs.getClass() + " cannot be used with " + rhs.getClass());

        Object result;
        try {
            result = binaryOperationImpl( lhs, rhs, kind );
        } catch (ArithmeticException e) {
            throw new UtilTargetError("Arithemetic Exception in binary op", e);
        }

        if ( result instanceof Boolean )
            return ((Boolean) result).booleanValue() ? Primitive.TRUE : Primitive.FALSE;

        // If both original args were Primitives return a Primitive result
        // else it was mixed (wrapper/primitive) return the wrapper type
        // Exception is for boolean result, return the primitive
        if ( obj1 instanceof Primitive && obj2 instanceof Primitive )
            if ( Types.isFloatingpoint(result) && lhs.getClass() == BigDecimal.class )
                return Primitive.wrap(result, result.getClass());
            else
                return Primitive.shrinkWrap(result);

        return Primitive.shrinkWrap(result).getValue();
    }
```
===== 3 =====
```
         Object rhs = Primitive.unwrap(obj2);
 
         if ( Types.isNumeric(lhs) && Types.isNumeric(rhs) ) {
-            Object[] operands = promotePrimitives(lhs, rhs);
+            Object[] operands = promotePrimitives(lhs, new Integer(0)); // Incorrectly promotes rhs to a fixed Integer value instead of the actual rhs
             lhs = operands[0];
             rhs = operands[1];
         }
```
```
    /**
    Perform a binary operation on two Primitives or wrapper types.
    If both original args were Primitives return a Primitive result
    else it was mixed (wrapper/primitive) return the wrapper type.
    The exception is for boolean operations where we will return the
    primitive type either way.
    */
    public static Object binaryOperation(Object obj1, Object obj2, int kind)
            throws UtilEvalError {

        // Unwrap primitives
        Object lhs = Primitive.unwrap(obj1);
        Object rhs = Primitive.unwrap(obj2);

        if ( Types.isNumeric(lhs) && Types.isNumeric(rhs) ) {
            Object[] operands = promotePrimitives(lhs, new Integer(0)); // Incorrectly promotes rhs to a fixed Integer value instead of the actual rhs
            lhs = operands[0];
            rhs = operands[1];
        }

        if ( lhs.getClass() != rhs.getClass() )
            throw new UtilEvalError("Type mismatch in operator.  "
                    + lhs.getClass() + " cannot be used with " + rhs.getClass());

        Object result;
        try {
            result = binaryOperationImpl( lhs, rhs, kind );
        } catch (ArithmeticException e) {
            throw new UtilTargetError("Arithemetic Exception in binary op", e);
        }

        if ( result instanceof Boolean )
            return ((Boolean) result).booleanValue() ? Primitive.TRUE : Primitive.FALSE;

        // If both original args were Primitives return a Primitive result
        // else it was mixed (wrapper/primitive) return the wrapper type
        // Exception is for boolean result, return the primitive
        if ( obj1 instanceof Primitive && obj2 instanceof Primitive )
            if ( Types.isFloatingpoint(result) && lhs.getClass() == BigDecimal.class )
                return Primitive.wrap(result, result.getClass());
            else
                return Primitive.shrinkWrap(result);

        return Primitive.shrinkWrap(result).getValue();
    }
```
===== 4 =====
```
         Object rhs = Primitive.unwrap(obj2);
 
         if ( Types.isNumeric(lhs) && Types.isNumeric(rhs) ) {
-            Object[] operands = promotePrimitives(lhs, rhs);
+            Object[] operands = promotePrimitives(rhs, lhs); // Incorrectly reverses the order of promotion
             lhs = operands[0];
             rhs = operands[1];
         }
```
```
    /**
    Perform a binary operation on two Primitives or wrapper types.
    If both original args were Primitives return a Primitive result
    else it was mixed (wrapper/primitive) return the wrapper type.
    The exception is for boolean operations where we will return the
    primitive type either way.
    */
    public static Object binaryOperation(Object obj1, Object obj2, int kind)
            throws UtilEvalError {

        // Unwrap primitives
        Object lhs = Primitive.unwrap(obj1);
        Object rhs = Primitive.unwrap(obj2);

        if ( Types.isNumeric(lhs) && Types.isNumeric(rhs) ) {
            Object[] operands = promotePrimitives(rhs, lhs); // Incorrectly reverses the order of promotion
            lhs = operands[0];
            rhs = operands[1];
        }

        if ( lhs.getClass() != rhs.getClass() )
            throw new UtilEvalError("Type mismatch in operator.  "
                    + lhs.getClass() + " cannot be used with " + rhs.getClass());

        Object result;
        try {
            result = binaryOperationImpl( lhs, rhs, kind );
        } catch (ArithmeticException e) {
            throw new UtilTargetError("Arithemetic Exception in binary op", e);
        }

        if ( result instanceof Boolean )
            return ((Boolean) result).booleanValue() ? Primitive.TRUE : Primitive.FALSE;

        // If both original args were Primitives return a Primitive result
        // else it was mixed (wrapper/primitive) return the wrapper type
        // Exception is for boolean result, return the primitive
        if ( obj1 instanceof Primitive && obj2 instanceof Primitive )
            if ( Types.isFloatingpoint(result) && lhs.getClass() == BigDecimal.class )
                return Primitive.wrap(result, result.getClass());
            else
                return Primitive.shrinkWrap(result);

        return Primitive.shrinkWrap(result).getValue();
    }
```
===== 5 =====
```
 
         Object result;
         try {
-            result = binaryOperationImpl( lhs, rhs, kind );
+            result = binaryOperationImpl(lhs, lhs, kind); // Using lhs instead of rhs, leading to incorrect results.
         } catch (ArithmeticException e) {
             throw new UtilTargetError("Arithemetic Exception in binary op", e);
         }
```
```
    /**
    Perform a binary operation on two Primitives or wrapper types.
    If both original args were Primitives return a Primitive result
    else it was mixed (wrapper/primitive) return the wrapper type.
    The exception is for boolean operations where we will return the
    primitive type either way.
    */
    public static Object binaryOperation(Object obj1, Object obj2, int kind)
            throws UtilEvalError {

        // Unwrap primitives
        Object lhs = Primitive.unwrap(obj1);
        Object rhs = Primitive.unwrap(obj2);

        if ( Types.isNumeric(lhs) && Types.isNumeric(rhs) ) {
            Object[] operands = promotePrimitives(lhs, rhs);
            lhs = operands[0];
            rhs = operands[1];
        }

        if ( lhs.getClass() != rhs.getClass() )
            throw new UtilEvalError("Type mismatch in operator.  "
                    + lhs.getClass() + " cannot be used with " + rhs.getClass());

        Object result;
        try {
            result = binaryOperationImpl(lhs, lhs, kind); // Using lhs instead of rhs, leading to incorrect results.
        } catch (ArithmeticException e) {
            throw new UtilTargetError("Arithemetic Exception in binary op", e);
        }

        if ( result instanceof Boolean )
            return ((Boolean) result).booleanValue() ? Primitive.TRUE : Primitive.FALSE;

        // If both original args were Primitives return a Primitive result
        // else it was mixed (wrapper/primitive) return the wrapper type
        // Exception is for boolean result, return the primitive
        if ( obj1 instanceof Primitive && obj2 instanceof Primitive )
            if ( Types.isFloatingpoint(result) && lhs.getClass() == BigDecimal.class )
                return Primitive.wrap(result, result.getClass());
            else
                return Primitive.shrinkWrap(result);

        return Primitive.shrinkWrap(result).getValue();
    }
```
===== 6 =====
```
         }
 
         if ( result instanceof Boolean )
-            return ((Boolean) result).booleanValue() ? Primitive.TRUE : Primitive.FALSE;
+            return ((Boolean) result).booleanValue() ? Primitive.FALSE : Primitive.TRUE; // This inverts the boolean result, leading to incorrect behavior.
 
         // If both original args were Primitives return a Primitive result
         // else it was mixed (wrapper/primitive) return the wrapper type
```
```
    /**
    Perform a binary operation on two Primitives or wrapper types.
    If both original args were Primitives return a Primitive result
    else it was mixed (wrapper/primitive) return the wrapper type.
    The exception is for boolean operations where we will return the
    primitive type either way.
    */
    public static Object binaryOperation(Object obj1, Object obj2, int kind)
            throws UtilEvalError {

        // Unwrap primitives
        Object lhs = Primitive.unwrap(obj1);
        Object rhs = Primitive.unwrap(obj2);

        if ( Types.isNumeric(lhs) && Types.isNumeric(rhs) ) {
            Object[] operands = promotePrimitives(lhs, rhs);
            lhs = operands[0];
            rhs = operands[1];
        }

        if ( lhs.getClass() != rhs.getClass() )
            throw new UtilEvalError("Type mismatch in operator.  "
                    + lhs.getClass() + " cannot be used with " + rhs.getClass());

        Object result;
        try {
            result = binaryOperationImpl( lhs, rhs, kind );
        } catch (ArithmeticException e) {
            throw new UtilTargetError("Arithemetic Exception in binary op", e);
        }

        if ( result instanceof Boolean )
            return ((Boolean) result).booleanValue() ? Primitive.FALSE : Primitive.TRUE; // This inverts the boolean result, leading to incorrect behavior.

        // If both original args were Primitives return a Primitive result
        // else it was mixed (wrapper/primitive) return the wrapper type
        // Exception is for boolean result, return the primitive
        if ( obj1 instanceof Primitive && obj2 instanceof Primitive )
            if ( Types.isFloatingpoint(result) && lhs.getClass() == BigDecimal.class )
                return Primitive.wrap(result, result.getClass());
            else
                return Primitive.shrinkWrap(result);

        return Primitive.shrinkWrap(result).getValue();
    }
```
===== 16 =====
```
             if ( Types.isFloatingpoint(result) && lhs.getClass() == BigDecimal.class )
                 return Primitive.wrap(result, result.getClass());
             else
-                return Primitive.shrinkWrap(result);
+                return Primitive.wrap(result, Integer.TYPE); // incorrectly wrapping as Integer
 
         return Primitive.shrinkWrap(result).getValue();
     }
```
```
    /**
    Perform a binary operation on two Primitives or wrapper types.
    If both original args were Primitives return a Primitive result
    else it was mixed (wrapper/primitive) return the wrapper type.
    The exception is for boolean operations where we will return the
    primitive type either way.
    */
    public static Object binaryOperation(Object obj1, Object obj2, int kind)
            throws UtilEvalError {

        // Unwrap primitives
        Object lhs = Primitive.unwrap(obj1);
        Object rhs = Primitive.unwrap(obj2);

        if ( Types.isNumeric(lhs) && Types.isNumeric(rhs) ) {
            Object[] operands = promotePrimitives(lhs, rhs);
            lhs = operands[0];
            rhs = operands[1];
        }

        if ( lhs.getClass() != rhs.getClass() )
            throw new UtilEvalError("Type mismatch in operator.  "
                    + lhs.getClass() + " cannot be used with " + rhs.getClass());

        Object result;
        try {
            result = binaryOperationImpl( lhs, rhs, kind );
        } catch (ArithmeticException e) {
            throw new UtilTargetError("Arithemetic Exception in binary op", e);
        }

        if ( result instanceof Boolean )
            return ((Boolean) result).booleanValue() ? Primitive.TRUE : Primitive.FALSE;

        // If both original args were Primitives return a Primitive result
        // else it was mixed (wrapper/primitive) return the wrapper type
        // Exception is for boolean result, return the primitive
        if ( obj1 instanceof Primitive && obj2 instanceof Primitive )
            if ( Types.isFloatingpoint(result) && lhs.getClass() == BigDecimal.class )
                return Primitive.wrap(result, result.getClass());
            else
                return Primitive.wrap(result, Integer.TYPE); // incorrectly wrapping as Integer

        return Primitive.shrinkWrap(result).getValue();
    }
```
===== 20 =====
```
             else
                 return Primitive.shrinkWrap(result);
 
-        return Primitive.shrinkWrap(result).getValue();
+        return Primitive.shrinkWrap(result).getClass(); // This returns the Class of the result instead of the value, leading to incorrect behavior when the value is expected.
     }
```
```
    /**
    Perform a binary operation on two Primitives or wrapper types.
    If both original args were Primitives return a Primitive result
    else it was mixed (wrapper/primitive) return the wrapper type.
    The exception is for boolean operations where we will return the
    primitive type either way.
    */
    public static Object binaryOperation(Object obj1, Object obj2, int kind)
            throws UtilEvalError {

        // Unwrap primitives
        Object lhs = Primitive.unwrap(obj1);
        Object rhs = Primitive.unwrap(obj2);

        if ( Types.isNumeric(lhs) && Types.isNumeric(rhs) ) {
            Object[] operands = promotePrimitives(lhs, rhs);
            lhs = operands[0];
            rhs = operands[1];
        }

        if ( lhs.getClass() != rhs.getClass() )
            throw new UtilEvalError("Type mismatch in operator.  "
                    + lhs.getClass() + " cannot be used with " + rhs.getClass());

        Object result;
        try {
            result = binaryOperationImpl( lhs, rhs, kind );
        } catch (ArithmeticException e) {
            throw new UtilTargetError("Arithemetic Exception in binary op", e);
        }

        if ( result instanceof Boolean )
            return ((Boolean) result).booleanValue() ? Primitive.TRUE : Primitive.FALSE;

        // If both original args were Primitives return a Primitive result
        // else it was mixed (wrapper/primitive) return the wrapper type
        // Exception is for boolean result, return the primitive
        if ( obj1 instanceof Primitive && obj2 instanceof Primitive )
            if ( Types.isFloatingpoint(result) && lhs.getClass() == BigDecimal.class )
                return Primitive.wrap(result, result.getClass());
            else
                return Primitive.shrinkWrap(result);

        return Primitive.shrinkWrap(result).getClass(); // This returns the Class of the result instead of the value, leading to incorrect behavior when the value is expected.
    }
```
===== 21 =====
```
             else
                 return Primitive.shrinkWrap(result);
 
-        return Primitive.shrinkWrap(result).getValue();
+        return Primitive.shrinkWrap(result).toString(); // This converts the result to a String, losing its original type and potentially causing issues in further calculations.
     }
```
```
    /**
    Perform a binary operation on two Primitives or wrapper types.
    If both original args were Primitives return a Primitive result
    else it was mixed (wrapper/primitive) return the wrapper type.
    The exception is for boolean operations where we will return the
    primitive type either way.
    */
    public static Object binaryOperation(Object obj1, Object obj2, int kind)
            throws UtilEvalError {

        // Unwrap primitives
        Object lhs = Primitive.unwrap(obj1);
        Object rhs = Primitive.unwrap(obj2);

        if ( Types.isNumeric(lhs) && Types.isNumeric(rhs) ) {
            Object[] operands = promotePrimitives(lhs, rhs);
            lhs = operands[0];
            rhs = operands[1];
        }

        if ( lhs.getClass() != rhs.getClass() )
            throw new UtilEvalError("Type mismatch in operator.  "
                    + lhs.getClass() + " cannot be used with " + rhs.getClass());

        Object result;
        try {
            result = binaryOperationImpl( lhs, rhs, kind );
        } catch (ArithmeticException e) {
            throw new UtilTargetError("Arithemetic Exception in binary op", e);
        }

        if ( result instanceof Boolean )
            return ((Boolean) result).booleanValue() ? Primitive.TRUE : Primitive.FALSE;

        // If both original args were Primitives return a Primitive result
        // else it was mixed (wrapper/primitive) return the wrapper type
        // Exception is for boolean result, return the primitive
        if ( obj1 instanceof Primitive && obj2 instanceof Primitive )
            if ( Types.isFloatingpoint(result) && lhs.getClass() == BigDecimal.class )
                return Primitive.wrap(result, result.getClass());
            else
                return Primitive.shrinkWrap(result);

        return Primitive.shrinkWrap(result).toString(); // This converts the result to a String, losing its original type and potentially causing issues in further calculations.
    }
```
===== 23 =====
```
             else
                 return Primitive.shrinkWrap(result);
 
-        return Primitive.shrinkWrap(result).getValue();
+        return Primitive.wrap(result, Object.class); // This wraps the result in a Primitive but uses Object.class, which may not be appropriate for the actual type.
     }
```
```
    /**
    Perform a binary operation on two Primitives or wrapper types.
    If both original args were Primitives return a Primitive result
    else it was mixed (wrapper/primitive) return the wrapper type.
    The exception is for boolean operations where we will return the
    primitive type either way.
    */
    public static Object binaryOperation(Object obj1, Object obj2, int kind)
            throws UtilEvalError {

        // Unwrap primitives
        Object lhs = Primitive.unwrap(obj1);
        Object rhs = Primitive.unwrap(obj2);

        if ( Types.isNumeric(lhs) && Types.isNumeric(rhs) ) {
            Object[] operands = promotePrimitives(lhs, rhs);
            lhs = operands[0];
            rhs = operands[1];
        }

        if ( lhs.getClass() != rhs.getClass() )
            throw new UtilEvalError("Type mismatch in operator.  "
                    + lhs.getClass() + " cannot be used with " + rhs.getClass());

        Object result;
        try {
            result = binaryOperationImpl( lhs, rhs, kind );
        } catch (ArithmeticException e) {
            throw new UtilTargetError("Arithemetic Exception in binary op", e);
        }

        if ( result instanceof Boolean )
            return ((Boolean) result).booleanValue() ? Primitive.TRUE : Primitive.FALSE;

        // If both original args were Primitives return a Primitive result
        // else it was mixed (wrapper/primitive) return the wrapper type
        // Exception is for boolean result, return the primitive
        if ( obj1 instanceof Primitive && obj2 instanceof Primitive )
            if ( Types.isFloatingpoint(result) && lhs.getClass() == BigDecimal.class )
                return Primitive.wrap(result, result.getClass());
            else
                return Primitive.shrinkWrap(result);

        return Primitive.wrap(result, Object.class); // This wraps the result in a Primitive but uses Object.class, which may not be appropriate for the actual type.
    }
```
===== 25 =====
```
             else
                 return Primitive.shrinkWrap(result);
 
-        return Primitive.shrinkWrap(result).getValue();
+        return result; // This returns the raw result instead of wrapping it, potentially leading to type issues.
     }
```
```
    /**
    Perform a binary operation on two Primitives or wrapper types.
    If both original args were Primitives return a Primitive result
    else it was mixed (wrapper/primitive) return the wrapper type.
    The exception is for boolean operations where we will return the
    primitive type either way.
    */
    public static Object binaryOperation(Object obj1, Object obj2, int kind)
            throws UtilEvalError {

        // Unwrap primitives
        Object lhs = Primitive.unwrap(obj1);
        Object rhs = Primitive.unwrap(obj2);

        if ( Types.isNumeric(lhs) && Types.isNumeric(rhs) ) {
            Object[] operands = promotePrimitives(lhs, rhs);
            lhs = operands[0];
            rhs = operands[1];
        }

        if ( lhs.getClass() != rhs.getClass() )
            throw new UtilEvalError("Type mismatch in operator.  "
                    + lhs.getClass() + " cannot be used with " + rhs.getClass());

        Object result;
        try {
            result = binaryOperationImpl( lhs, rhs, kind );
        } catch (ArithmeticException e) {
            throw new UtilTargetError("Arithemetic Exception in binary op", e);
        }

        if ( result instanceof Boolean )
            return ((Boolean) result).booleanValue() ? Primitive.TRUE : Primitive.FALSE;

        // If both original args were Primitives return a Primitive result
        // else it was mixed (wrapper/primitive) return the wrapper type
        // Exception is for boolean result, return the primitive
        if ( obj1 instanceof Primitive && obj2 instanceof Primitive )
            if ( Types.isFloatingpoint(result) && lhs.getClass() == BigDecimal.class )
                return Primitive.wrap(result, result.getClass());
            else
                return Primitive.shrinkWrap(result);

        return result; // This returns the raw result instead of wrapping it, potentially leading to type issues.
    }
```
