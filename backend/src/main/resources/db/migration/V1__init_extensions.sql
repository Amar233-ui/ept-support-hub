-- Extensions required by the application. Also created by infra/postgres/init for local dev;
-- IF NOT EXISTS keeps this idempotent. The functional schema starts in V2 (milestone M1).
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
