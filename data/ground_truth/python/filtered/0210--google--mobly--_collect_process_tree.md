https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/utils.py#L260-L297
```
🈚️

subprocess used

@icontract.ensure(
    lambda result: isinstance(result, list),
    "结果必须是 list。"
)
@icontract.ensure(
    lambda result: all(isinstance(pid, int) for pid in result),
    "所有元素必须是整数 pid。"
)
@icontract.ensure(
    lambda result: all(pid > 0 for pid in result),
    "所有 pid 必须是正数。"
)
@icontract.ensure(
    lambda result: len(result) == len(set(result)),
    "结果列表中不应该出现重复的 pid。"
)
@icontract.ensure(
    lambda starting_pid, result: starting_pid not in result,
    "结果不应包含起始进程自身。"
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
===== 0 =====
```
   ret = []
   stack = [starting_pid]
 
-  while stack:
+  while len(stack) > 1:
     pid = stack.pop()
     if platform.system() == 'Darwin':
       command = ['pgrep', '-P', str(pid)]
```
```
def _collect_process_tree(starting_pid):
  """Collects PID list of the descendant processes from the given PID.

  This function only available on Unix like system.

  Args:
    starting_pid: The PID to start recursively traverse.

  Returns:
    A list of pid of the descendant processes.
  """
  ret = []
  stack = [starting_pid]

  while len(stack) > 1:
    pid = stack.pop()
    if platform.system() == 'Darwin':
      command = ['pgrep', '-P', str(pid)]
    else:
      command = [
          'ps',
          '-o',
          'pid',
          '--ppid',
          str(pid),
          '--noheaders',
      ]
    try:
      ps_results = subprocess.check_output(command).decode().strip()
    except subprocess.CalledProcessError:
      # Ignore if there is not child process.
      continue

    children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
    stack.extend(children_pid_list)
    ret.extend(children_pid_list)

  return ret
```
===== 1 =====
```
   ret = []
   stack = [starting_pid]
 
-  while stack:
+  while not stack:
     pid = stack.pop()
     if platform.system() == 'Darwin':
       command = ['pgrep', '-P', str(pid)]
```
```
def _collect_process_tree(starting_pid):
  """Collects PID list of the descendant processes from the given PID.

  This function only available on Unix like system.

  Args:
    starting_pid: The PID to start recursively traverse.

  Returns:
    A list of pid of the descendant processes.
  """
  ret = []
  stack = [starting_pid]

  while not stack:
    pid = stack.pop()
    if platform.system() == 'Darwin':
      command = ['pgrep', '-P', str(pid)]
    else:
      command = [
          'ps',
          '-o',
          'pid',
          '--ppid',
          str(pid),
          '--noheaders',
      ]
    try:
      ps_results = subprocess.check_output(command).decode().strip()
    except subprocess.CalledProcessError:
      # Ignore if there is not child process.
      continue

    children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
    stack.extend(children_pid_list)
    ret.extend(children_pid_list)

  return ret
```
===== 2 =====
```
 
   while stack:
     pid = stack.pop()
