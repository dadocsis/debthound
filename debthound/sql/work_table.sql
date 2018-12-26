CREATE TABLE `debthound`.`work_document_etl` (
  `defendant_name` VARCHAR(1500) NOT NULL,
  `jud_doc_id` INT NOT NULL,
  `deed_doc_id` INT NOT NULL);


ALTER TABLE `debthound`.`work_document_etl` 
ADD COLUMN `plantiff_name` VARCHAR(1500) NOT NULL AFTER `defendant_name`;
