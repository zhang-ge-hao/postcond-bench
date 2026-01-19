https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/scheduling/HighestResponseRatioNextScheduling.java#L58-L103
```
🈚️

Timeout.

//@ ensures \result.length == noOfProcesses;
//@ ensures java.util.stream.IntStream.range(0, noOfProcesses).allMatch(i -> \result[i] >= 0);
//@ ensures java.util.stream.IntStream.range(0, noOfProcesses).allMatch(i -> \result[i] >= burstTimes[i]);
//@ ensures noOfProcesses > 0 && java.util.stream.IntStream.range(0, Math.max(0, noOfProcesses - 1)).allMatch(i -> arrivalTimes[i] <= arrivalTimes[i + 1]) ==> \result[0] == burstTimes[0];
//@ ensures java.util.stream.IntStream.range(0, noOfProcesses).anyMatch(i -> java.util.stream.IntStream.range(0, noOfProcesses).anyMatch(j -> i != j && arrivalTimes[i] == arrivalTimes[j])) ==> java.util.stream.IntStream.range(0, noOfProcesses).anyMatch(k -> \result[k] > burstTimes[k]);
//@ ensures java.util.stream.IntStream.range(0, noOfProcesses).map(i -> arrivalTimes[i] + \result[i]).max().orElse(0) <= java.util.stream.IntStream.range(0, noOfProcesses).map(i -> arrivalTimes[i]).max().orElse(0) + java.util.stream.IntStream.range(0, noOfProcesses).map(i -> burstTimes[i]).sum();
//@ ensures java.util.stream.IntStream.range(0, noOfProcesses).allMatch(i -> arrivalTimes[i] >= 0 && burstTimes[i] >= 0) && java.util.stream.IntStream.range(1, noOfProcesses).allMatch(i -> arrivalTimes[i] >= arrivalTimes[i - 1] && arrivalTimes[i] - arrivalTimes[i - 1] >= burstTimes[i - 1]) ==> java.util.stream.IntStream.range(0, noOfProcesses).allMatch(i -> \result[i] == burstTimes[i]);
```
```
//@ ensures \result.length == noOfProcesses;
//@ ensures java.util.stream.IntStream.range(0, noOfProcesses).allMatch(i -> \result[i] >= 0);
//@ ensures java.util.stream.IntStream.range(0, noOfProcesses).allMatch(i -> \result[i] >= burstTimes[i]);
//@ ensures noOfProcesses > 0 && java.util.stream.IntStream.range(0, Math.max(0, noOfProcesses - 1)).allMatch(i -> arrivalTimes[i] <= arrivalTimes[i + 1]) ==> \result[0] == burstTimes[0];
```
[5, 6, 8, 11, 13]
===== 5 =====
```
         while (finishedProcessCount < noOfProcesses) {
             int nextProcessIndex = findNextProcess(processes, currentTime);
             if (nextProcessIndex == PROCESS_NOT_FOUND) {
-                currentTime++;
+                currentTime--;
                 continue;
             }
```
```
    /**
     * Calculates the Turn Around Time (TAT) for each process.
     *
     * <p>Turn Around Time is calculated as the total time a process spends
     * in the system from arrival to completion. It is the sum of the burst time
     * and the waiting time.</p>
     *
     * @param processNames Array of process names.
     * @param arrivalTimes Array of arrival times corresponding to each process.
     * @param burstTimes Array of burst times for each process.
     * @param noOfProcesses The number of processes.
     * @return An array of Turn Around Times for each process.
     */
    public static int[] calculateTurnAroundTime(final String[] processNames, final int[] arrivalTimes, final int[] burstTimes, final int noOfProcesses) {
        int currentTime = 0;
        int[] turnAroundTime = new int[noOfProcesses];
        Process[] processes = new Process[noOfProcesses];

        for (int i = 0; i < noOfProcesses; i++) {
            processes[i] = new Process(processNames[i], arrivalTimes[i], burstTimes[i]);
        }

        Arrays.sort(processes, Comparator.comparingInt(p -> p.arrivalTime));

        int finishedProcessCount = 0;
        while (finishedProcessCount < noOfProcesses) {
            int nextProcessIndex = findNextProcess(processes, currentTime);
            if (nextProcessIndex == PROCESS_NOT_FOUND) {
                currentTime--;
                continue;
            }

            Process currentProcess = processes[nextProcessIndex];
            currentTime = Math.max(currentTime, currentProcess.arrivalTime);
            currentProcess.turnAroundTime = currentTime + currentProcess.burstTime - currentProcess.arrivalTime;
            currentTime += currentProcess.burstTime;
            currentProcess.finished = true;
            finishedProcessCount++;
        }

        for (int i = 0; i < noOfProcesses; i++) {
            turnAroundTime[i] = processes[i].turnAroundTime;
        }

        return turnAroundTime;
    }
```
===== 6 =====
```
             }
 
             Process currentProcess = processes[nextProcessIndex];
-            currentTime = Math.max(currentTime, currentProcess.arrivalTime);
+            currentTime += currentProcess.arrivalTime; // Increases currentTime by the arrival time, which can lead to incorrect scheduling.
             currentProcess.turnAroundTime = currentTime + currentProcess.burstTime - currentProcess.arrivalTime;
             currentTime += currentProcess.burstTime;
             currentProcess.finished = true;
```
```
    /**
     * Calculates the Turn Around Time (TAT) for each process.
     *
     * <p>Turn Around Time is calculated as the total time a process spends
     * in the system from arrival to completion. It is the sum of the burst time
     * and the waiting time.</p>
     *
     * @param processNames Array of process names.
     * @param arrivalTimes Array of arrival times corresponding to each process.
     * @param burstTimes Array of burst times for each process.
     * @param noOfProcesses The number of processes.
     * @return An array of Turn Around Times for each process.
     */
    public static int[] calculateTurnAroundTime(final String[] processNames, final int[] arrivalTimes, final int[] burstTimes, final int noOfProcesses) {
        int currentTime = 0;
        int[] turnAroundTime = new int[noOfProcesses];
        Process[] processes = new Process[noOfProcesses];

        for (int i = 0; i < noOfProcesses; i++) {
            processes[i] = new Process(processNames[i], arrivalTimes[i], burstTimes[i]);
        }

        Arrays.sort(processes, Comparator.comparingInt(p -> p.arrivalTime));

        int finishedProcessCount = 0;
        while (finishedProcessCount < noOfProcesses) {
            int nextProcessIndex = findNextProcess(processes, currentTime);
            if (nextProcessIndex == PROCESS_NOT_FOUND) {
                currentTime++;
                continue;
            }

            Process currentProcess = processes[nextProcessIndex];
            currentTime += currentProcess.arrivalTime; // Increases currentTime by the arrival time, which can lead to incorrect scheduling.
            currentProcess.turnAroundTime = currentTime + currentProcess.burstTime - currentProcess.arrivalTime;
            currentTime += currentProcess.burstTime;
            currentProcess.finished = true;
            finishedProcessCount++;
        }

        for (int i = 0; i < noOfProcesses; i++) {
            turnAroundTime[i] = processes[i].turnAroundTime;
        }

        return turnAroundTime;
    }
```
===== 8 =====
```
             }
 
             Process currentProcess = processes[nextProcessIndex];
-            currentTime = Math.max(currentTime, currentProcess.arrivalTime);
+            currentTime = currentProcess.arrivalTime; // Sets currentTime to the arrival time, ignoring any previous time.
             currentProcess.turnAroundTime = currentTime + currentProcess.burstTime - currentProcess.arrivalTime;
             currentTime += currentProcess.burstTime;
             currentProcess.finished = true;
```
```
    /**
     * Calculates the Turn Around Time (TAT) for each process.
     *
     * <p>Turn Around Time is calculated as the total time a process spends
     * in the system from arrival to completion. It is the sum of the burst time
     * and the waiting time.</p>
     *
     * @param processNames Array of process names.
     * @param arrivalTimes Array of arrival times corresponding to each process.
     * @param burstTimes Array of burst times for each process.
     * @param noOfProcesses The number of processes.
     * @return An array of Turn Around Times for each process.
     */
    public static int[] calculateTurnAroundTime(final String[] processNames, final int[] arrivalTimes, final int[] burstTimes, final int noOfProcesses) {
        int currentTime = 0;
        int[] turnAroundTime = new int[noOfProcesses];
        Process[] processes = new Process[noOfProcesses];

        for (int i = 0; i < noOfProcesses; i++) {
            processes[i] = new Process(processNames[i], arrivalTimes[i], burstTimes[i]);
        }

        Arrays.sort(processes, Comparator.comparingInt(p -> p.arrivalTime));

        int finishedProcessCount = 0;
        while (finishedProcessCount < noOfProcesses) {
            int nextProcessIndex = findNextProcess(processes, currentTime);
            if (nextProcessIndex == PROCESS_NOT_FOUND) {
                currentTime++;
                continue;
            }

            Process currentProcess = processes[nextProcessIndex];
            currentTime = currentProcess.arrivalTime; // Sets currentTime to the arrival time, ignoring any previous time.
            currentProcess.turnAroundTime = currentTime + currentProcess.burstTime - currentProcess.arrivalTime;
            currentTime += currentProcess.burstTime;
            currentProcess.finished = true;
            finishedProcessCount++;
        }

        for (int i = 0; i < noOfProcesses; i++) {
            turnAroundTime[i] = processes[i].turnAroundTime;
        }

        return turnAroundTime;
    }
```
===== 11 =====
```
 
             Process currentProcess = processes[nextProcessIndex];
             currentTime = Math.max(currentTime, currentProcess.arrivalTime);
-            currentProcess.turnAroundTime = currentTime + currentProcess.burstTime - currentProcess.arrivalTime;
+            currentProcess.turnAroundTime = currentTime + currentProcess.burstTime + currentProcess.arrivalTime;
             currentTime += currentProcess.burstTime;
             currentProcess.finished = true;
             finishedProcessCount++;
```
```
    /**
     * Calculates the Turn Around Time (TAT) for each process.
     *
     * <p>Turn Around Time is calculated as the total time a process spends
     * in the system from arrival to completion. It is the sum of the burst time
     * and the waiting time.</p>
     *
     * @param processNames Array of process names.
     * @param arrivalTimes Array of arrival times corresponding to each process.
     * @param burstTimes Array of burst times for each process.
     * @param noOfProcesses The number of processes.
     * @return An array of Turn Around Times for each process.
     */
    public static int[] calculateTurnAroundTime(final String[] processNames, final int[] arrivalTimes, final int[] burstTimes, final int noOfProcesses) {
        int currentTime = 0;
        int[] turnAroundTime = new int[noOfProcesses];
        Process[] processes = new Process[noOfProcesses];

        for (int i = 0; i < noOfProcesses; i++) {
            processes[i] = new Process(processNames[i], arrivalTimes[i], burstTimes[i]);
        }

        Arrays.sort(processes, Comparator.comparingInt(p -> p.arrivalTime));

        int finishedProcessCount = 0;
        while (finishedProcessCount < noOfProcesses) {
            int nextProcessIndex = findNextProcess(processes, currentTime);
            if (nextProcessIndex == PROCESS_NOT_FOUND) {
                currentTime++;
                continue;
            }

            Process currentProcess = processes[nextProcessIndex];
            currentTime = Math.max(currentTime, currentProcess.arrivalTime);
            currentProcess.turnAroundTime = currentTime + currentProcess.burstTime + currentProcess.arrivalTime;
            currentTime += currentProcess.burstTime;
            currentProcess.finished = true;
            finishedProcessCount++;
        }

        for (int i = 0; i < noOfProcesses; i++) {
            turnAroundTime[i] = processes[i].turnAroundTime;
        }

        return turnAroundTime;
    }
```
===== 13 =====
```
             Process currentProcess = processes[nextProcessIndex];
             currentTime = Math.max(currentTime, currentProcess.arrivalTime);
             currentProcess.turnAroundTime = currentTime + currentProcess.burstTime - currentProcess.arrivalTime;
-            currentTime += currentProcess.burstTime;
+            currentTime -= currentProcess.burstTime;
             currentProcess.finished = true;
             finishedProcessCount++;
         }
```
```
    /**
     * Calculates the Turn Around Time (TAT) for each process.
     *
     * <p>Turn Around Time is calculated as the total time a process spends
     * in the system from arrival to completion. It is the sum of the burst time
     * and the waiting time.</p>
     *
     * @param processNames Array of process names.
     * @param arrivalTimes Array of arrival times corresponding to each process.
     * @param burstTimes Array of burst times for each process.
     * @param noOfProcesses The number of processes.
     * @return An array of Turn Around Times for each process.
     */
    public static int[] calculateTurnAroundTime(final String[] processNames, final int[] arrivalTimes, final int[] burstTimes, final int noOfProcesses) {
        int currentTime = 0;
        int[] turnAroundTime = new int[noOfProcesses];
        Process[] processes = new Process[noOfProcesses];

        for (int i = 0; i < noOfProcesses; i++) {
            processes[i] = new Process(processNames[i], arrivalTimes[i], burstTimes[i]);
        }

        Arrays.sort(processes, Comparator.comparingInt(p -> p.arrivalTime));

        int finishedProcessCount = 0;
        while (finishedProcessCount < noOfProcesses) {
            int nextProcessIndex = findNextProcess(processes, currentTime);
            if (nextProcessIndex == PROCESS_NOT_FOUND) {
                currentTime++;
                continue;
            }

            Process currentProcess = processes[nextProcessIndex];
            currentTime = Math.max(currentTime, currentProcess.arrivalTime);
            currentProcess.turnAroundTime = currentTime + currentProcess.burstTime - currentProcess.arrivalTime;
            currentTime -= currentProcess.burstTime;
            currentProcess.finished = true;
            finishedProcessCount++;
        }

        for (int i = 0; i < noOfProcesses; i++) {
            turnAroundTime[i] = processes[i].turnAroundTime;
        }

        return turnAroundTime;
    }
```
