CREATE TABLE IF NOT EXISTS prefixes (
    guild_id BIGINT NOT NULL,
    prefix   VARCHAR(12) NOT NULL,
    UNIQUE (guild_id, prefix)
);

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'blacklist_type') THEN
        CREATE TYPE blacklist_type AS ENUM ('user', 'guild');
    END IF;
END
$$;

CREATE TABLE IF NOT EXISTS blacklist (
    id   BIGINT PRIMARY KEY,
    type BLACKLIST_TYPE NOT NULL
);
