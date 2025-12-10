https://github.com/Coreoz/Wisp/blob/1076065124550231680c5ece56dbb281eeedcc1c/./src/main/java/com/coreoz/wisp/LongRunningJobMonitor.java#L75-L110
```
//@ ensures (\old(job.status()) == JobStatus.RUNNING && !\old(longRunningJobs.containsKey(job)) && \old(job.lastExecutionStartedTimeInMillis()) != null && \old(job.threadRunningJob()) != null && currentTime - \old(job.lastExecutionStartedTimeInMillis()) > detectionThresholdInMillis) ==> \result == true;
//@ ensures \result == true ==> (\old(job.status()) == JobStatus.RUNNING && !\old(longRunningJobs.containsKey(job)) && \old(job.lastExecutionStartedTimeInMillis()) != null && \old(job.threadRunningJob()) != null && currentTime - \old(job.lastExecutionStartedTimeInMillis()) > detectionThresholdInMillis);
//@ ensures \result == true ==> longRunningJobs.containsKey(job);
//@ ensures \result == true ==> longRunningJobs.get(job).executionsCount == \old(job.executionsCount());
//@ ensures \result == true ==> longRunningJobs.get(job).jobStartedtimeInMillis == \old(job.lastExecutionStartedTimeInMillis()).longValue();
```
```
//@ ensures (\old(job.status()) == JobStatus.RUNNING && !\old(longRunningJobs.containsKey(job)) && \old(job.lastExecutionStartedTimeInMillis()) != null && \old(job.threadRunningJob()) != null && currentTime - \old(job.lastExecutionStartedTimeInMillis()) > detectionThresholdInMillis) ==> \result == true;
//@ ensures \result == true ==> longRunningJobs.containsKey(job);
//@ ensures \result == true ==> longRunningJobs.get(job).executionsCount == \old(job.executionsCount());
//@ ensures \result == true ==> longRunningJobs.get(job).jobStartedtimeInMillis == \old(job.lastExecutionStartedTimeInMillis()).longValue();
```
[0, 3, 14, 19]
===== 0 =====
```
 	 * Returned value is made available for testing purposes.
 	 */
 	boolean detectLongRunningJob(long currentTime, Job job) {
-		if(job.status() == JobStatus.RUNNING && !longRunningJobs.containsKey(job)) {
+		if(!longRunningJobs.containsKey(job)) {
 			int jobExecutionsCount = job.executionsCount();
 			Long jobStartedtimeInMillis = job.lastExecutionStartedTimeInMillis();
 			Thread threadRunningJob = job.threadRunningJob();
```
```
	/**
	 * Check whether a job is running for too long or not.
	 *
	 * @return true if the is running for too long, else false.
	 * Returned value is made available for testing purposes.
	 */
	boolean detectLongRunningJob(long currentTime, Job job) {
		if(!longRunningJobs.containsKey(job)) {
			int jobExecutionsCount = job.executionsCount();
			Long jobStartedtimeInMillis = job.lastExecutionStartedTimeInMillis();
			Thread threadRunningJob = job.threadRunningJob();

			if(jobStartedtimeInMillis != null
				&& threadRunningJob != null
				&& currentTime - jobStartedtimeInMillis > detectionThresholdInMillis) {
				logger.warn(
					"Job '{}' is still running after {}ms (detection threshold = {}ms), stack trace = {}",
					job.name(),
					currentTime - jobStartedtimeInMillis,
					detectionThresholdInMillis,
					Stream
						.of(threadRunningJob.getStackTrace())
						.map(StackTraceElement::toString)
						.collect(Collectors.joining("\n  "))
				);

				longRunningJobs.put(
					job,
					new LongRunningJobInfo(jobStartedtimeInMillis, jobExecutionsCount)
				);

				return true;
			}
		}
		return false;
	}
```
===== 3 =====
```
 	 * Returned value is made available for testing purposes.
 	 */
 	boolean detectLongRunningJob(long currentTime, Job job) {
-		if(job.status() == JobStatus.RUNNING && !longRunningJobs.containsKey(job)) {
+		if(job.status() == JobStatus.RUNNING) {
 			int jobExecutionsCount = job.executionsCount();
 			Long jobStartedtimeInMillis = job.lastExecutionStartedTimeInMillis();
 			Thread threadRunningJob = job.threadRunningJob();
```
```
	/**
	 * Check whether a job is running for too long or not.
	 *
	 * @return true if the is running for too long, else false.
	 * Returned value is made available for testing purposes.
	 */
	boolean detectLongRunningJob(long currentTime, Job job) {
		if(job.status() == JobStatus.RUNNING) {
			int jobExecutionsCount = job.executionsCount();
			Long jobStartedtimeInMillis = job.lastExecutionStartedTimeInMillis();
			Thread threadRunningJob = job.threadRunningJob();

			if(jobStartedtimeInMillis != null
				&& threadRunningJob != null
				&& currentTime - jobStartedtimeInMillis > detectionThresholdInMillis) {
				logger.warn(
					"Job '{}' is still running after {}ms (detection threshold = {}ms), stack trace = {}",
					job.name(),
					currentTime - jobStartedtimeInMillis,
					detectionThresholdInMillis,
					Stream
						.of(threadRunningJob.getStackTrace())
						.map(StackTraceElement::toString)
						.collect(Collectors.joining("\n  "))
				);

				longRunningJobs.put(
					job,
					new LongRunningJobInfo(jobStartedtimeInMillis, jobExecutionsCount)
				);

				return true;
			}
		}
		return false;
	}
```
===== 14 =====
```
 
 			if(jobStartedtimeInMillis != null
 				&& threadRunningJob != null
-				&& currentTime - jobStartedtimeInMillis > detectionThresholdInMillis) {
+				&& currentTime - jobStartedtimeInMillis != detectionThresholdInMillis) {
 				logger.warn(
 					"Job '{}' is still running after {}ms (detection threshold = {}ms), stack trace = {}",
 					job.name(),
```
```
	/**
	 * Check whether a job is running for too long or not.
	 *
	 * @return true if the is running for too long, else false.
	 * Returned value is made available for testing purposes.
	 */
	boolean detectLongRunningJob(long currentTime, Job job) {
		if(job.status() == JobStatus.RUNNING && !longRunningJobs.containsKey(job)) {
			int jobExecutionsCount = job.executionsCount();
			Long jobStartedtimeInMillis = job.lastExecutionStartedTimeInMillis();
			Thread threadRunningJob = job.threadRunningJob();

			if(jobStartedtimeInMillis != null
				&& threadRunningJob != null
				&& currentTime - jobStartedtimeInMillis != detectionThresholdInMillis) {
				logger.warn(
					"Job '{}' is still running after {}ms (detection threshold = {}ms), stack trace = {}",
					job.name(),
					currentTime - jobStartedtimeInMillis,
					detectionThresholdInMillis,
					Stream
						.of(threadRunningJob.getStackTrace())
						.map(StackTraceElement::toString)
						.collect(Collectors.joining("\n  "))
				);

				longRunningJobs.put(
					job,
					new LongRunningJobInfo(jobStartedtimeInMillis, jobExecutionsCount)
				);

				return true;
			}
		}
		return false;
	}
```
===== 19 =====
```
 
 			if(jobStartedtimeInMillis != null
 				&& threadRunningJob != null
-				&& currentTime - jobStartedtimeInMillis > detectionThresholdInMillis) {
+				&& currentTime - jobStartedtimeInMillis >= detectionThresholdInMillis) {
 				logger.warn(
 					"Job '{}' is still running after {}ms (detection threshold = {}ms), stack trace = {}",
 					job.name(),
```
```
	/**
	 * Check whether a job is running for too long or not.
	 *
	 * @return true if the is running for too long, else false.
	 * Returned value is made available for testing purposes.
	 */
	boolean detectLongRunningJob(long currentTime, Job job) {
		if(job.status() == JobStatus.RUNNING && !longRunningJobs.containsKey(job)) {
			int jobExecutionsCount = job.executionsCount();
			Long jobStartedtimeInMillis = job.lastExecutionStartedTimeInMillis();
			Thread threadRunningJob = job.threadRunningJob();

			if(jobStartedtimeInMillis != null
				&& threadRunningJob != null
				&& currentTime - jobStartedtimeInMillis >= detectionThresholdInMillis) {
				logger.warn(
					"Job '{}' is still running after {}ms (detection threshold = {}ms), stack trace = {}",
					job.name(),
					currentTime - jobStartedtimeInMillis,
					detectionThresholdInMillis,
					Stream
						.of(threadRunningJob.getStackTrace())
						.map(StackTraceElement::toString)
						.collect(Collectors.joining("\n  "))
				);

				longRunningJobs.put(
					job,
					new LongRunningJobInfo(jobStartedtimeInMillis, jobExecutionsCount)
				);

				return true;
			}
		}
		return false;
	}
```
