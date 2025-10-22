CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE SCHEMA fsl;

CREATE TABLE fsl.users(
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  username text NOT NULL UNIQUE,
  display_name text,
  "password" text NOT NULL,
  access_level integer NOT NULL DEFAULT 3,
  last_login timestamp,
  created_at timestamp DEFAULT now() NOT NULL,
  is_active boolean DEFAULT true NOT NULL,
  CONSTRAINT fsl_user_pkey PRIMARY KEY(id)
);

CREATE TABLE fsl.settings(
  setting_key text NOT NULL,
  value text NOT NULL,
  CONSTRAINT fsl_settings_pkey PRIMARY KEY(setting_key)
);

CREATE TABLE fsl.access_level_info (
  id SERIAL NOT NULL,
  prio integer NOT NULL,
  display_name text NOT NULL,
  "descr" text,
  color text NOT NULL,
  CONSTRAINT access_level_info_id_key UNIQUE (id),
  CONSTRAINT access_level_info_pkey PRIMARY KEY (id)
);

ALTER TABLE fsl.users
  ADD CONSTRAINT users_access_level_fkey
    FOREIGN KEY (access_level)
    REFERENCES fsl.access_level_info (id);