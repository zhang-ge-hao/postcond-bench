package com.example.fatrunner;

import org.junit.platform.engine.*;
import org.junit.platform.engine.support.descriptor.*;
import org.junit.platform.launcher.*;
import org.junit.platform.launcher.core.*;
import org.junit.platform.launcher.listeners.*;
import org.junit.platform.reporting.legacy.xml.LegacyXmlReportGeneratingListener;

import java.io.*;
import java.lang.reflect.InvocationTargetException;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.stream.Collectors;

import static org.junit.platform.engine.discovery.DiscoverySelectors.*;
import static org.junit.platform.launcher.EngineFilter.includeEngines;

// JaCoCo core/report
import org.jacoco.core.analysis.CoverageBuilder;
import org.jacoco.core.analysis.IBundleCoverage;
import org.jacoco.core.analysis.Analyzer;
import org.jacoco.core.tools.ExecFileLoader;
import org.jacoco.report.IReportVisitor;
import org.jacoco.report.MultiSourceFileLocator;
import org.jacoco.report.DirectorySourceFileLocator;
import org.jacoco.report.xml.XMLFormatter;

public class Main {

  public static void main(String[] args) {
    Map<String, List<String>> opts = parseArgs(args);

    // ---- config source roots (for source mapping in jacoco.xml) -------------
    configureSourceRoots(opts);

    // ---- parse -Dtest / -DexcludedTests (exact match only) ------------------
    ExactProps exact = parseExactSystemProperties(); // include / exclude sets

    // ---- Build a broad discovery request (Jupiter + Vintage) ----------------
    LauncherDiscoveryRequestBuilder rb = LauncherDiscoveryRequestBuilder.request();

    // 1) only Jupiter + Vintage
    rb.filters(includeEngines("junit-jupiter", "junit-vintage"));

    // 2) classpath roots scan + default test naming
    Set<Path> roots = classpathRoots();
    rb.selectors(selectClasspathRoots(roots));
    rb.filters(org.junit.platform.engine.discovery.ClassNameFilter
        .includeClassNamePatterns(".*(Test|Tests|TestCase|IT)$"));

    // // 3) explicit selectors for -Dtest includes (even if not matching naming)
    // addExplicitSelectorsForIncludes(rb, exact);

    // 4) tag filters (from CLI)
    for (String inc : opts.getOrDefault("include-tag", Collections.emptyList()))
      rb.filters(TagFilter.includeTags(inc));
    for (String exc : opts.getOrDefault("exclude-tag", Collections.emptyList()))
      rb.filters(TagFilter.excludeTags(exc));

    Launcher launcher = LauncherFactory.create();

    // ---- Phase 1: discover all candidates; then exact filter ----------------
    TestPlan plan = launcher.discover(rb.build());
    List<DiscoveredTest> allTests = collectDiscoveredTests(plan);
    List<DiscoveredTest> selected = filterByExactProps(allTests, exact);

    if (exact.hasIncludes() && selected.isEmpty()) {
      System.err.println("[Runner] WARN: -Dtest 指定的用例未匹配到任何已发现的测试。");
    }

    // ---- Phase 2: execute by UniqueId (works for JUnit4/5/parameterized) ----
    LauncherDiscoveryRequestBuilder exec = LauncherDiscoveryRequestBuilder.request();
    exec.filters(includeEngines("junit-jupiter", "junit-vintage"));
    if (selected.isEmpty() && !exact.hasIncludes()) {
      for (DiscoveredTest t : allTests) exec.selectors(selectUniqueId(t.uniqueId));
    } else {
      for (DiscoveredTest t : selected) exec.selectors(selectUniqueId(t.uniqueId));
    }

    // ---- listeners ----------------------------------------------------------
    SummaryGeneratingListener summaryListener = new SummaryGeneratingListener();

    // Surefire-compatible XML reports (like `mvn test`)
    Path surefireDir = Paths.get("target", "surefire-reports").toAbsolutePath();
    try { Files.createDirectories(surefireDir); } catch (IOException ignore) {}
    LegacyXmlReportGeneratingListener surefireXml =
        new LegacyXmlReportGeneratingListener(
            surefireDir,
            new PrintWriter(System.out, true)
        );

    launcher.registerTestExecutionListeners(summaryListener, surefireXml);

    // ---- Execute ------------------------------------------------------------
    launcher.execute(exec.build());

    // ---- After execute: force JaCoCo dump to file before loading ------------
    try {
      Class<?> rt = Class.forName("org.jacoco.agent.rt.RT");
      Object agent = rt.getMethod("getAgent").invoke(null);
      if (agent != null) {
        agent.getClass().getMethod("dump", boolean.class).invoke(agent, false); // don't reset
        System.err.println("[JaCoCo] dump(false) after execute.");
      } else {
        System.err.println("[JaCoCo] agent not present (getAgent()==null).");
      }
    } catch (Throwable t) {
      System.err.println("[JaCoCo] dump failed: " + rootCause(t));
    }

    // ---- Load exec data & generate jacoco.xml -------------------------------
    try {
      ExecFileLoader loader = loadExecData(); // merge in-memory + jacoco.exec if available
      generateJacocoReports(loader, discoverClassDirs(), SRC_ROOTS);
    } catch (Throwable t) {
      System.err.println("WARN: coverage report generation failed: " + rootCause(t));
    }

    // ---- Console summary ----------------------------------------------------
    TestExecutionSummary s = summaryListener.getSummary();
    try (PrintWriter out = new PrintWriter(System.out)) { s.printTo(out); }
    try (PrintWriter err = new PrintWriter(System.err)) { s.printFailuresTo(err); }

    System.exit((int) Math.min(255, s.getFailures().size()));
  }

