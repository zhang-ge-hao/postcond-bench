https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/others/CRCAlgorithm.java#L170-L197
```
🈚️

Random used.

//@ ensures correctMess == \old(correctMess);
//@ ensures wrongMessCaught == \old(wrongMessCaught);
//@ ensures wrongMessNotCaught == \old(wrongMessNotCaught);
//@ ensures message.size() == \old(message.size());
//@ ensures wrongMess == \old(wrongMess) || wrongMess == \old(wrongMess) + 1;
//@ ensures messageChanged ==> wrongMess == \old(wrongMess) + 1;
//@ ensures !messageChanged ==> wrongMess == \old(wrongMess);
//@ ensures ber == 0.0 ==> messageChanged == \old(messageChanged);
//@ ensures ber == 0.0 && !\old(messageChanged) ==> (!messageChanged && wrongMess == \old(wrongMess));
//@ ensures ber == 1.0 && !message.isEmpty() && !\old(messageChanged) ==> (messageChanged && wrongMess == \old(wrongMess) + 1);
//@ ensures wrongMess >= 0 && correctMess >= 0 && wrongMessCaught >= 0 && wrongMessNotCaught >= 0;
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
===== 0 =====
```
      */
     public void changeMess() {
         for (int y : message) {
-            double x = randomGenerator.nextDouble();
+            double x = 0.5; // Always sets x to a constant value, ignoring randomness
             while (x < 0.0000 || x > 1.00000) {
                 x = randomGenerator.nextDouble();
             }
```
```
    /**
     * Once the message is transmitted, some of it's elements, is possible to
     * change from 1 to 0, or from 0 to 1, because of the Bit Error Rate (ber).
     * For every element of the message, a random double number is created. If
     * that number is smaller than ber, then the spesific element changes. On
     * the other hand, if it's bigger than ber, it does not. Based on these
     * changes. the boolean variable messageChanged, gets the value: true, or
     * false.
     */
    public void changeMess() {
        for (int y : message) {
            double x = 0.5; // Always sets x to a constant value, ignoring randomness
            while (x < 0.0000 || x > 1.00000) {
                x = randomGenerator.nextDouble();
            }
            if (x < ber) {
                messageChanged = true;
                if (y == 1) {
                    message.set(message.indexOf(y), 0);
                } else {
                    message.set(message.indexOf(y), 1);
                }
            }
        }
        if (messageChanged) {
            wrongMess++;
        }
    }
```
===== 1 =====
```
             while (x < 0.0000 || x > 1.00000) {
                 x = randomGenerator.nextDouble();
             }
-            if (x < ber) {
+            if (x == ber) {
                 messageChanged = true;
                 if (y == 1) {
                     message.set(message.indexOf(y), 0);
```
```
    /**
     * Once the message is transmitted, some of it's elements, is possible to
     * change from 1 to 0, or from 0 to 1, because of the Bit Error Rate (ber).
     * For every element of the message, a random double number is created. If
     * that number is smaller than ber, then the spesific element changes. On
     * the other hand, if it's bigger than ber, it does not. Based on these
     * changes. the boolean variable messageChanged, gets the value: true, or
     * false.
     */
    public void changeMess() {
        for (int y : message) {
            double x = randomGenerator.nextDouble();
            while (x < 0.0000 || x > 1.00000) {
                x = randomGenerator.nextDouble();
            }
            if (x == ber) {
                messageChanged = true;
                if (y == 1) {
                    message.set(message.indexOf(y), 0);
                } else {
                    message.set(message.indexOf(y), 1);
                }
            }
        }
        if (messageChanged) {
            wrongMess++;
        }
    }
```
===== 2 =====
```
             while (x < 0.0000 || x > 1.00000) {
                 x = randomGenerator.nextDouble();
             }
-            if (x < ber) {
+            if (x > ber) {
                 messageChanged = true;
                 if (y == 1) {
                     message.set(message.indexOf(y), 0);
```
```
    /**
     * Once the message is transmitted, some of it's elements, is possible to
     * change from 1 to 0, or from 0 to 1, because of the Bit Error Rate (ber).
     * For every element of the message, a random double number is created. If
     * that number is smaller than ber, then the spesific element changes. On
     * the other hand, if it's bigger than ber, it does not. Based on these
     * changes. the boolean variable messageChanged, gets the value: true, or
     * false.
     */
    public void changeMess() {
        for (int y : message) {
            double x = randomGenerator.nextDouble();
            while (x < 0.0000 || x > 1.00000) {
                x = randomGenerator.nextDouble();
            }
            if (x > ber) {
                messageChanged = true;
                if (y == 1) {
                    message.set(message.indexOf(y), 0);
                } else {
                    message.set(message.indexOf(y), 1);
                }
            }
        }
        if (messageChanged) {
            wrongMess++;
        }
    }
```
===== 3 =====
```
             while (x < 0.0000 || x > 1.00000) {
                 x = randomGenerator.nextDouble();
             }
-            if (x < ber) {
+            if (x >= ber) {
                 messageChanged = true;
                 if (y == 1) {
                     message.set(message.indexOf(y), 0);
```
```
    /**
     * Once the message is transmitted, some of it's elements, is possible to
     * change from 1 to 0, or from 0 to 1, because of the Bit Error Rate (ber).
     * For every element of the message, a random double number is created. If
     * that number is smaller than ber, then the spesific element changes. On
     * the other hand, if it's bigger than ber, it does not. Based on these
     * changes. the boolean variable messageChanged, gets the value: true, or
     * false.
     */
    public void changeMess() {
        for (int y : message) {
            double x = randomGenerator.nextDouble();
            while (x < 0.0000 || x > 1.00000) {
                x = randomGenerator.nextDouble();
            }
            if (x >= ber) {
                messageChanged = true;
                if (y == 1) {
                    message.set(message.indexOf(y), 0);
                } else {
                    message.set(message.indexOf(y), 1);
                }
            }
        }
        if (messageChanged) {
            wrongMess++;
        }
    }
```
===== 4 =====
```
                 }
             }
         }
-        if (messageChanged) {
+        if (!messageChanged) {
             wrongMess++;
         }
     }
```
```
    /**
     * Once the message is transmitted, some of it's elements, is possible to
     * change from 1 to 0, or from 0 to 1, because of the Bit Error Rate (ber).
     * For every element of the message, a random double number is created. If
     * that number is smaller than ber, then the spesific element changes. On
     * the other hand, if it's bigger than ber, it does not. Based on these
     * changes. the boolean variable messageChanged, gets the value: true, or
     * false.
     */
    public void changeMess() {
        for (int y : message) {
            double x = randomGenerator.nextDouble();
            while (x < 0.0000 || x > 1.00000) {
                x = randomGenerator.nextDouble();
            }
            if (x < ber) {
                messageChanged = true;
                if (y == 1) {
                    message.set(message.indexOf(y), 0);
                } else {
                    message.set(message.indexOf(y), 1);
                }
            }
        }
        if (!messageChanged) {
            wrongMess++;
        }
    }
```
===== 5 =====
```
                 }
             }
         }
-        if (messageChanged) {
+        if (ber > 0.5) {
             wrongMess++;
         }
     }
```
```
    /**
     * Once the message is transmitted, some of it's elements, is possible to
     * change from 1 to 0, or from 0 to 1, because of the Bit Error Rate (ber).
     * For every element of the message, a random double number is created. If
     * that number is smaller than ber, then the spesific element changes. On
     * the other hand, if it's bigger than ber, it does not. Based on these
     * changes. the boolean variable messageChanged, gets the value: true, or
     * false.
     */
    public void changeMess() {
        for (int y : message) {
            double x = randomGenerator.nextDouble();
            while (x < 0.0000 || x > 1.00000) {
                x = randomGenerator.nextDouble();
            }
            if (x < ber) {
                messageChanged = true;
                if (y == 1) {
                    message.set(message.indexOf(y), 0);
                } else {
                    message.set(message.indexOf(y), 1);
                }
            }
        }
        if (ber > 0.5) {
            wrongMess++;
        }
    }
```
===== 6 =====
```
                 }
             }
         }
-        if (messageChanged) {
+        if (message.size() == messSize) {
             wrongMess++;
         }
     }
```
```
    /**
     * Once the message is transmitted, some of it's elements, is possible to
     * change from 1 to 0, or from 0 to 1, because of the Bit Error Rate (ber).
     * For every element of the message, a random double number is created. If
     * that number is smaller than ber, then the spesific element changes. On
     * the other hand, if it's bigger than ber, it does not. Based on these
     * changes. the boolean variable messageChanged, gets the value: true, or
     * false.
     */
    public void changeMess() {
        for (int y : message) {
            double x = randomGenerator.nextDouble();
            while (x < 0.0000 || x > 1.00000) {
                x = randomGenerator.nextDouble();
            }
            if (x < ber) {
                messageChanged = true;
                if (y == 1) {
                    message.set(message.indexOf(y), 0);
                } else {
                    message.set(message.indexOf(y), 1);
                }
            }
        }
        if (message.size() == messSize) {
            wrongMess++;
        }
    }
```
===== 7 =====
```
                 }
             }
         }
