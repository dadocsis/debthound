Select @sat_doc_id := `id` from sitedoctype where name = 'SAT';
Select @deed_doc_id := `id` from sitedoctype where name = 'D';
Select @jud_doc_id := `id` from sitedoctype where name = 'JUD C';

insert into site (base_url, spider_name, last_scrape_datetime, last_poll_datetime) 
values ('https://officialrecords.mypinellasclerk.org', 'pinellas', '2009-04-07', '1000-01-01');

SET @last_id_in_table1 = LAST_INSERT_ID();

insert into sitedoctype_association (site_id, doctype_id) 
values (@last_id_in_table1, @sat_doc_id),(@last_id_in_table1, @deed_doc_id), (@last_id_in_table1, @jud_doc_id);


select 
	* 
from site s
join sitedoctype_association stda
	on s.id = stda.site_id
join sitedoctype sdt 
	on sdt.id = stda.doctype_id