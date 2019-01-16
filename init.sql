CREATE USER 'bugbountylink'@'localhost' IDENTIFIED BY 'password';
CREATE DATABASE bugbountylink;
GRANT ALL PRIVILEGES ON bugbountylink.* To 'bugbountylink'@'localhost';
CREATE TABLE links (id varchar(20),dest varchar(1024));
