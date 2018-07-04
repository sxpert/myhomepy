-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'EN_DEVICE'
-- 
-- ---

DROP TABLE IF EXISTS `EN_DEVICE`;
		
CREATE TABLE `EN_DEVICE` (
  `id_device` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `code` MEDIUMTEXT NULL DEFAULT NULL,
  `name` MEDIUMTEXT NULL DEFAULT NULL,
  `id_brand` INTEGER NULL DEFAULT NULL,
  `id_line` INTEGER NULL DEFAULT NULL,
  `visible` bit NULL DEFAULT NULL,
  `id_item` INTEGER NULL DEFAULT NULL,
  `visibility_type` INTEGER NULL DEFAULT NULL,
  `dependent` INTEGER NULL DEFAULT NULL,
  `is_gateway` bit NULL DEFAULT NULL,
  `descr` MEDIUMTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id_device`)
);

-- ---
-- Table 'EN_ITEM'
-- 
-- ---

DROP TABLE IF EXISTS `EN_ITEM`;
		
CREATE TABLE `EN_ITEM` (
  `id_item` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `descr` MEDIUMTEXT NULL DEFAULT NULL,
  `id_family` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id_item`)
);

-- ---
-- Table 'EN_FIRMWARE'
-- 
-- ---

DROP TABLE IF EXISTS `EN_FIRMWARE`;
		
CREATE TABLE `EN_FIRMWARE` (
  `id_item` INTEGER NULL DEFAULT NULL,
  `firmware_V` INTEGER NULL DEFAULT NULL,
  `firmware_R` INTEGER NULL DEFAULT NULL,
  `slots` INTEGER NULL DEFAULT NULL,
  `id_status` INTEGER NULL DEFAULT NULL,
  `FW_default` INTEGER NULL DEFAULT NULL,
  `id_firmware` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  PRIMARY KEY (`id_firmware`)
);

-- ---
-- Table 'EN_STATUS'
-- 
-- ---

DROP TABLE IF EXISTS `EN_STATUS`;
		
CREATE TABLE `EN_STATUS` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `name` INTEGER NULL DEFAULT NULL,
  `description` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'AS_OBJECT_FIRMWARE'
-- 
-- ---

DROP TABLE IF EXISTS `AS_OBJECT_FIRMWARE`;
		
CREATE TABLE `AS_OBJECT_FIRMWARE` (
  `id_key_object` INTEGER NULL DEFAULT NULL,
  `id_object_firmware` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `id_firmware` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id_object_firmware`)
);

-- ---
-- Table 'AS_OBJECT_SYSTEM'
-- 
-- ---

DROP TABLE IF EXISTS `AS_OBJECT_SYSTEM`;
		
CREATE TABLE `AS_OBJECT_SYSTEM` (
  `id_system` INTEGER NULL DEFAULT NULL,
  `id_key_object` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  PRIMARY KEY (`id_key_object`)
);

-- ---
-- Table 'EN_KEY_OBJECT'
-- 
-- ---

DROP TABLE IF EXISTS `EN_KEY_OBJECT`;
		
CREATE TABLE `EN_KEY_OBJECT` (
  `id_key_object` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `descr` MEDIUMTEXT NULL DEFAULT NULL,
  `slots` INTEGER NULL DEFAULT NULL,
  `visible` bit NULL DEFAULT NULL,
  `id_family` INTEGER NULL DEFAULT NULL,
  `key_object` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id_key_object`)
);

-- ---
-- Table 'EN_SYSTEM'
-- 
-- ---

DROP TABLE IF EXISTS `EN_SYSTEM`;
		
CREATE TABLE `EN_SYSTEM` (
  `id_system` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `name` MEDIUMTEXT NULL DEFAULT NULL,
  `descr` MEDIUMTEXT NULL DEFAULT NULL,
  `xml_key_system` MEDIUMTEXT NULL DEFAULT NULL,
  `sys_modobj` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id_system`)
);

-- ---
-- Table 'EN_CONF'
-- 
-- ---

DROP TABLE IF EXISTS `EN_CONF`;
		
CREATE TABLE `EN_CONF` (
  `id_firmware` INTEGER NULL DEFAULT NULL,
  `id_conf` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `id_key_object` INTEGER NULL DEFAULT NULL,
  `conf_name` INTEGER NULL DEFAULT NULL,
  `id_conf_type` INTEGER NULL DEFAULT NULL,
  `descr` MEDIUMTEXT NULL DEFAULT NULL,
  `descr_ext` MEDIUMTEXT NULL DEFAULT NULL,
  `hidden` INTEGER NULL DEFAULT NULL,
  `idx` INTEGER NULL DEFAULT NULL,
  `id_conf_data_type` INTEGER NULL DEFAULT NULL,
  `progressive` INTEGER NULL DEFAULT NULL,
  `visible` INTEGER NULL DEFAULT NULL,
  `read_only` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id_conf`)
);

