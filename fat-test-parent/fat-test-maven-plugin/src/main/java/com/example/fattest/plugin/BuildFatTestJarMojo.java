package com.example.fattest.plugin;

import org.apache.maven.artifact.Artifact;
import org.apache.maven.plugin.AbstractMojo;
import org.apache.maven.plugin.MojoExecutionException;
import org.apache.maven.plugins.annotations.*;
import org.apache.maven.project.MavenProject;
import org.apache.maven.project.ProjectDependenciesResolver;
import org.apache.maven.project.DefaultDependencyResolutionRequest;
import org.apache.maven.project.DependencyResolutionResult;

import org.eclipse.aether.RepositorySystemSession;
import org.eclipse.aether.graph.DependencyNode;
import org.eclipse.aether.graph.Dependency;
import org.eclipse.aether.util.filter.ScopeDependencyFilter;

import java.io.*;
import java.net.URI;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.jar.*;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

@Mojo(
    name = "build",
    defaultPhase = LifecyclePhase.PACKAGE,
    requiresDependencyResolution = ResolutionScope.TEST,
    threadSafe = true
)
@Execute(phase = LifecyclePhase.TEST_COMPILE) // 先确保 test-classes 生成
public class BuildFatTestJarMojo extends AbstractMojo {

  @Parameter(defaultValue = "${project}", readonly = true, required = true)
  private MavenProject project;

  @Parameter(defaultValue = "${repositorySystemSession}", readonly = true, required = true)
  private RepositorySystemSession repoSession;

  @Component
  private ProjectDependenciesResolver dependenciesResolver;

  @Parameter(property = "outputFile",
      defaultValue = "${project.build.directory}/${project.artifactId}-${project.version}-fat-tests.jar")
  private File outputFile;

  @Parameter(property = "includeSources", defaultValue = "true")
  private boolean includeSources;

  /** 是否把 provided/system 依赖（含传递闭包）一并打入 */
  @Parameter(property = "fattest.includeProvided", defaultValue = "true")
  private boolean includeProvided;

  /** 是否额外输出一个可供 javac 使用的 classpath.txt */
  @Parameter(property = "fattest.writeClasspathTxt", defaultValue = "true")
  private boolean writeClasspathTxt;

  @Parameter(property = "fattest.classpathTxt",
      defaultValue = "${project.build.directory}/fattest/classpath.txt")
  private File classpathTxt;

