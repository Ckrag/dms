CREATE DATABASE dms;
\connect dms;

CREATE TABLE apps (
  id VARCHAR(20),
  description VARCHAR(300),
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(id)
);

/*
INSERT INTO favorite_colors
  (name, color)
VALUES
  ('Lancelot', 'blue'),
  ('Galahad', 'yellow');
*/