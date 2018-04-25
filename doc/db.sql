
-- 2018.3.13

-- 图片信息

CREATE TABLE `image` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `room_sha_identity` varchar(64) DEFAULT NULL COMMENT '房屋sha_identity外键',
  `name` varchar(64) DEFAULT NULL COMMENT '图片名称',
  `post_time` datetime DEFAULT NULL COMMENT '上传照片时间',
  `path` varchar(512) DEFAULT NULL COMMENT '图片存放路径',
  `url` varchar(512) DEFAULT NULL COMMENT '图片url',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `room_sha_identity` (`room_sha_identity`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 创建用户表

CREATE TABLE `user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL COMMENT '用户名',
  `password` varchar(256) DEFAULT NULL COMMENT '密码',
  `sex` int(11) NOT NULL DEFAULT '0' COMMENT '性别 0 女 1 男',
  `age` int(11) DEFAULT NULL COMMENT '年龄',
  `phone` varchar(128) NOT NULL DEFAULT '' COMMENT '手机号码',
  `type` int(11) NOT NULL DEFAULT '0' COMMENT '0 个人 1 经纪人',
  `avatar` varchar(256) DEFAULT NULL COMMENT '用户头像信息',
  `verify` int(11) NOT NULL DEFAULT '0' COMMENT '用户是否认证 0 未认证, 1 认证',
  `company_name` varchar(256) DEFAULT NULL COMMENT '公司名称',
  `company_addr` varchar(512) DEFAULT NULL COMMENT '公司地址',
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone_2` (`phone`),
  KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8;
-- 创建房产表

CREATE TABLE `room` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `sha_identity` varchar(32) NOT NULL DEFAULT '' COMMENT ' md5(title+phone) 判断用户是否重复发布同一内容的房产信息',
  `title` varchar(256) DEFAULT NULL COMMENT '标题',
  `phone` varchar(20) DEFAULT NULL COMMENT '用户联系方式,关联用户 外键',
  `post_time` datetime DEFAULT NULL COMMENT '发布时间',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `house_name` varchar(256) DEFAULT NULL COMMENT '楼盘名称',
  `config` varchar(256) DEFAULT NULL COMMENT '房屋配置',
  `position` varchar(36) DEFAULT NULL COMMENT '房屋地址位置',
  `price` float DEFAULT NULL COMMENT '价格',
  `pre_price` float DEFAULT NULL COMMENT '房屋单价',
  `area` float DEFAULT NULL COMMENT '面积',
  `floor` int(11) DEFAULT NULL COMMENT '楼层',
  `total_floor` int(11) DEFAULT NULL COMMENT '总层高',
  `has_kitchen_bath` tinyint(1) DEFAULT NULL COMMENT '是否有厨卫',
  `five_year` tinyint(1) DEFAULT NULL COMMENT '产权是否满五年',
  `lobby` varchar(36) DEFAULT NULL COMMENT '客厅',
  `live_room` varchar(36) DEFAULT NULL COMMENT '卧室',
  `orientation` varchar(36) DEFAULT NULL COMMENT '朝向',
  `type` varchar(36) DEFAULT NULL COMMENT '住宅/商铺',
  `mark` varchar(10240) DEFAULT NULL COMMENT '其他描述信息',
  PRIMARY KEY (`id`),
  UNIQUE KEY `sha_identity` (`sha_identity`),
  KEY `title` (`title`),
  KEY `phone` (`phone`),
  KEY `house_name` (`house_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 租房表

CREATE TABLE `rent_room` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `sha_identity` varchar(32) DEFAULT NULL COMMENT 'md5(title+phone) 判断用户是否重复发布同一内容的房产信息',
  `phone` varchar(20) DEFAULT NULL COMMENT '用户联系方式,关联用户 外键',
  `title` varchar(256) DEFAULT NULL COMMENT '标题',
  `post_time` datetime DEFAULT NULL COMMENT '发布时间',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `house_name` varchar(256) DEFAULT NULL COMMENT '楼盘名称',
  `config` varchar(256) DEFAULT NULL COMMENT '房屋配置',
  `position` varchar(36) DEFAULT NULL COMMENT '房屋地址位置',
  `price` float DEFAULT NULL COMMENT '价格',
  `area` varchar(36) DEFAULT NULL COMMENT '面积',
  `floor` varchar(36) DEFAULT NULL COMMENT '楼层',
  `total_floor` varchar(36) DEFAULT NULL COMMENT '总层高',
  `rent_type` varchar(256) DEFAULT NULL COMMENT '出租类型',
  `lobby` varchar(36) DEFAULT NULL COMMENT '客厅',
  `live_room` varchar(36) DEFAULT NULL COMMENT '卧室',
  `orientation` varchar(36) DEFAULT NULL COMMENT '朝向',
  `type` varchar(36) DEFAULT NULL COMMENT '住宅/商铺',
  `has_kitchen_bath` int(11) DEFAULT NULL COMMENT '是否有厨卫',
  `mark` varchar(10240) DEFAULT NULL COMMENT '其他描述信息',
  `url` varchar(256) DEFAULT NULL COMMENT '采集的地址',
  PRIMARY KEY (`id`),
  UNIQUE KEY `sha_identity` (`sha_identity`),
  KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;