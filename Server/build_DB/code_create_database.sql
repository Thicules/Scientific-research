-- CREATE DATABASE IF NOT EXISTS `weblogin` DEFAULT CHARACTER SET UTF8MB4 COLLATE UTF8MB4_general_ci;
-- USE `weblogin`;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+07:00";

CREATE TABLE IF NOT EXISTS `accounts` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`email` varchar(100) NOT NULL,
  	`password` varchar(255) NOT NULL,
    `fullname` varchar(255),
    `gender` varchar(50),
    `phone` int(11),
    `date_of_birth` date,
    `street` varchar(255),
    `city` varchar(255),
    `state` varchar(255),
    `job` varchar(255),
    `ava` varchar(255),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=UTF8MB4;

CREATE TABLE IF NOT EXISTS `images` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `namepics` varchar(255) NOT NULL,
    `result` varchar(50) NOT NULL,
    `position` varchar(50) NOT NULL,
    `upload_date` date NOT NULL,
    `path` varchar(255) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `accounts` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

-- DROP TABLE IF EXISTS accounts;

-- SELECT * FROM weblogin.accounts;