  // ========================================================================
  // Discovery & exact filtering
  // ========================================================================

  static class DiscoveredTest {
    final String uniqueId;
    final String className;   // FQCN
    final String methodName;  // may be null
    DiscoveredTest(String uniqueId, String className, String methodName) {
      this.uniqueId = uniqueId; this.className = className; this.methodName = methodName;
    }
  }

  private static List<DiscoveredTest> collectDiscoveredTests(TestPlan plan) {
    List<DiscoveredTest> out = new ArrayList<>();
    for (TestIdentifier ti : plan.getRoots()) {
      traverse(plan, ti, out);
    }
    return out;
  }

  private static void traverse(TestPlan plan, TestIdentifier id, List<DiscoveredTest> out) {
    if (id.isTest()) {
      String className = null, methodName = null;
      Optional<TestSource> src = id.getSource();
      if (src.isPresent()) {
        TestSource s = src.get();
        if (s instanceof MethodSource) {
          MethodSource ms = (MethodSource) s;
          className = ms.getClassName();
          methodName = ms.getMethodName();
        } else if (s instanceof ClassSource) {
          ClassSource cs = (ClassSource) s;
          className = cs.getClassName();
        }
      }
      if (className != null) out.add(new DiscoveredTest(id.getUniqueId(), className, methodName));
    }
    for (TestIdentifier c : plan.getChildren(id)) traverse(plan, c, out);
  }

  static class ExactProps {
    final Set<String> includeExact = new LinkedHashSet<>();
    final Set<String> excludeExact = new LinkedHashSet<>();
    boolean hasIncludes() { return !includeExact.isEmpty(); }
  }

  private static ExactProps parseExactSystemProperties() {
    ExactProps ep = new ExactProps();
    String inc = System.getProperty("test");
    String exc = System.getProperty("excludedTests");
    if (exc == null || exc.isBlank()) exc = System.getProperty("excludeTests");
    if (inc != null && !inc.isBlank()) {
      for (String t : inc.split(",")) {
        String s = t.trim();
        if (!s.isEmpty()) ep.includeExact.add(s);
      }
    }
    if (exc != null && !exc.isBlank()) {
      for (String t : exc.split(",")) {
        String s = t.trim();
        if (!s.isEmpty()) ep.excludeExact.add(s);
      }
    }
    return ep;
  }

