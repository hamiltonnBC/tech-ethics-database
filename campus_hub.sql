-- MySQL dump 10.13  Distrib 8.4.4, for Linux (x86_64)
--
-- Host: localhost    Database: db
-- ------------------------------------------------------
-- Server version	8.4.4

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
-- Table structure for table `Departments`
--

DROP TABLE IF EXISTS `Departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Departments` (
  `id` tinyint DEFAULT NULL,
  `name` varchar(16) DEFAULT NULL,
  `location` varchar(29) DEFAULT NULL,
  `contact_email` varchar(18) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Departments`
--

LOCK TABLES `Departments` WRITE;
/*!40000 ALTER TABLE `Departments` DISABLE KEYS */;
INSERT INTO `Departments` VALUES (1,'Media Studies','Communications Bldg, Room 201','media@campus.edu'),(2,'Computer Science','Tech Lab A','cs@campus.edu'),(3,'Library Services','Main Library Hub','library@campus.edu');
/*!40000 ALTER TABLE `Departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ResourceLog`
--

DROP TABLE IF EXISTS `ResourceLog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ResourceLog` (
  `id` tinyint DEFAULT NULL,
  `student_id` tinyint DEFAULT NULL,
  `resource_id` tinyint DEFAULT NULL,
  `borrowed_date` varchar(0) DEFAULT NULL,
  `returned_date` varchar(0) DEFAULT NULL,
  `status` varchar(8) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ResourceLog`
--

LOCK TABLES `ResourceLog` WRITE;
/*!40000 ALTER TABLE `ResourceLog` DISABLE KEYS */;
INSERT INTO `ResourceLog` VALUES (1,1,1,'','','Returned'),(2,2,3,'','','Returned'),(3,3,2,'','','Active'),(4,1,4,'','','Active');
/*!40000 ALTER TABLE `ResourceLog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Resources`
--

DROP TABLE IF EXISTS `Resources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Resources` (
  `id` tinyint DEFAULT NULL,
  `name` varchar(27) DEFAULT NULL,
  `description` varchar(38) DEFAULT NULL,
  `type` varchar(8) DEFAULT NULL,
  `department_id` tinyint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Resources`
--

LOCK TABLES `Resources` WRITE;
/*!40000 ALTER TABLE `Resources` DISABLE KEYS */;
INSERT INTO `Resources` VALUES (1,'Canon EOS 80D','DSLR Camera for student media projects','Hardware',1),(2,'MacBook Pro M2','Laptop with Adobe Suite and Xcode','Hardware',2),(3,'Private Study Room 4A','Quiet workspace with whiteboard','Room',3),(4,'JetBrains IntelliJ IDEA IDE','Educational Software License Keys','Software',2);
/*!40000 ALTER TABLE `Resources` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Reviews`
--

DROP TABLE IF EXISTS `Reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Reviews` (
  `id` tinyint DEFAULT NULL,
  `student_id` tinyint DEFAULT NULL,
  `resource_id` tinyint DEFAULT NULL,
  `rating` tinyint DEFAULT NULL,
  `comment` varchar(41) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Reviews`
--

LOCK TABLES `Reviews` WRITE;
/*!40000 ALTER TABLE `Reviews` DISABLE KEYS */;
INSERT INTO `Reviews` VALUES (1,1,1,5,'Great camera, easy to use.'),(2,2,3,4,'Nice and quiet, but the markers were dry.');
/*!40000 ALTER TABLE `Reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Students`
--

DROP TABLE IF EXISTS `Students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Students` (
  `id` tinyint DEFAULT NULL,
  `first_name` varchar(7) DEFAULT NULL,
  `last_name` varchar(7) DEFAULT NULL,
  `email` varchar(19) DEFAULT NULL,
  `enrollment_year` smallint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Students`
--

LOCK TABLES `Students` WRITE;
/*!40000 ALTER TABLE `Students` DISABLE KEYS */;
INSERT INTO `Students` VALUES (1,'Alice','Smith','asmith@campus.edu',2022),(2,'Bob','Johnson','bjohnson@campus.edu',2023),(3,'Charlie','Brown','cbrown@campus.edu',2024),(4,'Diana','Prince','dprince@campus.edu',2023);
/*!40000 ALTER TABLE `Students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sqlite_sequence`
--

DROP TABLE IF EXISTS `sqlite_sequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sqlite_sequence` (
  `name` varchar(11) DEFAULT NULL,
  `seq` tinyint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sqlite_sequence`
--

LOCK TABLES `sqlite_sequence` WRITE;
/*!40000 ALTER TABLE `sqlite_sequence` DISABLE KEYS */;
INSERT INTO `sqlite_sequence` VALUES ('Departments',3),('Resources',4),('Students',4),('ResourceLog',4),('Reviews',2);
/*!40000 ALTER TABLE `sqlite_sequence` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-11 13:29:57
