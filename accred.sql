-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema accreditationsystem
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema accreditationsystem
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `accreditationsystem` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
USE `accreditationsystem` ;

-- -----------------------------------------------------
-- Table `accreditationsystem`.`centres`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `accreditationsystem`.`centres` (
  `CentreID` INT NOT NULL AUTO_INCREMENT,
  `CentreName` VARCHAR(200) NOT NULL,
  `Address` VARCHAR(255) NULL DEFAULT NULL,
  `ContactEmail` VARCHAR(150) NULL DEFAULT NULL,
  `ContactPhone` VARCHAR(50) NULL DEFAULT NULL,
  `IsActive` TINYINT(1) NULL DEFAULT '1',
  PRIMARY KEY (`CentreID`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `accreditationsystem`.`candidates`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `accreditationsystem`.`candidates` (
  `CandidateID` INT NOT NULL AUTO_INCREMENT,
  `PersonUID` VARCHAR(50) NOT NULL,
  `FirstName` VARCHAR(100) NOT NULL,
  `LastName` VARCHAR(100) NOT NULL,
  `NINumber` VARCHAR(50) NULL DEFAULT NULL,
  `Gender` ENUM('Male', 'Female', 'Other', 'PreferNotToSay') NULL DEFAULT NULL,
  `Ethnicity` VARCHAR(100) NULL DEFAULT NULL,
  `DateOfBirth` DATE NULL DEFAULT NULL,
  `CentreID` INT NOT NULL,
  PRIMARY KEY (`CandidateID`),
  UNIQUE INDEX `PersonUID` (`PersonUID` ASC) VISIBLE,
  UNIQUE INDEX `NINumber` (`NINumber` ASC) VISIBLE,
  INDEX `CentreID` (`CentreID` ASC) VISIBLE,
  CONSTRAINT `candidates_ibfk_1`
    FOREIGN KEY (`CentreID`)
    REFERENCES `accreditationsystem`.`centres` (`CentreID`)
    ON DELETE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `accreditationsystem`.`certificates`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `accreditationsystem`.`certificates` (
  `CertificateID` INT NOT NULL AUTO_INCREMENT,
  `CertificateName` VARCHAR(200) NOT NULL,
  `Level` VARCHAR(50) NULL DEFAULT NULL,
  `Description` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`CertificateID`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `accreditationsystem`.`courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `accreditationsystem`.`courses` (
  `CourseID` INT NOT NULL AUTO_INCREMENT,
  `CourseCode` VARCHAR(50) NOT NULL,
  `CourseName` VARCHAR(200) NOT NULL,
  `Description` TEXT NULL DEFAULT NULL,
  `DurationWeeks` INT NULL DEFAULT NULL,
  `CertificateID` INT NOT NULL,
  PRIMARY KEY (`CourseID`),
  UNIQUE INDEX `CourseCode` (`CourseCode` ASC) VISIBLE,
  INDEX `CertificateID` (`CertificateID` ASC) VISIBLE,
  CONSTRAINT `courses_ibfk_1`
    FOREIGN KEY (`CertificateID`)
    REFERENCES `accreditationsystem`.`certificates` (`CertificateID`)
    ON DELETE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `accreditationsystem`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `accreditationsystem`.`users` (
  `UserID` INT NOT NULL AUTO_INCREMENT,
  `CentreID` INT NULL DEFAULT NULL,
  `FirstName` VARCHAR(100) NOT NULL,
  `LastName` VARCHAR(100) NOT NULL,
  `Email` VARCHAR(150) NOT NULL,
  `PasswordHash` VARCHAR(255) NOT NULL,
  `Role` ENUM('AccreditationStaff', 'CentreStaff', 'Instructor') NOT NULL,
  `IsActive` TINYINT(1) NULL DEFAULT '1',
  PRIMARY KEY (`UserID`),
  UNIQUE INDEX `Email` (`Email` ASC) VISIBLE,
  INDEX `CentreID` (`CentreID` ASC) VISIBLE,
  CONSTRAINT `users_ibfk_1`
    FOREIGN KEY (`CentreID`)
    REFERENCES `accreditationsystem`.`centres` (`CentreID`)
    ON DELETE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `accreditationsystem`.`cohorts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `accreditationsystem`.`cohorts` (
  `CohortID` INT NOT NULL AUTO_INCREMENT,
  `CentreID` INT NOT NULL,
  `CourseID` INT NOT NULL,
  `InstructorID` INT NULL DEFAULT NULL,
  `StartDate` DATE NOT NULL,
  `EndDate` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`CohortID`),
  INDEX `CentreID` (`CentreID` ASC) VISIBLE,
  INDEX `CourseID` (`CourseID` ASC) VISIBLE,
  INDEX `InstructorID` (`InstructorID` ASC) VISIBLE,
  CONSTRAINT `cohorts_ibfk_1`
    FOREIGN KEY (`CentreID`)
    REFERENCES `accreditationsystem`.`centres` (`CentreID`)
    ON DELETE CASCADE,
  CONSTRAINT `cohorts_ibfk_2`
    FOREIGN KEY (`CourseID`)
    REFERENCES `accreditationsystem`.`courses` (`CourseID`)
    ON DELETE CASCADE,
  CONSTRAINT `cohorts_ibfk_3`
    FOREIGN KEY (`InstructorID`)
    REFERENCES `accreditationsystem`.`users` (`UserID`)
    ON DELETE SET NULL)
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `accreditationsystem`.`courseregistrations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `accreditationsystem`.`courseregistrations` (
  `RegistrationID` INT NOT NULL AUTO_INCREMENT,
  `CandidateID` INT NOT NULL,
  `CohortID` INT NOT NULL,
  `RegistrationDate` DATE NOT NULL,
  `PaymentStatus` ENUM('Pending', 'Paid', 'Failed') NULL DEFAULT 'Pending',
  `Status` ENUM('Registered', 'InProgress', 'Completed', 'Withdrawn') NULL DEFAULT 'Registered',
  `Result` VARCHAR(50) NULL DEFAULT NULL,
  `CompletionDate` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`RegistrationID`),
  INDEX `CandidateID` (`CandidateID` ASC) VISIBLE,
  INDEX `CohortID` (`CohortID` ASC) VISIBLE,
  CONSTRAINT `courseregistrations_ibfk_1`
    FOREIGN KEY (`CandidateID`)
    REFERENCES `accreditationsystem`.`candidates` (`CandidateID`)
    ON DELETE CASCADE,
  CONSTRAINT `courseregistrations_ibfk_2`
    FOREIGN KEY (`CohortID`)
    REFERENCES `accreditationsystem`.`cohorts` (`CohortID`)
    ON DELETE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `accreditationsystem`.`issuedcertificates`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `accreditationsystem`.`issuedcertificates` (
  `IssuedCertificateID` INT NOT NULL AUTO_INCREMENT,
  `CandidateID` INT NOT NULL,
  `CertificateID` INT NOT NULL,
  `RegistrationID` INT NOT NULL,
  `DateIssued` DATE NOT NULL,
  PRIMARY KEY (`IssuedCertificateID`),
  INDEX `CandidateID` (`CandidateID` ASC) VISIBLE,
  INDEX `CertificateID` (`CertificateID` ASC) VISIBLE,
  INDEX `RegistrationID` (`RegistrationID` ASC) VISIBLE,
  CONSTRAINT `issuedcertificates_ibfk_1`
    FOREIGN KEY (`CandidateID`)
    REFERENCES `accreditationsystem`.`candidates` (`CandidateID`)
    ON DELETE CASCADE,
  CONSTRAINT `issuedcertificates_ibfk_2`
    FOREIGN KEY (`CertificateID`)
    REFERENCES `accreditationsystem`.`certificates` (`CertificateID`)
    ON DELETE CASCADE,
  CONSTRAINT `issuedcertificates_ibfk_3`
    FOREIGN KEY (`RegistrationID`)
    REFERENCES `accreditationsystem`.`courseregistrations` (`RegistrationID`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
