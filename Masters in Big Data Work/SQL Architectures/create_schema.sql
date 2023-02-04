-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema solarsystem
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema solarsystem
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `solarsystem` DEFAULT CHARACTER SET utf8mb4 ;
USE `solarsystem` ;

-- -----------------------------------------------------
-- Table `solarsystem`.`elements`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `solarsystem`.`elements` (
  `ATOMIC_NUMBER` INT UNSIGNED NOT NULL,
  `NAME` VARCHAR(20) NOT NULL,
  `SYMBOL` VARCHAR(3) NOT NULL,
  `ATOMIC_MASS` DECIMAL(9,3) NOT NULL,
  `NEUTRONS` SMALLINT(2) NOT NULL,
  `PROTONS` SMALLINT(2) NOT NULL,
  `ELECTRONS` SMALLINT(2) NOT NULL,
  PRIMARY KEY (`ATOMIC_NUMBER`),
  UNIQUE INDEX `ELEMENT_ID_UNIQUE` (`ATOMIC_NUMBER` ASC) VISIBLE,
  UNIQUE INDEX `NAME_UNIQUE` (`NAME` ASC) VISIBLE,
  UNIQUE INDEX `SYMBOL_UNIQUE` (`SYMBOL` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `solarsystem`.`body_types`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `solarsystem`.`body_types` (
  `BODY_TYPE_ID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `NAME` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`BODY_TYPE_ID`),
  UNIQUE INDEX `BODY_TYPE_ID_UNIQUE` (`BODY_TYPE_ID` ASC) VISIBLE,
  UNIQUE INDEX `NAME_UNIQUE` (`NAME` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `solarsystem`.`bodies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `solarsystem`.`bodies` (
  `BODY_ID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `BODY_TYPE_ID` INT UNSIGNED NOT NULL,
  `NAME` VARCHAR(20) NOT NULL,
  `MASS_EM` DOUBLE NULL,
  `RADIUS_KM` DECIMAL(9,2) NULL,
  `SURFACE_AREA_KM2` BIGINT(8) UNSIGNED NULL,
  `DENSITY_G_CM3` FLOAT NULL,
  `ROTATION_DAYS` FLOAT NULL,
  `RINGS` TINYINT UNSIGNED NULL,
  PRIMARY KEY (`BODY_ID`),
  UNIQUE INDEX `BODY_ID_UNIQUE` (`BODY_ID` ASC) VISIBLE,
  INDEX `BODY_TYPE_ID_idx` (`BODY_TYPE_ID` ASC) VISIBLE,
  CONSTRAINT `BODY_TYPE_ID_FK`
    FOREIGN KEY (`BODY_TYPE_ID`)
    REFERENCES `solarsystem`.`body_types` (`BODY_TYPE_ID`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `solarsystem`.`body_relation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `solarsystem`.`body_relation` (
  `BODY_ID` INT UNSIGNED NOT NULL,
  `PARENT_ID` INT UNSIGNED NOT NULL,
  `DISTANCE_PARENT_AU` DOUBLE NULL,
  `ORBIT_YR` DECIMAL(6,2) NULL,
  INDEX `BODY_ID_FK_idx` (`BODY_ID` ASC) VISIBLE,
  INDEX `PARENT_ID_FK_idx` (`PARENT_ID` ASC) VISIBLE,
  PRIMARY KEY (`BODY_ID`, `PARENT_ID`),
  CONSTRAINT `BODY_ID_FK`
    FOREIGN KEY (`BODY_ID`)
    REFERENCES `solarsystem`.`bodies` (`BODY_ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `PARENT_ID_FK`
    FOREIGN KEY (`PARENT_ID`)
    REFERENCES `solarsystem`.`bodies` (`BODY_ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `solarsystem`.`composition`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `solarsystem`.`composition` (
  `BODY_ID` INT UNSIGNED NOT NULL,
  `ATOMIC_NUMBER` INT UNSIGNED NOT NULL,
  `PERCENTAGE` DECIMAL(4,3) NOT NULL,
  PRIMARY KEY (`BODY_ID`, `ATOMIC_NUMBER`),
  INDEX `ELEMENT_ID_FK_idx` (`ATOMIC_NUMBER` ASC) VISIBLE,
  CONSTRAINT `BODY_ID_FK_2`
    FOREIGN KEY (`BODY_ID`)
    REFERENCES `solarsystem`.`bodies` (`BODY_ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `ATOMIC_NUMBER_FK`
    FOREIGN KEY (`ATOMIC_NUMBER`)
    REFERENCES `solarsystem`.`elements` (`ATOMIC_NUMBER`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
