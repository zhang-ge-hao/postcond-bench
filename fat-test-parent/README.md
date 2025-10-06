```
rm -rf $PI_WORKDIR/.m2/repository/

mvn -DskipTests clean install -Dmaven.repo.local=$PI_WORKDIR/.m2/repository/
```

```
rm -rf ./.m2 ./META-INF ./target/ jacoco.exec && cp -r $PI_WORKDIR/.m2 ./.m2

mvn -DskipTests clean com.example:fat-test-maven-plugin:0.1.0:build -Dmaven.repo.local=./.m2/repository/

jar xf target/*-fat-tests.jar META-INF/fattest/jacoco-agent.jar

java -javaagent:META-INF/fattest/jacoco-agent.jar=destfile=jacoco.exec,output=file,append=false,dumponexit=true -jar target/*-fat-tests.jar --append --src-roots src/main/java,src/test/java
```