  private static void addExplicitSelectorsForIncludes(LauncherDiscoveryRequestBuilder rb, ExactProps ep) {
    if (ep.includeExact.isEmpty()) return;
    for (String it : ep.includeExact) {
      int pos = it.indexOf('#');
      if (pos < 0) {
        rb.selectors(selectClass(it));
      } else {
        String cls = it.substring(0, pos);
        String mth = it.substring(pos + 1);
        rb.selectors(selectMethod(cls, mth));
      }
    }
  }

  private static List<DiscoveredTest> filterByExactProps(List<DiscoveredTest> all, ExactProps ep) {
    if (all.isEmpty()) return all;
    if (!ep.hasIncludes() && ep.excludeExact.isEmpty()) return all;

    Map<String, List<DiscoveredTest>> byClass =
        all.stream().collect(Collectors.groupingBy(t -> t.className, LinkedHashMap::new, Collectors.toList()));
    Map<String, List<DiscoveredTest>> byMethod = new LinkedHashMap<>();
    for (DiscoveredTest t : all) {
      if (t.methodName != null) {
        byMethod.computeIfAbsent(t.className + "#" + t.methodName, k -> new ArrayList<>()).add(t);
      }
    }

    LinkedHashSet<DiscoveredTest> sel = new LinkedHashSet<>();
    if (ep.hasIncludes()) {
      for (String k : ep.includeExact) {
        if (k.indexOf('#') < 0) {
          List<DiscoveredTest> v = byClass.get(k);
          if (v != null) sel.addAll(v);
        } else {
          List<DiscoveredTest> v = byMethod.get(k);
          if (v != null) sel.addAll(v);
        }
      }
    } else {
      sel.addAll(all);
    }

    if (!ep.excludeExact.isEmpty()) {
      sel.removeIf(t -> ep.excludeExact.contains(t.className) ||
          (t.methodName != null && ep.excludeExact.contains(t.className + "#" + t.methodName)));
    }

    return new ArrayList<>(sel);
  }

  // ========================================================================
  // JaCoCo: exec loading + report generation
  // ========================================================================

  private static ExecFileLoader loadExecData() throws Exception {
    ExecFileLoader loader = new ExecFileLoader();

    // a) from in-memory agent (if present)
    try {
      Class<?> rt = Class.forName("org.jacoco.agent.rt.RT");
      Object agent = rt.getMethod("getAgent").invoke(null);
      if (agent != null) {
        byte[] bytes = (byte[]) agent.getClass().getMethod("getExecutionData", boolean.class).invoke(agent, false);
        if (bytes != null && bytes.length > 0) {
          loader.load(new ByteArrayInputStream(bytes));
          System.err.println("[JaCoCo] merged in-memory exec: " + bytes.length + " bytes");
        }
      }
    } catch (Throwable ignore) {}

    // b) merge jacoco.exec in CWD (even if already had memory data)
    Path cwdExec = Paths.get("jacoco.exec");
    if (Files.exists(cwdExec)) {
      long sz = Files.size(cwdExec);
      if (sz > 0) {
        try {
          loader.load(cwdExec.toFile());
          System.err.println("[JaCoCo] merged file exec: " + cwdExec.toAbsolutePath() + " (" + sz + " bytes)");
        } catch (Throwable t) {
          System.err.println("[JaCoCo] WARN: failed to load jacoco.exec: " + rootCause(t));
        }
      } else {
        System.err.println("[JaCoCo] WARN: jacoco.exec is empty.");
      }
    } else {
      System.err.println("[JaCoCo] WARN: jacoco.exec not found.");
    }

    int entries = loader.getExecutionDataStore().getContents().size();
    int sessions = loader.getSessionInfoStore().getInfos().size();
    System.err.println("[JaCoCo] exec entries=" + entries + ", sessions=" + sessions);

    return loader; // may be empty; we'll still generate XML (all 0) for diagnostics
  }

