# syntax=docker/dockerfile:1

# ---------- dev: hot reload via spring-boot:run on mounted sources ----------
FROM eclipse-temurin:21-jdk AS dev
WORKDIR /app
COPY .mvn/ .mvn/
COPY mvnw pom.xml ./
RUN chmod +x mvnw && ./mvnw -q -B dependency:go-offline
COPY src/ src/
EXPOSE 8080
HEALTHCHECK --interval=10s --timeout=3s --start-period=120s --retries=10 \
  CMD curl -fs http://localhost:8080/api/actuator/health/liveness || exit 1
CMD ["./mvnw", "-q", "-B", "spring-boot:run", "-Dspring-boot.run.jvmArguments=-XX:TieredStopAtLevel=1"]

# ---------- build ----------
FROM eclipse-temurin:21-jdk AS build
WORKDIR /app
COPY .mvn/ .mvn/
COPY mvnw pom.xml ./
RUN chmod +x mvnw && ./mvnw -q -B dependency:go-offline
COPY src/ src/
RUN ./mvnw -q -B package -DskipTests \
    && java -Djarmode=tools -jar target/support-hub-*.jar extract --layers --launcher --destination extracted

# ---------- prod: JRE only, non-root ----------
FROM eclipse-temurin:21-jre AS prod
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/* \
    && useradd --system --uid 10001 --create-home app \
    && mkdir -p /data/storage && chown app /data/storage
WORKDIR /app
COPY --from=build /app/extracted/dependencies/ ./
COPY --from=build /app/extracted/spring-boot-loader/ ./
COPY --from=build /app/extracted/snapshot-dependencies/ ./
COPY --from=build /app/extracted/application/ ./
USER app
EXPOSE 8080
ENV SPRING_PROFILES_ACTIVE=prod \
    JAVA_TOOL_OPTIONS="-XX:MaxRAMPercentage=75"
HEALTHCHECK --interval=15s --timeout=3s --start-period=60s --retries=5 \
  CMD curl -fs http://localhost:8080/api/actuator/health/liveness || exit 1
ENTRYPOINT ["java", "org.springframework.boot.loader.launch.JarLauncher"]
