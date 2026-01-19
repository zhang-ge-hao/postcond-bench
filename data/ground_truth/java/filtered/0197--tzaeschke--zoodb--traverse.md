https://github.com/tzaeschke/zoodb/blob/311c96bc6f9413762c54b4638c85a60558707aab/./src/org/zoodb/internal/ObjectGraphTraverser.java#L157-L194
```
🈚️

originally wrong. mutants passed

//@ ensures true;
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
===== 0 =====
```
     	//We have to check for && because 'traversalRequired' is not triggered by new objects,
     	//but new objects may have new objects referenced that are not marked as persistent.
     	//See issue #57.
-    	if (!traversalRequired && !cache.hasDirtyPojos()) {
+    	if (!traversalRequired && cache.hasDirtyPojos()) {
     		//shortcut
     		return;
     	}
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache();
	        traverseWorkList();
    	} finally {
    		workList.clear();
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 1 =====
```
     	//We have to check for && because 'traversalRequired' is not triggered by new objects,
     	//but new objects may have new objects referenced that are not marked as persistent.
     	//See issue #57.
-    	if (!traversalRequired && !cache.hasDirtyPojos()) {
+    	if (!traversalRequired || cache.hasDirtyPojos()) {
     		//shortcut
     		return;
     	}
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired || cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache();
	        traverseWorkList();
    	} finally {
    		workList.clear();
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 2 =====
```
     	//We have to check for && because 'traversalRequired' is not triggered by new objects,
     	//but new objects may have new objects referenced that are not marked as persistent.
     	//See issue #57.
-    	if (!traversalRequired && !cache.hasDirtyPojos()) {
+    	if (traversalRequired && !cache.hasDirtyPojos()) {
     		//shortcut
     		return;
     	}
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache();
	        traverseWorkList();
    	} finally {
    		workList.clear();
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 3 =====
```
     	//We have to check for && because 'traversalRequired' is not triggered by new objects,
     	//but new objects may have new objects referenced that are not marked as persistent.
     	//See issue #57.
-    	if (!traversalRequired && !cache.hasDirtyPojos()) {
+    	if (traversalRequired || cache.hasDirtyPojos()) {
     		//shortcut
     		return;
     	}
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (traversalRequired || cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache();
	        traverseWorkList();
    	} finally {
    		workList.clear();
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 4 =====
```
 //                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
 //                + " MP=" + mpCount);
     	try {
-	    	traverseCache();
+	    	
 	        traverseWorkList();
     	} finally {
     		workList.clear();
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	
	        traverseWorkList();
    	} finally {
    		workList.clear();
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 5 =====
```
 //                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
 //                + " MP=" + mpCount);
     	try {
-	    	traverseCache();
+	    	traverseCache(); // This will be a duplicate call, leading to unnecessary processing and potential performance issues.
 	        traverseWorkList();
     	} finally {
     		workList.clear();
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache(); // This will be a duplicate call, leading to unnecessary processing and potential performance issues.
	        traverseWorkList();
    	} finally {
    		workList.clear();
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 6 =====
```
 //                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
 //                + " MP=" + mpCount);
     	try {
-	    	traverseCache();
+	    	traverseCache(); // This will be called but without clearing the work list first, potentially leading to stale data being processed.
 	        traverseWorkList();
     	} finally {
     		workList.clear();
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache(); // This will be called but without clearing the work list first, potentially leading to stale data being processed.
	        traverseWorkList();
    	} finally {
    		workList.clear();
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 7 =====
```
 //                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
 //                + " MP=" + mpCount);
     	try {
-	    	traverseCache();
+	    	traverseWorkList(); // This will cause the cache to be ignored, potentially missing new objects.
 	        traverseWorkList();
     	} finally {
     		workList.clear();
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseWorkList(); // This will cause the cache to be ignored, potentially missing new objects.
	        traverseWorkList();
    	} finally {
    		workList.clear();
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 8 =====
```
 //                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
 //                + " MP=" + mpCount);
     	try {
-	    	traverseCache();
+	    	traverseWorkList(); // This will cause the method to only process the work list, ignoring the cache entirely.
 	        traverseWorkList();
     	} finally {
     		workList.clear();
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseWorkList(); // This will cause the method to only process the work list, ignoring the cache entirely.
	        traverseWorkList();
    	} finally {
    		workList.clear();
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 9 =====
```
 //                + " MP=" + mpCount);
     	try {
 	    	traverseCache();
-	        traverseWorkList();
+	        
     	} finally {
     		workList.clear();
     		toBecomePersistent.clear();
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache();
	        
    	} finally {
    		workList.clear();
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 10 =====
```
 //                + " MP=" + mpCount);
     	try {
 	    	traverseCache();
-	        traverseWorkList();
+	        toBecomePersistent.clear(); // This will remove all objects that should become persistent, leading to data loss.
     	} finally {
     		workList.clear();
     		toBecomePersistent.clear();
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache();
	        toBecomePersistent.clear(); // This will remove all objects that should become persistent, leading to data loss.
    	} finally {
    		workList.clear();
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 11 =====
```
 //                + " MP=" + mpCount);
     	try {
 	    	traverseCache();
-	        traverseWorkList();
+	        traverseCache(); // This will cause an infinite loop as it keeps traversing the cache again.
     	} finally {
     		workList.clear();
     		toBecomePersistent.clear();
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache();
	        traverseCache(); // This will cause an infinite loop as it keeps traversing the cache again.
    	} finally {
    		workList.clear();
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 12 =====
```
 //                + " MP=" + mpCount);
     	try {
 	    	traverseCache();
-	        traverseWorkList();
+	        traverseWorkList(); // This will be a duplicate call, potentially causing unnecessary processing without any effect.
     	} finally {
     		workList.clear();
     		toBecomePersistent.clear();
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache();
	        traverseWorkList(); // This will be a duplicate call, potentially causing unnecessary processing without any effect.
    	} finally {
    		workList.clear();
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 13 =====
```
 //                + " MP=" + mpCount);
     	try {
 	    	traverseCache();
-	        traverseWorkList();
+	        workList.clear(); // This will clear the work list, preventing any objects from being processed.
     	} finally {
     		workList.clear();
     		toBecomePersistent.clear();
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache();
	        workList.clear(); // This will clear the work list, preventing any objects from being processed.
    	} finally {
    		workList.clear();
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 14 =====
```
 	    	traverseCache();
 	        traverseWorkList();
     	} finally {
-    		workList.clear();
+    		
     		toBecomePersistent.clear();
     		//We have to clear the seenObjects here, see also issue #58.
     		seenObjects.clear();
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache();
	        traverseWorkList();
    	} finally {
    		
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 15 =====
```
 	    	traverseCache();
 	        traverseWorkList();
     	} finally {
-    		workList.clear();
+    		seenObjects.clear();
     		toBecomePersistent.clear();
     		//We have to clear the seenObjects here, see also issue #58.
     		seenObjects.clear();
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache();
	        traverseWorkList();
    	} finally {
    		seenObjects.clear();
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 16 =====
```
 	    	traverseCache();
 	        traverseWorkList();
     	} finally {
-    		workList.clear();
+    		toBecomePersistent.clear();
     		toBecomePersistent.clear();
     		//We have to clear the seenObjects here, see also issue #58.
     		seenObjects.clear();
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache();
	        traverseWorkList();
    	} finally {
    		toBecomePersistent.clear();
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 17 =====
```
 	    	traverseCache();
 	        traverseWorkList();
     	} finally {
-    		workList.clear();
+    		workList.removeAll(workList);
     		toBecomePersistent.clear();
     		//We have to clear the seenObjects here, see also issue #58.
     		seenObjects.clear();
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache();
	        traverseWorkList();
    	} finally {
    		workList.removeAll(workList);
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 18 =====
```
 	    	traverseCache();
 	        traverseWorkList();
     	} finally {
-    		workList.clear();
+    		workList.trimToSize();
     		toBecomePersistent.clear();
     		//We have to clear the seenObjects here, see also issue #58.
     		seenObjects.clear();
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache();
	        traverseWorkList();
    	} finally {
    		workList.trimToSize();
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 19 =====
```
 	        traverseWorkList();
     	} finally {
     		workList.clear();
-    		toBecomePersistent.clear();
+    		
     		//We have to clear the seenObjects here, see also issue #58.
     		seenObjects.clear();
     	}
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache();
	        traverseWorkList();
    	} finally {
    		workList.clear();
    		
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 20 =====
```
 	        traverseWorkList();
     	} finally {
     		workList.clear();
-    		toBecomePersistent.clear();
+    		toBecomePersistent.removeAll(toBecomePersistent); // This will clear the list but in an indirect way.
     		//We have to clear the seenObjects here, see also issue #58.
     		seenObjects.clear();
     	}
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache();
	        traverseWorkList();
    	} finally {
    		workList.clear();
    		toBecomePersistent.removeAll(toBecomePersistent); // This will clear the list but in an indirect way.
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.clear();
    	}
        traversalRequired = false;
    }
```
===== 21 =====
```
     		workList.clear();
     		toBecomePersistent.clear();
     		//We have to clear the seenObjects here, see also issue #58.
-    		seenObjects.clear();
+    		
     	}
         traversalRequired = false;
     }
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache();
	        traverseWorkList();
    	} finally {
    		workList.clear();
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		
    	}
        traversalRequired = false;
    }
