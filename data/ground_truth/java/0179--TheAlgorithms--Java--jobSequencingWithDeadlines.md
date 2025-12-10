https://github.com/TheAlgorithms/Java/blob/bb6385e756a0159a29655c745682e95ca7b41ada/./src/main/java/com/thealgorithms/scheduling/JobSchedulingWithDeadline.java#L47-L87
```
//@ ensures \result != null && \result.length == 2;
//@ ensures \result[0] >= 0 && \result[0] <= jobs.length;
//@ ensures \result[1] >= 0 && \result[1] <= Arrays.stream(jobs).mapToInt(job -> job.profit).sum();
//@ ensures Arrays.stream(jobs).anyMatch(job -> job.profit > 0 && job.arrivalTime <= job.deadline) ==> \result[1] > 0;
//@ ensures java.util.stream.IntStream.range(0, Math.max(0, jobs.length - 1)).allMatch(i -> jobs[i].profit >= jobs[i+1].profit);
//@ ensures Arrays.stream(jobs).filter(job -> job.profit == Arrays.stream(jobs).mapToInt(j -> j.profit).max().orElse(0)).anyMatch(job -> job.arrivalTime <= job.deadline) ==> (\result[1] >= Arrays.stream(jobs).mapToInt(j -> j.profit).max().orElse(0) && \result[0] >= 1);
//@ ensures \result[0] <= Arrays.stream(jobs).mapToInt(job -> job.deadline).max().orElse(0);
//@ ensures (jobs.length >= 2 && Arrays.stream(jobs).allMatch(job -> job.arrivalTime == 1) && Arrays.stream(jobs).mapToInt(job -> job.deadline).min().orElse(0) == 1 && Arrays.stream(jobs).mapToInt(job -> job.deadline).max().orElse(0) > 1 && Arrays.stream(jobs).anyMatch(job -> job.deadline == 1 && job.profit == Arrays.stream(jobs).mapToInt(j -> j.profit).max().orElse(0))) ==> \result[0] >= 2;
//@ ensures \result[0] <= jobs.length - (int)((Arrays.stream(jobs).filter(job -> job.arrivalTime == 1 && job.deadline == 1).count() > 1L ? Arrays.stream(jobs).filter(job -> job.arrivalTime == 1 && job.deadline == 1).count() - 1L : 0L));
```
```
//@ ensures \result != null && \result.length == 2;
//@ ensures \result[0] >= 0 && \result[0] <= jobs.length;
//@ ensures \result[1] >= 0 && \result[1] <= Arrays.stream(jobs).mapToInt(job -> job.profit).sum();
//@ ensures Arrays.stream(jobs).anyMatch(job -> job.profit > 0 && job.arrivalTime <= job.deadline) ==> \result[1] > 0;
//@ ensures java.util.stream.IntStream.range(0, Math.max(0, jobs.length - 1)).allMatch(i -> jobs[i].profit >= jobs[i+1].profit);
//@ ensures Arrays.stream(jobs).filter(job -> job.profit == Arrays.stream(jobs).mapToInt(j -> j.profit).max().orElse(0)).anyMatch(job -> job.arrivalTime <= job.deadline) ==> (\result[1] >= Arrays.stream(jobs).mapToInt(j -> j.profit).max().orElse(0) && \result[0] >= 1);
//@ ensures \result[0] <= Arrays.stream(jobs).mapToInt(job -> job.deadline).max().orElse(0);
```
[6, 7, 20, 21]
===== 6 =====
```
     public static int[] jobSequencingWithDeadlines(Job[] jobs) {
         Arrays.sort(jobs, Comparator.comparingInt(job -> - job.profit));
 
-        int maxDeadline = Arrays.stream(jobs).mapToInt(job -> job.deadline).max().orElse(0);
+        int maxDeadline = Arrays.stream(jobs).mapToInt(job -> job.deadline).filter(d -> d > 0).findFirst().orElse(0);
 
         int[] timeSlots = new int[maxDeadline];
         Arrays.fill(timeSlots, -1);
```
```
    /**
     * Schedules jobs to maximize profit while respecting their deadlines and arrival times.
     *
     * This method sorts the jobs in descending order of profit and attempts
     * to allocate them to time slots that are before or on their deadlines,
     * provided they have arrived. The function returns an array where the first element
     * is the total number of jobs scheduled and the second element is the total profit earned.
     *
     * @param jobs An array of Job objects, each representing a job with an ID, arrival time,
     *             deadline, and profit.
     * @return An array of two integers: the first element is the count of jobs
     *         that were successfully scheduled, and the second element is the
     *         total profit earned from those jobs.
     */
    public static int[] jobSequencingWithDeadlines(Job[] jobs) {
        Arrays.sort(jobs, Comparator.comparingInt(job -> - job.profit));

        int maxDeadline = Arrays.stream(jobs).mapToInt(job -> job.deadline).filter(d -> d > 0).findFirst().orElse(0);

        int[] timeSlots = new int[maxDeadline];
        Arrays.fill(timeSlots, -1);

        int count = 0;
        int maxProfit = 0;

        // Schedule the jobs
        for (Job job : jobs) {
            if (job.arrivalTime <= job.deadline) {
                for (int i = Math.min(job.deadline - 1, maxDeadline - 1); i >= job.arrivalTime - 1; i--) {
                    if (timeSlots[i] == -1) {
                        timeSlots[i] = job.jobId;
                        count++;
                        maxProfit += job.profit;
                        break;
                    }
                }
            }
        }

        return new int[] {count, maxProfit};
    }
```
===== 7 =====
```
     public static int[] jobSequencingWithDeadlines(Job[] jobs) {
         Arrays.sort(jobs, Comparator.comparingInt(job -> - job.profit));
 
-        int maxDeadline = Arrays.stream(jobs).mapToInt(job -> job.deadline).max().orElse(0);
+        int maxDeadline = Arrays.stream(jobs).mapToInt(job -> job.deadline).min().orElse(0);
 
         int[] timeSlots = new int[maxDeadline];
         Arrays.fill(timeSlots, -1);
```
```
    /**
     * Schedules jobs to maximize profit while respecting their deadlines and arrival times.
     *
     * This method sorts the jobs in descending order of profit and attempts
     * to allocate them to time slots that are before or on their deadlines,
     * provided they have arrived. The function returns an array where the first element
     * is the total number of jobs scheduled and the second element is the total profit earned.
     *
     * @param jobs An array of Job objects, each representing a job with an ID, arrival time,
     *             deadline, and profit.
     * @return An array of two integers: the first element is the count of jobs
     *         that were successfully scheduled, and the second element is the
     *         total profit earned from those jobs.
     */
    public static int[] jobSequencingWithDeadlines(Job[] jobs) {
        Arrays.sort(jobs, Comparator.comparingInt(job -> - job.profit));

        int maxDeadline = Arrays.stream(jobs).mapToInt(job -> job.deadline).min().orElse(0);

        int[] timeSlots = new int[maxDeadline];
        Arrays.fill(timeSlots, -1);

        int count = 0;
        int maxProfit = 0;

        // Schedule the jobs
        for (Job job : jobs) {
            if (job.arrivalTime <= job.deadline) {
                for (int i = Math.min(job.deadline - 1, maxDeadline - 1); i >= job.arrivalTime - 1; i--) {
                    if (timeSlots[i] == -1) {
                        timeSlots[i] = job.jobId;
                        count++;
                        maxProfit += job.profit;
                        break;
                    }
                }
            }
        }

        return new int[] {count, maxProfit};
    }
```
===== 20 =====
```
         // Schedule the jobs
         for (Job job : jobs) {
             if (job.arrivalTime <= job.deadline) {
-                for (int i = Math.min(job.deadline - 1, maxDeadline - 1); i >= job.arrivalTime - 1; i--) {
+                for (int i = 0; i < maxDeadline; i++) {
                     if (timeSlots[i] == -1) {
                         timeSlots[i] = job.jobId;
                         count++;
```
```
    /**
     * Schedules jobs to maximize profit while respecting their deadlines and arrival times.
     *
     * This method sorts the jobs in descending order of profit and attempts
     * to allocate them to time slots that are before or on their deadlines,
     * provided they have arrived. The function returns an array where the first element
     * is the total number of jobs scheduled and the second element is the total profit earned.
     *
     * @param jobs An array of Job objects, each representing a job with an ID, arrival time,
     *             deadline, and profit.
     * @return An array of two integers: the first element is the count of jobs
     *         that were successfully scheduled, and the second element is the
     *         total profit earned from those jobs.
     */
    public static int[] jobSequencingWithDeadlines(Job[] jobs) {
        Arrays.sort(jobs, Comparator.comparingInt(job -> - job.profit));

        int maxDeadline = Arrays.stream(jobs).mapToInt(job -> job.deadline).max().orElse(0);

        int[] timeSlots = new int[maxDeadline];
        Arrays.fill(timeSlots, -1);

        int count = 0;
        int maxProfit = 0;

        // Schedule the jobs
        for (Job job : jobs) {
            if (job.arrivalTime <= job.deadline) {
                for (int i = 0; i < maxDeadline; i++) {
                    if (timeSlots[i] == -1) {
                        timeSlots[i] = job.jobId;
                        count++;
                        maxProfit += job.profit;
                        break;
                    }
                }
            }
        }

        return new int[] {count, maxProfit};
    }
```
===== 21 =====
```
         // Schedule the jobs
         for (Job job : jobs) {
             if (job.arrivalTime <= job.deadline) {
-                for (int i = Math.min(job.deadline - 1, maxDeadline - 1); i >= job.arrivalTime - 1; i--) {
+                for (int i = Math.min(job.deadline + 1, maxDeadline - 1); i >= job.arrivalTime - 1; i--) {
                     if (timeSlots[i] == -1) {
                         timeSlots[i] = job.jobId;
                         count++;
```
```
    /**
     * Schedules jobs to maximize profit while respecting their deadlines and arrival times.
     *
     * This method sorts the jobs in descending order of profit and attempts
     * to allocate them to time slots that are before or on their deadlines,
     * provided they have arrived. The function returns an array where the first element
     * is the total number of jobs scheduled and the second element is the total profit earned.
     *
     * @param jobs An array of Job objects, each representing a job with an ID, arrival time,
     *             deadline, and profit.
     * @return An array of two integers: the first element is the count of jobs
     *         that were successfully scheduled, and the second element is the
     *         total profit earned from those jobs.
     */
    public static int[] jobSequencingWithDeadlines(Job[] jobs) {
        Arrays.sort(jobs, Comparator.comparingInt(job -> - job.profit));

        int maxDeadline = Arrays.stream(jobs).mapToInt(job -> job.deadline).max().orElse(0);

        int[] timeSlots = new int[maxDeadline];
        Arrays.fill(timeSlots, -1);

        int count = 0;
        int maxProfit = 0;

        // Schedule the jobs
        for (Job job : jobs) {
            if (job.arrivalTime <= job.deadline) {
                for (int i = Math.min(job.deadline + 1, maxDeadline - 1); i >= job.arrivalTime - 1; i--) {
                    if (timeSlots[i] == -1) {
                        timeSlots[i] = job.jobId;
                        count++;
                        maxProfit += job.profit;
                        break;
                    }
                }
            }
        }

        return new int[] {count, maxProfit};
    }
```
