https://github.com/jmeter-maven-plugin/jmeter-maven-plugin/blob/13092f3e53c1f9e0f87a81c5b47bc5d814530d55/./src/main/java/com/lazerycode/jmeter/mojo/AbstractJMeterMojo.java#L245-L272
```
//@ ensures \result != null;
//@ ensures \result.getClass().getName().equals("com.lazerycode.jmeter.configuration.JMeterArgumentsArray");
//@ ensures resultsDirectory != null && logsDirectory != null ==> \result.setTestFile(new java.io.File("dummy.jmx"), new java.io.File(".")).buildArgumentsArray().equals((testResultsTimestamp ? (generateReports && disableGUI ? new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath).setResultsDirectory(resultsDirectory.getAbsolutePath()).setResultFileOutputFormatIsCSV(isCSVFormat).setProxyConfig(proxyConfig).setLogRootOverride(overrideRootLogLevel).setLogsDirectory(logsDirectory.getAbsolutePath()).addACustomPropertiesFiles(customPropertiesFiles).setReportsDirectory(reportDirectory != null ? reportDirectory.getAbsolutePath() : null).setResultsTimestamp(true).appendTimestamp(appendResultsTimestamp).setResultsFileNameDateFormat(resultsFileNameDateFormat) : new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath).setResultsDirectory(resultsDirectory.getAbsolutePath()).setResultFileOutputFormatIsCSV(isCSVFormat).setProxyConfig(proxyConfig).setLogRootOverride(overrideRootLogLevel).setLogsDirectory(logsDirectory.getAbsolutePath()).addACustomPropertiesFiles(customPropertiesFiles).setResultsTimestamp(true).appendTimestamp(appendResultsTimestamp).setResultsFileNameDateFormat(resultsFileNameDateFormat)) : (generateReports && disableGUI ? new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath).setResultsDirectory(resultsDirectory.getAbsolutePath()).setResultFileOutputFormatIsCSV(isCSVFormat).setProxyConfig(proxyConfig).setLogRootOverride(overrideRootLogLevel).setLogsDirectory(logsDirectory.getAbsolutePath()).addACustomPropertiesFiles(customPropertiesFiles).setReportsDirectory(reportDirectory != null ? reportDirectory.getAbsolutePath() : null) : new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath).setResultsDirectory(resultsDirectory.getAbsolutePath()).setResultFileOutputFormatIsCSV(isCSVFormat).setProxyConfig(proxyConfig).setLogRootOverride(overrideRootLogLevel).setLogsDirectory(logsDirectory.getAbsolutePath()).addACustomPropertiesFiles(customPropertiesFiles))).setTestFile(new java.io.File("dummy.jmx"), new java.io.File(".")).buildArgumentsArray());
```
```
//@ ensures \result != null;
//@ ensures \result.getClass().getName().equals("com.lazerycode.jmeter.configuration.JMeterArgumentsArray");
//@ ensures \old(isCSVFormat) == true ==> (\result.setResultFileOutputFormatIsCSV(\old(isCSVFormat)) == \result);
//@ ensures \old(isCSVFormat) == false ==> (\result.setResultFileOutputFormatIsCSV(\old(isCSVFormat)) == \result);
//@ ensures \old(proxyConfig) == null ? true : (\result.setProxyConfig(\old(proxyConfig)) == \result);
//@ ensures \old(overrideRootLogLevel) == null ? true : (\result.setLogRootOverride(\old(overrideRootLogLevel)) == \result);
//@ ensures \old(logsDirectory) == null ? true : (\result.setLogsDirectory(\old(logsDirectory).getAbsolutePath()) == \result);
//@ ensures \old(resultsDirectory) == null ? true : (\result.setResultsDirectory(\old(resultsDirectory).getAbsolutePath()) == \result);
//@ ensures \old(generateReports) && \old(disableGUI) ? (\result.setReportsDirectory(\old(reportDirectory).getAbsolutePath()) == \result) : true;
//@ ensures \old(testResultsTimestamp) ? (\result.setResultsTimestamp(true) == \result && \result.appendTimestamp(\old(appendResultsTimestamp)) == \result) : true;
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
===== 0 =====
```
      */
     protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
         JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
