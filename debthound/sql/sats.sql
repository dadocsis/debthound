	CREATE TEMPORARY TABLE tmp_sats    
    select distinct
		jud.party2 as `defendant_name`
        ,jud.party1 as `plantiff_name`
		#,jud.id as `jud_doc_id`
        #,deed.id as `deed_doc_id`
	from 
		site s 
        join document jud
        on s.id = jud.site_id
		join document deed
		on deed.party1 = jud.party2 
			and jud.doctype_id = 2 
            and deed.doctype_id = 1
            and deed.site_id = s.id
		left join document sat 
		on sat.party2 = jud.party2 
			and sat.doctype_id = 3 
            and sat.party1 = jud.party1 
            and sat.date > jud.date
            and sat.site_id = s.id
		left join entity black_listed_plantiffs 
        on black_listed_plantiffs.name = jud.party1 and black_listed_plantiffs.black_listed = 1
        left join entity black_listed_defendants 
        on black_listed_defendants.name = jud.party2 and black_listed_plantiffs.black_listed = 1
	where  black_listed_plantiffs.name is null and black_listed_defendants.name is null
		and jud.party2 not in ('PALM BEACH COUNTY', 'FL') and jud.party2 != ''
		and deed.date > jud.date and sat.cfn is not null
        and s.id = 2;
        
	delete from entity_flag_association
    where entity_id in (
    select 
				distinct e.id
	  from		entity e
      join		documentfact f
        on		e.id = f.entity_id
      join		tmp_sats ts
        on 		ts.defendant_name = e.name);
	
    with e_ids as (
    select 
				distinct e.id as id
	  from		entity e
      join		documentfact f
        on		e.id = f.entity_id
      join		tmp_sats ts
        on 		ts.defendant_name = e.name)
        delete from documentfact
			where entity_id in (select id from e_ids);
    
    Drop temporary table tmp_sats;