  private static void generateJacocoReports(ExecFileLoader loader, List<Path> classDirs, List<Path> sourceRoots) throws IOException {
    Path outDir = Paths.get("target", "site", "jacoco").toAbsolutePath();
    Files.createDirectories(outDir);

    XMLFormatter xmlFormatter = new XMLFormatter();
    try (OutputStream os = Files.newOutputStream(outDir.resolve("jacoco.xml"))) {
      IReportVisitor visitor = xmlFormatter.createVisitor(os);

      // 1) write session & exec data (even if empty)
      visitor.visitInfo(loader.getSessionInfoStore().getInfos(), loader.getExecutionDataStore().getContents());

      // 2) analyze classes: first from disk dirs, then (if needed) from self jar
      CoverageBuilder coverageBuilder = new CoverageBuilder();
      Analyzer analyzer = new Analyzer(loader.getExecutionDataStore(), coverageBuilder);

      int before = coverageBuilder.getClasses().size();
      for (Path dir : classDirs) {
        if (Files.isDirectory(dir)) {
          System.err.println("[JaCoCo] analyzing dir: " + dir);
          analyzer.analyzeAll(dir.toFile());
        }
      }
      int afterDirs = coverageBuilder.getClasses().size();
      System.err.println("[JaCoCo] classes after dir-scan: " + afterDirs);

      if (afterDirs == before) {
        // scan classes directly from the running fat jar
        Path selfJar = null;
        try {
          URL loc = Main.class.getProtectionDomain().getCodeSource().getLocation();
          if (loc != null && "file".equalsIgnoreCase(loc.getProtocol())) {
            Path cand = Paths.get(loc.toURI());
            if (Files.isRegularFile(cand)) selfJar = cand;
          }
        } catch (Exception e) {
          System.err.println("[JaCoCo] WARN: cannot locate self jar: " + rootCause(e));
        }

        if (selfJar != null) {
          System.err.println("[JaCoCo] analyzing classes from self jar: " + selfJar);
          int cnt = 0;
          try (java.util.zip.ZipFile zf = new java.util.zip.ZipFile(selfJar.toFile())) {
            Enumeration<? extends java.util.zip.ZipEntry> en = zf.entries();
            while (en.hasMoreElements()) {
              java.util.zip.ZipEntry ze = en.nextElement();
              if (!ze.isDirectory() && ze.getName().endsWith(".class")) {
                try (InputStream is = zf.getInputStream(ze)) {
                  analyzer.analyzeClass(is, ze.getName());
                  cnt++;
                } catch (IOException ioe) {
                  System.err.println("[JaCoCo] WARN: analyze jar entry failed: " + ze.getName() + " : " + rootCause(ioe));
                }
              }
            }
          } catch (IOException ioe) {
            System.err.println("[JaCoCo] WARN: open self jar failed: " + rootCause(ioe));
          }
          System.err.println("[JaCoCo] jar entries analyzed: " + cnt);
        } else {
          System.err.println("[JaCoCo] WARN: self jar not resolved; no classes to analyze.");
        }
        System.err.println("[JaCoCo] classes after jar-scan: " + coverageBuilder.getClasses().size());
      }

      // 3) source mapping (optional but helpful)
      int tabWidth = 4;
      MultiSourceFileLocator msl = new MultiSourceFileLocator(tabWidth);
      for (Path src : sourceRoots) {
        if (Files.isDirectory(src)) {
          msl.add(new DirectorySourceFileLocator(src.toFile(), StandardCharsets.UTF_8.name(), tabWidth));
        }
      }

      String bundleName = Optional.ofNullable(System.getProperty("project.name")).orElse("project");
      IBundleCoverage bundle = coverageBuilder.getBundle(bundleName);
      System.err.println("[JaCoCo] bundle classes total: " + bundle.getClassCounter().getTotalCount());

      visitor.visitBundle(bundle, msl);
      visitor.visitEnd();
      os.flush();
    }
  }

  // ========================================================================
  // Utilities
  // ========================================================================

