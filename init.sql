CREATE USER 'bugbountylink'@'localhost' IDENTIFIED BY 'bugbountylink123!';
CREATE DATABASE bugbountylink;
GRANT ALL PRIVILEGES ON bugbountylink.* To 'bugbountylink'@'localhost';
CREATE TABLE links (
  id varchar(20) NOT NULL PRIMARY KEY,
  dest varchar(1024) NOT NULL
);
