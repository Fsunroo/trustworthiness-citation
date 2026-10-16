SELECT id,payload FROM articles WHERE json_extract(payload,'$.data."Eligibility decision"')='Include' AND COALESCE(json_extract(payload,'$.secondaryReviewStatus'),'')!='Pending' ORDER BY id;
