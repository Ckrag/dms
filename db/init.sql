CREATE DATABASE dms;
\connect dms;

CREATE TABLE apps (
  	id VARCHAR(20),
  	description VARCHAR(300),
  	created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  	PRIMARY KEY(id)
);

CREATE TABLE app_data (
	id VARCHAR(20) REFERENCES apps,
	txt TEXT
);

CREATE OR REPLACE FUNCTION add_entry(app_id VARCHAR(20), data TEXT)
	INSERT INTO app_data VALUES (app_id, data);
END;

CREATE OR REPLACE FUNCTION add_app(app_id VARCHAR(20), app_description VARCHAR(300))
	INSERT INTO apps (id, description)
	VALUES (app_id, app_description)
	ON CONFLICT(id) DO NOTHING;
END;

CREATE OR REPLACE FUNCTION remove_app(app_id VARCHAR(20))
	DELETE FROM apps WHERE id = app_id;
	DELETE FROM 
END;