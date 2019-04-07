SELECT COUNT(*) FROM debthound.document;
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ;
with
Judgements AS 
	(SELECT distinct
		d.*
	FROM debthound.document d
	JOIN debthound.sitedoctype_association sda 
		on d.site_id = sda.site_id and d.doctype_id = sda.doctype_id
	JOIN debthound.sitedoctype sd
		on sda.doctype_id = sd.id
		where sd.name = 'JUD C'),
Deeds AS
	(SELECT distinct
		d.*
	FROM debthound.document d
	JOIN debthound.sitedoctype_association sda 
		on d.site_id = sda.site_id and d.doctype_id = sda.doctype_id
	JOIN debthound.sitedoctype sd
		on sda.doctype_id = sd.id
		where sd.name = 'D')
Select distinct
	j.party1 as Plantif,
    j.party2 as Defendant,    
    j.legal as Judgment_Legal,
    j.cfn as Judgment_CFN,
    j.date as Judgment_Date,
    d.party1 as Deed_Grantor,
    d.party2 as Deed_Grantee,
    d.date as Deed_Date,
    d.legal as Deed_Legal,
    d.cfn as Deed_CFN,
    j.image_uri as Judgment_Image,
    d.image_uri as Deed_Image  
    
FROM Judgements j 
JOIN Deeds d 
	on j.party2 = d.party1 and trim(j.party2) != ''
where d.site_id = 1;
COMMIT;


select * from document d where d.site_id = 2 and cfn = '108325810' LIMIT 5000