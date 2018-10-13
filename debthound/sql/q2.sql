use debthound;

select 
    jud.party1 as `Judgment Plaintif`
	,jud.party2 as `Judgment Defendant`
    ,jud.date as `Judgment File Date`
    ,jud.consideration as `Judgment consideration`
    ,jud.cfn as `Judgment cfn`
    ,deed.date as `Deed File Date`
    ,deed.legal as `Deed Legal`
    ,deed.consideration as `Deed Consideration`
    ,deed.cfn as `Deed cfn` 
    ,jud.image_uri as `Judgment Image`
    ,deed.image_uri as `Deed Image`
from 
	document jud
    join document deed
	on deed.party1 = jud.party2 and jud.doctype_id = 2 and deed.doctype_id = 1
    left join document sat 
    on sat.party2 = jud.party2 and sat.doctype_id = 3 and sat.party1 = jud.party1 and sat.date > jud.date
where  jud.party1 not in ('FLORIDA', 'PALM BEACH COUNTY', 'FL', 'FLORIDA,PALM BEACH COUNTY', 'PALM BEACH COUNTY,FLORIDA') 
	and jud.party2 not in ('PALM BEACH COUNTY', 'FL') and jud.party2 != ''
	and deed.date > jud.date and sat.cfn is null

order by jud.date

# this query searches judc defendants match deed grantor in the exact name of judgment party2 == deed party1
# since it is an exact name search it wont pick up deed grantors that are husband and wife
# likewise if judgment is against multiple parts this query wont pick up a deed issued by one of the single partys (Ask Trish if we should try and find those scenarios)
# deeds granted prior to judgments are filtered out
# Palm beach county and State of FL as Defendants or Deed grantors are filtered out
# Judments that have a Sat dated > Jud are filtered out. Will need to see if this can be tweaked due to obvious false positives.