-- ---
-- Table 'EN_CONF_TYPE'
-- 
-- ---

DROP TABLE IF EXISTS `EN_CONF_TYPE`;
		
CREATE TABLE `EN_CONF_TYPE` (
  `id_conf_type` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `descr` MEDIUMTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id_conf_type`)
);

-- ---
-- Table 'EN_CONF_DATA_TYPE'
-- 
-- ---

DROP TABLE IF EXISTS `EN_CONF_DATA_TYPE`;
		
CREATE TABLE `EN_CONF_DATA_TYPE` (
  `id_conf_data_type` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `data_type` MEDIUMTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id_conf_data_type`)
);

-- ---
-- Table 'EN_CONF_RANGE'
-- 
-- ---

DROP TABLE IF EXISTS `EN_CONF_RANGE`;
		
CREATE TABLE `EN_CONF_RANGE` (
  `value` MEDIUMTEXT NULL DEFAULT NULL,
  `name` MEDIUMTEXT NULL DEFAULT NULL,
  `descr_ext` MEDIUMTEXT NULL DEFAULT NULL,
  `default` MEDIUMTEXT NULL DEFAULT NULL,
  `progressive` INTEGER NULL DEFAULT NULL,
  `id_conf` INTEGER NULL DEFAULT NULL,
  `id_conf_range` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `digit` INTEGER NULL DEFAULT NULL,
  `step` INTEGER NULL DEFAULT NULL,
  `min_value` INTEGER NULL DEFAULT NULL,
  `max_value` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id_conf_range`)
);

-- ---
-- Table 'EN_CONDITION'
-- 
-- ---

DROP TABLE IF EXISTS `EN_CONDITION`;
		
CREATE TABLE `EN_CONDITION` (
  `id_condition` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `condition` MEDIUMTEXT NULL DEFAULT NULL,
  `id_conv_rule` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id_condition`)
);

-- ---
-- Table 'EN_CONV_RULE'
-- 
-- ---

DROP TABLE IF EXISTS `EN_CONV_RULE`;
		
CREATE TABLE `EN_CONV_RULE` (
  `id_conv_rule` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `item_conf` MEDIUMTEXT NULL DEFAULT NULL,
  `item_conf_value` MEDIUMTEXT NULL DEFAULT NULL,
  `object_conf` MEDIUMTEXT NULL DEFAULT NULL,
  `object_conf_value` MEDIUMTEXT NULL DEFAULT NULL,
  `always_true` INTEGER NULL DEFAULT NULL,
  `jump_id_conv_rule` INTEGER NULL DEFAULT NULL,
  `id` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id_conv_rule`)
);

-- ---
-- Table 'AS_SLOT_CONDITION'
-- 
-- ---

DROP TABLE IF EXISTS `AS_SLOT_CONDITION`;
		
CREATE TABLE `AS_SLOT_CONDITION` (
  `id_slot` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `id_condition` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id_slot`)
);

-- ---
-- Table 'EN_SLOTS'
-- 
-- ---

DROP TABLE IF EXISTS `EN_SLOTS`;
		
CREATE TABLE `EN_SLOTS` (
  `id_object_firmware` INTEGER NULL DEFAULT NULL,
  `id_slot` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `first_slot` INTEGER NULL DEFAULT NULL,
  `fixed_ko` bit NULL DEFAULT NULL,
  PRIMARY KEY (`id_slot`)
);

-- ---
-- Table 'EN_FILTER'
-- 
-- ---

DROP TABLE IF EXISTS `EN_FILTER`;
		
CREATE TABLE `EN_FILTER` (
  `id_conf` INTEGER NULL DEFAULT NULL,
  `id_object_firmware` INTEGER NULL DEFAULT NULL,
  `id_filter` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `note` MEDIUMTEXT NULL DEFAULT NULL,
  `whole_range` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id_filter`)
);

-- ---
-- Table 'AS_ITEM_SYSTEM'
-- 
-- ---

DROP TABLE IF EXISTS `AS_ITEM_SYSTEM`;
		
CREATE TABLE `AS_ITEM_SYSTEM` (
  `id_item` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `id_system` INTEGER NULL DEFAULT NULL,
  `modobj` INTEGER NULL DEFAULT NULL,
  `main` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id_item`)
);

-- ---
-- Table 'EN_BUILDS'
-- 
-- ---

DROP TABLE IF EXISTS `EN_BUILDS`;
		
