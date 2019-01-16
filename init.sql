CREATE USER 'bugbountylink'@'localhost' IDENTIFIED BY 'password';
CREATE DATABASE bugbountylink;
GRANT ALL PRIVILEGES ON bugbountylink.* To 'bugbountylink'@'localhost';
CREATE TABLE links (
  id varchar(20) NOT NULL,
  dest varchar(1024) NOT NULL,
  UNIQUE (id)
);
