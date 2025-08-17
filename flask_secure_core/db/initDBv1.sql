CREATE SCHEMA fsl;
CREATE TABLE fsl.user(
  id uuid NOT NULL,
  username text NOT NULL UNIQUE,
  display_name text NOT NULL,
  password_hash text NOT NULL,
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