-    if platform.system() == 'Darwin':
+    if platform.system() == 'Linux' or platform.system() == 'Darwin':
       command = ['pgrep', '-P', str(pid)]
     else:
       command = [
```
```
def _collect_process_tree(starting_pid):
  """Collects PID list of the descendant processes from the given PID.

  This function only available on Unix like system.

  Args:
    starting_pid: The PID to start recursively traverse.

  Returns:
    A list of pid of the descendant processes.
  """
  ret = []
  stack = [starting_pid]

  while stack:
    pid = stack.pop()
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
      command = ['pgrep', '-P', str(pid)]
    else:
      command = [
          'ps',
          '-o',
          'pid',
          '--ppid',
          str(pid),
          '--noheaders',
      ]
    try:
      ps_results = subprocess.check_output(command).decode().strip()
    except subprocess.CalledProcessError:
      # Ignore if there is not child process.
      continue

    children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
    stack.extend(children_pid_list)
    ret.extend(children_pid_list)

  return ret
```
===== 3 =====
```
 
   while stack:
     pid = stack.pop()
-    if platform.system() == 'Darwin':
+    if platform.system() == 'Linux':
       command = ['pgrep', '-P', str(pid)]
     else:
       command = [
```
```
def _collect_process_tree(starting_pid):
  """Collects PID list of the descendant processes from the given PID.

  This function only available on Unix like system.

  Args:
    starting_pid: The PID to start recursively traverse.

  Returns:
    A list of pid of the descendant processes.
  """
  ret = []
  stack = [starting_pid]

  while stack:
    pid = stack.pop()
    if platform.system() == 'Linux':
      command = ['pgrep', '-P', str(pid)]
    else:
      command = [
          'ps',
          '-o',
          'pid',
          '--ppid',
          str(pid),
          '--noheaders',
      ]
    try:
      ps_results = subprocess.check_output(command).decode().strip()
    except subprocess.CalledProcessError:
      # Ignore if there is not child process.
      continue

    children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
    stack.extend(children_pid_list)
    ret.extend(children_pid_list)

  return ret
```
===== 4 =====
```
           '--noheaders',
       ]
     try:
-      ps_results = subprocess.check_output(command).decode().strip()
+      ps_results = subprocess.check_output(command, stderr=subprocess.STDOUT).decode().strip()
     except subprocess.CalledProcessError:
       # Ignore if there is not child process.
       continue
```
```
def _collect_process_tree(starting_pid):
  """Collects PID list of the descendant processes from the given PID.

  This function only available on Unix like system.

  Args:
    starting_pid: The PID to start recursively traverse.

  Returns:
    A list of pid of the descendant processes.
  """
  ret = []
  stack = [starting_pid]

  while stack:
    pid = stack.pop()
    if platform.system() == 'Darwin':
      command = ['pgrep', '-P', str(pid)]
    else:
      command = [
          'ps',
          '-o',
          'pid',
          '--ppid',
          str(pid),
          '--noheaders',
      ]
    try:
      ps_results = subprocess.check_output(command, stderr=subprocess.STDOUT).decode().strip()
    except subprocess.CalledProcessError:
      # Ignore if there is not child process.
      continue

    children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
    stack.extend(children_pid_list)
    ret.extend(children_pid_list)

  return ret
```
===== 5 =====
```
           '--noheaders',
       ]
     try:
-      ps_results = subprocess.check_output(command).decode().strip()
+      ps_results = subprocess.check_output(command, timeout=5).decode().strip()  # Introduces a timeout that may not be appropriate
     except subprocess.CalledProcessError:
       # Ignore if there is not child process.
       continue
```
```
def _collect_process_tree(starting_pid):
  """Collects PID list of the descendant processes from the given PID.

  This function only available on Unix like system.

  Args:
    starting_pid: The PID to start recursively traverse.

  Returns:
    A list of pid of the descendant processes.
  """
  ret = []
  stack = [starting_pid]

  while stack:
    pid = stack.pop()
    if platform.system() == 'Darwin':
      command = ['pgrep', '-P', str(pid)]
    else:
      command = [
          'ps',
          '-o',
          'pid',
          '--ppid',
          str(pid),
          '--noheaders',
      ]
    try:
      ps_results = subprocess.check_output(command, timeout=5).decode().strip()  # Introduces a timeout that may not be appropriate
    except subprocess.CalledProcessError:
      # Ignore if there is not child process.
      continue

    children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
    stack.extend(children_pid_list)
    ret.extend(children_pid_list)

  return ret
```
===== 6 =====
```
       # Ignore if there is not child process.
       continue
 
-    children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
+    children_pid_list = [p.strip() for p in ps_results.split('\n')]
     stack.extend(children_pid_list)
     ret.extend(children_pid_list)
```
```
def _collect_process_tree(starting_pid):
  """Collects PID list of the descendant processes from the given PID.

  This function only available on Unix like system.

  Args:
    starting_pid: The PID to start recursively traverse.

  Returns:
    A list of pid of the descendant processes.
  """
  ret = []
  stack = [starting_pid]

  while stack:
    pid = stack.pop()
    if platform.system() == 'Darwin':
      command = ['pgrep', '-P', str(pid)]
    else:
      command = [
          'ps',
          '-o',
          'pid',
          '--ppid',
          str(pid),
          '--noheaders',
      ]
    try:
      ps_results = subprocess.check_output(command).decode().strip()
    except subprocess.CalledProcessError:
      # Ignore if there is not child process.
      continue

    children_pid_list = [p.strip() for p in ps_results.split('\n')]
    stack.extend(children_pid_list)
    ret.extend(children_pid_list)

  return ret
