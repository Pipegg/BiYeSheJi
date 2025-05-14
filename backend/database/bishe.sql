/*
Navicat MySQL Data Transfer

Source Server         : localhost_3308
Source Server Version : 50726
Source Host           : localhost:3308
Source Database       : djangovue23517jydmxdznjyfzxtdsjysx

Target Server Type    : MYSQL
Target Server Version : 50726
File Encoding         : 65001

Date: 2024-12-30 23:24:50
*/
CREATE DATABASE bishe;
USE bishe;
SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for `admins`
-- ----------------------------
DROP TABLE IF EXISTS `admins`;
CREATE TABLE `admins` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL COMMENT '帐号',
  `pwd` varchar(50) NOT NULL COMMENT '密码',
  `xingming` varchar(50) NOT NULL COMMENT '姓名',
  `xingbie` varchar(10) NOT NULL COMMENT '性别',
  `lianxifangshi` varchar(50) NOT NULL COMMENT '联系方式',
  `touxiang` varchar(255) NOT NULL COMMENT '头像',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='管理员';

-- ----------------------------
-- Records of admins
-- ----------------------------
INSERT INTO `admins` VALUES ('1', 'admin', 'admin', '小卡', '男', '16526000000', '/static/upload/b0ec9e492f5178d34f01bc8db2ca49c9.jpg');

