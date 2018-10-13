USE `debthound`;
DROP procedure IF EXISTS `document_etl`;

DELIMITER $$
USE `debthound`$$
CREATE PROCEDURE `document_etl` (IN jud_doctype_id INT, IN deed_doctype_id INT, IN sat_doctype_id INT)
BEGIN
TRUNCATE TABLE work_document_etl;

INSERT INTO work_document_etl 
    
	select 
		jud.party2 as `defendant_name`        
		,jud.id as `jud_doc_id`
        ,deed.id as `deed_doc_id`
	from 
		document jud
		join document deed
		on deed.party1 = jud.party2 and jud.doctype_id = jud_doctype_id and deed.doctype_id = deed_doctype_id
		left join document sat 
		on sat.party2 = jud.party2 and sat.doctype_id = sat_doctype_id and sat.party1 = jud.party1 and sat.date > jud.date
	where  jud.party1 not in ('FLORIDA', 'PALM BEACH COUNTY', 'FL', 'FLORIDA,PALM BEACH COUNTY', 'PALM BEACH COUNTY,FLORIDA') 
		and jud.party2 not in ('PALM BEACH COUNTY', 'FL') and jud.party2 != ''
		and deed.date > jud.date and sat.cfn is null

	order by jud.date;    
    
    INSERT INTO entity
		(`name`)
		select distinct 
			defendant_name
		from work_document_etl tr 
			left join entity e
            on tr.defendant_name = e.name
		where e.id is null;
	
    INSERT into documentfact
    (`document_id`, `entity_id`)
    with  
		judgments AS (
			select distinct jud_doc_id as did, defendant_name from work_document_etl
			union all
            select distinct deed_doc_id as did, defendant_name from work_document_etl
        ),
        results AS (
			select j.did, e.id from entity e join judgments j on e.name = j.defendant_name
        )
	Select r.* 
	from results r
	left join documentfact df on df.document_id = r.did
	where df.document_id is null;
    
   --  select * from documentfact
    
    

END$$

DELIMITER ;