```
===== 22 =====
```
     		workList.clear();
     		toBecomePersistent.clear();
     		//We have to clear the seenObjects here, see also issue #58.
-    		seenObjects.clear();
+    		seenObjects.add(new Object()); // Adds a new object to seenObjects, which is not relevant and could lead to incorrect tracking.
     	}
         traversalRequired = false;
     }
```
```
	/**
     * This class is only public so it can be accessed by the test harness. 
     * Please do not use.
     */
    public final void traverse() {
    	//We have to check for && because 'traversalRequired' is not triggered by new objects,
    	//but new objects may have new objects referenced that are not marked as persistent.
    	//See issue #57.
    	if (!traversalRequired && !cache.hasDirtyPojos()) {
    		//shortcut
    		return;
    	}
        //Intention is to find the NEW objects that will become persistent
        //through reachability.
        //For this, we have to check objects that are DIRTY or NEW (by 
        //makePersistent()). 
//    	DBLogger.debugPrintln(1, "Starting OGT: " + workList.size());
//        long t1 = System.currentTimeMillis();
//        long nObjects = 0;
//
//        nObjects += traverseCache();
//        nObjects += traverseWorkList();
//                
//        long t2 = System.currentTimeMillis();
//        DBLogger.debugPrintln(1, "Finished OGT: " + nObjects + " (seen="
//                + seenObjects.size() + " ) / " + (t2-t1)/1000.0
//                + " MP=" + mpCount);
    	try {
	    	traverseCache();
	        traverseWorkList();
    	} finally {
    		workList.clear();
    		toBecomePersistent.clear();
    		//We have to clear the seenObjects here, see also issue #58.
    		seenObjects.add(new Object()); // Adds a new object to seenObjects, which is not relevant and could lead to incorrect tracking.
    	}
        traversalRequired = false;
    }
```
