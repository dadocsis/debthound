

USE `debthound`;
DROP function IF EXISTS `get_or_create_entity_flag`;

DELIMITER $$
USE `debthound`$$
CREATE function `get_or_create_entity_flag` (name varchar(50), color varchar(50))
RETURNS INT DETERMINISTIC
BEGIN
	declare flag_id INT;    
    select id into flag_id from entityflag f where f.name = name LIMIT 1;
    set flag_id = ifnull(flag_id, -1);
    
    IF flag_id = -1 THEN 
		INSERT INTO entityflag VALUES(NULL, name, color);
        SET flag_id = last_insert_id();
    END IF;
    return flag_id;
END$$

DELIMITER ;

USE `debthound`;
DROP procedure IF EXISTS `document_etl`;

DELIMITER $$
USE `debthound`$$
CREATE PROCEDURE `document_etl` (IN _site_id INT)
BEGIN

declare jud_doctype_id, 
		deed_doctype_id, 
        sat_doctype_id,
        _entity_flag_id INT;

select distinct
	sdt_cj.id,  
	sdt_deed.id,  
    sdt_sat.id into 
    jud_doctype_id,
    deed_doctype_id,
    sat_doctype_id
from 
	site s 
	join sitedoctype_association sdta 
    on s.id = sdta.site_id
	join sitedoctype sdt_cj
    		on sdt_cj.description = 'Certified Judgment'
	join sitedoctype sdt_deed
    on sdt_deed.description = 'Deed'
	left join sitedoctype sdt_sat
    on sdt_sat.description = 'Satisfaction'
where s.id = _site_id;

TRUNCATE TABLE work_document_etl;

INSERT INTO work_document_etl 
    
	select 
		jud.party2 as `defendant_name`        
		,jud.id as `jud_doc_id`
        ,deed.id as `deed_doc_id`
	from 
		site s 
        join document jud
        on s.id = jud.site_id
		join document deed
		on deed.party1 = jud.party2 
			and jud.doctype_id = jud_doctype_id 
            and deed.doctype_id = deed_doctype_id
            and deed.site_id = s.id
		left join document sat 
		on sat.party2 = jud.party2 
			and sat.doctype_id = sat_doctype_id 
            and sat.party1 = jud.party1 
            and sat.date > jud.date
            and sat.site_id = s.id
	where  jud.party1 not in ('FLORIDA', 'PALM BEACH COUNTY', 'FL', 'FLORIDA,PALM BEACH COUNTY', 'PALM BEACH COUNTY,FLORIDA') 
		and jud.party2 not in ('PALM BEACH COUNTY', 'FL') and jud.party2 != ''
		and deed.date > jud.date and sat.cfn is null

	order by jud.date;      
    
	# First find the existing entities that have new documents
	CREATE TEMPORARY TABLE tmp_entity_existing    
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
    
    set _entity_flag_id = get_or_create_entity_flag('new lead from existing!', 'green');
    
	INSERT INTO entity_flag_association (entity_id, entity_flag_id)
	select distinct te.id, _entity_flag_id
	from tmp_entity_existing te
        left join entity_flag_association efa
        on efa.entity_id = te.id and efa.entity_flag_id = _entity_flag_id
	where efa.entity_id is null;
    
	INSERT into documentfact
		(`document_id`, `entity_id`)
		Select te.did, e.id
        from tmp_entity_existing te;
    
    # Now Find new entities
    CREATE TEMPORARY TABLE tmp_entity
    		select distinct 
			defendant_name as name
		from work_document_etl tr 
			left join entity e
            on tr.defendant_name = e.name
		where e.id is null;
        
    INSERT INTO entity
		(`name`)
		select te.name
		from tmp_entity te;
	
	set _entity_flag_id = get_or_create_entity_flag('new lead!', 'green');
    
    INSERT INTO entity_flag_association (entity_id, entity_flag_id)
		select e.id, _entity_flag_id
        from tmp_entity te
			join entity e
            on te.name = e.name;
	
	
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
    

   drop temporary table tmp_entity_existing;
   drop temporary table tmp_entity;
    
    

END$$

DELIMITER ;

