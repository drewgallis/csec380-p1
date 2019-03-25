-- schema created from db documentation

DROP DATABASE IF EXISTS mydb;
CREATE DATABASE mydb;
USE mydb;

CREATE TABLE User (
    id INT NOT NULL AUTO_INCREMENt,
    username VARCHAR(20) NOT NULL ,
    password VARCHAR(255) NOT NULL ,
    valid_login BOOLEAN NOT NULL DEFAULT False,
    PRIMARY KEY(id)
);

CREATE TABLE VideoStats (
    id INT NOT NULL ,
    username VARCHAR(20) NOT NULL ,
    url VARCHAR(255) NOT NULL ,
    video_name VARCHAR(100) NOT NULL ,
    time_stamp TIMESTAMP NOT NULL,
    FOREIGN KEY(id) REFERENCES User(id)
);

CREATE TABLE Videos (
    id INT NOT NULL ,
    username VARCHAR(20) NOT NULL ,
    vidPath VARCHAR(50) NOT NULL,
    FOREIGN KEY(id) REFERENCES User(id)
);