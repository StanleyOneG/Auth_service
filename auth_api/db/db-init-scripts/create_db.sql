CREATE SCHEMA IF NOT EXISTS auth;

CREATE TABLE IF NOT EXISTS auth.user (
    id uuid PRIMARY KEY,
    login TEXT NOT NULL,
    email TEXT NOT NULL,
    password VARCHAR NOT NULL,
    UNIQUE(login, email)
);
CREATE TABLE IF NOT EXISTS auth.user_info (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL REFERENCES auth.user(id),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    age INTEGER,
    CONSTRAINT user_info_fk_user_on_delete FOREIGN KEY(user_id) REFERENCES auth.user(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS auth.permission (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    UNIQUE(name)
);
CREATE TABLE IF NOT EXISTS auth.user_permission (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL REFERENCES auth.user(id),
    permission_id uuid NOT NULL REFERENCES auth.permission(id),
    CONSTRAINT user_permission_fk_user_on_delete FOREIGN KEY(user_id) REFERENCES auth.user(id) ON DELETE CASCADE,
    CONSTRAINT user_permission_fk_permission_on_delete FOREIGN KEY(permission_id) REFERENCES auth.permission(id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX user_permission_unique_idx ON auth.user_permission (user_id, permission_id);

CREATE TABLE IF NOT EXISTS auth.user_login_history (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL REFERENCES auth.user(id),
    login_at timestamp with time zone,
    user_agent TEXT NOT NULL,
    CONSTRAINT user_login_history_fk_user_on_delete FOREIGN KEY(user_id) REFERENCES auth.user(id) ON DELETE CASCADE
);
CREATE INDEX user_login_history_login_at_idx ON auth.user_login_history(login_at);
