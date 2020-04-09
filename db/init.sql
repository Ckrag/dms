CREATE DATABASE dms;
\c dms 

CREATE TABLE apps (
  	id VARCHAR(20),
  	description VARCHAR(300),
  	created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  	PRIMARY KEY(id)
);

CREATE TABLE app_data (
	app_id VARCHAR(20) REFERENCES apps(id),
	created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	txt TEXT
);

CREATE INDEX app_data_grouping_index ON app_data (app_id);

CREATE INDEX entry_creation_time_idx ON app_data (created, app_id);

CREATE OR REPLACE FUNCTION add_app_entry(_app_id VARCHAR(20), data TEXT)
	RETURNS void AS $$
	BEGIN
		INSERT INTO app_data (app_id, txt) VALUES (_app_id, data);
	END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_app(app_id VARCHAR(20), app_description VARCHAR(300))
	RETURNS void AS $$
	BEGIN
		INSERT INTO apps (id, description)
		VALUES (app_id, app_description)
		ON CONFLICT(id) DO NOTHING;
	END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION remove_app(_app_id VARCHAR(20))
	RETURNS void as $$
	BEGIN
		DELETE FROM app_data WHERE app_id=_app_id;
		DELETE FROM apps WHERE id=_app_id;
	END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_apps()
RETURNS SETOF apps as $$
	BEGIN
		RETURN QUERY SELECT * FROM apps;
	END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_app(app_id VARCHAR(20))
RETURNS SETOF apps as $$
	BEGIN
		RETURN QUERY SELECT * FROM apps WHERE id=app_id LIMIT 1;
	END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_app_entries_with_number_limit(_app_id VARCHAR(20), entries_limit INTEGER)
RETURNS SETOF app_data as $$
	BEGIN
		RETURN QUERY SELECT * FROM (SELECT * FROM app_data WHERE app_id=_app_id ORDER BY created DESC LIMIT entries_limit) AS entries ORDER BY created ASC;
	END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_app_entries_with_time_limit(_app_id VARCHAR(20), minute_limit INTEGER)
RETURNS SETOF app_data as $$
        BEGIN
                RETURN QUERY SELECT * FROM app_data WHERE app_id=_app_id AND created > now() - INTERVAL '1 min' * minute_limit;
        END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_all_app_entries(_app_id VARCHAR(20))
RETURNS SETOF app_data as $$
        BEGIN
                RETURN QUERY SELECT * FROM app_data WHERE app_id=_app_id;
        END;
$$ LANGUAGE plpgsql;

