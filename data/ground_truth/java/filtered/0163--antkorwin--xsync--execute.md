https://github.com/antkorwin/xsync/blob/6e46fbfd1fa0bf36ffd214f51057009f1051476a/./src/main/java/com/antkorwin/xsync/XSync.java#L73-L115
```
🈚️

mock util needed.
`twoKeysSynchronizeEvaluate` in `src/test/java/com/antkorwin/xsync/MultiKeysXSyncTest.java`.
Count number of errors but not output error messages.

//@ ensures System.identityHashCode(\old(mutexFactory.getMutex(firstKey))) == System.identityHashCode(\old(mutexFactory.getMutex(secondKey))) <==> System.identityHashCode(mutexFactory.getMutex(firstKey)) == System.identityHashCode(mutexFactory.getMutex(secondKey));
//@ ensures System.identityHashCode(\old(mutexFactory.getMutex(firstKey))) != System.identityHashCode(\old(mutexFactory.getMutex(secondKey))) <==> System.identityHashCode(mutexFactory.getMutex(firstKey)) != System.identityHashCode(mutexFactory.getMutex(secondKey));
//@ ensures (System.identityHashCode(\old(mutexFactory.getMutex(firstKey))) <= System.identityHashCode(\old(mutexFactory.getMutex(secondKey)))) || (System.identityHashCode(\old(mutexFactory.getMutex(firstKey))) >= System.identityHashCode(\old(mutexFactory.getMutex(secondKey))));
```
```
//@ ensures System.identityHashCode(\old(mutexFactory.getMutex(firstKey))) == System.identityHashCode(\old(mutexFactory.getMutex(secondKey))) <==> System.identityHashCode(mutexFactory.getMutex(firstKey)) == System.identityHashCode(mutexFactory.getMutex(secondKey));
//@ ensures System.identityHashCode(\old(mutexFactory.getMutex(firstKey))) != System.identityHashCode(\old(mutexFactory.getMutex(secondKey))) <==> System.identityHashCode(mutexFactory.getMutex(firstKey)) != System.identityHashCode(mutexFactory.getMutex(secondKey));
//@ ensures (System.identityHashCode(\old(mutexFactory.getMutex(firstKey))) <= System.identityHashCode(\old(mutexFactory.getMutex(secondKey)))) || (System.identityHashCode(\old(mutexFactory.getMutex(firstKey))) >= System.identityHashCode(\old(mutexFactory.getMutex(secondKey))));
```
[0, 1, 2, 3, 4, 5]
===== 0 =====
```
 		XMutex<KeyT> firstMutex = mutexFactory.getMutex(firstKey);
 		XMutex<KeyT> secondMutex = mutexFactory.getMutex(secondKey);
 
-		int firstHash = System.identityHashCode(firstMutex);
+		int firstHash = System.identityHashCode(firstMutex) + 1; // Introduces a bias in the hash value
 		int secondHash = System.identityHashCode(secondMutex);
 
 		if (firstHash > secondHash) {
```
```
	/**
	 * Execute the runnable within a pair of synchronized blocks
	 * which built from the first and the second keys.
	 * <p>
	 * Note that the ordering of keys in synchronized blocks doesn't depend
	 * on the ordering of keys in this method arguments. The order depends
	 * on the values of keys, it prevents your code from deadlocking.
	 * So, you don't need to care about the order of the keys if you use XSync.
	 *
	 * @param firstKey  the first key to use in the synchronization blocks
	 * @param secondKey the second key
	 * @param runnable  code which you want to synchronize
	 */
	public void execute(KeyT firstKey, KeyT secondKey, Runnable runnable) {

		XMutex<KeyT> firstMutex = mutexFactory.getMutex(firstKey);
		XMutex<KeyT> secondMutex = mutexFactory.getMutex(secondKey);

		int firstHash = System.identityHashCode(firstMutex) + 1; // Introduces a bias in the hash value
		int secondHash = System.identityHashCode(secondMutex);

		if (firstHash > secondHash) {
			XMutex<KeyT> tmp = firstMutex;
			firstMutex = secondMutex;
			secondMutex = tmp;
		}

		if (firstHash != secondHash) {
			synchronized (firstMutex) {
				synchronized (secondMutex) {
					runnable.run();
				}
			}
		} else {
			synchronized (globalLock) {
				synchronized (firstMutex) {
					synchronized (secondMutex) {
						runnable.run();
					}
				}
			}
		}
	}
```
===== 1 =====
```
 		XMutex<KeyT> firstMutex = mutexFactory.getMutex(firstKey);
 		XMutex<KeyT> secondMutex = mutexFactory.getMutex(secondKey);
 
-		int firstHash = System.identityHashCode(firstMutex);
+		int firstHash = System.identityHashCode(firstMutex) - 1; // Offsets the hash value, potentially causing deadlocks
 		int secondHash = System.identityHashCode(secondMutex);
 
 		if (firstHash > secondHash) {
```
```
	/**
	 * Execute the runnable within a pair of synchronized blocks
	 * which built from the first and the second keys.
	 * <p>
	 * Note that the ordering of keys in synchronized blocks doesn't depend
	 * on the ordering of keys in this method arguments. The order depends
	 * on the values of keys, it prevents your code from deadlocking.
	 * So, you don't need to care about the order of the keys if you use XSync.
	 *
	 * @param firstKey  the first key to use in the synchronization blocks
	 * @param secondKey the second key
	 * @param runnable  code which you want to synchronize
	 */
	public void execute(KeyT firstKey, KeyT secondKey, Runnable runnable) {

		XMutex<KeyT> firstMutex = mutexFactory.getMutex(firstKey);
		XMutex<KeyT> secondMutex = mutexFactory.getMutex(secondKey);

		int firstHash = System.identityHashCode(firstMutex) - 1; // Offsets the hash value, potentially causing deadlocks
		int secondHash = System.identityHashCode(secondMutex);

		if (firstHash > secondHash) {
			XMutex<KeyT> tmp = firstMutex;
			firstMutex = secondMutex;
			secondMutex = tmp;
		}

		if (firstHash != secondHash) {
			synchronized (firstMutex) {
				synchronized (secondMutex) {
					runnable.run();
				}
			}
		} else {
			synchronized (globalLock) {
				synchronized (firstMutex) {
					synchronized (secondMutex) {
						runnable.run();
					}
				}
			}
		}
	}
```
===== 2 =====
```
 			secondMutex = tmp;
 		}
 
-		if (firstHash != secondHash) {
+		if (firstHash % 2 == 0) {
 			synchronized (firstMutex) {
 				synchronized (secondMutex) {
 					runnable.run();
```
```
	/**
	 * Execute the runnable within a pair of synchronized blocks
	 * which built from the first and the second keys.
	 * <p>
	 * Note that the ordering of keys in synchronized blocks doesn't depend
	 * on the ordering of keys in this method arguments. The order depends
	 * on the values of keys, it prevents your code from deadlocking.
	 * So, you don't need to care about the order of the keys if you use XSync.
	 *
	 * @param firstKey  the first key to use in the synchronization blocks
	 * @param secondKey the second key
	 * @param runnable  code which you want to synchronize
	 */
	public void execute(KeyT firstKey, KeyT secondKey, Runnable runnable) {

		XMutex<KeyT> firstMutex = mutexFactory.getMutex(firstKey);
		XMutex<KeyT> secondMutex = mutexFactory.getMutex(secondKey);

		int firstHash = System.identityHashCode(firstMutex);
		int secondHash = System.identityHashCode(secondMutex);

		if (firstHash > secondHash) {
			XMutex<KeyT> tmp = firstMutex;
			firstMutex = secondMutex;
			secondMutex = tmp;
		}

		if (firstHash % 2 == 0) {
			synchronized (firstMutex) {
				synchronized (secondMutex) {
					runnable.run();
				}
			}
		} else {
			synchronized (globalLock) {
				synchronized (firstMutex) {
					synchronized (secondMutex) {
						runnable.run();
					}
				}
			}
		}
	}
```
===== 3 =====
```
 			secondMutex = tmp;
 		}
 
-		if (firstHash != secondHash) {
+		if (firstHash <= secondHash) {
 			synchronized (firstMutex) {
 				synchronized (secondMutex) {
 					runnable.run();
```
```
	/**
	 * Execute the runnable within a pair of synchronized blocks
	 * which built from the first and the second keys.
	 * <p>
	 * Note that the ordering of keys in synchronized blocks doesn't depend
	 * on the ordering of keys in this method arguments. The order depends
	 * on the values of keys, it prevents your code from deadlocking.
	 * So, you don't need to care about the order of the keys if you use XSync.
	 *
	 * @param firstKey  the first key to use in the synchronization blocks
	 * @param secondKey the second key
	 * @param runnable  code which you want to synchronize
	 */
	public void execute(KeyT firstKey, KeyT secondKey, Runnable runnable) {

		XMutex<KeyT> firstMutex = mutexFactory.getMutex(firstKey);
		XMutex<KeyT> secondMutex = mutexFactory.getMutex(secondKey);

		int firstHash = System.identityHashCode(firstMutex);
		int secondHash = System.identityHashCode(secondMutex);

		if (firstHash > secondHash) {
			XMutex<KeyT> tmp = firstMutex;
			firstMutex = secondMutex;
			secondMutex = tmp;
		}

		if (firstHash <= secondHash) {
			synchronized (firstMutex) {
				synchronized (secondMutex) {
					runnable.run();
				}
			}
		} else {
			synchronized (globalLock) {
				synchronized (firstMutex) {
					synchronized (secondMutex) {
						runnable.run();
					}
				}
			}
		}
	}
```
===== 4 =====
```
 			secondMutex = tmp;
 		}
 
-		if (firstHash != secondHash) {
+		if (firstHash == secondHash) {
 			synchronized (firstMutex) {
 				synchronized (secondMutex) {
 					runnable.run();
```
```
	/**
	 * Execute the runnable within a pair of synchronized blocks
	 * which built from the first and the second keys.
	 * <p>
	 * Note that the ordering of keys in synchronized blocks doesn't depend
	 * on the ordering of keys in this method arguments. The order depends
	 * on the values of keys, it prevents your code from deadlocking.
	 * So, you don't need to care about the order of the keys if you use XSync.
	 *
	 * @param firstKey  the first key to use in the synchronization blocks
	 * @param secondKey the second key
	 * @param runnable  code which you want to synchronize
	 */
	public void execute(KeyT firstKey, KeyT secondKey, Runnable runnable) {

		XMutex<KeyT> firstMutex = mutexFactory.getMutex(firstKey);
		XMutex<KeyT> secondMutex = mutexFactory.getMutex(secondKey);

		int firstHash = System.identityHashCode(firstMutex);
		int secondHash = System.identityHashCode(secondMutex);

		if (firstHash > secondHash) {
			XMutex<KeyT> tmp = firstMutex;
			firstMutex = secondMutex;
			secondMutex = tmp;
		}

		if (firstHash == secondHash) {
			synchronized (firstMutex) {
				synchronized (secondMutex) {
					runnable.run();
				}
			}
		} else {
			synchronized (globalLock) {
				synchronized (firstMutex) {
					synchronized (secondMutex) {
						runnable.run();
					}
				}
			}
		}
	}
```
===== 5 =====
```
 			secondMutex = tmp;
 		}
 
-		if (firstHash != secondHash) {
+		if (firstHash > 0) {
 			synchronized (firstMutex) {
 				synchronized (secondMutex) {
 					runnable.run();
```
```
	/**
	 * Execute the runnable within a pair of synchronized blocks
	 * which built from the first and the second keys.
	 * <p>
	 * Note that the ordering of keys in synchronized blocks doesn't depend
	 * on the ordering of keys in this method arguments. The order depends
	 * on the values of keys, it prevents your code from deadlocking.
	 * So, you don't need to care about the order of the keys if you use XSync.
	 *
	 * @param firstKey  the first key to use in the synchronization blocks
	 * @param secondKey the second key
	 * @param runnable  code which you want to synchronize
	 */
	public void execute(KeyT firstKey, KeyT secondKey, Runnable runnable) {

		XMutex<KeyT> firstMutex = mutexFactory.getMutex(firstKey);
		XMutex<KeyT> secondMutex = mutexFactory.getMutex(secondKey);

		int firstHash = System.identityHashCode(firstMutex);
		int secondHash = System.identityHashCode(secondMutex);

		if (firstHash > secondHash) {
			XMutex<KeyT> tmp = firstMutex;
			firstMutex = secondMutex;
			secondMutex = tmp;
		}

		if (firstHash > 0) {
			synchronized (firstMutex) {
				synchronized (secondMutex) {
					runnable.run();
				}
			}
		} else {
			synchronized (globalLock) {
				synchronized (firstMutex) {
					synchronized (secondMutex) {
						runnable.run();
					}
				}
			}
		}
	}
```