  private static Set<Path> classpathRoots() {
    Set<Path> set = new LinkedHashSet<>();
    String cp = System.getProperty("java.class.path");
    if (cp != null && !cp.isEmpty()) {
      for (String e : cp.split(File.pathSeparator)) {
        if (e != null && !e.isBlank()) set.add(Paths.get(e).toAbsolutePath().normalize());
      }
    }
    try {
      URL loc = Main.class.getProtectionDomain().getCodeSource().getLocation();
      if (loc != null) set.add(Paths.get(loc.toURI()).toAbsolutePath().normalize());
    } catch (Exception ignore) {}
    return set;
  }

  private static Map<String, List<String>> parseArgs(String[] args) {
    Map<String, List<String>> m = new HashMap<>();
    String k = null;
    for (String a : args) {
      if (a.startsWith("--")) { k = a.substring(2); m.putIfAbsent(k, new ArrayList<>()); }
      else if (k != null) { for (String v : a.split(",")) if (!v.isEmpty()) m.get(k).add(v.trim()); }
    }
    return m;
  }

  // ---------- project-relative path support --------------------------------

  private static List<Path> SRC_ROOTS = discoverDefaultSourceRoots();

  private static void configureSourceRoots(Map<String, List<String>> opts) {
    List<String> fromCli = opts.get("src-roots");
    String fromSys = System.getProperty("fattest.sourceRoots");
    List<String> tokens = new ArrayList<>();
    if (fromCli != null && !fromCli.isEmpty()) tokens.addAll(fromCli);
    if (fromSys != null && !fromSys.isBlank()) tokens.add(fromSys);

    if (!tokens.isEmpty()) {
      List<Path> roots = new ArrayList<>();
      Path base = Paths.get(System.getProperty("user.dir"));
      for (String tokenList : tokens) {
        for (String token : tokenList.split(",")) {
          String t = token.trim();
          if (t.isEmpty()) continue;
          Path p = base.resolve(t).toAbsolutePath().normalize();
          if (Files.isDirectory(p)) roots.add(p);
        }
      }
      if (!roots.isEmpty()) SRC_ROOTS = roots;
    }
  }

  private static List<Path> discoverDefaultSourceRoots() {
    Path base = Paths.get(System.getProperty("user.dir"));
    String[] defaults = {
        "src/main/java", "src/test/java",
        "src/main/kotlin", "src/test/kotlin",
        "src/main/scala", "src/test/scala"
    };
    List<Path> roots = new ArrayList<>();
    for (String d : defaults) {
      Path p = base.resolve(d).toAbsolutePath().normalize();
      if (Files.isDirectory(p)) roots.add(p);
    }
    return roots;
  }

  private static List<Path> discoverClassDirs() {
    // Prefer common build output folders
    List<Path> candidates = new ArrayList<>();
    Path base = Paths.get(System.getProperty("user.dir")).toAbsolutePath().normalize();
    String[][] patterns = {
        {"target", "classes"},
        {"target", "test-classes"},
        {"build", "classes", "java", "main"},
        {"build", "classes", "java", "test"}
    };
    for (String[] p : patterns) {
      Path dir = base.resolve(Paths.get("", p));
      if (Files.isDirectory(dir)) candidates.add(dir);
    }
    // Fallback: any classpath directories containing .class files
    for (Path cp : classpathRoots()) {
      if (Files.isDirectory(cp)) {
        try {
          boolean hasClass = Files.walk(cp, 2).anyMatch(f -> f.toString().endsWith(".class"));
          if (hasClass && !candidates.contains(cp)) candidates.add(cp);
        } catch (IOException ignore) {}
      }
    }
    return candidates;
  }

  // Extract the deepest cause for concise logs
  private static Throwable rootCause(Throwable t) {
    if (t == null) return null;
    Throwable c = t;
    if (c instanceof InvocationTargetException && ((InvocationTargetException) c).getCause() != null) {
      c = ((InvocationTargetException) c).getCause();
    }
    while (c.getCause() != null && c.getCause() != c) c = c.getCause();
    return c;
  }
}
