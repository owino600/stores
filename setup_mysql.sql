-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS STORE_MYSQL_DB;
CREATE USER IF NOT EXISTS 'store_dev'@'localhost' IDENTIFIED BY 'store_pwd';
GRANT ALL PRIVILEGES ON `STORE_MYSQL_DB`.* TO 'store_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'store_dev'@'localhost';
FLUSH PRIVILEGES;