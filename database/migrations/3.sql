alter table terms add column categories text[];

create table if not exists admins
(
    user_id     bigint,
    added_by_id bigint
);

update info set schema_version = 3;