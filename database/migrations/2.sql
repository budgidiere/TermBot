alter table terms add column synonyms text[];

update info set schema_version = 2;