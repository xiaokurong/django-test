/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50545
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50545
File Encoding         : 65001

Date: 2019-04-25 18:14:21
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `blog_post`
-- ----------------------------
DROP TABLE IF EXISTS `blog_post`;
CREATE TABLE `blog_post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(250) NOT NULL,
  `slug` varchar(250) NOT NULL,
  `body` longtext NOT NULL,
  `publish` datetime NOT NULL,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  `status` varchar(10) NOT NULL,
  `author_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `blog_post_author_id_dd7a8485_fk_auth_user_id` (`author_id`),
  KEY `blog_post_slug_b95473f2` (`slug`),
  CONSTRAINT `blog_post_author_id_dd7a8485_fk_auth_user_id` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of blog_post
-- ----------------------------
INSERT INTO `blog_post` VALUES ('2', 'my post2', 'my-post2', 'my second post2', '2019-04-24 09:59:47', '2019-04-24 10:00:19', '2019-04-24 10:00:19', 'draft', '1');
INSERT INTO `blog_post` VALUES ('3', 'New title', 'one-more-post', 'Post body.', '2019-04-24 10:08:54', '2019-04-24 10:08:54', '2019-04-24 10:08:54', 'draft', '1');
INSERT INTO `blog_post` VALUES ('4', 'my post3', 'my-post3', 'my post3 body', '2019-04-25 03:02:00', '2019-04-25 03:02:29', '2019-04-25 03:02:29', 'published', '1');
INSERT INTO `blog_post` VALUES ('5', 'my post4', 'my-post4', 'my post4 body', '2019-04-25 03:02:42', '2019-04-25 03:03:06', '2019-04-25 03:03:06', 'published', '1');