-                .setResultsDirectory(resultsDirectory.getAbsolutePath())
+                .setResultsDirectory("") // This sets the results directory to an empty string, which may lead to incorrect file paths being used.
                 .setResultFileOutputFormatIsCSV(isCSVFormat)
                 .setProxyConfig(proxyConfig)
                 .setLogRootOverride(overrideRootLogLevel)
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory("") // This sets the results directory to an empty string, which may lead to incorrect file paths being used.
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 1 =====
```
      */
     protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
         JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
-                .setResultsDirectory(resultsDirectory.getAbsolutePath())
+                .setResultsDirectory("invalid/path") // This sets an invalid path, which may cause issues when trying to write results, but won't raise an exception immediately.
                 .setResultFileOutputFormatIsCSV(isCSVFormat)
                 .setProxyConfig(proxyConfig)
                 .setLogRootOverride(overrideRootLogLevel)
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory("invalid/path") // This sets an invalid path, which may cause issues when trying to write results, but won't raise an exception immediately.
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 2 =====
```
      */
     protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
         JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
-                .setResultsDirectory(resultsDirectory.getAbsolutePath())
+                .setResultsDirectory(null) // This will cause the results directory to be set to null, leading to potential NullPointerExceptions later.
                 .setResultFileOutputFormatIsCSV(isCSVFormat)
                 .setProxyConfig(proxyConfig)
                 .setLogRootOverride(overrideRootLogLevel)
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(null) // This will cause the results directory to be set to null, leading to potential NullPointerExceptions later.
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 3 =====
```
      */
     protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
         JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
-                .setResultsDirectory(resultsDirectory.getAbsolutePath())
+                .setResultsDirectory(resultsDirectory.getAbsolutePath() + "/results") // This appends an extra "/results" to the path, which may not be intended and could lead to incorrect file handling.
                 .setResultFileOutputFormatIsCSV(isCSVFormat)
                 .setProxyConfig(proxyConfig)
                 .setLogRootOverride(overrideRootLogLevel)
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath() + "/results") // This appends an extra "/results" to the path, which may not be intended and could lead to incorrect file handling.
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 4 =====
```
     protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
         JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                 .setResultsDirectory(resultsDirectory.getAbsolutePath())
-                .setResultFileOutputFormatIsCSV(isCSVFormat)
+                .setResultFileOutputFormatIsCSV(!isCSVFormat)
                 .setProxyConfig(proxyConfig)
                 .setLogRootOverride(overrideRootLogLevel)
                 .setLogsDirectory(logsDirectory.getAbsolutePath())
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(!isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 5 =====
```
     protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
         JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                 .setResultsDirectory(resultsDirectory.getAbsolutePath())
-                .setResultFileOutputFormatIsCSV(isCSVFormat)
+                .setResultFileOutputFormatIsCSV(false)
                 .setProxyConfig(proxyConfig)
                 .setLogRootOverride(overrideRootLogLevel)
                 .setLogsDirectory(logsDirectory.getAbsolutePath())
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(false)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 6 =====
```
     protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
         JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                 .setResultsDirectory(resultsDirectory.getAbsolutePath())
-                .setResultFileOutputFormatIsCSV(isCSVFormat)
+                .setResultFileOutputFormatIsCSV(isCSVFormat && false)
                 .setProxyConfig(proxyConfig)
                 .setLogRootOverride(overrideRootLogLevel)
                 .setLogsDirectory(logsDirectory.getAbsolutePath())
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat && false)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 7 =====
```
     protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
         JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                 .setResultsDirectory(resultsDirectory.getAbsolutePath())
-                .setResultFileOutputFormatIsCSV(isCSVFormat)
+                .setResultFileOutputFormatIsCSV(isCSVFormat ? false : true)
                 .setProxyConfig(proxyConfig)
                 .setLogRootOverride(overrideRootLogLevel)
                 .setLogsDirectory(logsDirectory.getAbsolutePath())
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat ? false : true)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 8 =====
```
                 .setResultsDirectory(resultsDirectory.getAbsolutePath())
                 .setResultFileOutputFormatIsCSV(isCSVFormat)
                 .setProxyConfig(proxyConfig)