-        if (messageChanged) {
+        if (message.size() > 0) {
             wrongMess++;
         }
     }
```
```
    /**
     * Once the message is transmitted, some of it's elements, is possible to
     * change from 1 to 0, or from 0 to 1, because of the Bit Error Rate (ber).
     * For every element of the message, a random double number is created. If
     * that number is smaller than ber, then the spesific element changes. On
     * the other hand, if it's bigger than ber, it does not. Based on these
     * changes. the boolean variable messageChanged, gets the value: true, or
     * false.
     */
    public void changeMess() {
        for (int y : message) {
            double x = randomGenerator.nextDouble();
            while (x < 0.0000 || x > 1.00000) {
                x = randomGenerator.nextDouble();
            }
            if (x < ber) {
                messageChanged = true;
                if (y == 1) {
                    message.set(message.indexOf(y), 0);
                } else {
                    message.set(message.indexOf(y), 1);
                }
            }
        }
        if (message.size() > 0) {
            wrongMess++;
        }
    }
```
===== 8 =====
```
                 }
             }
         }
-        if (messageChanged) {
+        if (messageChanged && wrongMess == 0) {
             wrongMess++;
         }
     }
```
```
    /**
     * Once the message is transmitted, some of it's elements, is possible to
     * change from 1 to 0, or from 0 to 1, because of the Bit Error Rate (ber).
     * For every element of the message, a random double number is created. If
     * that number is smaller than ber, then the spesific element changes. On
     * the other hand, if it's bigger than ber, it does not. Based on these
     * changes. the boolean variable messageChanged, gets the value: true, or
     * false.
     */
    public void changeMess() {
        for (int y : message) {
            double x = randomGenerator.nextDouble();
            while (x < 0.0000 || x > 1.00000) {
                x = randomGenerator.nextDouble();
            }
            if (x < ber) {
                messageChanged = true;
                if (y == 1) {
                    message.set(message.indexOf(y), 0);
                } else {
                    message.set(message.indexOf(y), 1);
                }
            }
        }
        if (messageChanged && wrongMess == 0) {
            wrongMess++;
        }
    }
```
===== 9 =====
```
             }
         }
         if (messageChanged) {
-            wrongMess++;
+            wrongMess--;
         }
     }
```
```
    /**
     * Once the message is transmitted, some of it's elements, is possible to
     * change from 1 to 0, or from 0 to 1, because of the Bit Error Rate (ber).
     * For every element of the message, a random double number is created. If
     * that number is smaller than ber, then the spesific element changes. On
     * the other hand, if it's bigger than ber, it does not. Based on these
     * changes. the boolean variable messageChanged, gets the value: true, or
     * false.
     */
    public void changeMess() {
        for (int y : message) {
            double x = randomGenerator.nextDouble();
            while (x < 0.0000 || x > 1.00000) {
                x = randomGenerator.nextDouble();
            }
            if (x < ber) {
                messageChanged = true;
                if (y == 1) {
                    message.set(message.indexOf(y), 0);
                } else {
                    message.set(message.indexOf(y), 1);
                }
            }
        }
        if (messageChanged) {
            wrongMess--;
        }
    }
```
