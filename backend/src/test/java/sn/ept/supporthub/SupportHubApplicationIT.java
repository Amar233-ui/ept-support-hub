package sn.ept.supporthub;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Import;
import org.springframework.jdbc.core.JdbcTemplate;

@SpringBootTest
@Import(TestcontainersConfiguration.class)
class SupportHubApplicationIT {

    @Autowired
    JdbcTemplate jdbc;

    @Test
    void contextLoadsAndFlywayEnablesPgvector() {
        Integer count =
                jdbc.queryForObject("select count(*) from pg_extension where extname = 'vector'", Integer.class);
        assertThat(count).isEqualTo(1);
    }
}
