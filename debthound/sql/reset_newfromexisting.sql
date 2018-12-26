/*
select * from entity e where e.id = 268;

select		d.* 
from 		documentfact f
join		document d 
on			d.id = f.document_id
where		f.entity_id = 268;

select d.* from document d where d.id in (1870654)

call document_etl(2);
*/

with 
	fact as (
		select 	
				e.id
				,e.name
				,d.site_id
		  from 	documentfact df
				join document d
				on d.id = df.document_id 
				join entity e
				on df.entity_id = e.id 
				inner join site s1 
				on s1.id = d.site_id 
		 # where d.site
		group by
				e.id
				,e.name
				,d.site_id
	 )
	,dfe_to_remove as (
		select 
				f.id 
		from 	fact f 
		group by 
				f.id 
		having  count(f.site_id) > 1
	 )
    ,dfd_to_remove as ( 
		select 
				d.id,
                d.cfn,
                dfe.id as e_id
		  from  dfe_to_remove dfe
          join	documentfact df
		  on	dfe.id = df.entity_id
          join 	document d
          on	df.document_id = d.id
          where d.site_id = 2
	)
    delete from documentfact where document_id in (Select id from dfd_to_remove);
    delete from entity_flag_association where entity_flag_id = 11;
    
    
