CREATE DATABASE dms;
\connect dms;

CREATE TABLE apps (
  	id VARCHAR(20),
  	description VARCHAR(300),
  	created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  	PRIMARY KEY(id)
);

CREATE TABLE app_data (
	app_id VARCHAR(20) REFERENCES apps,
	txt TEXT
);

/*
CREATE OR REPLACE FUNCTION totalRecords ()
RETURNS integer AS $total$
declare
	total integer;
BEGIN
   SELECT count(*) into total FROM COMPANY;
   RETURN total;
END;
$total$ LANGUAGE plpgsql;
*/

CREATE OR REPLACE FUNCTION add_app_entry(app_id VARCHAR(20), data TEXT)
	RETURNS void AS $$
	BEGIN
		INSERT INTO app_data VALUES (app_id, data);
	END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION add_app(app_id VARCHAR(20), app_description VARCHAR(300))
	RETURNS void AS $$
	BEGIN
		INSERT INTO apps (id, description)
		VALUES (app_id, app_description)
		ON CONFLICT(id) DO NOTHING;
	END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION remove_app(app_id VARCHAR(20))
	RETURNS void as $$
	BEGIN
		DELETE FROM apps WHERE id=app_id;
		DELETE FROM app_data WHERE app_id=app_id;
	END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_apps()
RETURNS varchar[] as $all_apps$
	declare
		all_apps varchar[];
	BEGIN
		SELECT * FROM apps INTO all_apps;
		RETURN all_apps;
	END;
$all_apps$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_app(app_id VARCHAR(20))
RETURNS varchar as $app$
	declare
		app RECORD;
	BEGIN
		SELECT * INTO app FROM apps WHERE id=app_id;
		RETURN app;
	END;
$app$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_app_entries(app_id VARCHAR(20))
RETURNS text[] as $app_entries$
	declare
		app_entries text[];
	BEGIN
		SELECT * FROM app_data WHERE id=app_id INTO app_entries ;
		RETURN app_entries;
	END;
$app_entries$ LANGUAGE plpgsql;