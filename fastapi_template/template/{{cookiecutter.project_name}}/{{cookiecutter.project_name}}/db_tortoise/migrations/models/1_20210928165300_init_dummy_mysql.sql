-- upgrade --
CREATE TABLE IF NOT EXISTS `dummymodel` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(200) NOT NULL
) CHARACTER SET utf8mb4 COMMENT='Model for demo purpose.';
-- downgrade --
DROP TABLE `dummymodel`;
