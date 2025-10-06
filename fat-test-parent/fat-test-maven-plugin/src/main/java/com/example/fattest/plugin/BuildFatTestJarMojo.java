package com.example.fattest.plugin;

import org.apache.maven.artifact.Artifact;
import org.apache.maven.plugin.AbstractMojo;
import org.apache.maven.plugin.MojoExecutionException;
import org.apache.maven.plugins.annotations.*;
import org.apache.maven.project.MavenProject;

import java.io.*;
import java.net.*;
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

  @Parameter(property = "outputFile",
      defaultValue = "${project.build.directory}/${project.artifactId}-${project.version}-fat-tests.jar")
  private File outputFile;

  @Parameter(property = "includeSources", defaultValue = "true")
  private boolean includeSources;

  @Override
  public void execute() throws MojoExecutionException {
    Path staging = null;
    try {
      staging = Files.createTempDirectory("fat-tests-");

      Path classes = Paths.get(project.getBuild().getOutputDirectory());
      Path testClasses = Paths.get(project.getBuild().getTestOutputDirectory());

      // 1) 放入项目 main/test 产物
      if (Files.isDirectory(classes)) copyDir(classes, staging);
      if (Files.isDirectory(testClasses)) copyDir(testClasses, staging);

      // 1.1 写入“主代码 class 清单”供 runner 限定覆盖率范围
      if (Files.isDirectory(classes)) {
        List<String> mainClasses = new ArrayList<>();
        try (var s = Files.walk(classes)) {
          s.filter(p -> p.toString().endsWith(".class"))
              .forEach(p -> mainClasses.add(classes.relativize(p).toString().replace('\\', '/')));
        }
        Path meta = staging.resolve("META-INF/fattest");
        Files.createDirectories(meta);
        Files.write(meta.resolve("project-classes.lst"), mainClasses, StandardCharsets.UTF_8);
      }

      // 2) 先解包“目标项目依赖”（含 test 作用域）—— 以项目版本为准
      @SuppressWarnings("unchecked")
      Set<Artifact> arts = project.getArtifacts();
      for (Artifact a : arts) {
        if (!"jar".equals(a.getType())) continue;
        unpackJar(a.getFile().toPath(), staging);
      }

      // 3) 按需补齐：runner / JUnit Platform / Vintage / JUnit4 / JaCoCo（agent + core + ASM）
      // 3.0 runner（总是需要）
      if (!exists(staging, "com/example/fatrunner/Main.class")) {
        Path runnerJar = locateJarOf("com/example/fatrunner/Main.class");
        if (runnerJar != null) unpackJar(runnerJar, staging);
        else getLog().warn("Runner jar not found on plugin classpath.");
      }

      // 3.1 JUnit Platform launcher（若项目没带，则用插件侧 console-standalone）
      if (!exists(staging, "org/junit/platform/launcher/core/LauncherDiscoveryRequestBuilder.class")) {
        Path junitPlatform = locateJarOf("org/junit/platform/console/ConsoleLauncher.class");
        if (junitPlatform == null)
          junitPlatform = locateJarOf("org/junit/platform/launcher/core/LauncherDiscoveryRequestBuilder.class");
        if (junitPlatform != null) unpackJar(junitPlatform, staging);
        else getLog().warn("No JUnit Platform launcher found; tests may not run.");
      }

      // 3.2 Vintage（JUnit4 桥），按需补
      if (!exists(staging, "org/junit/vintage/engine/VintageTestEngine.class")) {
        Path vintage = locateJarOf("org/junit/vintage/engine/VintageTestEngine.class");
        if (vintage != null) unpackJar(vintage, staging);
      }

      // 3.2.1 ECJ（Vintage 的 TestSource 可能会用到）
      if (!exists(staging, "org/eclipse/jdt/internal/compiler/ast/AbstractMethodDeclaration.class")) {
        Path ecj = locateJarOf("org/eclipse/jdt/internal/compiler/ast/AbstractMethodDeclaration.class");
        if (ecj != null) unpackJar(ecj, staging);
        else getLog().warn("ECJ not found; Vintage source mapping may fail.");
      }

      // 3.2.2
      Set<Artifact> deps = new LinkedHashSet<>();
      deps.addAll(project.getDependencyArtifacts()); // 直接依赖，含 scope 信息
      for (Artifact a : deps) {
        if (!"jar".equals(a.getType())) continue;
        String scope = a.getScope();
        if ("provided".equals(scope) || "system".equals(scope)) {
          unpackJar(a.getFile().toPath(), staging);
        }
      }

      // 3.3 JUnit4 本体，按需补
      if (!exists(staging, "org/junit/runner/JUnitCore.class")) {
        Path junit4 = locateJarOf("org/junit/runner/JUnitCore.class");
        if (junit4 != null) unpackJar(junit4, staging);
      }

      // 3.4 JaCoCo agent：总是把完整 JAR 原样打进资源位，另外若 RT.class 缺失再解包到 classpath
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

      // 3.5 JaCoCo core（解析 exec），按需补
      if (!exists(staging, "org/jacoco/core/analysis/ICoverageVisitor.class")) {
        Path jacocoCore = locateJarOf("org/jacoco/core/analysis/ICoverageVisitor.class");
        if (jacocoCore == null) jacocoCore = locateJarOf("org/jacoco/core/tools/ExecFileLoader.class");
        if (jacocoCore != null) unpackJar(jacocoCore, staging);
        else getLog().warn("JaCoCo core not found; coverage reporting will be disabled.");
      }

      // 3.6 ASM 依赖，按需补
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

      // 3.7 JaCoCo report（生成 jacoco.xml 需要），按需补
      if (!exists(staging, "org/jacoco/report/ISourceFileLocator.class")) {
        Path jacocoReport = locateJarOf("org/jacoco/report/ISourceFileLocator.class");
        if (jacocoReport != null) unpackJar(jacocoReport, staging);
        else getLog().warn("JaCoCo report not found; jacoco.xml generation will fail at runtime.");
      }

      // 3.8 JUnit Platform reporting（LegacyXmlReportGeneratingListener 所需），按需补
      if (!exists(staging, "org/junit/platform/reporting/legacy/xml/LegacyXmlReportGeneratingListener.class")) {
        Path jpr = locateJarOf("org/junit/platform/reporting/legacy/xml/LegacyXmlReportGeneratingListener.class");
        if (jpr != null) unpackJar(jpr, staging);
        else getLog().warn("junit-platform-reporting not found; Surefire-style XML won't be generated.");
      }

      {
        Path asm = locateJarOf("org/objectweb/asm/ClassReader.class");
        if (asm != null) {
          unpackJar(asm, staging);
        } else {
          getLog().warn("ASM core jar not found on plugin classpath.");
        }

        Path asmTree = locateJarOf("org/objectweb/asm/tree/ClassNode.class");
        if (asmTree != null) {
          unpackJar(asmTree, staging);
        } else {
          getLog().warn("ASM tree jar not found on plugin classpath.");
        }

        Path asmCommons = locateJarOf("org/objectweb/asm/commons/AdviceAdapter.class");
        if (asmCommons != null) {
          unpackJar(asmCommons, staging);
        } else {
          getLog().warn("ASM commons jar not found on plugin classpath.");
        }
      }

      // 4) 可选：源码塞入
      if (includeSources) {
        Path src = project.getBasedir().toPath().resolve("src");
        if (Files.isDirectory(src)) copyDir(src, staging.resolve("_sources"));
      }

      // 5) 写 MANIFEST + 打包（跳过 MANIFEST，排序，置零时间戳）
      Manifest mf = new Manifest();
      Attributes att = mf.getMainAttributes();
      att.put(Attributes.Name.MANIFEST_VERSION, "1.0");
      att.put(Attributes.Name.MAIN_CLASS, "com.example.fatrunner.Main");

      Files.createDirectories(outputFile.toPath().getParent());
      try (JarOutputStream jos = new JarOutputStream(new FileOutputStream(outputFile), mf)) {
        // 收集并排序所有将要写入的文件
        List<Path> files;
        try (var stream = Files.walk(staging)) {
          files = stream.filter(Files::isRegularFile).sorted().toList();
        }
        for (Path p : files) {
          String entryName = staging.relativize(p).toString().replace('\\', '/');
          if ("META-INF/MANIFEST.MF".equalsIgnoreCase(entryName)) continue; // 避免重复
          JarEntry e = new JarEntry(entryName);
          e.setTime(0L);
          jos.putNextEntry(e);
          Files.copy(p, jos);
          jos.closeEntry();
        }
      }

      getLog().info("Wrote fat test jar: " + outputFile.getAbsolutePath());

    } catch (Exception e) {
      throw new MojoExecutionException("Failed to build fat test jar", e);
    } finally {
      // 清理临时目录（尽力而为）
      if (staging != null) {
        try (var s = Files.walk(staging)) {
          s.sorted(Comparator.reverseOrder()).forEach(p -> {
            try { Files.deleteIfExists(p); } catch (IOException ignore) {}
          });
        } catch (IOException ignore) {}
      }
    }
  }

  // --------------------------------------------------------------------------
  // Helpers
  // --------------------------------------------------------------------------

  private static boolean exists(Path root, String entry) {
    return Files.exists(root.resolve(entry));
  }

  private static void copyDir(Path from, Path to) throws IOException {
    try (var s = Files.walk(from)) {
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
          // 已存在则换行后追加，避免黏连
          Files.write(out, new byte[]{'\n'}, StandardOpenOption.APPEND);
          zis.transferTo(Files.newOutputStream(out, StandardOpenOption.APPEND));
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
    // 如果是普通 file:// 目录（开发态），直接返回该目录（极少见）
    if (s.startsWith("file:")) {
      return Paths.get(new File(URI.create(s)).toURI());
    }
    return null;
    }
}