-                .setLogRootOverride(overrideRootLogLevel)
+                .setLogRootOverride("DEBUG") // Assuming DEBUG is not a valid log level
                 .setLogsDirectory(logsDirectory.getAbsolutePath())
                 .addACustomPropertiesFiles(customPropertiesFiles);
         if (generateReports && disableGUI) {
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride("DEBUG") // Assuming DEBUG is not a valid log level
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 9 =====
```
                 .setResultFileOutputFormatIsCSV(isCSVFormat)
                 .setProxyConfig(proxyConfig)
                 .setLogRootOverride(overrideRootLogLevel)
-                .setLogsDirectory(logsDirectory.getAbsolutePath())
+                .setLogsDirectory("") // Setting an empty string instead of a valid path
                 .addACustomPropertiesFiles(customPropertiesFiles);
         if (generateReports && disableGUI) {
             testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory("") // Setting an empty string instead of a valid path
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 10 =====
```
                 .setResultFileOutputFormatIsCSV(isCSVFormat)
                 .setProxyConfig(proxyConfig)
                 .setLogRootOverride(overrideRootLogLevel)
-                .setLogsDirectory(logsDirectory.getAbsolutePath())
+                .setLogsDirectory("invalid/path") // Setting a non-existent path
                 .addACustomPropertiesFiles(customPropertiesFiles);
         if (generateReports && disableGUI) {
             testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory("invalid/path") // Setting a non-existent path
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 11 =====
```
                 .setResultFileOutputFormatIsCSV(isCSVFormat)
                 .setProxyConfig(proxyConfig)
                 .setLogRootOverride(overrideRootLogLevel)
-                .setLogsDirectory(logsDirectory.getAbsolutePath())
+                .setLogsDirectory(logsDirectory.getAbsolutePath() + "/logs") // Appending an extra directory that may not exist
                 .addACustomPropertiesFiles(customPropertiesFiles);
         if (generateReports && disableGUI) {
             testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath() + "/logs") // Appending an extra directory that may not exist
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 12 =====
```
                 .setResultFileOutputFormatIsCSV(isCSVFormat)
                 .setProxyConfig(proxyConfig)
                 .setLogRootOverride(overrideRootLogLevel)
-                .setLogsDirectory(logsDirectory.getAbsolutePath())
+                .setLogsDirectory(logsDirectory.getAbsolutePath().replace("logs", "invalidLogs")) // Changing the directory name incorrectly
                 .addACustomPropertiesFiles(customPropertiesFiles);
         if (generateReports && disableGUI) {
             testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath().replace("logs", "invalidLogs")) // Changing the directory name incorrectly
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 13 =====
```
                 .setResultFileOutputFormatIsCSV(isCSVFormat)
                 .setProxyConfig(proxyConfig)
                 .setLogRootOverride(overrideRootLogLevel)
-                .setLogsDirectory(logsDirectory.getAbsolutePath())
+                .setLogsDirectory(null)
                 .addACustomPropertiesFiles(customPropertiesFiles);
         if (generateReports && disableGUI) {
             testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(null)
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 14 =====
```
                 .setLogRootOverride(overrideRootLogLevel)
                 .setLogsDirectory(logsDirectory.getAbsolutePath())
                 .addACustomPropertiesFiles(customPropertiesFiles);
-        if (generateReports && disableGUI) {
+        if (generateReports && !disableGUI) {
             testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
         }
         if (testResultsTimestamp) {
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && !disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 15 =====
```
                 .setLogsDirectory(logsDirectory.getAbsolutePath())
                 .addACustomPropertiesFiles(customPropertiesFiles);
         if (generateReports && disableGUI) {
-            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
+            
         }
         if (testResultsTimestamp) {
             testArgs.setResultsTimestamp(true)
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 16 =====
```
                 .setLogsDirectory(logsDirectory.getAbsolutePath())
                 .addACustomPropertiesFiles(customPropertiesFiles);
         if (generateReports && disableGUI) {
-            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
+            testArgs.setReportsDirectory("");
         }
         if (testResultsTimestamp) {
             testArgs.setResultsTimestamp(true)
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory("");
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 17 =====
```
                 .setLogsDirectory(logsDirectory.getAbsolutePath())
                 .addACustomPropertiesFiles(customPropertiesFiles);
         if (generateReports && disableGUI) {
-            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
+            testArgs.setReportsDirectory(null);
         }
         if (testResultsTimestamp) {
             testArgs.setResultsTimestamp(true)
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(null);
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 18 =====
```
                 .setLogsDirectory(logsDirectory.getAbsolutePath())
                 .addACustomPropertiesFiles(customPropertiesFiles);
         if (generateReports && disableGUI) {
-            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
+            testArgs.setReportsDirectory(resultsDirectory.getAbsolutePath());
         }
         if (testResultsTimestamp) {
             testArgs.setResultsTimestamp(true)
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(resultsDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 19 =====
```
                 .setLogsDirectory(logsDirectory.getAbsolutePath())
                 .addACustomPropertiesFiles(customPropertiesFiles);
         if (generateReports && disableGUI) {
-            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
+            testArgs.setResultsDirectory(reportDirectory.getAbsolutePath());
         }
         if (testResultsTimestamp) {
             testArgs.setResultsTimestamp(true)
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setResultsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 20 =====
```
                 .setLogsDirectory(logsDirectory.getAbsolutePath())
                 .addACustomPropertiesFiles(customPropertiesFiles);
         if (generateReports && disableGUI) {
-            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
+            testArgs.setResultsDirectory(resultsDirectory.getAbsolutePath() + "/reports");
         }
         if (testResultsTimestamp) {
             testArgs.setResultsTimestamp(true)
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setResultsDirectory(resultsDirectory.getAbsolutePath() + "/reports");
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 21 =====
```
         if (generateReports && disableGUI) {
             testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
         }
-        if (testResultsTimestamp) {
+        if (!testResultsTimestamp) {
             testArgs.setResultsTimestamp(true)
                     .appendTimestamp(appendResultsTimestamp)
                     .setResultsFileNameDateFormat(resultsFileNameDateFormat);
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (!testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 22 =====
```
         if (generateReports && disableGUI) {
             testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
         }
-        if (testResultsTimestamp) {
+        if (testResultsTimestamp && !appendResultsTimestamp) {
             testArgs.setResultsTimestamp(true)
                     .appendTimestamp(appendResultsTimestamp)
                     .setResultsFileNameDateFormat(resultsFileNameDateFormat);
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp && !appendResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 23 =====
```
         if (generateReports && disableGUI) {
             testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
         }
-        if (testResultsTimestamp) {
+        if (testResultsTimestamp && resultsFileNameDateFormat == null) {
             testArgs.setResultsTimestamp(true)
                     .appendTimestamp(appendResultsTimestamp)
                     .setResultsFileNameDateFormat(resultsFileNameDateFormat);
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp && resultsFileNameDateFormat == null) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 24 =====
```
             testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
         }
         if (testResultsTimestamp) {
-            testArgs.setResultsTimestamp(true)
-                    .appendTimestamp(appendResultsTimestamp)
-                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
+            
         }
 
         return testArgs;
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            
        }

        return testArgs;
    }
```
===== 25 =====
```
             testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
         }
         if (testResultsTimestamp) {
-            testArgs.setResultsTimestamp(true)
+            testArgs.appendTimestamp(false)
                     .appendTimestamp(appendResultsTimestamp)
                     .setResultsFileNameDateFormat(resultsFileNameDateFormat);
         }
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.appendTimestamp(false)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 26 =====
```
             testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
         }
         if (testResultsTimestamp) {
-            testArgs.setResultsTimestamp(true)
+            testArgs.setResultsFileNameDateFormat("invalid_format")
                     .appendTimestamp(appendResultsTimestamp)
                     .setResultsFileNameDateFormat(resultsFileNameDateFormat);
         }
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsFileNameDateFormat("invalid_format")
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 27 =====
```
             testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
         }
         if (testResultsTimestamp) {
-            testArgs.setResultsTimestamp(true)
+            testArgs.setResultsFileNameDateFormat(null)
                     .appendTimestamp(appendResultsTimestamp)
                     .setResultsFileNameDateFormat(resultsFileNameDateFormat);
         }
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsFileNameDateFormat(null)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 28 =====
```
             testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
         }
         if (testResultsTimestamp) {
-            testArgs.setResultsTimestamp(true)
+            testArgs.setResultsTimestamp(false)
                     .appendTimestamp(appendResultsTimestamp)
                     .setResultsFileNameDateFormat(resultsFileNameDateFormat);
         }
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(false)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 29 =====
```
         }
         if (testResultsTimestamp) {
             testArgs.setResultsTimestamp(true)
-                    .appendTimestamp(appendResultsTimestamp)
+                    .appendTimestamp(!appendResultsTimestamp)
                     .setResultsFileNameDateFormat(resultsFileNameDateFormat);
         }
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(!appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 30 =====
```
         }
         if (testResultsTimestamp) {
             testArgs.setResultsTimestamp(true)
-                    .appendTimestamp(appendResultsTimestamp)
+                    .appendTimestamp(appendResultsTimestamp && !testResultsTimestamp)
                     .setResultsFileNameDateFormat(resultsFileNameDateFormat);
         }
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp && !testResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 31 =====
```
         }
         if (testResultsTimestamp) {
             testArgs.setResultsTimestamp(true)
-                    .appendTimestamp(appendResultsTimestamp)
+                    .appendTimestamp(appendResultsTimestamp ? false : true)
                     .setResultsFileNameDateFormat(resultsFileNameDateFormat);
         }
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp ? false : true)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 32 =====
```
         }
         if (testResultsTimestamp) {
             testArgs.setResultsTimestamp(true)
-                    .appendTimestamp(appendResultsTimestamp)
+                    .appendTimestamp(false)
                     .setResultsFileNameDateFormat(resultsFileNameDateFormat);
         }
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(false)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
        }

        return testArgs;
    }
```
===== 33 =====
```
         if (testResultsTimestamp) {
             testArgs.setResultsTimestamp(true)
                     .appendTimestamp(appendResultsTimestamp)
-                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
+                    .setResultsFileNameDateFormat(""); // Sets an empty string instead of the intended format
         }
 
         return testArgs;
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(""); // Sets an empty string instead of the intended format
        }

        return testArgs;
    }
```
===== 34 =====
```
         if (testResultsTimestamp) {
             testArgs.setResultsTimestamp(true)
                     .appendTimestamp(appendResultsTimestamp)
-                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
+                    .setResultsFileNameDateFormat("defaultFormat"); // Sets a hardcoded default format instead of the provided one
         }
 
         return testArgs;
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat("defaultFormat"); // Sets a hardcoded default format instead of the provided one
        }

        return testArgs;
    }
```
===== 35 =====
```
         if (testResultsTimestamp) {
             testArgs.setResultsTimestamp(true)
                     .appendTimestamp(appendResultsTimestamp)
-                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
+                    .setResultsFileNameDateFormat(null);
         }
 
         return testArgs;
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(null);
        }

        return testArgs;
    }
```
===== 36 =====
```
         if (testResultsTimestamp) {
             testArgs.setResultsTimestamp(true)
                     .appendTimestamp(appendResultsTimestamp)
-                    .setResultsFileNameDateFormat(resultsFileNameDateFormat);
+                    .setResultsFileNameDateFormat(resultsFileNameDateFormat + "_suffix"); // Appends a suffix to the format, altering the intended behavior
         }
 
         return testArgs;
```
```
    /**
     * Generate the initial JMeter Arguments array that is used to create the command line that we pass to JMeter.
     *
     * @param disableGUI Prevent JMeter gGUI from starting up
     * @param isCSVFormat Determines if results output is in CSV formate of legacy JTL format
     * @param jmeterDirectoryPath Path to the JMeter directory
     * @return
     * @throws MojoExecutionException If unable to generate arguments array
     */
    protected JMeterArgumentsArray computeJMeterArgumentsArray(boolean disableGUI, boolean isCSVFormat, String jmeterDirectoryPath) throws MojoExecutionException {
        JMeterArgumentsArray testArgs = new JMeterArgumentsArray(disableGUI, jmeterDirectoryPath)
                .setResultsDirectory(resultsDirectory.getAbsolutePath())
                .setResultFileOutputFormatIsCSV(isCSVFormat)
                .setProxyConfig(proxyConfig)
                .setLogRootOverride(overrideRootLogLevel)
                .setLogsDirectory(logsDirectory.getAbsolutePath())
                .addACustomPropertiesFiles(customPropertiesFiles);
        if (generateReports && disableGUI) {
            testArgs.setReportsDirectory(reportDirectory.getAbsolutePath());
        }
        if (testResultsTimestamp) {
            testArgs.setResultsTimestamp(true)
                    .appendTimestamp(appendResultsTimestamp)
                    .setResultsFileNameDateFormat(resultsFileNameDateFormat + "_suffix"); // Appends a suffix to the format, altering the intended behavior
        }

        return testArgs;
    }
```
