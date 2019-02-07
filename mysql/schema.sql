-- schema created from db documentation

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