  @Override
  public void execute() throws MojoExecutionException {
    Path staging = null;
    try {
      staging = Files.createTempDirectory("fat-tests-");

      // -------------------------------
      // 0) 收集基础路径
      // -------------------------------
      Path classes = Paths.get(project.getBuild().getOutputDirectory());
      Path testClasses = Paths.get(project.getBuild().getTestOutputDirectory());

      // -------------------------------
      // 1) 放入项目 main/test 产物
      // -------------------------------
      if (Files.isDirectory(classes)) copyDir(classes, staging);
      if (Files.isDirectory(testClasses)) copyDir(testClasses, staging);

      // 1.1 写入“主代码 class 清单”供 runner 限定覆盖率范围
      if (Files.isDirectory(classes)) {
        List<String> mainClasses = new ArrayList<String>();
        try (java.util.stream.Stream<Path> s = Files.walk(classes)) {
          s.filter(p -> p.toString().endsWith(".class"))
           .forEach(p -> mainClasses.add(
               classes.relativize(p).toString().replace('\\', '/')));
        } catch (IOException ioe) {
          throw new MojoExecutionException("Walk main classes failed", ioe);
        }
        Path meta = staging.resolve("META-INF/fattest");
        Files.createDirectories(meta);
        Files.write(meta.resolve("project-classes.lst"), mainClasses, StandardCharsets.UTF_8);
      }

      // -------------------------------
      // 2) 以“测试运行时 classpath”为准解包（目录 copy，jar 解包）
      // -------------------------------
      // 2) 用 testClasspathElements 先把目录复制进来（通常包含本模块和部分 reactor 目录）
      @SuppressWarnings("unchecked")
      List<String> testCp = project.getTestClasspathElements();
      for (String cp : testCp) {
        Path p = Paths.get(cp);
        if (Files.isDirectory(p)) {
          copyDir(p, staging);
        }
      }

      // 2.1) 再解常规依赖 JAR（TEST 分辨率）：project.getArtifacts()
      @SuppressWarnings("unchecked")
      Set<org.apache.maven.artifact.Artifact> arts = project.getArtifacts();
      if (arts != null) {
        for (org.apache.maven.artifact.Artifact a : arts) {
          File f = a.getFile();
          if (f != null && f.getName().endsWith(".jar")) {
            unpackJar(f.toPath(), staging);
          }
        }
      }

      // 2.2) reactor 依赖回落：有些依赖是同一个 reactor 里的模块，此时 a.getFile() 可能为 null，
      //     需要把它们的 target/classes / target/test-classes 也拷进来
      Map<String, MavenProject> refs = project.getProjectReferences();
      if (arts != null && refs != null && !refs.isEmpty()) {
        for (org.apache.maven.artifact.Artifact a : arts) {
          if (a.getFile() != null) continue;
          String key = a.getGroupId() + ":" + a.getArtifactId();
          MavenProject mp = refs.get(key);
          if (mp == null) continue;
          Path out = Paths.get(mp.getBuild().getOutputDirectory());
          Path testOut = Paths.get(mp.getBuild().getTestOutputDirectory());
          if (Files.isDirectory(out)) copyDir(out, staging);
          if (Files.isDirectory(testOut)) copyDir(testOut, staging);
        }
      }

      // -------------------------------
      // 3) 补齐 provided/system 的“传递闭包”（受开关控制）
      // -------------------------------
      if (includeProvided) {
        for (Path jar : resolveProvidedClosureJars()) {
          unpackJar(jar, staging);
        }
      }

      // -------------------------------
      // 4) 按需补齐 runner / JUnit Platform / Vintage / ECJ / JUnit4 / JaCoCo / ASM / reporting
      // -------------------------------

      // 4.0 runner（总是需要）
      if (!exists(staging, "com/example/fatrunner/Main.class")) {
        Path runnerJar = locateJarOf("com/example/fatrunner/Main.class");
        if (runnerJar != null) unpackJar(runnerJar, staging);
        else getLog().warn("Runner jar not found on plugin classpath.");
      }

      // 4.1 JUnit Platform launcher（若项目没带，则用插件侧 console-standalone）
      if (!exists(staging, "org/junit/platform/launcher/core/LauncherDiscoveryRequestBuilder.class")) {
        Path junitPlatform = locateJarOf("org/junit/platform/console/ConsoleLauncher.class");
        if (junitPlatform == null)
          junitPlatform = locateJarOf("org/junit/platform/launcher/core/LauncherDiscoveryRequestBuilder.class");
        if (junitPlatform != null) unpackJar(junitPlatform, staging);
        else getLog().warn("No JUnit Platform launcher found; tests may not run.");
      }

      // 4.2 Vintage（JUnit4 桥），按需补
      if (!exists(staging, "org/junit/vintage/engine/VintageTestEngine.class")) {
        Path vintage = locateJarOf("org/junit/vintage/engine/VintageTestEngine.class");
        if (vintage != null) unpackJar(vintage, staging);
      }

      // 4.2.1 ECJ（Vintage 的 TestSource 可能会用到）
      if (!exists(staging, "org/eclipse/jdt/internal/compiler/ast/AbstractMethodDeclaration.class")) {
        Path ecj = locateJarOf("org/eclipse/jdt/internal/compiler/ast/AbstractMethodDeclaration.class");
        if (ecj != null) unpackJar(ecj, staging);
        else getLog().warn("ECJ not found; Vintage source mapping may fail.");
      }

      // 4.3 JUnit4 本体，按需补
      if (!exists(staging, "org/junit/runner/JUnitCore.class")) {
        Path junit4 = locateJarOf("org/junit/runner/JUnitCore.class");
        if (junit4 != null) unpackJar(junit4, staging);
      }

      // 4.4 JaCoCo agent
      Path jacocoAgentJar = locateJarOf("org/jacoco/agent/rt/RT.class");
      if (jacocoAgentJar != null) {
        Path meta = staging.resolve("META-INF/fattest");
        Files.createDirectories(meta);
        Files.copy(jacocoAgentJar, meta.resolve("jacoco-agent.jar"), StandardCopyOption.REPLACE_EXISTING);
        if (!exists(staging, "org/jacoco/agent/rt/RT.class")) {
          unpackJar(jacocoAgentJar, staging);
        }
      } else {
        getLog().warn("JaCoCo agent jar not found on plugin classpath; coverage via -javaagent unavailable.");
      }

      // 4.5 JaCoCo core（解析 exec），按需补
      if (!exists(staging, "org/jacoco/core/analysis/ICoverageVisitor.class")) {
        Path jacocoCore = locateJarOf("org/jacoco/core/analysis/ICoverageVisitor.class");
        if (jacocoCore == null) jacocoCore = locateJarOf("org/jacoco/core/tools/ExecFileLoader.class");
        if (jacocoCore != null) unpackJar(jacocoCore, staging);
        else getLog().warn("JaCoCo core not found; coverage reporting will be disabled.");
      }

      // 4.6 ASM 依赖，按需补
      if (!exists(staging, "org/objectweb/asm/ClassReader.class")) {
        Path asm = locateJarOf("org/objectweb/asm/ClassReader.class");
        if (asm != null) unpackJar(asm, staging);
      }
      if (!exists(staging, "org/objectweb/asm/tree/ClassNode.class")) {
        Path asmTree = locateJarOf("org/objectweb/asm/tree/ClassNode.class");
        if (asmTree != null) unpackJar(asmTree, staging);
      }
      if (!exists(staging, "org/objectweb/asm/commons/AdviceAdapter.class")) {
        Path asmCommons = locateJarOf("org/objectweb/asm/commons/AdviceAdapter.class");
        if (asmCommons != null) unpackJar(asmCommons, staging);
      }

      // 4.7 JaCoCo report（生成 jacoco.xml 需要），按需补
      if (!exists(staging, "org/jacoco/report/ISourceFileLocator.class")) {
        Path jacocoReport = locateJarOf("org/jacoco/report/ISourceFileLocator.class");
        if (jacocoReport != null) unpackJar(jacocoReport, staging);
        else getLog().warn("JaCoCo report not found; jacoco.xml generation will fail at runtime.");
      }

      // 4.8 JUnit Platform reporting（LegacyXmlReportGeneratingListener 所需），按需补
      if (!exists(staging, "org/junit/platform/reporting/legacy/xml/LegacyXmlReportGeneratingListener.class")) {
        Path jpr = locateJarOf("org/junit/platform/reporting/legacy/xml/LegacyXmlReportGeneratingListener.class");
        if (jpr != null) unpackJar(jpr, staging);
        else getLog().warn("junit-platform-reporting not found; Surefire-style XML won't be generated.");
      }

      // -------------------------------
      // 5) 可选：源码塞入
      // -------------------------------
      if (includeSources) {
        Path src = project.getBasedir().toPath().resolve("src");
        if (Files.isDirectory(src)) copyDir(src, staging.resolve("_sources"));
      }

      // -------------------------------
      // 6) 写 MANIFEST + 打包（跳过 MANIFEST，排序，置零时间戳）
      // -------------------------------
      Manifest mf = new Manifest();
      Attributes att = mf.getMainAttributes();
      att.put(Attributes.Name.MANIFEST_VERSION, "1.0");
      att.put(Attributes.Name.MAIN_CLASS, "com.example.fatrunner.Main");

      Files.createDirectories(outputFile.toPath().getParent());
      try (JarOutputStream jos = new JarOutputStream(new FileOutputStream(outputFile), mf)) {
        List<Path> files;
        try (java.util.stream.Stream<Path> stream = Files.walk(staging)) {
          files = new ArrayList<Path>();
          stream.filter(Files::isRegularFile).forEach(files::add);
          Collections.sort(files);
        }
        for (Path p : files) {
          String entryName = staging.relativize(p).toString().replace('\\', '/');
          if ("META-INF/MANIFEST.MF".equalsIgnoreCase(entryName)) continue;
          JarEntry e = new JarEntry(entryName);
          e.setTime(0L);
          jos.putNextEntry(e);
          Files.copy(p, jos);
          jos.closeEntry();
        }
      }

      // -------------------------------
      // 7) （可选）输出 classpath.txt，便于 javac 单文件编译
      // -------------------------------
      if (writeClasspathTxt) {
        writeClasspathTxt(collectClasspathForTxt(testCp, includeProvided));
      }

      getLog().info("Wrote fat test jar: " + outputFile.getAbsolutePath());

    } catch (Exception e) {
      throw new MojoExecutionException("Failed to build fat test jar", e);
    } finally {
      if (staging != null) {
        try (java.util.stream.Stream<Path> s = Files.walk(staging)) {
          List<Path> all = new ArrayList<Path>();
          s.forEach(all::add);
          Collections.reverse(all);
          for (Path p : all) {
            try { Files.deleteIfExists(p); } catch (IOException ignore) {}
          }
        } catch (IOException ignore) {}
      }
    }
  }

