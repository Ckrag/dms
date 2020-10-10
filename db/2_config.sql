CREATE TABLE app_config (
    app_id VARCHAR(20) REFERENCES apps(id) ON DELETE CASCADE,
    data_series_var TEXT,
    PRIMARY KEY(app_id)
);

CREATE INDEX app_config_index ON app_config (app_id);

INSERT INTO app_config (app_id, data_series_var)
    SELECT id, null FROM apps
	LEFT JOIN app_config ac ON apps.id=ac.app_id
	WHERE ac.app_id IS NULL
