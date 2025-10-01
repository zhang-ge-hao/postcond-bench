# Original `pom.xml`

```
{original_config}
```

# Guideline

I would like to reproduce a Java project with Maven. Above is the original `pom.xml` file. 

I am in the Docker container environment. The JDK 21 is installed. The Maven 3.9.x is also installed.

Please provide a Python script to modify the XML file (the Python file will be in the same directory as the pom.xml file). Running it will achieve the following:

1. The project Java version is not lower than Java 10.
2. Running `mvn test` can get an XML report files in `target/surefire-reports/*.xml`.
3. Running `mvn test` can get an XML coverage report in `target/site/jacoco/jacoco.xml`.

Note that:

1. your response should only include the Python script you would like to run.
2. Edit using Python's native XML library.