CREATE TABLE `EN_BUILDS` (
  `id_build` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `firmware_b` INTEGER NULL DEFAULT NULL,
  `localization_level` INTEGER NULL DEFAULT NULL,
  `id_firmware` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id_build`)
);

-- ---
-- Table 'AS_HIDDEN_KCONF'
-- 
-- ---

DROP TABLE IF EXISTS `AS_HIDDEN_KCONF`;
		
CREATE TABLE `AS_HIDDEN_KCONF` (
  `id_conf_range` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `id_conf` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id_conf_range`)
);

-- ---
-- Table 'EN_FILTER_RANGE'
-- 
-- ---

DROP TABLE IF EXISTS `EN_FILTER_RANGE`;
		
CREATE TABLE `EN_FILTER_RANGE` (
  `id_filter` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `range` INTEGER NULL DEFAULT NULL,
  `note` MEDIUMTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id_filter`)
);

-- ---
-- Foreign Keys 
-- ---

ALTER TABLE `EN_DEVICE` ADD FOREIGN KEY (id_item) REFERENCES `EN_ITEM` (`id_item`);
ALTER TABLE `EN_FIRMWARE` ADD FOREIGN KEY (id_item) REFERENCES `EN_ITEM` (`id_item`);
ALTER TABLE `EN_FIRMWARE` ADD FOREIGN KEY (id_status) REFERENCES `EN_STATUS` (`id`);
ALTER TABLE `AS_OBJECT_FIRMWARE` ADD FOREIGN KEY (id_key_object) REFERENCES `EN_KEY_OBJECT` (`id_key_object`);
ALTER TABLE `AS_OBJECT_FIRMWARE` ADD FOREIGN KEY (id_firmware) REFERENCES `EN_FIRMWARE` (`id_firmware`);
ALTER TABLE `AS_OBJECT_SYSTEM` ADD FOREIGN KEY (id_system) REFERENCES `EN_SYSTEM` (`id_system`);
ALTER TABLE `AS_OBJECT_SYSTEM` ADD FOREIGN KEY (id_key_object) REFERENCES `EN_KEY_OBJECT` (`id_key_object`);
ALTER TABLE `EN_CONF` ADD FOREIGN KEY (id_firmware) REFERENCES `EN_FIRMWARE` (`id_firmware`);
ALTER TABLE `EN_CONF` ADD FOREIGN KEY (id_key_object) REFERENCES `EN_KEY_OBJECT` (`id_key_object`);
ALTER TABLE `EN_CONF` ADD FOREIGN KEY (id_conf_type) REFERENCES `EN_CONF_TYPE` (`id_conf_type`);
ALTER TABLE `EN_CONF` ADD FOREIGN KEY (id_conf_data_type) REFERENCES `EN_CONF_DATA_TYPE` (`id_conf_data_type`);
ALTER TABLE `EN_CONF_RANGE` ADD FOREIGN KEY (id_conf) REFERENCES `EN_CONF` (`id_conf`);
ALTER TABLE `EN_CONDITION` ADD FOREIGN KEY (id_conv_rule) REFERENCES `EN_CONV_RULE` (`id_conv_rule`);
ALTER TABLE `AS_SLOT_CONDITION` ADD FOREIGN KEY (id_slot) REFERENCES `EN_SLOTS` (`id_slot`);
ALTER TABLE `AS_SLOT_CONDITION` ADD FOREIGN KEY (id_condition) REFERENCES `EN_CONDITION` (`id_condition`);
ALTER TABLE `EN_SLOTS` ADD FOREIGN KEY (id_object_firmware) REFERENCES `AS_OBJECT_FIRMWARE` (`id_object_firmware`);
ALTER TABLE `EN_FILTER` ADD FOREIGN KEY (id_conf) REFERENCES `EN_CONF` (`id_conf`);
ALTER TABLE `EN_FILTER` ADD FOREIGN KEY (id_object_firmware) REFERENCES `AS_OBJECT_FIRMWARE` (`id_object_firmware`);
ALTER TABLE `AS_ITEM_SYSTEM` ADD FOREIGN KEY (id_item) REFERENCES `EN_ITEM` (`id_item`);
ALTER TABLE `AS_ITEM_SYSTEM` ADD FOREIGN KEY (id_system) REFERENCES `EN_SYSTEM` (`id_system`);
ALTER TABLE `EN_BUILDS` ADD FOREIGN KEY (id_firmware) REFERENCES `EN_FIRMWARE` (`id_firmware`);
ALTER TABLE `AS_HIDDEN_KCONF` ADD FOREIGN KEY (id_conf_range) REFERENCES `EN_CONF_RANGE` (`id_conf_range`);
ALTER TABLE `AS_HIDDEN_KCONF` ADD FOREIGN KEY (id_conf) REFERENCES `EN_CONF` (`id_conf`);
ALTER TABLE `EN_FILTER_RANGE` ADD FOREIGN KEY (id_filter) REFERENCES `EN_FILTER` (`id_filter`);

-- ---
-- Table Properties
-- ---

-- ALTER TABLE `EN_DEVICE` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `EN_ITEM` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `EN_FIRMWARE` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `EN_STATUS` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `AS_OBJECT_FIRMWARE` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `AS_OBJECT_SYSTEM` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `EN_KEY_OBJECT` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `EN_SYSTEM` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `EN_CONF` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `EN_CONF_TYPE` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `EN_CONF_DATA_TYPE` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `EN_CONF_RANGE` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `EN_CONDITION` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `EN_CONV_RULE` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `AS_SLOT_CONDITION` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `EN_SLOTS` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `EN_FILTER` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `AS_ITEM_SYSTEM` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `EN_BUILDS` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `AS_HIDDEN_KCONF` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `EN_FILTER_RANGE` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `EN_DEVICE` (`id_device`,`code`,`name`,`id_brand`,`id_line`,`visible`,`id_item`,`visibility_type`,`dependent`,`is_gateway`,`descr`) VALUES
-- ('','','','','','','','','','','');
-- INSERT INTO `EN_ITEM` (`id_item`,`descr`,`id_family`) VALUES
-- ('','','');
-- INSERT INTO `EN_FIRMWARE` (`id_item`,`firmware_V`,`firmware_R`,`slots`,`id_status`,`FW_default`,`id_firmware`) VALUES
-- ('','','','','','','');
-- INSERT INTO `EN_STATUS` (`id`,`name`,`description`) VALUES
-- ('','','');
-- INSERT INTO `AS_OBJECT_FIRMWARE` (`id_key_object`,`id_object_firmware`,`id_firmware`) VALUES
-- ('','','');
-- INSERT INTO `AS_OBJECT_SYSTEM` (`id_system`,`id_key_object`) VALUES
-- ('','');
-- INSERT INTO `EN_KEY_OBJECT` (`id_key_object`,`descr`,`slots`,`visible`,`id_family`,`key_object`) VALUES
-- ('','','','','','');
-- INSERT INTO `EN_SYSTEM` (`id_system`,`name`,`descr`,`xml_key_system`,`sys_modobj`) VALUES
-- ('','','','','');
-- INSERT INTO `EN_CONF` (`id_firmware`,`id_conf`,`id_key_object`,`conf_name`,`id_conf_type`,`descr`,`descr_ext`,`hidden`,`idx`,`id_conf_data_type`,`progressive`,`visible`,`read_only`) VALUES
-- ('','','','','','','','','','','','','');
-- INSERT INTO `EN_CONF_TYPE` (`id_conf_type`,`descr`) VALUES
-- ('','');
-- INSERT INTO `EN_CONF_DATA_TYPE` (`id_conf_data_type`,`data_type`) VALUES
-- ('','');
-- INSERT INTO `EN_CONF_RANGE` (`value`,`name`,`descr_ext`,`default`,`progressive`,`id_conf`,`id_conf_range`,`digit`,`step`,`min_value`,`max_value`) VALUES
-- ('','','','','','','','','','','');
-- INSERT INTO `EN_CONDITION` (`id_condition`,`condition`,`id_conv_rule`) VALUES
-- ('','','');
-- INSERT INTO `EN_CONV_RULE` (`id_conv_rule`,`item_conf`,`item_conf_value`,`object_conf`,`object_conf_value`,`always_true`,`jump_id_conv_rule`,`id`) VALUES
-- ('','','','','','','','');
-- INSERT INTO `AS_SLOT_CONDITION` (`id_slot`,`id_condition`) VALUES
-- ('','');
-- INSERT INTO `EN_SLOTS` (`id_object_firmware`,`id_slot`,`first_slot`,`fixed_ko`) VALUES
-- ('','','','');
-- INSERT INTO `EN_FILTER` (`id_conf`,`id_object_firmware`,`id_filter`,`note`,`whole_range`) VALUES
-- ('','','','','');
-- INSERT INTO `AS_ITEM_SYSTEM` (`id_item`,`id_system`,`modobj`,`main`) VALUES
-- ('','','','');
-- INSERT INTO `EN_BUILDS` (`id_build`,`firmware_b`,`localization_level`,`id_firmware`) VALUES
-- ('','','','');
-- INSERT INTO `AS_HIDDEN_KCONF` (`id_conf_range`,`id_conf`) VALUES
-- ('','');
-- INSERT INTO `EN_FILTER_RANGE` (`id_filter`,`range`,`note`) VALUES
-- ('','','');