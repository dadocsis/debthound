SELECT * FROM debthound.sitescrapelog;

delete from debthound.sitescrapelog;
truncate debthound.sitescrapelog;

SET FOREIGN_KEY_CHECKS = 0; 
-- truncate table debthound.sitescrapelogdetails;
-- truncate table debthound.sitescrapelog;
-- truncate table debthound.document;
truncate table entity;
SET FOREIGN_KEY_CHECKS = 1;