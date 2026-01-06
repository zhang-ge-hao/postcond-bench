https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/physics/Gravitation.java#L21-L50
```
// @ ensures \result != null;
// @ ensures \result.length == 2;
// @ ensures ((x1 - x2) == 0.0 && (y1 - y2) == 0.0) ==> (\result[0] == 0.0 && \result[1] == 0.0);
// @ ensures (((x1 - x2) != 0.0 || (y1 - y2) != 0.0) && !(Double.isNaN(m1) || Double.isNaN(x1) || Double.isNaN(y1) || Double.isNaN(m2) || Double.isNaN(x2) || Double.isNaN(y2))) ==> (\result[0] == GRAVITATIONAL_CONSTANT * m1 * m2 * (x1 - x2) / Math.pow(((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)), 1.5) && \result[1] == GRAVITATIONAL_CONSTANT * m1 * m2 * (y1 - y2) / Math.pow(((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)), 1.5));
// @ ensures (((x1 - x2) != 0.0 || (y1 - y2) != 0.0) && (Double.isNaN(m1) || Double.isNaN(x1) || Double.isNaN(y1) || Double.isNaN(m2) || Double.isNaN(x2) || Double.isNaN(y2))) ==> (Double.isNaN(\result[0]) && Double.isNaN(\result[1]));
```
```
Corner case missed.

What’s happening is a floating-point underflow in the squared distance, and that underflow can trigger your early-return path even when the bodies are not at the same position. If, at the same time, any input is NaN, your postcondition expects the result to be NaN, but your method returns {0,0}—so the postcondition is violated.
```
jml_fail
```
//@ ensures ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)) == 0 ==> \result[0] == 0 && \result[1] == 0;
//@ ensures ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)) != 0 ==> Math.hypot(\result[0], \result[1]) == GRAVITATIONAL_CONSTANT * m1 * m2 / ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2));
//@ ensures ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)) != 0 ==> \result[0] * (y1 - y2) == \result[1] * (x1 - x2);
```