  // --------------------------------------------------------------------------
  // Helpers
  // --------------------------------------------------------------------------

  /** 解析 provided/system 的“传递闭包”，并返回所有 jar 路径 */
  private Set<Path> resolveProvidedClosureJars() throws MojoExecutionException {
    try {
      DefaultDependencyResolutionRequest req =
          new DefaultDependencyResolutionRequest(project, repoSession);

      // ❌ 不要用 ScopeDependencyFilter(include=provided,system)
      //    它会把其它 scope 的边裁掉，导致图不完整
      // ✅ 直接解析完整图，然后在遍历时挑出 scope=provided/system
      DependencyResolutionResult res = dependenciesResolver.resolve(req);

      Set<Path> jars = new LinkedHashSet<>();
      var root = res.getDependencyGraph();
      if (root != null) {
        Deque<org.eclipse.aether.graph.DependencyNode> stack = new ArrayDeque<>();
        stack.push(root);
        while (!stack.isEmpty()) {
          var node = stack.pop();
          var children = node.getChildren();
          if (children != null) {
            for (int i = children.size() - 1; i >= 0; i--) stack.push(children.get(i));
          }
          var dep = node.getDependency();
          if (dep == null) continue;

          // Aether 节点上拿“有效 scope”
          String scope = dep.getScope();
          if (!"provided".equals(scope) && !"system".equals(scope)) continue;

          var a = dep.getArtifact();
          if (a == null) continue;
          File f = a.getFile();
          if (f != null && f.getName().endsWith(".jar")) {
            jars.add(f.toPath());
          }
        }
      }
      if (getLog().isDebugEnabled()) {
        getLog().debug("[fattest] provided/system jars: " + jars.size());
      }
      return jars;
    } catch (Exception e) {
      throw new MojoExecutionException("Failed resolving provided/system scope closure", e);
    }
  }