-- ----------------------------
-- Table structure for `buzhizuoye`
-- ----------------------------
DROP TABLE IF EXISTS `buzhizuoye`;
CREATE TABLE `buzhizuoye` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `kechengxinxiid` int(10) unsigned NOT NULL COMMENT '课程信息id',
  `kechengbianhao` varchar(50) NOT NULL COMMENT '课程编号',
  `kechengmingcheng` varchar(255) NOT NULL COMMENT '课程名称',
  `kechengfenlei` int(10) unsigned NOT NULL COMMENT '课程分类',
  `fabujiaoshi` varchar(50) NOT NULL COMMENT '发布教师',
  `zuoyebianhao` varchar(50) NOT NULL COMMENT '作业编号',
  `jiezhiriqi` varchar(25) NOT NULL COMMENT '截至日期',
  `zuoyemingcheng` varchar(255) NOT NULL COMMENT '作业名称',
  `zuoyefujian` varchar(255) NOT NULL COMMENT '作业附件',
  `yitijiaorenshu` int(11) NOT NULL DEFAULT '0' COMMENT '已提交人数',
  `zuoyemiaoshu` text NOT NULL COMMENT '作业描述',
  PRIMARY KEY (`id`),
  KEY `buzhizuoye_kechengxinxiid_index` (`kechengxinxiid`),
  KEY `buzhizuoye_kechengfenlei_index` (`kechengfenlei`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COMMENT='布置作业';

-- ----------------------------
-- Records of buzhizuoye
-- ----------------------------
INSERT INTO `buzhizuoye` VALUES ('1', '10', '12262021485', '算法设计与分析', '1', '100', '122919471367', '2024-12-29 19:47:48', ' 算法设计作业1', '/static/upload/c272437989c6f5dd540751242dc3586b.jpg', '2', '算法设计与分析算法设计与分析算法设计与分析算法设计与分析算法设计与分析算法设计与分析算法设计与分析算法设计与分析算法设计与分析');
INSERT INTO `buzhizuoye` VALUES ('2', '10', '12262021485', '算法设计与分析', '1', '100', '122919485923', '2024-12-29 19:48:17', ' 算法设计作业2', '/static/upload/c272437989c6f5dd540751242dc3586b.jpg', '0', '算法设计与分析算法设计与分析算法设计与分析算法设计与分析算法设计与分析算法设计与分析算法设计与分析算法设计与分析');
INSERT INTO `buzhizuoye` VALUES ('3', '9', '122620205286', '大数据解析与应用导论', '1', '100', '122919486522', '2024-12-29 19:48:27', ' 大数据解析作业1', '/static/upload/c272437989c6f5dd540751242dc3586b.jpg', '0', '大数据解析与应用导论大数据解析与应用导论大数据解析与应用导论大数据解析与应用导论大数据解析与应用导论大数据解析与应用导论');
INSERT INTO `buzhizuoye` VALUES ('4', '9', '122620205286', '大数据解析与应用导论', '1', '100', '122919485008', '2024-12-29 19:48:42', ' 大数据解析作业2', '/static/upload/c272437989c6f5dd540751242dc3586b.jpg', '0', '\n大数据解析与应用导论\n大数据解析与应用导论\n大数据解析与应用导论\n大数据解析与应用导论\n大数据解析与应用导论\n大数据解析与应用导论\n大数据解析与应用导论');
INSERT INTO `buzhizuoye` VALUES ('5', '8', '122620201377', '高级财务管理', '2', '100', '122919486197', '2024-12-29 19:48:52', '高级财务作业1', '/static/upload/c272437989c6f5dd540751242dc3586b.jpg', '0', '高级财务管理高级财务管理高级财务管理高级财务管理高级财务管理高级财务管理高级财务管理高级财务管理高级财务管理高级财务管理高级财务管理高级财务管理');
INSERT INTO `buzhizuoye` VALUES ('6', '8', '122620201377', '高级财务管理', '2', '100', '122919492859', '2024-12-29 19:49:05', '高级财务作业2', '/static/upload/c272437989c6f5dd540751242dc3586b.jpg', '0', '高级财务管理高级财务管理高级财务管理高级财务管理高级财务管理高级财务管理高级财务管理高级财务管理高级财务管理高级财务管理高级财务管理高级财务管理高级财务管理');
INSERT INTO `buzhizuoye` VALUES ('7', '11', '123023164203', '信息信息', '5', '100', '123023167613', '2024-12-30 23:16:52', '信息信息', '/static/upload/e6c8053fda96680543207a5c8811e1ac.webp', '0', '信息');

-- ----------------------------
-- Table structure for `django_content_type`
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES ('1', 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES ('2', 'admins', 'admins');
INSERT INTO `django_content_type` VALUES ('3', 'xuesheng', 'xuesheng');
INSERT INTO `django_content_type` VALUES ('4', 'youqinglianjie', 'youqinglianjie');
INSERT INTO `django_content_type` VALUES ('5', 'lunbotu', 'lunbotu');
INSERT INTO `django_content_type` VALUES ('6', 'shoucang', 'shoucang');
INSERT INTO `django_content_type` VALUES ('7', 'siliao', 'siliao');
INSERT INTO `django_content_type` VALUES ('8', 'xiaoxi', 'xiaoxi');
INSERT INTO `django_content_type` VALUES ('9', 'luntanjiaoliu', 'luntanjiaoliu');
INSERT INTO `django_content_type` VALUES ('10', 'luntanfenlei', 'luntanfenlei');
INSERT INTO `django_content_type` VALUES ('11', 'jiaoliuhuifu', 'jiaoliuhuifu');
INSERT INTO `django_content_type` VALUES ('12', 'jiaoshi', 'jiaoshi');
INSERT INTO `django_content_type` VALUES ('13', 'kechengfenlei', 'kechengfenlei');
INSERT INTO `django_content_type` VALUES ('14', 'kechengxinxi', 'kechengxinxi');
INSERT INTO `django_content_type` VALUES ('15', 'kechengshipin', 'kechengshipin');
INSERT INTO `django_content_type` VALUES ('16', 'kechengziyuan', 'kechengziyuan');
INSERT INTO `django_content_type` VALUES ('17', 'kechengxuexi', 'kechengxuexi');
INSERT INTO `django_content_type` VALUES ('18', 'xuexijindu', 'xuexijindu');
INSERT INTO `django_content_type` VALUES ('19', 'xuexijilu', 'xuexijilu');
INSERT INTO `django_content_type` VALUES ('20', 'buzhizuoye', 'buzhizuoye');
INSERT INTO `django_content_type` VALUES ('21', 'tijiaozuoye', 'tijiaozuoye');
INSERT INTO `django_content_type` VALUES ('22', 'zuoyepiyue', 'zuoyepiyue');
INSERT INTO `django_content_type` VALUES ('23', 'wenda', 'wenda');
INSERT INTO `django_content_type` VALUES ('24', 'huida', 'huida');
INSERT INTO `django_content_type` VALUES ('25', 'wendaxiaoxi', 'wendaxiaoxi');

-- ----------------------------
-- Table structure for `django_migrations`
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES ('1', 'contenttypes', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('2', 'contenttypes', '0002_remove_content_type_name', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('3', 'admins', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('4', 'xuesheng', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('5', 'youqinglianjie', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('6', 'lunbotu', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('7', 'shoucang', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('8', 'siliao', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('9', 'xiaoxi', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('10', 'luntanjiaoliu', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('11', 'luntanfenlei', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('12', 'jiaoliuhuifu', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('13', 'jiaoshi', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('14', 'kechengfenlei', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('15', 'kechengxinxi', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('16', 'kechengshipin', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('17', 'kechengziyuan', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('18', 'kechengxuexi', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('19', 'xuexijindu', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('20', 'xuexijilu', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('21', 'buzhizuoye', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('22', 'tijiaozuoye', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('23', 'zuoyepiyue', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('24', 'wenda', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('25', 'huida', '0001_initial', '2024-12-26 20:06:39');
INSERT INTO `django_migrations` VALUES ('26', 'wendaxiaoxi', '0001_initial', '2024-12-26 20:06:39');

-- ----------------------------
-- Table structure for `huida`
-- ----------------------------
DROP TABLE IF EXISTS `huida`;
CREATE TABLE `huida` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `wenti` int(10) unsigned NOT NULL COMMENT '问题',
  `huidaneirong` text NOT NULL COMMENT '回答内容',
  `quanzhi` int(11) NOT NULL DEFAULT '0' COMMENT '权值',
  `huidacishu` int(11) NOT NULL DEFAULT '0' COMMENT '回答次数',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `huida_wenti_index` (`wenti`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='回答';

-- ----------------------------
-- Records of huida
-- ----------------------------
INSERT INTO `huida` VALUES ('1', '1', '你好啊，我是小智，欢迎使用智能学习助手', '10', '3');
INSERT INTO `huida` VALUES ('2', '1', '我是小智，用的很不错', '10', '4');
INSERT INTO `huida` VALUES ('3', '2', '我是小智', '10', '1');
INSERT INTO `huida` VALUES ('4', '2', '我是你', '10', '1');
INSERT INTO `huida` VALUES ('5', '2', '好好学习吧，别问我啦', '10', '1');
INSERT INTO `huida` VALUES ('6', '3', '不用学会', '10', '1');
INSERT INTO `huida` VALUES ('7', '1', '你好！', '10', '4');
INSERT INTO `huida` VALUES ('8', '3', '努力看书', '10', '0');
INSERT INTO `huida` VALUES ('9', '3', '努力学习', '10', '0');
INSERT INTO `huida` VALUES ('10', '3', '音乐很容易的，只要加油就好', '10', '0');
INSERT INTO `huida` VALUES ('11', '5', '一般一般，世界第三', '10', '1');
INSERT INTO `huida` VALUES ('12', '5', '没有你厉害啦', '10', '0');
INSERT INTO `huida` VALUES ('13', '5', '还行啦', '10', '0');
INSERT INTO `huida` VALUES ('14', '6', '谢谢', '10', '1');

-- ----------------------------
-- Table structure for `jiaoliuhuifu`
-- ----------------------------
DROP TABLE IF EXISTS `jiaoliuhuifu`;
CREATE TABLE `jiaoliuhuifu` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `luntanjiaoliuid` int(10) unsigned NOT NULL COMMENT '论坛交流id',
  `bianhao` varchar(50) NOT NULL COMMENT '编号',
  `biaoti` varchar(50) NOT NULL COMMENT '标题',
  `fenlei` int(10) unsigned NOT NULL COMMENT '分类',
  `faburen` varchar(50) NOT NULL COMMENT '发布人',
  `jiaoliuneirong` longtext NOT NULL COMMENT '交流内容',
  `huifuren` varchar(50) NOT NULL COMMENT '回复人',
  `huifuquanxian` varchar(50) NOT NULL COMMENT '回复权限',
  `touxiang` varchar(255) NOT NULL COMMENT '头像',
  `xingming` varchar(50) NOT NULL COMMENT '姓名',
  `addtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '回复时间',
  PRIMARY KEY (`id`),
  KEY `jiaoliuhuifu_luntanjiaoliuid_index` (`luntanjiaoliuid`),
  KEY `jiaoliuhuifu_fenlei_index` (`fenlei`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COMMENT='交流回复';

-- ----------------------------
-- Records of jiaoliuhuifu
-- ----------------------------
INSERT INTO `jiaoliuhuifu` VALUES ('1', '4', '122620355276', '社会需求', '2', '001', '<p>666</p>', '002', '学生', '/static/upload/5d89086a778784b9574cdd9089d6efb2.jpg', '小娜', '2024-12-29 19:05:08');
INSERT INTO `jiaoliuhuifu` VALUES ('2', '4', '122620355276', '社会需求', '2', '001', '<blockquote>\n<p>回【1楼】楼，（小娜 的帖子）</p>\n<p>666</p>\n</blockquote>\n<p>&nbsp;</p>\n<p>&nbsp;</p>\n<p>66</p>', '002', '学生', '/static/upload/5d89086a778784b9574cdd9089d6efb2.jpg', '小娜', '2024-12-29 19:05:12');
INSERT INTO `jiaoliuhuifu` VALUES ('3', '1', '122620331195', '社会文化的变化', '2', '001', '<p>666</p>', '100', '教师', '/static/upload/a98d301c62635de0f4a9ba4cbc922b55.jpg', '张敏', '2024-12-30 15:42:38');
INSERT INTO `jiaoliuhuifu` VALUES ('4', '4', '122620355276', '社会需求', '2', '001', '<p>666</p>', '100', '教师', '/static/upload/a98d301c62635de0f4a9ba4cbc922b55.jpg', '张敏', '2024-12-30 23:05:17');
INSERT INTO `jiaoliuhuifu` VALUES ('5', '4', '122620355276', '社会需求', '2', '001', '<p>双方都是对方</p>', '100', '教师', '/static/upload/a98d301c62635de0f4a9ba4cbc922b55.jpg', '张敏', '2024-12-30 23:06:51');
INSERT INTO `jiaoliuhuifu` VALUES ('6', '1', '122620331195', '社会文化的变化', '2', '001', '<p>很好</p>', '100', '教师', '/static/upload/a98d301c62635de0f4a9ba4cbc922b55.jpg', '张敏', '2024-12-30 23:19:27');
INSERT INTO `jiaoliuhuifu` VALUES ('7', '1', '122620331195', '社会文化的变化', '2', '001', '<blockquote>\n<p>回【1楼】楼，（张敏 的帖子）</p>\n<p>很好</p>\n</blockquote>\n<p>很好</p>', '100', '教师', '/static/upload/a98d301c62635de0f4a9ba4cbc922b55.jpg', '张敏', '2024-12-30 23:19:33');
INSERT INTO `jiaoliuhuifu` VALUES ('8', '2', '122620344624', '从哲学认识论角度分析', '1', '001', '<p>66</p>', '003', '学生', '/static/upload/b0ec9e492f5178d34f01bc8db2ca49c9.jpg', '小洛克', '2024-12-30 23:20:37');
INSERT INTO `jiaoliuhuifu` VALUES ('9', '2', '122620344624', '从哲学认识论角度分析', '1', '001', '<blockquote>\n<p>回【1楼】楼，（小洛克 的帖子）</p>\n<p>66</p>\n</blockquote>\n<p>66</p>', '003', '学生', '/static/upload/b0ec9e492f5178d34f01bc8db2ca49c9.jpg', '小洛克', '2024-12-30 23:20:40');

-- ----------------------------
-- Table structure for `jiaoshi`
-- ----------------------------
DROP TABLE IF EXISTS `jiaoshi`;
CREATE TABLE `jiaoshi` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `gonghao` varchar(50) NOT NULL COMMENT '工号',
  `mima` varchar(50) NOT NULL COMMENT '密码',
  `xingming` varchar(50) NOT NULL COMMENT '姓名',
  `xingbie` varchar(10) NOT NULL COMMENT '性别',
  `zhicheng` varchar(50) NOT NULL COMMENT '职称',
  `lianxifangshi` varchar(50) NOT NULL COMMENT '联系方式',
  `youxiang` varchar(50) NOT NULL COMMENT '邮箱',
  `touxiang` varchar(255) NOT NULL COMMENT '头像',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COMMENT='教师';

-- ----------------------------
-- Records of jiaoshi
-- ----------------------------
INSERT INTO `jiaoshi` VALUES ('1', '100', '100', '张敏', '女', '教师', '15601566000', '1202@qq.com', '/static/upload/a98d301c62635de0f4a9ba4cbc922b55.jpg');
INSERT INTO `jiaoshi` VALUES ('2', '101', '101', '小虎', '男', '教师', '15002200000', '1511@qq.com', '/static/upload/798ceb1ce21606972c02be2d560a0047.jpg');

-- ----------------------------
-- Table structure for `kechengfenlei`
-- ----------------------------
DROP TABLE IF EXISTS `kechengfenlei`;
CREATE TABLE `kechengfenlei` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `fenleimingcheng` varchar(255) NOT NULL COMMENT '分类名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COMMENT='课程分类';

-- ----------------------------
-- Records of kechengfenlei
-- ----------------------------
INSERT INTO `kechengfenlei` VALUES ('1', '计算机');
INSERT INTO `kechengfenlei` VALUES ('2', '经济管理');
INSERT INTO `kechengfenlei` VALUES ('3', '艺术设计');
INSERT INTO `kechengfenlei` VALUES ('4', '医药卫生');
INSERT INTO `kechengfenlei` VALUES ('5', '农林园艺');

-- ----------------------------
-- Table structure for `kechengshipin`
-- ----------------------------
DROP TABLE IF EXISTS `kechengshipin`;
CREATE TABLE `kechengshipin` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `kechengxinxiid` int(10) unsigned NOT NULL COMMENT '课程信息id',
  `kechengbianhao` varchar(50) NOT NULL COMMENT '课程编号',
  `kechengmingcheng` varchar(255) NOT NULL COMMENT '课程名称',
  `kechengfenlei` int(10) unsigned NOT NULL COMMENT '课程分类',
  `fabujiaoshi` varchar(50) NOT NULL COMMENT '发布教师',
  `shipinmingcheng` varchar(255) NOT NULL COMMENT '视频名称',
  `shipin` varchar(255) NOT NULL COMMENT '视频',
  `xuexicishu` int(11) NOT NULL DEFAULT '0' COMMENT '学习次数',
  `shipinjieshao` longtext NOT NULL COMMENT '视频介绍',
  `addtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
  PRIMARY KEY (`id`),
  KEY `kechengshipin_kechengxinxiid_index` (`kechengxinxiid`),
  KEY `kechengshipin_kechengfenlei_index` (`kechengfenlei`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COMMENT='课程视频';

-- ----------------------------
-- Records of kechengshipin
-- ----------------------------
INSERT INTO `kechengshipin` VALUES ('1', '10', '12262021485', '算法设计与分析', '1', '100', '算法设计视频1', '/static/upload/87c56d50ec0ecb6092a6b90bbb575810.mp4', '1', '<p><span style=\"color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;\">《算法设计与分析》系统地介绍了算法设计与分析的概念和方法，共4篇内容。1篇介绍算法设计与分析的基本概念，结合穷举法、排序问题及其他一些算法，对算法的时间复杂性的概念及复杂性的分析方法作了较为详细的叙述；2篇以算法设计技术为纲，从合并排序、堆排序、离散集合的union和find作开始，进而介绍递归技术、分治法、贪婪法、动态规划、回溯法、分支与限界法和算法等算法设计技术及其复杂性分析；3篇介绍计算机应用领域里的一些算法，如图和网络流，以及计算几何中的一些问题；4篇介绍算法设计与分析中的一些理论问题，如NP完全问题、计算复杂性问题、下界理论问题，后介绍近似算法及其性能分析。《算法设计与分析》内容选材适当、编排合理、由浅入深、循序渐进、互相衔接、逐步展开，并附有大量实例，既注重算法的思想方法、推导过程和正确性的证明技术，也注重算法所涉及的数据结构、算法的具体实现和算法的工作过程。《算法设计与分析》可作为高等院校计算机专业本科生和研究生的教材，也可作为计算机科学与应用的科学技术人员的参考资料。</span></p>', '2024-12-29 19:43:27');
INSERT INTO `kechengshipin` VALUES ('2', '10', '12262021485', '算法设计与分析', '1', '100', ' 算法设计视频2', '/static/upload/87c56d50ec0ecb6092a6b90bbb575810.mp4', '1', '<p><span style=\"color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;\">《算法设计与分析》系统地介绍了算法设计与分析的概念和方法，共4篇内容。1篇介绍算法设计与分析的基本概念，结合穷举法、排序问题及其他一些算法，对算法的时间复杂性的概念及复杂性的分析方法作了较为详细的叙述；2篇以算法设计技术为纲，从合并排序、堆排序、离散集合的union和find作开始，进而介绍递归技术、分治法、贪婪法、动态规划、回溯法、分支与限界法和算法等算法设计技术及其复杂性分析；3篇介绍计算机应用领域里的一些算法，如图和网络流，以及计算几何中的一些问题；4篇介绍算法设计与分析中的一些理论问题，如NP完全问题、计算复杂性问题、下界理论问题，后介绍近似算法及其性能分析。《算法设计与分析》内容选材适当、编排合理、由浅入深、循序渐进、互相衔接、逐步展开，并附有大量实例，既注重算法的思想方法、推导过程和正确性的证明技术，也注重算法所涉及的数据结构、算法的具体实现和算法的工作过程。《算法设计与分析》可作为高等院校计算机专业本科生和研究生的教材，也可作为计算机科学与应用的科学技术人员的参考资料。</span></p>', '2024-12-29 19:43:45');
INSERT INTO `kechengshipin` VALUES ('3', '10', '12262021485', '算法设计与分析', '1', '100', ' 算法设计视频3', '/static/upload/87c56d50ec0ecb6092a6b90bbb575810.mp4', '2', '<p><span style=\"color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;\">《算法设计与分析》系统地介绍了算法设计与分析的概念和方法，共4篇内容。1篇介绍算法设计与分析的基本概念，结合穷举法、排序问题及其他一些算法，对算法的时间复杂性的概念及复杂性的分析方法作了较为详细的叙述；2篇以算法设计技术为纲，从合并排序、堆排序、离散集合的union和find作开始，进而介绍递归技术、分治法、贪婪法、动态规划、回溯法、分支与限界法和算法等算法设计技术及其复杂性分析；3篇介绍计算机应用领域里的一些算法，如图和网络流，以及计算几何中的一些问题；4篇介绍算法设计与分析中的一些理论问题，如NP完全问题、计算复杂性问题、下界理论问题，后介绍近似算法及其性能分析。《算法设计与分析》内容选材适当、编排合理、由浅入深、循序渐进、互相衔接、逐步展开，并附有大量实例，既注重算法的思想方法、推导过程和正确性的证明技术，也注重算法所涉及的数据结构、算法的具体实现和算法的工作过程。《算法设计与分析》可作为高等院校计算机专业本科生和研究生的教材，也可作为计算机科学与应用的科学技术人员的参考资料。</span></p>', '2024-12-29 19:43:55');
INSERT INTO `kechengshipin` VALUES ('4', '9', '122620205286', '大数据解析与应用导论', '1', '100', '大数据解析视频1', '/static/upload/87c56d50ec0ecb6092a6b90bbb575810.mp4', '0', '<p><span style=\"color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;\">《算法设计与分析》系统地介绍了算法设计与分析的概念和方法，共4篇内容。1篇介绍算法设计与分析的基本概念，结合穷举法、排序问题及其他一些算法，对算法的时间复杂性的概念及复杂性的分析方法作了较为详细的叙述；2篇以算法设计技术为纲，从合并排序、堆排序、离散集合的union和find作开始，进而介绍递归技术、分治法、贪婪法、动态规划、回溯法、分支与限界法和算法等算法设计技术及其复杂性分析；3篇介绍计算机应用领域里的一些算法，如图和网络流，以及计算几何中的一些问题；4篇介绍算法设计与分析中的一些理论问题，如NP完全问题、计算复杂性问题、下界理论问题，后介绍近似算法及其性能分析。《算法设计与分析》内容选材适当、编排合理、由浅入深、循序渐进、互相衔接、逐步展开，并附有大量实例，既注重算法的思想方法、推导过程和正确性的证明技术，也注重算法所涉及的数据结构、算法的具体实现和算法的工作过程。《算法设计与分析》可作为高等院校计算机专业本科生和研究生的教材，也可作为计算机科学与应用的科学技术人员的参考资料。</span></p>', '2024-12-29 19:44:23');
INSERT INTO `kechengshipin` VALUES ('5', '9', '122620205286', '大数据解析与应用导论', '1', '100', '大数据解析视频2', '/static/upload/87c56d50ec0ecb6092a6b90bbb575810.mp4', '0', '<p><span style=\"color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;\">《算法设计与分析》系统地介绍了算法设计与分析的概念和方法，共4篇内容。1篇介绍算法设计与分析的基本概念，结合穷举法、排序问题及其他一些算法，对算法的时间复杂性的概念及复杂性的分析方法作了较为详细的叙述；2篇以算法设计技术为纲，从合并排序、堆排序、离散集合的union和find作开始，进而介绍递归技术、分治法、贪婪法、动态规划、回溯法、分支与限界法和算法等算法设计技术及其复杂性分析；3篇介绍计算机应用领域里的一些算法，如图和网络流，以及计算几何中的一些问题；4篇介绍算法设计与分析中的一些理论问题，如NP完全问题、计算复杂性问题、下界理论问题，后介绍近似算法及其性能分析。《算法设计与分析》内容选材适当、编排合理、由浅入深、循序渐进、互相衔接、逐步展开，并附有大量实例，既注重算法的思想方法、推导过程和正确性的证明技术，也注重算法所涉及的数据结构、算法的具体实现和算法的工作过程。《算法设计与分析》可作为高等院校计算机专业本科生和研究生的教材，也可作为计算机科学与应用的科学技术人员的参考资料。</span></p>', '2024-12-29 19:44:32');
INSERT INTO `kechengshipin` VALUES ('6', '8', '122620201377', '高级财务管理', '2', '100', '高级财务视频1', '/static/upload/87c56d50ec0ecb6092a6b90bbb575810.mp4', '0', '<p><span style=\"color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;\">《算法设计与分析》系统地介绍了算法设计与分析的概念和方法，共4篇内容。1篇介绍算法设计与分析的基本概念，结合穷举法、排序问题及其他一些算法，对算法的时间复杂性的概念及复杂性的分析方法作了较为详细的叙述；2篇以算法设计技术为纲，从合并排序、堆排序、离散集合的union和find作开始，进而介绍递归技术、分治法、贪婪法、动态规划、回溯法、分支与限界法和算法等算法设计技术及其复杂性分析；3篇介绍计算机应用领域里的一些算法，如图和网络流，以及计算几何中的一些问题；4篇介绍算法设计与分析中的一些理论问题，如NP完全问题、计算复杂性问题、下界理论问题，后介绍近似算法及其性能分析。《算法设计与分析》内容选材适当、编排合理、由浅入深、循序渐进、互相衔接、逐步展开，并附有大量实例，既注重算法的思想方法、推导过程和正确性的证明技术，也注重算法所涉及的数据结构、算法的具体实现和算法的工作过程。《算法设计与分析》可作为高等院校计算机专业本科生和研究生的教材，也可作为计算机科学与应用的科学技术人员的参考资料。</span></p>', '2024-12-29 19:44:44');
INSERT INTO `kechengshipin` VALUES ('7', '8', '122620201377', '高级财务管理', '2', '100', '高级财务视频2', '/static/upload/87c56d50ec0ecb6092a6b90bbb575810.mp4', '2', '<p><span style=\"color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;\">《算法设计与分析》系统地介绍了算法设计与分析的概念和方法，共4篇内容。1篇介绍算法设计与分析的基本概念，结合穷举法、排序问题及其他一些算法，对算法的时间复杂性的概念及复杂性的分析方法作了较为详细的叙述；2篇以算法设计技术为纲，从合并排序、堆排序、离散集合的union和find作开始，进而介绍递归技术、分治法、贪婪法、动态规划、回溯法、分支与限界法和算法等算法设计技术及其复杂性分析；3篇介绍计算机应用领域里的一些算法，如图和网络流，以及计算几何中的一些问题；4篇介绍算法设计与分析中的一些理论问题，如NP完全问题、计算复杂性问题、下界理论问题，后介绍近似算法及其性能分析。《算法设计与分析》内容选材适当、编排合理、由浅入深、循序渐进、互相衔接、逐步展开，并附有大量实例，既注重算法的思想方法、推导过程和正确性的证明技术，也注重算法所涉及的数据结构、算法的具体实现和算法的工作过程。《算法设计与分析》可作为高等院校计算机专业本科生和研究生的教材，也可作为计算机科学与应用的科学技术人员的参考资料。</span></p>', '2024-12-29 19:44:53');
INSERT INTO `kechengshipin` VALUES ('8', '7', '122620201560', '消费者行为学', '2', '100', '消费者行为学视频1', '/static/upload/87c56d50ec0ecb6092a6b90bbb575810.mp4', '0', '<p><span style=\"color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;\">《算法设计与分析》系统地介绍了算法设计与分析的概念和方法，共4篇内容。1篇介绍算法设计与分析的基本概念，结合穷举法、排序问题及其他一些算法，对算法的时间复杂性的概念及复杂性的分析方法作了较为详细的叙述；2篇以算法设计技术为纲，从合并排序、堆排序、离散集合的union和find作开始，进而介绍递归技术、分治法、贪婪法、动态规划、回溯法、分支与限界法和算法等算法设计技术及其复杂性分析；3篇介绍计算机应用领域里的一些算法，如图和网络流，以及计算几何中的一些问题；4篇介绍算法设计与分析中的一些理论问题，如NP完全问题、计算复杂性问题、下界理论问题，后介绍近似算法及其性能分析。《算法设计与分析》内容选材适当、编排合理、由浅入深、循序渐进、互相衔接、逐步展开，并附有大量实例，既注重算法的思想方法、推导过程和正确性的证明技术，也注重算法所涉及的数据结构、算法的具体实现和算法的工作过程。《算法设计与分析》可作为高等院校计算机专业本科生和研究生的教材，也可作为计算机科学与应用的科学技术人员的参考资料。</span></p>', '2024-12-29 19:45:06');
INSERT INTO `kechengshipin` VALUES ('9', '7', '122620201560', '消费者行为学', '2', '100', '消费者行为学视频2', '/static/upload/87c56d50ec0ecb6092a6b90bbb575810.mp4', '0', '<p><span style=\"color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;\">《算法设计与分析》系统地介绍了算法设计与分析的概念和方法，共4篇内容。1篇介绍算法设计与分析的基本概念，结合穷举法、排序问题及其他一些算法，对算法的时间复杂性的概念及复杂性的分析方法作了较为详细的叙述；2篇以算法设计技术为纲，从合并排序、堆排序、离散集合的union和find作开始，进而介绍递归技术、分治法、贪婪法、动态规划、回溯法、分支与限界法和算法等算法设计技术及其复杂性分析；3篇介绍计算机应用领域里的一些算法，如图和网络流，以及计算几何中的一些问题；4篇介绍算法设计与分析中的一些理论问题，如NP完全问题、计算复杂性问题、下界理论问题，后介绍近似算法及其性能分析。《算法设计与分析》内容选材适当、编排合理、由浅入深、循序渐进、互相衔接、逐步展开，并附有大量实例，既注重算法的思想方法、推导过程和正确性的证明技术，也注重算法所涉及的数据结构、算法的具体实现和算法的工作过程。《算法设计与分析》可作为高等院校计算机专业本科生和研究生的教材，也可作为计算机科学与应用的科学技术人员的参考资料。</span></p>', '2024-12-29 19:45:15');
INSERT INTO `kechengshipin` VALUES ('10', '9', '122620205286', '大数据解析与应用导论', '1', '100', '大数据解析资源1', '/static/upload/c272437989c6f5dd540751242dc3586b.jpg', '0', '<p><span style=\"color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;\">《算法设计与分析》系统地介绍了算法设计与分析的概念和方法，共4篇内容。1篇介绍算法设计与分析的基本概念，结合穷举法、排序问题及其他一些算法，对算法的时间复杂性的概念及复杂性的分析方法作了较为详细的叙述；2篇以算法设计技术为纲，从合并排序、堆排序、离散集合的union和find作开始，进而介绍递归技术、分治法、贪婪法、动态规划、回溯法、分支与限界法和算法等算法设计技术及其复杂性分析；3篇介绍计算机应用领域里的一些算法，如图和网络流，以及计算几何中的一些问题；4篇介绍算法设计与分析中的一些理论问题，如NP完全问题、计算复杂性问题、下界理论问题，后介绍近似算法及其性能分析。《算法设计与分析》内容选材适当、编排合理、由浅入深、循序渐进、互相衔接、逐步展开，并附有大量实例，既注重算法的思想方法、推导过程和正确性的证明技术，也注重算法所涉及的数据结构、算法的具体实现和算法的工作过程。《算法设计与分析》可作为高等院校计算机专业本科生和研究生的教材，也可作为计算机科学与应用的科学技术人员的参考资料。</span></p>', '2024-12-29 19:46:23');
INSERT INTO `kechengshipin` VALUES ('11', '9', '122620205286', '大数据解析与应用导论', '1', '100', '大数据解析资源2', '/static/upload/c272437989c6f5dd540751242dc3586b.jpg', '0', '<p><span style=\"color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;\">《算法设计与分析》系统地介绍了算法设计与分析的概念和方法，共4篇内容。1篇介绍算法设计与分析的基本概念，结合穷举法、排序问题及其他一些算法，对算法的时间复杂性的概念及复杂性的分析方法作了较为详细的叙述；2篇以算法设计技术为纲，从合并排序、堆排序、离散集合的union和find作开始，进而介绍递归技术、分治法、贪婪法、动态规划、回溯法、分支与限界法和算法等算法设计技术及其复杂性分析；3篇介绍计算机应用领域里的一些算法，如图和网络流，以及计算几何中的一些问题；4篇介绍算法设计与分析中的一些理论问题，如NP完全问题、计算复杂性问题、下界理论问题，后介绍近似算法及其性能分析。《算法设计与分析》内容选材适当、编排合理、由浅入深、循序渐进、互相衔接、逐步展开，并附有大量实例，既注重算法的思想方法、推导过程和正确性的证明技术，也注重算法所涉及的数据结构、算法的具体实现和算法的工作过程。《算法设计与分析》可作为高等院校计算机专业本科生和研究生的教材，也可作为计算机科学与应用的科学技术人员的参考资料。</span></p>', '2024-12-29 19:46:31');
INSERT INTO `kechengshipin` VALUES ('12', '11', '123023164203', '信息信息', '5', '100', '信息信息', '/static/upload/87c56d50ec0ecb6092a6b90bbb575810.mp4', '0', '<p><img src=\"http://127.0.0.1:8006/static/upload/9d1fa3ebd40e3f22bfa44e195ac2d00f.png\"></p>', '2024-12-30 23:16:39');

-- ----------------------------
-- Table structure for `kechengxinxi`
-- ----------------------------
DROP TABLE IF EXISTS `kechengxinxi`;
CREATE TABLE `kechengxinxi` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `kechengbianhao` varchar(50) NOT NULL COMMENT '课程编号',
  `kechengmingcheng` varchar(255) NOT NULL COMMENT '课程名称',
  `kechengfenlei` int(10) unsigned NOT NULL COMMENT '课程分类',
  `kechengfengmian` varchar(255) NOT NULL COMMENT '课程封面',
  `kechengyaodian` varchar(50) NOT NULL COMMENT '课程要点',
  `kechengxiangqing` longtext NOT NULL COMMENT '课程详情',
  `addtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
  `fabujiaoshi` varchar(50) NOT NULL COMMENT '发布教师',
  `issh` varchar(10) NOT NULL DEFAULT '否' COMMENT '是否审核',
  PRIMARY KEY (`id`),
  KEY `kechengxinxi_kechengfenlei_index` (`kechengfenlei`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COMMENT='课程信息';

-- ----------------------------
-- Records of kechengxinxi
-- ----------------------------
INSERT INTO `kechengxinxi` VALUES ('1', '122620172573', '荒漠化防治学', '5', '/static/upload/f7b7fd27b87232ab50f02139efe3c403.png', '土地，是人类最宝贵的自然资源，也是人类生存和发展的基石', '<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; color: rgb(102, 102, 102); font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre-wrap; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; text-indent: 32px; line-height: 18px;\"><strong style=\"box-sizing: initial; font-weight: bold; font-family: \'Times New Roman\', serif;\">1. </strong><strong style=\"box-sizing: initial; font-weight: bold; font-family: 宋体;\">课程背景</strong></p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; color: rgb(102, 102, 102); font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre-wrap; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; text-indent: 32px; line-height: 18px;\"><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">土地荒漠化是全人类面临的重大挑战，也是我国的重要生态环境问题。目前，我国荒漠化、沙漠化土地面积仍然高达</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Times New Roman\', serif;\">261.16</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">和</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Times New Roman\', serif;\">172.12</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">万平方公里，危害全国</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Times New Roman\', serif;\">4</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">亿人口，直接经济约为损失</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Times New Roman\', serif;\">1200</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">亿元</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Times New Roman\', serif;\">/</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">年。因此，党的十九大报告明确提出：</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Times New Roman\', serif;\">&ldquo;</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">要开展国土绿化行动，推进荒漠化、石漠化、水土流失治理</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Times New Roman\', serif;\">&hellip;&hellip;&rdquo;</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">。在生态文明新时代，荒漠化防治是服务支撑国家重大战略、重大工程的重要任务，如何培养高质量的荒漠化防治人才，是我们面临的重大任务和挑战。</span></p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; color: rgb(102, 102, 102); font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre-wrap; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; text-indent: 32px; line-height: 18px;\"><strong style=\"box-sizing: initial; font-weight: bold; font-family: \'Times New Roman\', serif;\">2. </strong><strong style=\"box-sizing: initial; font-weight: bold; font-family: 宋体;\">课程概况</strong></p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; color: rgb(102, 102, 102); font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre-wrap; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; text-indent: 32px; line-height: 18px;\"><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Times New Roman\', serif;\">&ldquo;</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">荒漠化防治学</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Times New Roman\', serif;\">&rdquo;</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">是北京林业大学国家级一流本科专业建设点水土保持与荒漠化防治专业核心必修课。北京林业大学</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Times New Roman\', serif;\">&ldquo;</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">荒漠化防治学</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Times New Roman\', serif;\">&rdquo;</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">是一门传统课程，起源可追溯到</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Times New Roman\', serif;\">20</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">世纪</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Times New Roman\', serif;\">50</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">年代关君蔚院士开设的</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Times New Roman\', serif;\">&ldquo;</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">治沙学</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Times New Roman\', serif;\">&rdquo;</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">课程。长期以来，</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Times New Roman\', serif;\">北京林业</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">大学四代治沙人前赴后继，呕心沥血，课程建设始终在全国同类院校中处于引领地位。</span></p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; color: rgb(102, 102, 102); font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre-wrap; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; text-indent: 32px; line-height: 18px;\"><strong style=\"box-sizing: initial; font-weight: bold; font-family: \'Times New Roman\', serif;\">3. </strong><strong style=\"box-sizing: initial; font-weight: bold; font-family: 宋体;\">课程内容</strong></p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; color: rgb(102, 102, 102); font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre-wrap; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; text-indent: 32px; line-height: 18px;\"><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Times New Roman\', serif;\">&ldquo;</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">荒漠化防治学</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Times New Roman\', serif;\">&rdquo;</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">着重辨析土地荒漠化的概念与内涵，土地荒漠化形成机制、分布与危害，风蚀荒漠化防治的生态学和风沙物理学原理，风蚀荒漠化防治生物和工程技术措施，绿洲、草（牧）场、铁（公）路等典型区域沙害综合防治技术措施体系、典型模式，盐渍荒漠化、冻融荒漠化和石漠化防治的基本原理和技术，土地荒漠化监测与效益评价等内容。</span></p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; color: rgb(102, 102, 102); font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre-wrap; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; line-height: 18px;\"><strong style=\"box-sizing: initial; font-weight: bold; font-family: \'Times New Roman\', serif;\">&nbsp;&nbsp;&nbsp;&nbsp;4. </strong><strong style=\"box-sizing: initial; font-weight: bold; font-family: 宋体;\">课程特色</strong></p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; color: rgb(102, 102, 102); font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre-wrap; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; text-indent: 28px; line-height: 18px;\"><strong style=\"box-sizing: initial; font-weight: bold; font-family: 宋体;\">（</strong><strong style=\"box-sizing: initial; font-weight: bold; font-family: \'Times New Roman\', serif;\">1</strong><strong style=\"box-sizing: initial; font-weight: bold; font-family: 宋体;\">）理论和实践联系密切</strong> <span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">课程学习必须具有扎实的风沙物理学、荒漠生态学、流体力学、水文与水资源学、土壤学、地貌学、气象学、植物学等理论基础。其中，风沙物理学和荒漠生态学是课程的两大理论支柱。同时，课程具有极强的实践性，课程学习必须理论联系实际，躬亲实践，才能深刻学习荒漠化防治基本原理和技术方法，激发创新意识，并体验劳动的艰辛与乐趣。</span></p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; color: rgb(102, 102, 102); font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: pre-wrap; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; text-indent: 28px; line-height: 18px;\"><strong style=\"box-sizing: initial; font-weight: bold; font-family: 宋体;\">（</strong><strong style=\"box-sizing: initial; font-weight: bold; font-family: \'Times New Roman\', serif;\">2</strong><strong style=\"box-sizing: initial; font-weight: bold; font-family: 宋体;\">）交叉性和综合性鲜明</strong> <span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">荒漠化防治是一项复杂的系统工程，涉及水、土、气、生和人等众多影响因素。课程学习必须林学、生态、土壤、气象、地理、生物、环境等多学科交叉，工作实践必须林草、水利、自然资源、生态环境、交通等多行业综合。</span></p>', '2024-12-26 20:17:35', '100', '是');
INSERT INTO `kechengxinxi` VALUES ('2', '122620175460', '森林保护学', '5', '/static/upload/2742c9581cd62b82744b41108d0e410e.png', '《森林保护学》课程是面向林学、森林保护', '<div class=\"category-content j-cover-overflow\" style=\"box-sizing: initial; margin: 0px 0px 50px; padding: 0px; outline: none; position: relative; color: rgb(51, 51, 51); font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">\n<div class=\"f-richEditorText\" style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; border: 0px; text-align: left; word-break: break-word; overflow-wrap: break-word; font: 12px / 22px \'Helvetica Neue\', Helvetica, Arial, sans-serif; color: rgb(102, 102, 102); white-space: pre-wrap;\">\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\"><code style=\"box-sizing: initial; font-size: 1em; font-family: monospace; display: inline-block; white-space: pre-wrap; margin: 0.5em 0px; padding: 0.4em 0.6em; border-radius: 8px; background: rgb(239, 239, 239);\">《森林保护学》课程是系统介绍林木病虫害发生、发展过程及其规律的科学。本课程不仅向学生传授基本理论知识，介绍有害生物类型，还注重挖掘重大有害生物事件背后的故事，体现科学思想、科学方法和科学精神。在教学内容上，主要包括以下两个模块：</code></p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\"><code style=\"box-sizing: initial; font-size: 1em; font-family: monospace; display: inline-block; white-space: pre-wrap; margin: 0.5em 0px; padding: 0.4em 0.6em; border-radius: 8px; background: rgb(239, 239, 239);\">1.林木病害的现象和本质症状、林木病害病原、林木病害发生与流行、林木病害诊断与防治措施、重要林木病害及其防治；</code></p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\"><code style=\"box-sizing: initial; font-size: 1em; font-family: monospace; display: inline-block; white-space: pre-wrap; margin: 0.5em 0px; padding: 0.4em 0.6em; border-radius: 8px; background: rgb(239, 239, 239);\">2.昆虫的形态与功能、昆虫的生物学、昆虫分类、害虫防治原理与方法、重要林木害虫及其防治方法。</code></p>\n</div>\n</div>\n<div class=\"category-title f-f0\" style=\"box-sizing: initial; margin: 0px; padding: 0px 0px 10px; outline: none; font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 18px; font-weight: bold; color: rgb(51, 51, 51); font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">&nbsp;<span class=\"f-ib f-vam\" style=\"box-sizing: initial; display: inline-block; zoom: 1; vertical-align: middle;\">授课目标</span></div>\n<div class=\"category-content j-cover-overflow\" style=\"box-sizing: initial; margin: 0px 0px 50px; padding: 0px; outline: none; position: relative; color: rgb(51, 51, 51); font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">\n<div class=\"f-richEditorText\" style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; border: 0px; text-align: left; word-break: break-word; overflow-wrap: break-word; font: 12px / 22px \'Helvetica Neue\', Helvetica, Arial, sans-serif; color: rgb(102, 102, 102); white-space: pre-wrap;\">\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\">知识目标：掌握林木有害生物的识别、诊断的方法；掌握林木有害生物的发生规律；掌握林木有害生物的防治措施。</p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\">能力目标：能诊断常见林木有害生物；能根据有害生物特点制定防治方案 ；培养提出问题、分析问题和解决问题能力培养观察判断能力，能够分析和诊断常见林木有害生物。</p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\">价值目标：需要全面把握社会主义核心价值观，培养具有&ldquo;三农&rdquo;情怀，知农，爱农的新型森林保护人才。</p>\n</div>\n</div>', '2024-12-26 20:17:35', '100', '是');
INSERT INTO `kechengxinxi` VALUES ('3', '122620182330', '药物分析', '4', '/static/upload/2533bc6cdd7505b826db313593ae8b26.png', '药物分析是研究药品质量及其控制规律的科学', '<div class=\"category-title f-f0\" style=\"box-sizing: initial; margin: 0px; padding: 0px 0px 10px; outline: none; font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 18px; font-weight: bold; color: rgb(51, 51, 51); font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">&nbsp;<span class=\"f-ib f-vam\" style=\"box-sizing: initial; display: inline-block; zoom: 1; vertical-align: middle;\">课程概述</span></div>\n<div class=\"category-content j-cover-overflow\" style=\"box-sizing: initial; margin: 0px 0px 50px; padding: 0px; outline: none; position: relative; color: rgb(51, 51, 51); font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">\n<div class=\"f-richEditorText\" style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; border: 0px; text-align: left; word-break: break-word; overflow-wrap: break-word; font: 12px / 22px \'Helvetica Neue\', Helvetica, Arial, sans-serif; color: rgb(102, 102, 102); white-space: pre-wrap;\">\n<p class=\"ql-align-justify\" style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\"><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px;\">中国药科大学</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px; font-family: \'Times New Roman\', \'serif\';\">&ldquo;</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px;\">药物分析</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px; font-family: \'Times New Roman\', \'serif\';\">&rdquo;</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px;\">课程于</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px; font-family: \'Times New Roman\', \'serif\';\">1960</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px;\">年在我国率先创办。我校药物分析教学团队率先编著</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px; font-family: \'Times New Roman\', \'serif\';\">,</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px;\">并一直主编《药物分析》国家级规划教材；</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px; font-family: \'Times New Roman\', \'serif\';\">&ldquo;</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px;\">药物分析</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px; font-family: \'Times New Roman\', \'serif\';\">&rdquo;</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px;\">课程先后被评为国家精品课程（</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px; font-family: \'Times New Roman\', \'serif\';\">2008</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px;\">）、国家双语教学示范课程（</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px; font-family: \'Times New Roman\', \'serif\';\">2010</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px;\">），国家精品资源共享课（</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px; font-family: \'Times New Roman\', \'serif\';\">2013</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px;\">），国家精品开放课程（</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px; font-family: \'Times New Roman\', \'serif\';\">2017</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px;\">）。药物分析</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px; font-family: \'Times New Roman\', \'serif\';\">MOOC</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px;\">是在互联网科技飞速发展的背景下，适应国际药学教育发展的理念和趋势建设的。</span></p>\n<p class=\"ql-align-justify\" style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\"><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px;\">课程系统介绍药学与临床药学相关的药物分析专业知识、具体研究案例；理解和掌握药物分析学以先进的科学技术助力药品质量控制、新药研发、市场监督管理、临床合理应用等理念与方法技术。通过学习，树立强烈的药物质量与安全意识，激发社会责任感，弘扬严谨求实的科学精神。</span></p>\n<p class=\"ql-align-justify\" style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\"><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px;\">新版课程内容包括26个章节，可划分为四个模块：药物分析综合</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px; font-family: \'Times New Roman\', \'serif\';\">&mdash;</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px;\">化学药物和中药分析</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px; font-family: \'Times New Roman\', \'serif\';\">&mdash;</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: rgb(0, 0, 0); font-size: 14px; font-family: \'Times New Roman\', \'serif\';\">生物药物分析&mdash;</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black; font-size: 14px;\">前沿拓展。</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: black;\">通过课程学习，可为创新药物研发，药品质量控制，临床药学实践，药品监督管理等从业者提供必需的知识储备。</span></p>\n</div>\n</div>\n<div class=\"category-title f-f0\" style=\"box-sizing: initial; margin: 0px; padding: 0px 0px 10px; outline: none; font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 18px; font-weight: bold; color: rgb(51, 51, 51); font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">&nbsp;<span class=\"f-ib f-vam\" style=\"box-sizing: initial; display: inline-block; zoom: 1; vertical-align: middle;\">授课目标</span></div>\n<div class=\"category-content j-cover-overflow\" style=\"box-sizing: initial; margin: 0px 0px 50px; padding: 0px; outline: none; position: relative; color: rgb(51, 51, 51); font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">\n<div class=\"f-richEditorText\" style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; border: 0px; text-align: left; word-break: break-word; overflow-wrap: break-word; font: 12px / 22px \'Helvetica Neue\', Helvetica, Arial, sans-serif; color: rgb(102, 102, 102); white-space: pre-wrap;\">\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\">药学、药物分析、临床药学等相关专业在校生或从业人员</p>\n</div>\n</div>', '2024-12-26 20:17:35', '100', '是');
INSERT INTO `kechengxinxi` VALUES ('4', '122620186468', '神经系统疾病病人的护理', '4', '/static/upload/d86c81037e843ecb0108a5982bc31393.png', '神经系统疾病尤其脑血管病，对人群健康产生显著影响', '<div class=\"category-title f-f0\" style=\"box-sizing: initial; margin: 0px; padding: 0px 0px 10px; outline: none; font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 18px; font-weight: bold; color: rgb(51, 51, 51); font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">&nbsp;<span class=\"f-ib f-vam\" style=\"box-sizing: initial; display: inline-block; zoom: 1; vertical-align: middle;\">课程概述</span></div>\n<div class=\"category-content j-cover-overflow\" style=\"box-sizing: initial; margin: 0px 0px 50px; padding: 0px; outline: none; position: relative; color: rgb(51, 51, 51); font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">\n<div class=\"f-richEditorText\" style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; border: 0px; text-align: left; word-break: break-word; overflow-wrap: break-word; font: 12px / 22px \'Helvetica Neue\', Helvetica, Arial, sans-serif; color: rgb(102, 102, 102); white-space: pre-wrap;\">\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\">&nbsp; &nbsp; &nbsp; &nbsp;本课程为国家级线上一流课程，由北京大学跨专业教师团队集多年临床和教学经验倾情打造。既有来自北京大学护理学院和附属医院的护理团队教师，还有北京大学附属医院的神经专科医疗团队以及康复团队的教师。</p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\">&nbsp; &nbsp; &nbsp; 《神经系统疾病病人的护理》是护理学专业本科生的必修内容之一。由于神经系统是人体最精细、结构和功能最复杂的系统，与其他系统疾病相比，有其独特的临床表现、诊疗思路和学习方法。因此，本课程的总论部分将首先引导学生梳理神经系统的解剖和生理知识，进而介绍神经系统疾病的体格检查方法，常见症状和体征以及相应的护理与康复措施，帮助学生掌握神经系统疾病的共性内容。各论部分将依次讲授脑血管疾病、癫痫、重症肌无力、帕金森病、阿尔茨海默病、急性炎性脱髓鞘性多发神经病、多发性硬化的相关知识，包括病因及发病机制、临床表现、诊断及治疗要点、护理及康复措施。</p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\">&nbsp; &nbsp; &nbsp; &nbsp;总评成绩由四部分组成，其中论坛互动占5%，单元作业占20%，单元测验占25%，期末测试占50%。总评分数在60分及以上为合格，80分及以上为优秀。</p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\">&nbsp; &nbsp; &nbsp;期待大家的参与，祝大家学有所获！</p>\n</div>\n</div>', '2024-12-26 20:17:35', '100', '是');
INSERT INTO `kechengxinxi` VALUES ('5', '12262019403', '家居设计', '3', '/static/upload/35aa37048094e901fc9d088954a8aaf0.png', '本课程针对大众关心的家居设计话题，结合设计实践案例', '<div class=\"category-title f-f0\" style=\"box-sizing: initial; margin: 0px; padding: 0px 0px 10px; outline: none; font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 18px; font-weight: bold; color: rgb(51, 51, 51); font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">&nbsp;<span class=\"f-ib f-vam\" style=\"box-sizing: initial; display: inline-block; zoom: 1; vertical-align: middle;\">课程概述</span></div>\n<div class=\"category-content j-cover-overflow\" style=\"box-sizing: initial; margin: 0px 0px 50px; padding: 0px; outline: none; position: relative; color: rgb(51, 51, 51); font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">\n<div class=\"f-richEditorText\" style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; border: 0px; text-align: left; word-break: break-word; overflow-wrap: break-word; font: 12px / 22px \'Helvetica Neue\', Helvetica, Arial, sans-serif; color: rgb(102, 102, 102); white-space: pre-wrap;\">\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\"><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: rgb(0, 0, 0); font-family: arial, \'Microsoft Yahei\', sans-serif; font-size: 15px;\">家是我们</span> <a style=\"box-sizing: initial; color: rgb(68, 68, 68); text-decoration: underline; background-color: transparent; outline: none; cursor: pointer; transition: color 0.3s; touch-action: manipulation; font-family: arial, \'Microsoft Yahei\', sans-serif; font-size: 15px;\" href=\"https://rensheng.sanwen.net/\" target=\"_blank\" rel=\"noopener noreferrer\">人生</a> <span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: rgb(0, 0, 0); font-family: arial, \'Microsoft Yahei\', sans-serif; font-size: 15px;\">的驿站，是我们</span> <a style=\"box-sizing: initial; color: rgb(68, 68, 68); text-decoration: underline; background-color: transparent; outline: none; cursor: pointer; transition: color 0.3s; touch-action: manipulation; font-family: arial, \'Microsoft Yahei\', sans-serif; font-size: 15px;\" href=\"https://www.sanwen.net/suibi/shenghuo/\" target=\"_blank\" rel=\"noopener noreferrer\">生活</a> <span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; color: rgb(0, 0, 0); font-family: arial, \'Microsoft Yahei\', sans-serif; font-size: 15px;\">的乐园，也是我们避风的港湾。</span></p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\">怎样打造温馨舒适的家，彰显自身审美情趣，体现家居设计的个性化与实用性是当下热门的话题，本课程以家居装饰装修为主线，以家居设计的前期准备为起点，展开家居各个功能空间的风格、材质、光环境、色彩、智能等多方面设计内容的介绍。通过对家居设计的原则与方法的了解，使学生提升自身的美学素养，对于自己未来的栖身之所的设计做到游刃有余。把握家居设计的流行趋势，拓展家居智能化设计视野是本门课程的特色与亮点。</p>\n</div>\n</div>', '2024-12-26 20:17:35', '100', '是');
INSERT INTO `kechengxinxi` VALUES ('6', '122620192162', '设计的力量', '3', '/static/upload/7d81b5f219b73cd3c93f2495bc3cb9ea.png', '在全球化时代的语境中，设计产生的巨大价值更是深刻地影响着当代经济', '<div class=\"category-title f-f0\" style=\"box-sizing: initial; margin: 0px; padding: 0px 0px 10px; outline: none; font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 18px; font-weight: bold; color: rgb(51, 51, 51); font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">&nbsp;<span class=\"f-ib f-vam\" style=\"box-sizing: initial; display: inline-block; zoom: 1; vertical-align: middle;\">课程概述</span></div>\n<div class=\"category-content j-cover-overflow\" style=\"box-sizing: initial; margin: 0px 0px 50px; padding: 0px; outline: none; position: relative; color: rgb(51, 51, 51); font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">\n<div class=\"f-richEditorText\" style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; border: 0px; text-align: left; word-break: break-word; overflow-wrap: break-word; font: 12px / 22px \'Helvetica Neue\', Helvetica, Arial, sans-serif; color: rgb(102, 102, 102); white-space: pre-wrap;\">\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\">&nbsp;&nbsp;&nbsp;本课程主要以人类设计历史，尤其是过去250年中发生的重大历史事件为线索，梳理设计在国家发展过程中产生的重大影响。在当前我国实行经济转型、自主创新的过程中，设计对改变中国制造的形象以及真正成为创新型国家所发挥的创新引领作用显得尤为重要。</p>\n</div>\n</div>\n<div class=\"category-title f-f0\" style=\"box-sizing: initial; margin: 0px; padding: 0px 0px 10px; outline: none; font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 18px; font-weight: bold; color: rgb(51, 51, 51); font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">&nbsp;</div>', '2024-12-26 20:19:59', '100', '是');
INSERT INTO `kechengxinxi` VALUES ('7', '122620201560', '消费者行为学', '2', '/static/upload/f449473b35be741445af701b9ce24ac0.png', '在孟亮教授主讲的国家级一流本科课程（线上课程）', '<div class=\"category-title f-f0\" style=\"box-sizing: initial; margin: 0px; padding: 0px 0px 10px; outline: none; font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 18px; font-weight: bold; color: rgb(51, 51, 51); font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">&nbsp;<span class=\"f-ib f-vam\" style=\"box-sizing: initial; display: inline-block; zoom: 1; vertical-align: middle;\">课程概述</span></div>\n<div class=\"category-content j-cover-overflow\" style=\"box-sizing: initial; margin: 0px 0px 50px; padding: 0px; outline: none; position: relative; color: rgb(51, 51, 51); font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">\n<div class=\"f-richEditorText\" style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; border: 0px; text-align: left; word-break: break-word; overflow-wrap: break-word; font: 12px / 22px \'Helvetica Neue\', Helvetica, Arial, sans-serif; color: rgb(102, 102, 102); white-space: pre-wrap;\">\n<p class=\"ql-align-justify\" style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; text-indent: 32px; line-height: 19.2px;\"><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">本课程于2023年入选国家级一流本科课程（线上课程）。主讲教师孟亮为上海外国语大学教授、博士生导师、管理与组织系主任、上海市晨光学者，浙江大学管理学博士、宾夕法尼亚大学博士后，管理科学与工程学会优秀博士学位论文、浙江大学最高荣誉&ldquo;竺可桢奖&rdquo;获得者。</span></p>\n<p class=\"ql-align-justify\" style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; text-indent: 32px; line-height: 19.2px;\">&nbsp;</p>\n<p class=\"ql-align-justify\" style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; text-indent: 32px; line-height: 19.2px;\"><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">这是一个最好的时代，开网店、做直播、拍抖音，似乎处处都是商机。但这似乎又是一个最坏的时代，用心做好产品的你眼看着自己的产品门庭冷落、无人问津，而一些平淡无奇、甚至质量低下的产品却大行其道、获得巨大的商业成功。其实，我们每个人都是消费者，我们也都在试图吸引和取悦自己的目标消费者。而要真正做到这一点，依靠大手笔的营销推广或许都无济于事，我们需要去深入洞察消费者的心理。这正是《消费者行为学》这门课想要向你揭示的玄机。</span></p>\n<p class=\"ql-align-justify\" style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; text-indent: 32px; line-height: 19.2px;\">&nbsp;</p>\n<p class=\"ql-align-justify\" style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; text-indent: 32px; line-height: 19.2px;\"><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体;\">你知道消费者是有限理性的，在做出决策时很容易被商家所引导吗？你知道很多产品广告的目标是让消费者产生条件反射，从而下意识的做出购买行为吗？你知道如何去应用一致性原则改变消费者的态度吗？你知道东方卫视王牌节目《极限挑战》成功的秘诀所在吗？你知道网易云音乐是如何通过用户生成内容，获得听众的情感共鸣，在一众音乐播放类软件中脱颖而出的吗？以上这些有趣的内容，都是《消费者行为学》中的常见话题。如果你想知道这些问题的答案，就和上海外国语大学国际工商管理学院的孟亮老师一起，探索消费心理的奥秘吧。</span></p>\n</div>\n</div>', '2024-12-26 20:20:23', '100', '是');
INSERT INTO `kechengxinxi` VALUES ('8', '122620201377', '高级财务管理', '2', '/static/upload/eb7553825b91a3ea5a16d5500ce2e0f3.png', '高级财务管理》由西安交通大学管理学院副院长田高良教授主讲', '<div class=\"category-title f-f0\" style=\"box-sizing: initial; margin: 0px; padding: 0px 0px 10px; outline: none; font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 18px; font-weight: bold; color: rgb(51, 51, 51); font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">&nbsp;<span class=\"f-ib f-vam\" style=\"box-sizing: initial; display: inline-block; zoom: 1; vertical-align: middle;\">课程概述</span></div>\n<div class=\"category-content j-cover-overflow\" style=\"box-sizing: initial; margin: 0px 0px 50px; padding: 0px; outline: none; position: relative; color: rgb(51, 51, 51); font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">\n<div class=\"f-richEditorText\" style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; border: 0px; text-align: left; word-break: break-word; overflow-wrap: break-word; font: 12px / 22px \'Helvetica Neue\', Helvetica, Arial, sans-serif; color: rgb(102, 102, 102); white-space: pre-wrap;\">\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; text-indent: 32px; line-height: 24px;\"><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-size: 16px; font-family: 宋体;\">随着大数据、人工智能、移动互联网、云计算、区块链、物联网等新一代信息技术的蓬勃发展，对全球经济发展、社会进步、人民生活带来重大而深远的影响，也对财务管理理论与实务带来了前所未有的挑战。因此，我们必须把握好数字化、网络化、智能化的发展机遇，充分吸收新技术赋予的新能量，及时实现财务转型，从业财资税独立运行向业财资税一体化转变，由管控型财务向赋能型财务转变，从守护价值向创造价值转变。</span></p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; text-indent: 32px; line-height: 24px;\"><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体; font-size: 16px;\">本课程在大智移云时代背景下，透析财务管理环境，探讨财务理论前沿，分享财务创新案例。内容共十章：高级财务管理概述；企业财务战略概论；企业并购与重组；内部控制与风险管理；价值链管理研究；企业集团财务管理；中小企业财务管理；国际财务管理；和谐财务管理。另外，分析了三个典型案例：1.不忘创新，方得始终：美的集团的价值生态模式演进；2.海尔人单合一商业模式创新探索；3.解密中兴：基于财务云的价值创造之路。</span></p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; text-indent: 32px; line-height: 24px;\"><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: 宋体; font-size: 16px;\">通过本课程的学习，一方面可以掌握高级财务管理的基本理论，另一方面，深入理解大智移云时代财务管理的创新案例。本课程的特色和亮点：一是设计内容新颖。本书根据近几年财务管理环境的重大变化，设计了智能财务、内部控制与风险管理、价值链管理研究、和谐财务管理、行为财务学等新的热点问题，有利于读者掌握财务管理研究的最新内容。二是习题案例丰富。为了便于教师教和学生学，我们每章开始简要列出本章重点内容，每章结尾有本章小结，关键术语，复习思考题和微型案例，便于老师提纲挈领，把握重点；学生领会内容，开拓思路。三是理论实务结合。在系统讲授高级财务管理理论的基础上，重视与实务问题的衔接。主要章节通过案例、例题说明理论在实务中的应用，尽可能做到理论与实务紧密结合。</span></p>\n</div>\n</div>', '2024-12-26 20:20:47', '100', '是');
INSERT INTO `kechengxinxi` VALUES ('9', '122620205286', '大数据解析与应用导论', '1', '/static/upload/b576b3f29062fd8e42eeeba370b16bd0.png', '“大数据分析”是时下炙手可热的概念，如何更好地理解数据', '<div class=\"category-title f-f0\" style=\"box-sizing: initial; margin: 0px; padding: 0px 0px 10px; outline: none; font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 18px; font-weight: bold; color: rgb(51, 51, 51); font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">&nbsp;<span class=\"f-ib f-vam\" style=\"box-sizing: initial; display: inline-block; zoom: 1; vertical-align: middle;\">课程概述</span></div>\n<div class=\"category-content j-cover-overflow\" style=\"box-sizing: initial; margin: 0px 0px 50px; padding: 0px; outline: none; position: relative; color: rgb(51, 51, 51); font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">\n<div class=\"f-richEditorText\" style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; border: 0px; text-align: left; word-break: break-word; overflow-wrap: break-word; font: 12px / 22px \'Helvetica Neue\', Helvetica, Arial, sans-serif; color: rgb(102, 102, 102); white-space: pre-wrap;\">\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\"><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: SimSun; font-size: 13px;\">&ldquo;大数据&rdquo;这个概念几乎应用到了所有人类智力与发展的领域中。《大数据时代》这本书中有一句话：人类从依靠自身判断做决定到依靠数据做决定的转变，也是大数据作出的最大贡献之一。本课程从大数据解析的基本概念讲起，进而介绍大数据解析中常用的基础算法，包括数据预处理相关算法、判别分析、回归分析、聚类分析、决策树、典型相关分析、神经网络、自编码器和集成学习等，同时结合具体应用，帮助同学们深入学习数据挖掘的模型与方法，掌握大数据解析的钥匙，为各行业特别是工业大数据赋能。希望大家在学习的过程中，能够了解和认识到：本课程是一门实战性很强的基础课程，纸上得来终觉浅，绝知此事要躬行；抓准具体对象本身的特点、特性和问题，以问题驱动，而非以方法为导向，不要哪个方法热，追逐哪个，切忌脱离问题空谈花哨的方法；活用数据，不要迷信数据以及被数据绑架。</span></p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\"><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: SimSun; font-size: 13px;\">本课程的特色主要包括：</span></p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\"><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: SimSun; font-size: 13px;\">（</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Helvetica Neue\'; font-size: 13px;\">1</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: SimSun; font-size: 13px;\">）本课程讲授大数据分析的基本原理、相关方法和实例分析，让学生能够形成大数据思维意识，加深对课程知识的理解。</span></p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\"><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: SimSun; font-size: 13px;\">（</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Helvetica Neue\'; font-size: 13px;\">2</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: SimSun; font-size: 13px;\">）课程中介绍了大量的大数据应用案例，这些案例包括但不限于工业领域，为大家提供不同学科方向的思考和启发。</span></p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\"><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: SimSun; font-size: 13px;\">（</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: \'Helvetica Neue\'; font-size: 13px;\">3</span><span style=\"box-sizing: initial; overflow-wrap: break-word; white-space: pre-wrap; font-family: SimSun; font-size: 13px;\">）课程之余鼓励学生主动发现和思考生活中的大数据场景，将课程内容与实际紧密结合。</span></p>\n</div>\n</div>', '2024-12-26 20:21:08', '100', '是');
INSERT INTO `kechengxinxi` VALUES ('10', '12262021485', '算法设计与分析', '1', '/static/upload/cabb647c7f9b3421e22cd586545d955a.png', '物皆数，万事皆算。人之智慧，遵循万物之法则', '<div class=\"category-title f-f0\" style=\"box-sizing: initial; margin: 0px; padding: 0px 0px 10px; outline: none; font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 18px; font-weight: bold; color: rgb(51, 51, 51); font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">&nbsp;<span class=\"f-ib f-vam\" style=\"box-sizing: initial; display: inline-block; zoom: 1; vertical-align: middle;\">课程概述</span></div>\n<div class=\"category-content j-cover-overflow\" style=\"box-sizing: initial; margin: 0px 0px 50px; padding: 0px; outline: none; position: relative; color: rgb(51, 51, 51); font-family: \'Microsoft YaHei\', 微软雅黑, Helvetica, \'sans-serif\'; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">\n<div class=\"f-richEditorText\" style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none; border: 0px; text-align: left; word-break: break-word; overflow-wrap: break-word; font: 12px / 22px \'Helvetica Neue\', Helvetica, Arial, sans-serif; color: rgb(102, 102, 102); white-space: pre-wrap;\">\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\">1.为什么要学习《算法设计与分析》？该课程是计算机学科中处于核心地位的专业基础课，面向计算机类本科生，覆盖计算机科学与技术、物联网工程、软件工程、人工智能等专业。</p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\">&nbsp;</p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\">2.课程的主题是什么？学习以尽量少的计算资源来求解问题的计算机算法。</p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\">&nbsp;</p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\">3.学习这门课程可以获得什么？通过本课程的系统性学习，可以掌握递归与分治、动态规划、贪心、回溯、分支限界这些经典算法设计策略的核心思想及其相互关联，具备分析算法计算复杂性的理论知识，建立通过算法来减少时间和空间复杂性的计算思维。</p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\">&nbsp;</p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\">4.这门课有什么特色？（1）你看不到任何代码，真的、伪的都没有，只有方程或函数。是的，我们只分析算法最原始的初等数学的本质。（2）你所看到的方程或函数是如何在计算机上算数的？在你开始各种编程的语言的coding之前，我们先回归到抽象但强大的计算模型上，只有理解了算法是如何在有限状态自动机、图灵机、递归等计算模型上运行的，才能真正理解算法的本质，这也是区分计算机专业和非计算机专业的标志之一。（3）每一个经典问题都有它的前世今生，经典不是陈旧，而是永恒。我们不会止步于20世纪某一年的某个算法，而是对于同一个问题沿着它的时间线贯穿算法演化的脉络，教材之外，我们还有源源不断的论文来一同分享，一同震撼。</p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\">&nbsp;</p>\n<p style=\"box-sizing: initial; margin: 0px; padding: 0px; outline: none;\">5.ALGORITHM = All Get Open Really In The Math. 你准备好了吗？</p>\n</div>\n</div>', '2024-12-26 20:21:31', '100', '是');

-- ----------------------------
-- Table structure for `kechengxuexi`
-- ----------------------------
DROP TABLE IF EXISTS `kechengxuexi`;
CREATE TABLE `kechengxuexi` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `kechengxinxiid` int(10) unsigned NOT NULL COMMENT '课程信息id',
  `kechengbianhao` varchar(50) NOT NULL COMMENT '课程编号',
  `kechengmingcheng` varchar(255) NOT NULL COMMENT '课程名称',
  `kechengfenlei` int(10) unsigned NOT NULL COMMENT '课程分类',
  `fabujiaoshi` varchar(50) NOT NULL COMMENT '发布教师',
  `xuexibianhao` varchar(50) NOT NULL COMMENT '学习编号',
  `xuexijindu` int(11) NOT NULL DEFAULT '0' COMMENT '学习进度',
  `xueshengyonghu` varchar(50) NOT NULL COMMENT '学生用户',
  `xuexizhuangtai` varchar(50) NOT NULL COMMENT '学习状态',
  `addtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '学习时间',
  PRIMARY KEY (`id`),
  KEY `kechengxuexi_kechengxinxiid_index` (`kechengxinxiid`),
  KEY `kechengxuexi_kechengfenlei_index` (`kechengfenlei`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COMMENT='课程学习';

-- ----------------------------
-- Records of kechengxuexi
-- ----------------------------
INSERT INTO `kechengxuexi` VALUES ('1', '9', '122620205286', '大数据解析与应用导论', '1', '100', '122919079380', '100', '002', '已完成', '2024-12-29 19:07:43');
INSERT INTO `kechengxuexi` VALUES ('2', '8', '122620201377', '高级财务管理', '2', '100', '122919157879', '100', '002', '已完成', '2024-12-29 19:15:36');
INSERT INTO `kechengxuexi` VALUES ('3', '9', '122620205286', '大数据解析与应用导论', '1', '100', '12302111947', '100', '002', '已完成', '2024-12-30 21:11:34');
INSERT INTO `kechengxuexi` VALUES ('4', '10', '12262021485', '算法设计与分析', '1', '100', '123023204525', '100', '003', '已完成', '2024-12-30 23:20:51');

-- ----------------------------
-- Table structure for `kechengziyuan`
-- ----------------------------
DROP TABLE IF EXISTS `kechengziyuan`;
CREATE TABLE `kechengziyuan` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `kechengxinxiid` int(10) unsigned NOT NULL COMMENT '课程信息id',
  `kechengbianhao` varchar(50) NOT NULL COMMENT '课程编号',
  `kechengmingcheng` varchar(255) NOT NULL COMMENT '课程名称',
  `kechengfenlei` int(10) unsigned NOT NULL COMMENT '课程分类',
  `fabujiaoshi` varchar(50) NOT NULL COMMENT '发布教师',
  `ziyuanmingcheng` varchar(255) NOT NULL COMMENT '资源名称',
  `ziyuanfujian` varchar(255) NOT NULL COMMENT '资源附件',
  `ziyuanshuoming` longtext NOT NULL COMMENT '资源说明',
  `addtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
  PRIMARY KEY (`id`),
  KEY `kechengziyuan_kechengxinxiid_index` (`kechengxinxiid`),
  KEY `kechengziyuan_kechengfenlei_index` (`kechengfenlei`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COMMENT='课程资源';

-- ----------------------------
-- Records of kechengziyuan
-- ----------------------------
INSERT INTO `kechengziyuan` VALUES ('1', '10', '12262021485', '算法设计与分析', '1', '100', '算法设计资源1', '/static/upload/c272437989c6f5dd540751242dc3586b.jpg', '<p><span style=\"color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;\">《算法设计与分析》系统地介绍了算法设计与分析的概念和方法，共4篇内容。1篇介绍算法设计与分析的基本概念，结合穷举法、排序问题及其他一些算法，对算法的时间复杂性的概念及复杂性的分析方法作了较为详细的叙述；2篇以算法设计技术为纲，从合并排序、堆排序、离散集合的union和find作开始，进而介绍递归技术、分治法、贪婪法、动态规划、回溯法、分支与限界法和算法等算法设计技术及其复杂性分析；3篇介绍计算机应用领域里的一些算法，如图和网络流，以及计算几何中的一些问题；4篇介绍算法设计与分析中的一些理论问题，如NP完全问题、计算复杂性问题、下界理论问题，后介绍近似算法及其性能分析。《算法设计与分析》内容选材适当、编排合理、由浅入深、循序渐进、互相衔接、逐步展开，并附有大量实例，既注重算法的思想方法、推导过程和正确性的证明技术，也注重算法所涉及的数据结构、算法的具体实现和算法的工作过程。《算法设计与分析》可作为高等院校计算机专业本科生和研究生的教材，也可作为计算机科学与应用的科学技术人员的参考资料。</span></p>', '2024-12-29 19:45:56');
INSERT INTO `kechengziyuan` VALUES ('2', '10', '12262021485', '算法设计与分析', '1', '100', '算法设计资源2', '/static/upload/c272437989c6f5dd540751242dc3586b.jpg', '<p><span style=\"color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;\">《算法设计与分析》系统地介绍了算法设计与分析的概念和方法，共4篇内容。1篇介绍算法设计与分析的基本概念，结合穷举法、排序问题及其他一些算法，对算法的时间复杂性的概念及复杂性的分析方法作了较为详细的叙述；2篇以算法设计技术为纲，从合并排序、堆排序、离散集合的union和find作开始，进而介绍递归技术、分治法、贪婪法、动态规划、回溯法、分支与限界法和算法等算法设计技术及其复杂性分析；3篇介绍计算机应用领域里的一些算法，如图和网络流，以及计算几何中的一些问题；4篇介绍算法设计与分析中的一些理论问题，如NP完全问题、计算复杂性问题、下界理论问题，后介绍近似算法及其性能分析。《算法设计与分析》内容选材适当、编排合理、由浅入深、循序渐进、互相衔接、逐步展开，并附有大量实例，既注重算法的思想方法、推导过程和正确性的证明技术，也注重算法所涉及的数据结构、算法的具体实现和算法的工作过程。《算法设计与分析》可作为高等院校计算机专业本科生和研究生的教材，也可作为计算机科学与应用的科学技术人员的参考资料。</span></p>', '2024-12-29 19:46:08');
INSERT INTO `kechengziyuan` VALUES ('3', '8', '122620201377', '高级财务管理', '2', '100', '高级财务资源1', '/static/upload/c272437989c6f5dd540751242dc3586b.jpg', '<p><span style=\"color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;\">《算法设计与分析》系统地介绍了算法设计与分析的概念和方法，共4篇内容。1篇介绍算法设计与分析的基本概念，结合穷举法、排序问题及其他一些算法，对算法的时间复杂性的概念及复杂性的分析方法作了较为详细的叙述；2篇以算法设计技术为纲，从合并排序、堆排序、离散集合的union和find作开始，进而介绍递归技术、分治法、贪婪法、动态规划、回溯法、分支与限界法和算法等算法设计技术及其复杂性分析；3篇介绍计算机应用领域里的一些算法，如图和网络流，以及计算几何中的一些问题；4篇介绍算法设计与分析中的一些理论问题，如NP完全问题、计算复杂性问题、下界理论问题，后介绍近似算法及其性能分析。《算法设计与分析》内容选材适当、编排合理、由浅入深、循序渐进、互相衔接、逐步展开，并附有大量实例，既注重算法的思想方法、推导过程和正确性的证明技术，也注重算法所涉及的数据结构、算法的具体实现和算法的工作过程。《算法设计与分析》可作为高等院校计算机专业本科生和研究生的教材，也可作为计算机科学与应用的科学技术人员的参考资料。</span></p>', '2024-12-29 19:47:00');
INSERT INTO `kechengziyuan` VALUES ('4', '8', '122620201377', '高级财务管理', '2', '100', '高级财务资源2', '/static/upload/c272437989c6f5dd540751242dc3586b.jpg', '<p><span style=\"color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;\">《算法设计与分析》系统地介绍了算法设计与分析的概念和方法，共4篇内容。1篇介绍算法设计与分析的基本概念，结合穷举法、排序问题及其他一些算法，对算法的时间复杂性的概念及复杂性的分析方法作了较为详细的叙述；2篇以算法设计技术为纲，从合并排序、堆排序、离散集合的union和find作开始，进而介绍递归技术、分治法、贪婪法、动态规划、回溯法、分支与限界法和算法等算法设计技术及其复杂性分析；3篇介绍计算机应用领域里的一些算法，如图和网络流，以及计算几何中的一些问题；4篇介绍算法设计与分析中的一些理论问题，如NP完全问题、计算复杂性问题、下界理论问题，后介绍近似算法及其性能分析。《算法设计与分析》内容选材适当、编排合理、由浅入深、循序渐进、互相衔接、逐步展开，并附有大量实例，既注重算法的思想方法、推导过程和正确性的证明技术，也注重算法所涉及的数据结构、算法的具体实现和算法的工作过程。《算法设计与分析》可作为高等院校计算机专业本科生和研究生的教材，也可作为计算机科学与应用的科学技术人员的参考资料。</span></p>', '2024-12-29 19:47:13');
INSERT INTO `kechengziyuan` VALUES ('5', '9', '122620205286', '大数据解析与应用导论', '1', '100', ' 大数据解析资源1', '/static/upload/c272437989c6f5dd540751242dc3586b.jpg', '<p><span style=\"color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;\">《算法设计与分析》系统地介绍了算法设计与分析的概念和方法，共4篇内容。1篇介绍算法设计与分析的基本概念，结合穷举法、排序问题及其他一些算法，对算法的时间复杂性的概念及复杂性的分析方法作了较为详细的叙述；2篇以算法设计技术为纲，从合并排序、堆排序、离散集合的union和find作开始，进而介绍递归技术、分治法、贪婪法、动态规划、回溯法、分支与限界法和算法等算法设计技术及其复杂性分析；3篇介绍计算机应用领域里的一些算法，如图和网络流，以及计算几何中的一些问题；4篇介绍算法设计与分析中的一些理论问题，如NP完全问题、计算复杂性问题、下界理论问题，后介绍近似算法及其性能分析。《算法设计与分析》内容选材适当、编排合理、由浅入深、循序渐进、互相衔接、逐步展开，并附有大量实例，既注重算法的思想方法、推导过程和正确性的证明技术，也注重算法所涉及的数据结构、算法的具体实现和算法的工作过程。《算法设计与分析》可作为高等院校计算机专业本科生和研究生的教材，也可作为计算机科学与应用的科学技术人员的参考资料。</span></p>', '2024-12-29 19:47:35');
INSERT INTO `kechengziyuan` VALUES ('6', '9', '122620205286', '大数据解析与应用导论', '1', '100', ' 大数据解析资源2', '/static/upload/c272437989c6f5dd540751242dc3586b.jpg', '<p><span style=\"color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;\">《算法设计与分析》系统地介绍了算法设计与分析的概念和方法，共4篇内容。1篇介绍算法设计与分析的基本概念，结合穷举法、排序问题及其他一些算法，对算法的时间复杂性的概念及复杂性的分析方法作了较为详细的叙述；2篇以算法设计技术为纲，从合并排序、堆排序、离散集合的union和find作开始，进而介绍递归技术、分治法、贪婪法、动态规划、回溯法、分支与限界法和算法等算法设计技术及其复杂性分析；3篇介绍计算机应用领域里的一些算法，如图和网络流，以及计算几何中的一些问题；4篇介绍算法设计与分析中的一些理论问题，如NP完全问题、计算复杂性问题、下界理论问题，后介绍近似算法及其性能分析。《算法设计与分析》内容选材适当、编排合理、由浅入深、循序渐进、互相衔接、逐步展开，并附有大量实例，既注重算法的思想方法、推导过程和正确性的证明技术，也注重算法所涉及的数据结构、算法的具体实现和算法的工作过程。《算法设计与分析》可作为高等院校计算机专业本科生和研究生的教材，也可作为计算机科学与应用的科学技术人员的参考资料。</span></p>', '2024-12-29 19:47:43');
INSERT INTO `kechengziyuan` VALUES ('7', '11', '123023164203', '信息信息', '5', '100', '信息信息', '/static/upload/44203120ab6dce69763e78c510345f74.webp', '<p><img src=\"http://127.0.0.1:8006/static/upload/9d1fa3ebd40e3f22bfa44e195ac2d00f.png\"></p>', '2024-12-30 23:16:50');

-- ----------------------------
-- Table structure for `lunbotu`
-- ----------------------------
DROP TABLE IF EXISTS `lunbotu`;
CREATE TABLE `lunbotu` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL COMMENT '标题',
  `image` varchar(255) NOT NULL COMMENT '图片',
  `url` varchar(255) NOT NULL COMMENT '连接地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COMMENT='轮播图';

-- ----------------------------
-- Records of lunbotu
-- ----------------------------
INSERT INTO `lunbotu` VALUES ('1', '43', '/static/upload/9a662b049c96df333599c293a8628a14.png', '#');
INSERT INTO `lunbotu` VALUES ('2', '5', '/static/upload/e149ef0c813ce91c90e7422f66112a52.png', '#');
INSERT INTO `lunbotu` VALUES ('3', '6', '/static/upload/1b95c12069e74ec7254bf36a9ae06b87.png', '#');

-- ----------------------------
-- Table structure for `luntanfenlei`
-- ----------------------------
DROP TABLE IF EXISTS `luntanfenlei`;
CREATE TABLE `luntanfenlei` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `fenleimingcheng` varchar(255) NOT NULL COMMENT '分类名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COMMENT='论坛分类';

-- ----------------------------
-- Records of luntanfenlei
-- ----------------------------
INSERT INTO `luntanfenlei` VALUES ('1', '学习');
INSERT INTO `luntanfenlei` VALUES ('2', '交流');

-- ----------------------------
-- Table structure for `luntanjiaoliu`
-- ----------------------------
DROP TABLE IF EXISTS `luntanjiaoliu`;
CREATE TABLE `luntanjiaoliu` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `bianhao` varchar(50) NOT NULL COMMENT '编号',
  `biaoti` varchar(50) NOT NULL COMMENT '标题',
  `fenlei` int(10) unsigned NOT NULL COMMENT '分类',
  `tupian` varchar(255) NOT NULL COMMENT '图片',
  `huifushu` int(11) NOT NULL DEFAULT '0' COMMENT '回复数',
  `faburen` varchar(50) NOT NULL COMMENT '发布人',
  `hudongneirong` longtext NOT NULL COMMENT '互动内容',
  `quanxian` varchar(50) NOT NULL COMMENT '权限',
  `xingming` varchar(50) NOT NULL COMMENT '姓名',
  `touxiang` varchar(255) NOT NULL COMMENT '头像',
  `addtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
  `issh` varchar(10) NOT NULL DEFAULT '否' COMMENT '是否审核',
  PRIMARY KEY (`id`),
  KEY `luntanjiaoliu_fenlei_index` (`fenlei`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COMMENT='论坛交流';

-- ----------------------------
-- Records of luntanjiaoliu
-- ----------------------------
INSERT INTO `luntanjiaoliu` VALUES ('1', '122620331195', '社会文化的变化', '2', '/static/upload/da0ee2bc32c1a62cc1d17a2a4c11714c.png', '3', '001', '<p><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-text=\"true\">教育随着</span><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-text=\"true\"><a class=\"innerLink_S8kU6\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; color: rgb(19, 110, 194); text-decoration: none;\" href=\"https://baike.baidu.com/item/%E4%BA%BA%E7%B1%BB%E7%A4%BE%E4%BC%9A/3311270?fromModule=lemma_inlink\" target=\"_blank\" rel=\"noopener\" data-from-module=\"summary\">人类社会</a></span><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-text=\"true\">的产生而产生，又随着人类社会的发展而发展。在不同的历史阶段，由于</span><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-text=\"true\"><a class=\"innerLink_S8kU6\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; color: rgb(19, 110, 194); text-decoration: none;\" href=\"https://baike.baidu.com/item/%E7%94%9F%E4%BA%A7%E5%8A%9B/165852?fromModule=lemma_inlink\" target=\"_blank\" rel=\"noopener\" data-from-module=\"summary\">生产力</a></span><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-text=\"true\">发展水平的差异、政治</span><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-text=\"true\"><a class=\"innerLink_S8kU6\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; color: rgb(19, 110, 194); text-decoration: none;\" href=\"https://baike.baidu.com/item/%E7%BB%8F%E6%B5%8E%E5%88%B6%E5%BA%A6/3388162?fromModule=lemma_inlink\" target=\"_blank\" rel=\"noopener\" data-from-module=\"summary\">经济制度</a></span><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-text=\"true\">的不同、</span><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-text=\"true\"><a class=\"innerLink_S8kU6\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; color: rgb(19, 110, 194); text-decoration: none;\" href=\"https://baike.baidu.com/item/%E7%A4%BE%E4%BC%9A%E6%96%87%E5%8C%96/1417739?fromModule=lemma_inlink\" target=\"_blank\" rel=\"noopener\" data-from-module=\"summary\">社会文化</a></span><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-text=\"true\">的变化，教育也具有不同的性质和特点。</span></p>', '学生', '小赖', '/static/upload/a4fc82aec5903f334b98d0e263082d6e.jpg', '2024-12-26 20:34:40', '是');
INSERT INTO `luntanjiaoliu` VALUES ('2', '122620344624', '从哲学认识论角度分析', '1', '/static/upload/8ff5c6dca39f38275f0823b187c49aa9.png', '2', '001', '<p><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-ctrid-tzilr40sinag=\"tZIlr40SInAG\" data-text=\"true\">教育的定义方式决定着教育的定义内容。从哲学</span><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-text=\"true\"><a class=\"innerLink_S8kU6\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; color: rgb(19, 110, 194); text-decoration: none;\" href=\"https://baike.baidu.com/item/%E8%AE%A4%E8%AF%86%E8%AE%BA/15082508?fromModule=lemma_inlink\" target=\"_blank\" rel=\"noopener\" data-from-module=\"\">认识论</a></span><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-text=\"true\">角度分析，教育的定义方式可以分为</span><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-text=\"true\"><a class=\"innerLink_S8kU6\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; color: rgb(19, 110, 194); text-decoration: none;\" href=\"https://baike.baidu.com/item/%E5%AE%9E%E5%9C%A8%E8%AE%BA/881244?fromModule=lemma_inlink\" target=\"_blank\" rel=\"noopener\" data-from-module=\"\">实在论</a></span><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-text=\"true\">定义方式和现象学定义方式。教育的实在论定义方式把教育当作一个已经完成的实体或存在者，教育定义是对实体的&ldquo;符合&rdquo;或趋近；教育的现象学定义方式把教育当作一个正在发生的存在，教育定义是定义者参与其中而生发出的对教育的认识。</span></p>', '学生', '小赖', '/static/upload/a4fc82aec5903f334b98d0e263082d6e.jpg', '2024-12-26 20:35:17', '是');
INSERT INTO `luntanjiaoliu` VALUES ('3', '122620344624', '一是对人类来讲', '1', '/static/upload/c3dde2c6d2622e9f468ca4dddb7e2bbe.png', '0', '001', '<p><span style=\"color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; display: inline !important; float: none;\">教育的本质与作用可概括为三个方面：一是对人类来讲，教育的作用是文化和价值观念的传承与发展;二是对一个国家来说，办教育的目的是提高国民素质，为国家建设提供人力资源保障，增强国家竞争力;三是对受教育者个人而言，接受教育主要是为了追求人生幸福，包括精神的和物质的。</span></p>', '学生', '小赖', '/static/upload/a4fc82aec5903f334b98d0e263082d6e.jpg', '2024-12-26 20:35:40', '是');
INSERT INTO `luntanjiaoliu` VALUES ('4', '122620355276', '社会需求', '2', '/static/upload/78e1ff137935278e3caebe662f17bb4a.png', '4', '001', '<p><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-ctrid-u0gsckrxv3wu=\"u0GSCKrXv3wu\" data-text=\"true\">教育具有</span><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-text=\"true\"><a class=\"innerLink_S8kU6\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; color: rgb(19, 110, 194); text-decoration: none;\" href=\"https://baike.baidu.com/item/%E6%88%90%E9%95%BF/15564?fromModule=lemma_inlink\" target=\"_blank\" rel=\"noopener\" data-from-module=\"\">成长</a></span><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-text=\"true\">和</span><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-text=\"true\"><a class=\"innerLink_S8kU6\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; color: rgb(19, 110, 194); text-decoration: none;\" href=\"https://baike.baidu.com/item/%E7%AD%9B%E9%80%89/10883707?fromModule=lemma_inlink\" target=\"_blank\" rel=\"noopener\" data-from-module=\"\">筛选</a></span><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-text=\"true\">双重作用。孩子长大是一个自然的过程，成长是回避不了的议题，正确的方向是健康成长；而</span><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-text=\"true\"><a class=\"innerLink_S8kU6\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; color: rgb(19, 110, 194); text-decoration: none;\" href=\"https://baike.baidu.com/item/%E6%95%99%E8%82%B2%E8%B5%84%E6%BA%90/2502081?fromModule=lemma_inlink\" target=\"_blank\" rel=\"noopener\" data-from-module=\"\">教育资源</a></span><span class=\"text_QZdcK\" style=\"box-sizing: content-box; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; margin: 0px; padding: 0px; position: relative; color: rgb(51, 51, 51); font-family: \'Helvetica Neue\', Helvetica, Arial, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', \'WenQuanYi Micro Hei\', sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 28px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\" data-text=\"true\">是有限的，人是有差异的，因此又具有相应的筛选功能。实施义务教育的目的，就是让所有儿童都能够在符合育人规律的条件下成长，为未来满足基本的社会需求服务。</span></p>', '学生', '小赖', '/static/upload/a4fc82aec5903f334b98d0e263082d6e.jpg', '2024-12-26 20:35:59', '是');

-- ----------------------------
-- Table structure for `shoucang`
-- ----------------------------
DROP TABLE IF EXISTS `shoucang`;
CREATE TABLE `shoucang` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL COMMENT '用户',
  `xwid` int(11) NOT NULL DEFAULT '0' COMMENT '关联表id',
  `biao` varchar(50) NOT NULL COMMENT '关联表',
  `biaoti` varchar(255) NOT NULL COMMENT '标题',
  `addtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COMMENT='收藏';

-- ----------------------------
-- Records of shoucang
-- ----------------------------
INSERT INTO `shoucang` VALUES ('3', '002', '9', 'kechengxinxi', '大数据解析与应用导论', '2024-12-29 19:06:11');
INSERT INTO `shoucang` VALUES ('4', '001', '10', 'kechengxinxi', '算法设计与分析', '2024-12-29 19:52:00');
INSERT INTO `shoucang` VALUES ('5', '999', '10', 'kechengxinxi', '算法设计与分析', '2024-12-29 20:04:44');
INSERT INTO `shoucang` VALUES ('6', '003', '3', 'kechengxinxi', '药物分析', '2024-12-30 23:21:39');

-- ----------------------------
-- Table structure for `siliao`
-- ----------------------------
DROP TABLE IF EXISTS `siliao`;
CREATE TABLE `siliao` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `bianhao` varchar(50) NOT NULL COMMENT '编号',
  `shouxinren` varchar(50) NOT NULL COMMENT '收信人',
  `faxinren` varchar(50) NOT NULL COMMENT '发信人',
  `addtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '消息最后时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COMMENT='私聊';

-- ----------------------------
-- Records of siliao
-- ----------------------------
INSERT INTO `siliao` VALUES ('1', '2412292177849', '100', '999', '2024-12-29 21:35:53');
INSERT INTO `siliao` VALUES ('4', '2412302396944', '100', '001', '2024-12-30 23:09:52');
INSERT INTO `siliao` VALUES ('5', '2412302358630', '100', '003', '2024-12-30 23:23:18');

-- ----------------------------
-- Table structure for `tijiaozuoye`
-- ----------------------------
DROP TABLE IF EXISTS `tijiaozuoye`;
CREATE TABLE `tijiaozuoye` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `buzhizuoyeid` int(10) unsigned NOT NULL COMMENT '布置作业id',
  `kechengbianhao` varchar(50) NOT NULL COMMENT '课程编号',
  `kechengmingcheng` varchar(255) NOT NULL COMMENT '课程名称',
  `kechengfenlei` int(10) unsigned NOT NULL COMMENT '课程分类',
  `fabujiaoshi` varchar(50) NOT NULL COMMENT '发布教师',
  `zuoyebianhao` varchar(50) NOT NULL COMMENT '作业编号',
  `zuoyemingcheng` varchar(255) NOT NULL COMMENT '作业名称',
  `zuoyefujian` varchar(255) NOT NULL COMMENT '作业附件',
  `xueshengxingming` varchar(50) NOT NULL COMMENT '学生姓名',
  `zuoyezhuangtai` varchar(50) NOT NULL COMMENT '作业状态',
  `tijiaoxuesheng` varchar(50) NOT NULL COMMENT '提交学生',
  `addtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
  PRIMARY KEY (`id`),
  KEY `tijiaozuoye_buzhizuoyeid_index` (`buzhizuoyeid`),
  KEY `tijiaozuoye_kechengfenlei_index` (`kechengfenlei`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COMMENT='提交作业';

-- ----------------------------
-- Records of tijiaozuoye
-- ----------------------------
INSERT INTO `tijiaozuoye` VALUES ('1', '1', '12262021485', '算法设计与分析', '1', '100', '122919471367', ' 算法设计作业1', '/static/upload/c272437989c6f5dd540751242dc3586b.jpg', '张杰', '已批阅', '999', '2024-12-29 20:01:02');
INSERT INTO `tijiaozuoye` VALUES ('2', '1', '12262021485', '算法设计与分析', '1', '100', '122919471367', ' 算法设计作业1', '/static/upload/c272437989c6f5dd540751242dc3586b.jpg', '小洛克', '已批阅', '003', '2024-12-30 23:20:49');

-- ----------------------------
-- Table structure for `wenda`
-- ----------------------------
DROP TABLE IF EXISTS `wenda`;
CREATE TABLE `wenda` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `tiwenneirong` varchar(255) NOT NULL COMMENT '提问内容',
  `jiansuoleixing` varchar(50) NOT NULL COMMENT '检索类型',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='问答';

-- ----------------------------
-- Records of wenda
-- ----------------------------
INSERT INTO `wenda` VALUES ('1', '你好', '模糊');
INSERT INTO `wenda` VALUES ('2', '你是谁', '精准');
INSERT INTO `wenda` VALUES ('3', '怎么学会', '模糊');
INSERT INTO `wenda` VALUES ('4', '小智同学', '模糊');
INSERT INTO `wenda` VALUES ('5', '好厉害', '模糊');
INSERT INTO `wenda` VALUES ('6', '你好厉害', '模糊');

-- ----------------------------
-- Table structure for `wendaxiaoxi`
-- ----------------------------
DROP TABLE IF EXISTS `wendaxiaoxi`;
CREATE TABLE `wendaxiaoxi` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `xiaoxineirong` text NOT NULL COMMENT '消息内容',
  `huifuneirong` text NOT NULL COMMENT '回复内容',
  `guanlianhuifu` int(10) unsigned NOT NULL COMMENT '关联回复',
  `yonghu` varchar(50) NOT NULL COMMENT '用户',
  `addtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `wendaxiaoxi_guanlianhuifu_index` (`guanlianhuifu`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='问答消息';

-- ----------------------------
-- Records of wendaxiaoxi
-- ----------------------------
INSERT INTO `wendaxiaoxi` VALUES ('1', 'fff', '我还没学会怎么回答呢', '0', '001', '2024-04-22 06:04:01');
INSERT INTO `wendaxiaoxi` VALUES ('2', '11', '我还没学会怎么回答呢', '0', '001', '2024-04-22 06:04:32');
INSERT INTO `wendaxiaoxi` VALUES ('3', '111', '我还没学会怎么回答呢', '0', '001', '2024-04-22 06:04:47');
INSERT INTO `wendaxiaoxi` VALUES ('4', 'fff', '我还没学会怎么回答呢', '0', '001', '2024-04-22 06:05:04');
INSERT INTO `wendaxiaoxi` VALUES ('5', '112', '我还没学会怎么回答呢', '0', '001', '2024-04-22 06:05:56');
INSERT INTO `wendaxiaoxi` VALUES ('6', 'a', '我还没学会怎么回答呢', '0', '001', '2024-04-22 06:06:00');
INSERT INTO `wendaxiaoxi` VALUES ('7', '你好', '你好！', '7', '001', '2024-04-22 06:11:13');
INSERT INTO `wendaxiaoxi` VALUES ('8', '你好', '你好啊，我是小智，欢迎使用智能学习助手', '1', '001', '2024-04-22 06:11:54');
INSERT INTO `wendaxiaoxi` VALUES ('9', '你好', '我是小智，用的很不错', '2', '001', '2024-04-22 06:12:31');
INSERT INTO `wendaxiaoxi` VALUES ('10', '你好', '你好！', '7', '001', '2024-04-22 06:12:33');
INSERT INTO `wendaxiaoxi` VALUES ('11', '你好', '你好啊，我是小智，欢迎使用智能学习助手', '1', '001', '2024-04-22 06:12:37');
INSERT INTO `wendaxiaoxi` VALUES ('12', '怎么买学会', '我还没学会怎么回答呢', '0', '001', '2024-04-22 06:12:42');
INSERT INTO `wendaxiaoxi` VALUES ('13', '怎么学会', '不用学会', '6', '001', '2024-04-22 06:12:47');
INSERT INTO `wendaxiaoxi` VALUES ('14', 'ni ha', '我还没学会怎么回答呢', '0', '001', '2024-04-22 06:14:09');
INSERT INTO `wendaxiaoxi` VALUES ('15', '你好啊', '我还没学会怎么回答呢', '0', '001', '2024-04-22 06:14:14');
INSERT INTO `wendaxiaoxi` VALUES ('16', '你好', '我是小智，用的很不错', '2', '001', '2024-04-22 06:14:30');
INSERT INTO `wendaxiaoxi` VALUES ('17', '你好啊小智', '我还没学会怎么回答呢', '0', '001', '2024-04-22 06:14:35');
INSERT INTO `wendaxiaoxi` VALUES ('18', '你好', '我是小智，用的很不错', '2', '001', '2024-04-22 06:20:32');
INSERT INTO `wendaxiaoxi` VALUES ('19', '你好', '你好！', '7', '001', '2024-04-22 06:20:35');
INSERT INTO `wendaxiaoxi` VALUES ('20', '你很厉害噢', '我还没学会怎么回答呢', '0', '001', '2024-04-22 06:20:41');
INSERT INTO `wendaxiaoxi` VALUES ('21', '厉害哦', '我还没学会怎么回答呢', '0', '001', '2024-04-22 06:20:50');
INSERT INTO `wendaxiaoxi` VALUES ('22', '厉害', '一般一般，世界第三', '11', '001', '2024-04-22 06:20:53');
INSERT INTO `wendaxiaoxi` VALUES ('23', '小智同学', '我还没学会怎么回答呢', '0', 'None', '2024-12-30 22:58:07');
INSERT INTO `wendaxiaoxi` VALUES ('24', '小智', '我还没学会怎么回答呢', '0', 'None', '2024-12-30 22:58:34');
INSERT INTO `wendaxiaoxi` VALUES ('25', '小智', '我还没学会怎么回答呢', '0', 'None', '2024-12-30 22:58:52');
INSERT INTO `wendaxiaoxi` VALUES ('26', '小智', '我还没学会怎么回答呢', '0', 'None', '2024-12-30 23:00:22');
INSERT INTO `wendaxiaoxi` VALUES ('27', '小智', '我还没学会怎么回答呢', '0', 'None', '2024-12-30 23:01:05');
INSERT INTO `wendaxiaoxi` VALUES ('28', '你是谁', '好好学习吧，别问我啦', '5', 'None', '2024-12-30 23:02:20');
INSERT INTO `wendaxiaoxi` VALUES ('29', '你是谁', '我是你', '4', 'None', '2024-12-30 23:02:23');
INSERT INTO `wendaxiaoxi` VALUES ('30', '你是谁', '我是小智', '3', 'None', '2024-12-30 23:02:26');
INSERT INTO `wendaxiaoxi` VALUES ('31', '小智', '我还没学会怎么回答呢', '0', 'admin', '2024-12-30 23:12:03');
INSERT INTO `wendaxiaoxi` VALUES ('32', '小智同学', '我还没学会怎么回答呢', '0', 'admin', '2024-12-30 23:12:13');
INSERT INTO `wendaxiaoxi` VALUES ('33', '你好', '你好啊，我是小智，欢迎使用智能学习助手', '1', 'admin', '2024-12-30 23:12:28');
INSERT INTO `wendaxiaoxi` VALUES ('34', '小智', '我还没学会怎么回答呢', '0', 'admin', '2024-12-30 23:15:23');
INSERT INTO `wendaxiaoxi` VALUES ('35', '你好', '你好！', '7', 'admin', '2024-12-30 23:15:26');
INSERT INTO `wendaxiaoxi` VALUES ('36', '你好', '我是小智，用的很不错', '2', '001', '2024-12-30 23:17:26');
INSERT INTO `wendaxiaoxi` VALUES ('37', '你好', '谢谢', '14', '100', '2024-12-30 23:22:02');

-- ----------------------------
-- Table structure for `xiaoxi`
-- ----------------------------
DROP TABLE IF EXISTS `xiaoxi`;
CREATE TABLE `xiaoxi` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `siliaoid` int(10) unsigned NOT NULL COMMENT '私聊id',
  `bianhao` varchar(50) NOT NULL COMMENT '编号',
  `neirong` longtext NOT NULL COMMENT '内容',
  `fasongren` varchar(50) NOT NULL COMMENT '发送人',
  `fasongshijian` varchar(25) NOT NULL COMMENT '发送时间',
  `shifouzhakan` varchar(50) NOT NULL COMMENT '是否查看',
  PRIMARY KEY (`id`),
  KEY `xiaoxi_siliaoid_index` (`siliaoid`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COMMENT='消息';

-- ----------------------------
-- Records of xiaoxi
-- ----------------------------
INSERT INTO `xiaoxi` VALUES ('1', '1', '', '你好', '999', '2024-12-29 21:35:07', '是');
INSERT INTO `xiaoxi` VALUES ('2', '1', '', '你好', '999', '2024-12-29 21:35:20', '是');
INSERT INTO `xiaoxi` VALUES ('3', '1', '', '你好', '999', '2024-12-29 21:35:21', '是');
INSERT INTO `xiaoxi` VALUES ('4', '1', '', '你好', '100', '2024-12-29 21:35:47', '是');
INSERT INTO `xiaoxi` VALUES ('5', '1', '', '你好', '100', '2024-12-29 21:35:53', '是');
INSERT INTO `xiaoxi` VALUES ('6', '4', '', '你好', '001', '2024-12-30 23:09:27', '是');
INSERT INTO `xiaoxi` VALUES ('7', '4', '', '你好', '001', '2024-12-30 23:09:29', '是');
INSERT INTO `xiaoxi` VALUES ('8', '4', '', '漫画', '100', '2024-12-30 23:09:52', '否');
INSERT INTO `xiaoxi` VALUES ('9', '5', '', '你好', '003', '2024-12-30 23:20:58', '是');
INSERT INTO `xiaoxi` VALUES ('10', '5', '', '你好', '003', '2024-12-30 23:20:59', '是');
INSERT INTO `xiaoxi` VALUES ('11', '5', '', '没回你好', '100', '2024-12-30 23:21:55', '是');
INSERT INTO `xiaoxi` VALUES ('12', '5', '', '漫画', '100', '2024-12-30 23:23:18', '是');

-- ----------------------------
-- Table structure for `xuesheng`
-- ----------------------------
DROP TABLE IF EXISTS `xuesheng`;
CREATE TABLE `xuesheng` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `xuehao` varchar(50) NOT NULL COMMENT '学号',
  `mima` varchar(50) NOT NULL COMMENT '密码',
  `xingming` varchar(50) NOT NULL COMMENT '姓名',
  `xingbie` varchar(10) NOT NULL COMMENT '性别',
  `shouji` varchar(50) NOT NULL COMMENT '手机',
  `youxiang` varchar(50) NOT NULL COMMENT '邮箱',
  `shenfenzheng` varchar(50) NOT NULL COMMENT '身份证',
  `touxiang` varchar(255) NOT NULL COMMENT '头像',
  `issh` varchar(10) NOT NULL DEFAULT '否' COMMENT '是否审核',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COMMENT='学生';

-- ----------------------------
-- Records of xuesheng
-- ----------------------------
INSERT INTO `xuesheng` VALUES ('1', '001', '001', '小赖', '男', '16200000000', '11551@qq.com', '510421198706247567', '/static/upload/a4fc82aec5903f334b98d0e263082d6e.jpg', '是');
INSERT INTO `xuesheng` VALUES ('2', '002', '002', '小娜', '女', '16526000000', '15121@qq.com', '429021196902144384', '/static/upload/5d89086a778784b9574cdd9089d6efb2.jpg', '是');
INSERT INTO `xuesheng` VALUES ('3', '999', '999', '张杰', '男', '16526000000', '1511@qq.com', '429021196902144384', '/static/upload/a4fc82aec5903f334b98d0e263082d6e.jpg', '是');
INSERT INTO `xuesheng` VALUES ('4', '003', '003', '小洛克', '女', '16526200000', '154111@qq.com', '130731198205216488', '/static/upload/b0ec9e492f5178d34f01bc8db2ca49c9.jpg', '是');

-- ----------------------------
-- Table structure for `xuexijilu`
-- ----------------------------
DROP TABLE IF EXISTS `xuexijilu`;
CREATE TABLE `xuexijilu` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `kechengshipinid` int(10) unsigned NOT NULL COMMENT '课程视频id',
  `kechengbianhao` varchar(50) NOT NULL COMMENT '课程编号',
  `kechengmingcheng` varchar(255) NOT NULL COMMENT '课程名称',
  `kechengfenlei` int(10) unsigned NOT NULL COMMENT '课程分类',
  `fabujiaoshi` varchar(50) NOT NULL COMMENT '发布教师',
  `shipinmingcheng` varchar(255) NOT NULL COMMENT '视频名称',
  `xueshengyonghu` varchar(50) NOT NULL COMMENT '学生用户',
  `addtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '学习时间',
  PRIMARY KEY (`id`),
  KEY `xuexijilu_kechengshipinid_index` (`kechengshipinid`),
  KEY `xuexijilu_kechengfenlei_index` (`kechengfenlei`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COMMENT='学习记录';

-- ----------------------------
-- Records of xuexijilu
-- ----------------------------
INSERT INTO `xuexijilu` VALUES ('1', '7', '122620201377', '高级财务管理', '2', '100', '高级财务视频2', '002', '2024-12-30 21:24:27');
INSERT INTO `xuexijilu` VALUES ('2', '2', '12262021485', '算法设计与分析', '1', '100', ' 算法设计视频2', '003', '2024-12-30 23:22:40');
INSERT INTO `xuexijilu` VALUES ('3', '1', '12262021485', '算法设计与分析', '1', '100', '算法设计视频1', '003', '2024-12-30 23:22:51');

-- ----------------------------
-- Table structure for `xuexijindu`
-- ----------------------------
DROP TABLE IF EXISTS `xuexijindu`;
CREATE TABLE `xuexijindu` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `kechengxuexiid` int(10) unsigned NOT NULL COMMENT '课程学习id',
  `kechengbianhao` varchar(50) NOT NULL COMMENT '课程编号',
  `kechengmingcheng` varchar(255) NOT NULL COMMENT '课程名称',
  `kechengfenlei` int(10) unsigned NOT NULL COMMENT '课程分类',
  `xuexibianhao` varchar(50) NOT NULL COMMENT '学习编号',
  `fabujiaoshi` varchar(50) NOT NULL COMMENT '发布教师',
  `xueshengyonghu` varchar(50) NOT NULL COMMENT '学生用户',
  `xuexijindu` int(11) NOT NULL DEFAULT '0' COMMENT '学习进度',
  `addtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `xuexijindu_kechengxuexiid_index` (`kechengxuexiid`),
  KEY `xuexijindu_kechengfenlei_index` (`kechengfenlei`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COMMENT='学习进度';

-- ----------------------------
-- Records of xuexijindu
-- ----------------------------
INSERT INTO `xuexijindu` VALUES ('1', '1', '122620205286', '大数据解析与应用导论', '1', '122919079380', '100', '002', '50', '2024-12-29 19:15:10');
INSERT INTO `xuexijindu` VALUES ('9', '2', '122620201377', '高级财务管理', '2', '122919157879', '100', '002', '50', '2024-12-30 21:15:41');
INSERT INTO `xuexijindu` VALUES ('10', '2', '122620201377', '高级财务管理', '2', '122919157879', '100', '002', '55', '2024-12-30 21:17:05');
INSERT INTO `xuexijindu` VALUES ('11', '2', '122620201377', '高级财务管理', '2', '122919157879', '100', '002', '90', '2024-12-30 21:17:15');
INSERT INTO `xuexijindu` VALUES ('12', '2', '122620201377', '高级财务管理', '2', '122919157879', '100', '002', '100', '2024-12-30 21:17:20');
INSERT INTO `xuexijindu` VALUES ('13', '4', '12262021485', '算法设计与分析', '1', '123023204525', '100', '003', '50', '2024-12-30 23:21:10');
INSERT INTO `xuexijindu` VALUES ('14', '4', '12262021485', '算法设计与分析', '1', '123023204525', '100', '003', '60', '2024-12-30 23:21:15');
INSERT INTO `xuexijindu` VALUES ('15', '4', '12262021485', '算法设计与分析', '1', '123023204525', '100', '003', '70', '2024-12-30 23:21:19');
INSERT INTO `xuexijindu` VALUES ('16', '4', '12262021485', '算法设计与分析', '1', '123023204525', '100', '003', '100', '2024-12-30 23:21:23');

-- ----------------------------
-- Table structure for `youqinglianjie`
-- ----------------------------
DROP TABLE IF EXISTS `youqinglianjie`;
CREATE TABLE `youqinglianjie` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `wangzhanmingcheng` varchar(50) NOT NULL COMMENT '网站名称',
  `wangzhi` varchar(50) NOT NULL COMMENT '网址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COMMENT='友情链接';

-- ----------------------------
-- Records of youqinglianjie
-- ----------------------------
INSERT INTO `youqinglianjie` VALUES ('1', '百度', 'http://www.baidu.com');
INSERT INTO `youqinglianjie` VALUES ('2', '谷歌', 'http://www.google.cn');
INSERT INTO `youqinglianjie` VALUES ('3', '新浪', 'http://www.sina.com');
INSERT INTO `youqinglianjie` VALUES ('4', 'QQ', 'http://www.qq.com');
INSERT INTO `youqinglianjie` VALUES ('5', '网易', 'http://www.163.com');

-- ----------------------------
-- Table structure for `zuoyepiyue`
-- ----------------------------
DROP TABLE IF EXISTS `zuoyepiyue`;
CREATE TABLE `zuoyepiyue` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `tijiaozuoyeid` int(10) unsigned NOT NULL COMMENT '提交作业id',
  `kechengbianhao` varchar(50) NOT NULL COMMENT '课程编号',
  `kechengmingcheng` varchar(255) NOT NULL COMMENT '课程名称',
  `kechengfenlei` int(10) unsigned NOT NULL COMMENT '课程分类',
  `fabujiaoshi` varchar(50) NOT NULL COMMENT '发布教师',
  `zuoyemingcheng` varchar(255) NOT NULL COMMENT '作业名称',
  `zuoyefujian` varchar(255) NOT NULL COMMENT '作业附件',
  `xueshengxingming` varchar(50) NOT NULL COMMENT '学生姓名',
  `tijiaoxuesheng` varchar(50) NOT NULL COMMENT '提交学生',
  `fenshu` int(11) NOT NULL DEFAULT '0' COMMENT '分数',
  `pingyu` text NOT NULL COMMENT '评语',
  `addtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '批阅时间',
  PRIMARY KEY (`id`),
  KEY `zuoyepiyue_tijiaozuoyeid_index` (`tijiaozuoyeid`),
  KEY `zuoyepiyue_kechengfenlei_index` (`kechengfenlei`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COMMENT='作业批阅';

-- ----------------------------
-- Records of zuoyepiyue
-- ----------------------------
INSERT INTO `zuoyepiyue` VALUES ('1', '1', '12262021485', '算法设计与分析', '1', '100', ' 算法设计作业1', '/static/upload/c272437989c6f5dd540751242dc3586b.jpg', '张杰', '999', '88', '666', '2024-12-29 20:02:52');
INSERT INTO `zuoyepiyue` VALUES ('2', '2', '12262021485', '算法设计与分析', '1', '100', ' 算法设计作业1', '/static/upload/c272437989c6f5dd540751242dc3586b.jpg', '小洛克', '003', '88', '111', '2024-12-30 23:22:17');
