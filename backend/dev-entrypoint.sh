#!/bin/sh
# Dev container only. Runs the app with DevTools and recompiles when the mounted sources
# change; DevTools then restarts the Spring context (a few seconds). Polling is used because
# file events do not cross Docker Desktop bind mounts on Windows/macOS.
set -u

./mvnw -q -B spring-boot:run -Dspring-boot.run.jvmArguments="-XX:TieredStopAtLevel=1" &
APP_PID=$!

touch /tmp/last-build
while kill -0 "$APP_PID" 2>/dev/null; do
  sleep 2
  if [ -n "$(find src -newer /tmp/last-build -type f -print -quit)" ]; then
    touch /tmp/last-build
    echo "[dev] sources changed, recompiling..."
    ./mvnw -q -B -o compile || echo "[dev] compilation failed, fix the error and save again"
  fi
done

wait "$APP_PID"
