-- MySQL dump 10.13  Distrib 9.4.0, for Win64 (x86_64)
--
-- Host: localhost    Database: rest_bus
-- ------------------------------------------------------
-- Server version	9.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `final_bill`
--

DROP TABLE IF EXISTS `final_bill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `final_bill` (
  `billid` int NOT NULL,
  `amount` int DEFAULT NULL,
  `rating` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  `cust_name` varchar(100) DEFAULT NULL,
  `item_name` varchar(400) DEFAULT NULL,
  PRIMARY KEY (`billid`),
  CONSTRAINT `final_bill_ibfk_1` FOREIGN KEY (`billid`) REFERENCES `pre_bill` (`billid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `final_bill`
--

LOCK TABLES `final_bill` WRITE;
/*!40000 ALTER TABLE `final_bill` DISABLE KEYS */;
INSERT INTO `final_bill` VALUES (82,480,4,'2025-11-10','ARJUN','Pasta,Sandwich,'),(83,1480,3,'2025-11-10','antara','cheesy fries,Pasta,Sandwich,');
/*!40000 ALTER TABLE `final_bill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu`
--

DROP TABLE IF EXISTS `menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu` (
  `serial_number` int NOT NULL AUTO_INCREMENT,
  `item` varchar(200) DEFAULT NULL,
  `amount` int DEFAULT NULL,
  `rating` int DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `rating_list` varchar(255) DEFAULT NULL,
  `amt_ordered` int DEFAULT '0',
  PRIMARY KEY (`serial_number`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu`
--

LOCK TABLES `menu` WRITE;
/*!40000 ALTER TABLE `menu` DISABLE KEYS */;
INSERT INTO `menu` VALUES (1,'Pizza',250,NULL,'Italian',NULL,0),(2,'burgir',120,NULL,'Fast Food',NULL,0),(3,'Pasta',180,4,'Italian','4,3,',2),(4,'Sandwich',300,5,'Snacks','5,4,',2),(5,'cheesy fries',1000,3,'fast food','3,',1);
/*!40000 ALTER TABLE `menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pre_bill`
--

DROP TABLE IF EXISTS `pre_bill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pre_bill` (
  `billid` int NOT NULL AUTO_INCREMENT,
  `cust_name` varchar(100) DEFAULT NULL,
  `item_id` varchar(100) DEFAULT NULL,
  `item_name` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`billid`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pre_bill`
--

LOCK TABLES `pre_bill` WRITE;
/*!40000 ALTER TABLE `pre_bill` DISABLE KEYS */;
INSERT INTO `pre_bill` VALUES (82,'ARJUN','3,4,','Pasta,Sandwich,'),(83,'antara','5,3,4,','cheesy fries,Pasta,Sandwich,');
/*!40000 ALTER TABLE `pre_bill` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-10 21:21:15
