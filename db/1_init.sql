CREATE TABLE apps (
  	id VARCHAR(20),
  	description VARCHAR(300),
  	created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  	PRIMARY KEY(id)
);

CREATE TABLE app_data (
	app_id VARCHAR(20) REFERENCES apps(id) ON DELETE CASCADE,
	created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	txt TEXT
);

CREATE INDEX app_data_grouping_index ON app_data (app_id);

CREATE INDEX entry_creation_time_idx ON app_data (created, app_id);
