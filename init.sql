CREATE USER 'bugbountylink'@'localhost' IDENTIFIED BY 'bugbountylink123!';
CREATE DATABASE bugbountylink;
GRANT ALL PRIVILEGES ON bugbountylink.* To 'bugbountylink'@'localhost';
USE bugbountylink;
CREATE TABLE links (
  id varchar(20) NOT NULL PRIMARY KEY,
  dest varchar(1024) NOT NULL
);
CREATE TABLE link_events (
  ip varchar(64) NOT NULL,
  link varchar(20) NOT NULL,
  access_time bigint,
  UNIQUE(ip, link)
);