```
===== 7 =====
```
       continue
 
     children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
-    stack.extend(children_pid_list)
+    stack += children_pid_list[:1]  # Only adds the first child PID, missing others.
     ret.extend(children_pid_list)
 
   return ret
```
```
def _collect_process_tree(starting_pid):
  """Collects PID list of the descendant processes from the given PID.

  This function only available on Unix like system.

  Args:
    starting_pid: The PID to start recursively traverse.

  Returns:
    A list of pid of the descendant processes.
  """
  ret = []
  stack = [starting_pid]

  while stack:
    pid = stack.pop()
    if platform.system() == 'Darwin':
      command = ['pgrep', '-P', str(pid)]
    else:
      command = [
          'ps',
          '-o',
          'pid',
          '--ppid',
          str(pid),
          '--noheaders',
      ]
    try:
      ps_results = subprocess.check_output(command).decode().strip()
    except subprocess.CalledProcessError:
      # Ignore if there is not child process.
      continue

    children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
    stack += children_pid_list[:1]  # Only adds the first child PID, missing others.
    ret.extend(children_pid_list)

  return ret
```
===== 8 =====
```
       continue
 
     children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
-    stack.extend(children_pid_list)
+    stack.append(children_pid_list)  # Incorrectly appends the entire list as a single element.
     ret.extend(children_pid_list)
 
   return ret
```
```
def _collect_process_tree(starting_pid):
  """Collects PID list of the descendant processes from the given PID.

  This function only available on Unix like system.

  Args:
    starting_pid: The PID to start recursively traverse.

  Returns:
    A list of pid of the descendant processes.
  """
  ret = []
  stack = [starting_pid]

  while stack:
    pid = stack.pop()
    if platform.system() == 'Darwin':
      command = ['pgrep', '-P', str(pid)]
    else:
      command = [
          'ps',
          '-o',
          'pid',
          '--ppid',
          str(pid),
          '--noheaders',
      ]
    try:
      ps_results = subprocess.check_output(command).decode().strip()
    except subprocess.CalledProcessError:
      # Ignore if there is not child process.
      continue

    children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
    stack.append(children_pid_list)  # Incorrectly appends the entire list as a single element.
    ret.extend(children_pid_list)

  return ret
```
===== 9 =====
```
       continue
 
     children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
-    stack.extend(children_pid_list)
+    stack.extend(children_pid_list) if len(children_pid_list) > 2 else []  # Only adds if there are more than 2 children.
     ret.extend(children_pid_list)
 
   return ret
```
```
def _collect_process_tree(starting_pid):
  """Collects PID list of the descendant processes from the given PID.

  This function only available on Unix like system.

  Args:
    starting_pid: The PID to start recursively traverse.

  Returns:
    A list of pid of the descendant processes.
  """
  ret = []
  stack = [starting_pid]

  while stack:
    pid = stack.pop()
    if platform.system() == 'Darwin':
      command = ['pgrep', '-P', str(pid)]
    else:
      command = [
          'ps',
          '-o',
          'pid',
          '--ppid',
          str(pid),
          '--noheaders',
      ]
    try:
      ps_results = subprocess.check_output(command).decode().strip()
    except subprocess.CalledProcessError:
      # Ignore if there is not child process.
      continue

    children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
    stack.extend(children_pid_list) if len(children_pid_list) > 2 else []  # Only adds if there are more than 2 children.
    ret.extend(children_pid_list)

  return ret
```
===== 10 =====
```
       continue
 
     children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
-    stack.extend(children_pid_list)
+    stack.extend(children_pid_list[1:])  # Skips the first child PID, potentially missing important processes.
     ret.extend(children_pid_list)
 
   return ret
