/*
SQLyog Community v13.1.7 (64 bit)
MySQL - 8.0.27 : Database - projeto_01
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`projeto_01` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `projeto_01`;

/*Table structure for table `banco` */

DROP TABLE IF EXISTS `banco`;

CREATE TABLE `banco` (
  `codigo` int NOT NULL AUTO_INCREMENT,
  `nome_banco` varchar(20) DEFAULT NULL,
  `agencia` varchar(20) DEFAULT NULL,
  `conta` varchar(20) DEFAULT NULL,
  `cpf_cnpj` varchar(15) NOT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `banco` */

/*Table structure for table `classe` */

DROP TABLE IF EXISTS `classe`;

CREATE TABLE `classe` (
  `codigo` int NOT NULL AUTO_INCREMENT,
  `cpf_cnpj` varchar(15) NOT NULL,
  `classe` varchar(150) DEFAULT NULL,
  `cod_grupo` int DEFAULT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `classe` */

/*Table structure for table `fluxo_caixa` */

DROP TABLE IF EXISTS `fluxo_caixa`;

CREATE TABLE `fluxo_caixa` (
  `codigo` int NOT NULL AUTO_INCREMENT,
  `cpf_cnpj` varchar(15) NOT NULL,
  `descricao` varchar(150) DEFAULT NULL,
  `data_transacao` datetime DEFAULT NULL,
  `entrada` decimal(10,2) DEFAULT NULL,
  `saida` decimal(10,2) DEFAULT NULL,
  `codigo_classe` int DEFAULT NULL,
  `codigo_banco` int DEFAULT NULL,
  `codigo_tipo_pagamento` int DEFAULT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `fluxo_caixa` */

/*Table structure for table `grupo` */

DROP TABLE IF EXISTS `grupo`;

CREATE TABLE `grupo` (
  `codigo` int NOT NULL AUTO_INCREMENT,
  `cpf_cnpj` varchar(15) NOT NULL,
  `grupo` varchar(150) DEFAULT NULL,
  `cod_subgrupo` int DEFAULT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `grupo` */

/*Table structure for table `subgrupo` */

DROP TABLE IF EXISTS `subgrupo`;

CREATE TABLE `subgrupo` (
  `codigo` int NOT NULL AUTO_INCREMENT,
  `cpf_cnpj` varchar(15) NOT NULL,
  `subgrupo` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `subgrupo` */

/*Table structure for table `tipo_pagamento` */

DROP TABLE IF EXISTS `tipo_pagamento`;

CREATE TABLE `tipo_pagamento` (
  `codigo` int NOT NULL AUTO_INCREMENT,
  `cpf_cnpj` varchar(15) NOT NULL,
  `forma_pagamento` char(1) DEFAULT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `tipo_pagamento` */

/*Table structure for table `usuario` */

DROP TABLE IF EXISTS `usuario`;

CREATE TABLE `usuario` (
  `cpf_cnpj` varchar(15) NOT NULL,
  `nome` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `cep` varchar(10) DEFAULT NULL,
  `endereco` varchar(50) DEFAULT NULL,
  `sexo` varchar(1) DEFAULT NULL,
  `tipo` varchar(1) DEFAULT NULL,
  `usuario` varchar(50) DEFAULT NULL,
  `senha` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`cpf_cnpj`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `usuario` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
