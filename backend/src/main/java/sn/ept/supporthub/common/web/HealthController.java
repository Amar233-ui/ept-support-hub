package sn.ept.supporthub.common.web;

import java.time.Instant;
import org.springframework.beans.factory.ObjectProvider;
import org.springframework.boot.info.BuildProperties;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Lightweight liveness endpoint for the frontend. Detailed health (DB, disk) lives under
 * /actuator/health.
 */
@RestController
public class HealthController {

    private final String version;

    public HealthController(ObjectProvider<BuildProperties> buildProperties) {
        BuildProperties props = buildProperties.getIfAvailable();
        this.version = props != null ? props.getVersion() : "dev";
    }

    @GetMapping("/health")
    public HealthResponse health() {
        return new HealthResponse("UP", "backend", version, Instant.now());
    }

    public record HealthResponse(String status, String service, String version, Instant timestamp) {}
}
