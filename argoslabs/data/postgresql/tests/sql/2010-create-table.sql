-- create table


DROP SEQUENCE IF EXISTS seq_foo_id;
CREATE SEQUENCE seq_foo_id;

DROP TABLE IF EXISTS foo;
CREATE TABLE foo (
  id BIGINT NOT NULL default nextval('seq_foo_id'),
  name VARCHAR(30) NOT NULL,
  age INT NOT NULL,
  PRIMARY KEY (id)
);

