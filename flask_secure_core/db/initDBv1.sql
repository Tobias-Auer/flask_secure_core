CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE SCHEMA fsl;

CREATE TABLE fsl.users(
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  username text NOT NULL UNIQUE,
  display_name text,
  "password" text NOT NULL,
  access_level integer NOT NULL DEFAULT 3,
  last_login timestamp,
  created_at timestamp DEFAULT now(),
  is_active boolean DEFAULT true,
  CONSTRAINT fsl_user_pkey PRIMARY KEY(id)
);

CREATE TABLE fsl.settings(
  setting_key text NOT NULL,
  value text NOT NULL,
  CONSTRAINT fsl_settings_pkey PRIMARY KEY(setting_key)
);
