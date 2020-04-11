-- schema created from db documentation

DROP DATABASE IF EXISTS mydb;
CREATE DATABASE mydb;
USE mydb;

CREATE TABLE User (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL ,
    password VARCHAR(255) NOT NULL ,
    valid_login BOOLEAN NOT NULL DEFAULT False,
    PRIMARY KEY(id)
);