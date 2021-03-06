﻿-- schema created from db documentation

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

CREATE TABLE tmpUser (
    id_tmp INT NOT NULL AUTO_INCREMENt,
    username VARCHAR(20) NOT NULL ,
    password VARCHAR(255) NOT NULL ,
    valid_login BOOLEAN NOT NULL DEFAULT False,
    PRIMARY KEY(id_tmp)
);

CREATE TABLE VideoStats (
    id INT NOT NULL ,
    username VARCHAR(20) NOT NULL ,
    url VARCHAR(255) ,
    video_name VARCHAR(100) NOT NULL ,
    time_stamp TIMESTAMP NOT NULL
);