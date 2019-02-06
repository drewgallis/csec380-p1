-- Exported from QuickDBD: https://www.quickdatatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- Exported from QuickDBD: https://www.quickdatatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.
-- Modify this code to update the DB schema diagram.
-- To reset the sample schema, replace everything with
-- two dots ('..' - without quotes).

CREATE TABLE `User` (
    `id` int  NOT NULL ,
    `username` string  NOT NULL ,
    `password` string  NOT NULL ,
    `valid_login` boolean  NOT NULL ,
    PRIMARY KEY (
        `id`
    )
);

CREATE TABLE `VideoStats` (
    `id` int  NOT NULL ,
    `username` string  NOT NULL ,
    `url` string  NOT NULL ,
    `video_name` string  NOT NULL ,
    `timestamp` datetime  NOT NULL 
);

ALTER TABLE `VideoStats` ADD CONSTRAINT `fk_VideoStats_id_username` FOREIGN KEY(`id`, `username`)
REFERENCES `User` (`id`, `username`);

