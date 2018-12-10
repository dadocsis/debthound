
/*
insert into site (base_url, spider_name, last_scrape_datetime, last_poll_datetime) 
values ('https://officialrecords.broward.org', 'broward', '1000-01-01', '1000-01-01');
*/

/*
insert into sitedoctype_association (site_id, doctype_id) 
values (2, 1),(2, 2), (2, 3);
*/

select * from sitescrapelog order by start_datetime desc;
select * from sitescrapelogdetails where site_scrape_log_id = 245 and message like '%level: 30%'

select * from site
update site set last_scrape_datetime = '2013-12-25', last_poll_datetime = '2018-12-06' where id =2

select * from schedule
