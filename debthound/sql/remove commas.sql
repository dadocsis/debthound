update document
set  party1 = replace(party1, ',', '')
	 ,party2 = replace(party2, ',', '')
where site_id = 2 and regexp_substr(party1, '([A-Za-z],){2,}') is not null;

update entity
	set name = replace(name, ',', '')
where regexp_substr(name, '([A-Za-z],){2,}') is not null