  /** 为 classpath.txt 收集路径（classes/test-classes + artifacts JAR + provided/system 闭包） */
  private List<String> collectClasspathForTxt(List<String> testCp, boolean includeProvided) throws MojoExecutionException {
    LinkedHashSet<String> cp = new LinkedHashSet<>();

    // 0) 本模块输出目录优先
    addIfExists(cp, project.getBuild().getOutputDirectory());
    addIfExists(cp, project.getBuild().getTestOutputDirectory());

    // 1) 已解析依赖 JAR（TEST 分辨率）
    @SuppressWarnings("unchecked")
    Set<org.apache.maven.artifact.Artifact> arts = project.getArtifacts();
    if (arts != null) {
      for (org.apache.maven.artifact.Artifact a : arts) {
        File f = a.getFile();
        if (f != null && f.getName().endsWith(".jar")) {
          cp.add(f.getAbsolutePath());
        }
      }
    }

    // 1.1) reactor 依赖回落（a.getFile()==null）
    Map<String, MavenProject> refs = project.getProjectReferences();
    if (arts != null && refs != null && !refs.isEmpty()) {
      for (org.apache.maven.artifact.Artifact a : arts) {
        if (a.getFile() != null) continue;
        String key = a.getGroupId() + ":" + a.getArtifactId();
        MavenProject mp = refs.get(key);
        if (mp == null) continue;
        addIfExists(cp, mp.getBuild().getOutputDirectory());
        addIfExists(cp, mp.getBuild().getTestOutputDirectory());
      }
    }

    // 2) testClasspathElements 里的额外条目（去重由 LinkedHashSet 负责）
    for (String s : testCp) {
      if (s == null) continue;
      cp.add(Paths.get(s).toAbsolutePath().toString());
    }

    // 3) provided/system 的传递闭包
    if (includeProvided) {
      for (Path p : resolveProvidedClosureJars()) cp.add(p.toAbsolutePath().toString());
    }

    if (getLog().isDebugEnabled()) {
      getLog().debug("[fattest] classpath entries = " + cp.size());
    }
    return new ArrayList<>(cp);
  }

