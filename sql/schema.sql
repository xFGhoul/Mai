CREATE TABLE IF NOT EXISTS "guild" (
    "discord_id" BIGSERIAL NOT NULL PRIMARY KEY,
    "prefix" TEXT NOT NULL DEFAULT '-',
    "is_bot_blacklisted" BOOL NOT NULL  DEFAULT False,
    "blacklisted_reason" TEXT NOT NULL DEFAULT 'Breaking MAI TOS',
    "blacklisted_channels" BIGINT
);

CREATE TABLE IF NOT EXISTS "afk" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "user_id" BIGINT NOT NULL,
    "start_time" TIMESTAMPTZ NOT NULL,
    "enabled" BOOL NOT NULL DEFAULT False,
    "message" TEXT DEFAULT 'Away From Keyboard',
    "guild_id" BIGINT NOT NULL REFERENCES "guild" ("discord_id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "warns" (
    "warn_id" UUID NOT NULL PRIMARY KEY,
    "warned_id" BIGINT NOT NULL,
    "enabled" BOOL NOT NULL DEFAULT True,
    "warner_id" BIGINT NOT NULL,
    "reason" TEXT DEFAULT 'Breaking Guild Rules',
    "guild_id" BIGINT NOT NULL REFERENCES "guild" ("discord_id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "osu" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "username" TEXT NOT NULL,
    "skin" TEXT NOT NULL,
    "passive" BOOL NOT NULL  DEFAULT True,
    "discord_id" BIGINT NOT NULL,
    "guild_id" BIGINT NOT NULL REFERENCES "guild" ("discord_id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "counting" (
    "discord_id" BIGSERIAL NOT NULL PRIMARY KEY,
    "counting_channel" BIGINT,
    "counting_goal" BIGINT DEFAULT 0,
    "counting_number" BIGINT DEFAULT 0,
    "counting_warn_message" TEXT DEFAULT 'You Cant Count Twice',
    "enabled" BOOL NOT NULL DEFAULT True,
    "last_member_id" BIGINT,
    "webhook_url" VARCHAR(400),
    "guild_id" BIGINT NOT NULL REFERENCES "guild" ("discord_id") ON DELETE CASCADE
);