```
```
def _collect_process_tree(starting_pid):
  """Collects PID list of the descendant processes from the given PID.

  This function only available on Unix like system.

  Args:
    starting_pid: The PID to start recursively traverse.

  Returns:
    A list of pid of the descendant processes.
  """
  ret = []
  stack = [starting_pid]

  while stack:
    pid = stack.pop()
    if platform.system() == 'Darwin':
      command = ['pgrep', '-P', str(pid)]
    else:
      command = [
          'ps',
          '-o',
          'pid',
          '--ppid',
          str(pid),
          '--noheaders',
      ]
    try:
      ps_results = subprocess.check_output(command).decode().strip()
    except subprocess.CalledProcessError:
      # Ignore if there is not child process.
      continue

    children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
    stack.extend(children_pid_list[1:])  # Skips the first child PID, potentially missing important processes.
    ret.extend(children_pid_list)

  return ret
```
===== 11 =====
```
 
     children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
     stack.extend(children_pid_list)
-    ret.extend(children_pid_list)
+    ret = children_pid_list  # Replaces the entire list instead of extending it
 
   return ret
```
```
def _collect_process_tree(starting_pid):
  """Collects PID list of the descendant processes from the given PID.

  This function only available on Unix like system.

  Args:
    starting_pid: The PID to start recursively traverse.

  Returns:
    A list of pid of the descendant processes.
  """
  ret = []
  stack = [starting_pid]

  while stack:
    pid = stack.pop()
    if platform.system() == 'Darwin':
      command = ['pgrep', '-P', str(pid)]
    else:
      command = [
          'ps',
          '-o',
          'pid',
          '--ppid',
          str(pid),
          '--noheaders',
      ]
    try:
      ps_results = subprocess.check_output(command).decode().strip()
    except subprocess.CalledProcessError:
      # Ignore if there is not child process.
      continue

    children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
    stack.extend(children_pid_list)
    ret = children_pid_list  # Replaces the entire list instead of extending it

  return ret
```
===== 12 =====
```
 
     children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
     stack.extend(children_pid_list)
-    ret.extend(children_pid_list)
+    ret.append(children_pid_list)
 
   return ret
```
```
def _collect_process_tree(starting_pid):
  """Collects PID list of the descendant processes from the given PID.

  This function only available on Unix like system.

  Args:
    starting_pid: The PID to start recursively traverse.

  Returns:
    A list of pid of the descendant processes.
  """
  ret = []
  stack = [starting_pid]

  while stack:
    pid = stack.pop()
    if platform.system() == 'Darwin':
      command = ['pgrep', '-P', str(pid)]
    else:
      command = [
          'ps',
          '-o',
          'pid',
          '--ppid',
          str(pid),
          '--noheaders',
      ]
    try:
      ps_results = subprocess.check_output(command).decode().strip()
    except subprocess.CalledProcessError:
      # Ignore if there is not child process.
      continue

    children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
    stack.extend(children_pid_list)
    ret.append(children_pid_list)

  return ret
```
===== 13 =====
```
 
     children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
     stack.extend(children_pid_list)
-    ret.extend(children_pid_list)
+    ret.extend(children_pid_list[:1])  # Only adds the first child PID
 
   return ret
```
```
def _collect_process_tree(starting_pid):
  """Collects PID list of the descendant processes from the given PID.

  This function only available on Unix like system.

  Args:
    starting_pid: The PID to start recursively traverse.

  Returns:
    A list of pid of the descendant processes.
  """
  ret = []
  stack = [starting_pid]

  while stack:
    pid = stack.pop()
    if platform.system() == 'Darwin':
      command = ['pgrep', '-P', str(pid)]
    else:
      command = [
          'ps',
          '-o',
          'pid',
          '--ppid',
          str(pid),
          '--noheaders',
      ]
    try:
      ps_results = subprocess.check_output(command).decode().strip()
    except subprocess.CalledProcessError:
      # Ignore if there is not child process.
      continue

    children_pid_list = [int(p.strip()) for p in ps_results.split('\n')]
    stack.extend(children_pid_list)
    ret.extend(children_pid_list[:1])  # Only adds the first child PID

  return ret
```