  private void addIfExists(Set<String> set, String path) {
    if (path == null) return;
    Path p = Paths.get(path);
    if (Files.exists(p)) set.add(p.toString());
  }

  private void writeClasspathTxt(List<String> entries) throws IOException {
    Path out = classpathTxt.toPath();
    Files.createDirectories(out.getParent());
    Files.writeString(out, String.join(File.pathSeparator, entries), StandardCharsets.UTF_8);

    // 同目录下落一份逐行的 debug 列表
    Path dbg = out.getParent().resolve("classpath.debug.list");
    Files.write(out.getParent().resolve("classpath.debug.list"), 
                (String.join(System.lineSeparator(), entries) + System.lineSeparator()).getBytes(StandardCharsets.UTF_8));

    getLog().info("Wrote classpath file: " + out.toAbsolutePath());
    getLog().info("Wrote classpath debug list: " + dbg.toAbsolutePath());
  }

  private static boolean exists(Path root, String entry) {
    return Files.exists(root.resolve(entry));
  }

  private static void copyDir(Path from, Path to) throws IOException {
    try (java.util.stream.Stream<Path> s = Files.walk(from)) {
      s.forEach(p -> {
        try {
          Path q = to.resolve(from.relativize(p).toString());
          if (Files.isDirectory(p)) Files.createDirectories(q);
          else {
            Files.createDirectories(q.getParent());
            Files.copy(p, q, StandardCopyOption.REPLACE_EXISTING);
          }
        } catch (IOException e) { throw new UncheckedIOException(e); }
      });
    }
  }

  private static void unpackJar(Path jar, Path toDir) throws IOException {
    try (ZipInputStream zis = new ZipInputStream(Files.newInputStream(jar))) {
      ZipEntry e;
      while ((e = zis.getNextEntry()) != null) {
        String name = e.getName();
        if (e.isDirectory()) continue;
        if ("META-INF/MANIFEST.MF".equalsIgnoreCase(name)) continue; // 跳过清单
        Path out = toDir.resolve(name);
        Files.createDirectories(out.getParent());
        if (name.startsWith("META-INF/services/") && Files.exists(out)) {
          Files.write(out, new byte[]{'\n'}, StandardOpenOption.APPEND);
          try (OutputStream os = Files.newOutputStream(out, StandardOpenOption.APPEND)) {
            zis.transferTo(os);
          }
        } else {
          Files.copy(zis, out, StandardCopyOption.REPLACE_EXISTING);
        }
      }
    }
  }

  /** 在插件 ClassLoader 上定位某个类所属的 JAR。 */
  private static Path locateJarOf(String resourcePath) throws IOException {
    URL url = BuildFatTestJarMojo.class.getClassLoader().getResource(resourcePath);
    if (url == null) return null;
    String s = url.toString(); // e.g. jar:file:/.../xxx.jar!/org/...
    if (s.startsWith("jar:file:")) {
      s = s.substring("jar:file:".length(), s.indexOf('!'));
      return Paths.get(new File(s).toURI());
    }
    if (s.startsWith("file:")) { // 开发态 classes 目录（极少见）
      return Paths.get(new File(URI.create(s)).toURI());
    }
    return null;
  }
}
