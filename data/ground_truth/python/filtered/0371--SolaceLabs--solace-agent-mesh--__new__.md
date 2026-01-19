https://github.com/SolaceLabs/solace-agent-mesh/blob/6564748e81c0625394b55124c4d80e4af2f6042b/./src/solace_agent_mesh/common/utils/in_memory_cache.py#L18-L30
```
🈚️

thread safety
class object
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
===== 0 =====
```
         Returns:
             The singleton instance of InMemoryCache.
         """
-        if cls._instance is None:
+        if cls._initialized:
             with cls._lock:
                 if cls._instance is None:
                     cls._instance = super().__new__(cls)
```
```
    def __new__(cls):
        """Override __new__ to control instance creation (Singleton pattern).

        Uses a lock to ensure thread safety during the first instantiation.

        Returns:
            The singleton instance of InMemoryCache.
        """
        if cls._initialized:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```
===== 1 =====
```
         Returns:
             The singleton instance of InMemoryCache.
         """
-        if cls._instance is None:
+        if cls._instance is None and cls._lock.locked():
             with cls._lock:
                 if cls._instance is None:
                     cls._instance = super().__new__(cls)
```
```
    def __new__(cls):
        """Override __new__ to control instance creation (Singleton pattern).

        Uses a lock to ensure thread safety during the first instantiation.

        Returns:
            The singleton instance of InMemoryCache.
        """
        if cls._instance is None and cls._lock.locked():
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```
===== 2 =====
```
         Returns:
             The singleton instance of InMemoryCache.
         """
-        if cls._instance is None:
+        if cls._instance is not None:
             with cls._lock:
                 if cls._instance is None:
                     cls._instance = super().__new__(cls)
```
```
    def __new__(cls):
        """Override __new__ to control instance creation (Singleton pattern).

        Uses a lock to ensure thread safety during the first instantiation.

        Returns:
            The singleton instance of InMemoryCache.
        """
        if cls._instance is not None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```
===== 3 =====
```
         Returns:
             The singleton instance of InMemoryCache.
         """
-        if cls._instance is None:
+        if cls._instance is not None:
             with cls._lock:
                 if cls._instance is None:
                     cls._instance = super().__new__(cls)
-        return cls._instance+        return cls._instance
```
```
    def __new__(cls):
        """Override __new__ to control instance creation (Singleton pattern).

        Uses a lock to ensure thread safety during the first instantiation.

        Returns:
            The singleton instance of InMemoryCache.
        """
        if cls._instance is not None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

```
===== 4 =====
```
         """
         if cls._instance is None:
             with cls._lock:
-                if cls._instance is None:
+                if cls._initialized:
                     cls._instance = super().__new__(cls)
         return cls._instance
```
```
    def __new__(cls):
        """Override __new__ to control instance creation (Singleton pattern).

        Uses a lock to ensure thread safety during the first instantiation.

        Returns:
            The singleton instance of InMemoryCache.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._initialized:
                    cls._instance = super().__new__(cls)
        return cls._instance
```
===== 5 =====
```
         """
         if cls._instance is None:
             with cls._lock:
-                if cls._instance is None:
+                if cls._instance is not None:
                     cls._instance = super().__new__(cls)
         return cls._instance
```
```
    def __new__(cls):
        """Override __new__ to control instance creation (Singleton pattern).

        Uses a lock to ensure thread safety during the first instantiation.

        Returns:
            The singleton instance of InMemoryCache.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is not None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```
===== 6 =====
```
         """
         if cls._instance is None:
             with cls._lock:
-                if cls._instance is None:
+                if cls._instance is not None:
                     cls._instance = super().__new__(cls)
-        return cls._instance+        return cls._instance
```
```
    def __new__(cls):
        """Override __new__ to control instance creation (Singleton pattern).

        Uses a lock to ensure thread safety during the first instantiation.

        Returns:
            The singleton instance of InMemoryCache.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is not None:
                    cls._instance = super().__new__(cls)
        return cls._instance

```
===== 7 =====
```
         """
         if cls._instance is None:
             with cls._lock:
-                if cls._instance is None:
+                if cls._lock.acquire(blocking=False):
                     cls._instance = super().__new__(cls)
         return cls._instance
```
```
    def __new__(cls):
        """Override __new__ to control instance creation (Singleton pattern).

        Uses a lock to ensure thread safety during the first instantiation.

        Returns:
            The singleton instance of InMemoryCache.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._lock.acquire(blocking=False):
                    cls._instance = super().__new__(cls)
        return cls._instance
```
===== 8 =====
```
         if cls._instance is None:
             with cls._lock:
                 if cls._instance is None:
-                    cls._instance = super().__new__(cls)
+                    cls._instance = None
         return cls._instance
```
```
    def __new__(cls):
        """Override __new__ to control instance creation (Singleton pattern).

        Uses a lock to ensure thread safety during the first instantiation.

        Returns:
            The singleton instance of InMemoryCache.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = None
        return cls._instance
```
===== 9 =====
```
         if cls._instance is None:
             with cls._lock:
                 if cls._instance is None:
-                    cls._instance = super().__new__(cls)
-        return cls._instance+                    cls._instance = None
+        return cls._instance
```
```
    def __new__(cls):
        """Override __new__ to control instance creation (Singleton pattern).

        Uses a lock to ensure thread safety during the first instantiation.

        Returns:
            The singleton instance of InMemoryCache.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = None
        return cls._instance

```
===== 10 =====
```
         if cls._instance is None:
             with cls._lock:
                 if cls._instance is None:
-                    cls._instance = super().__new__(cls)
+                    cls._instance = super().__new__(object)
         return cls._instance
```
```
    def __new__(cls):
        """Override __new__ to control instance creation (Singleton pattern).

        Uses a lock to ensure thread safety during the first instantiation.

        Returns:
            The singleton instance of InMemoryCache.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(object)
        return cls._instance
```
