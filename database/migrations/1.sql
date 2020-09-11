create table if not exists terms
(
    id          serial primary key,
    term       text,
    description text,
    source      text,
    created     timestamp not null default (current_timestamp at time zone 'utc')
);

create table if not exists explanations
(
    topic       text,
    explanation text
);

create table if not exists blacklisted_channels
(
    channel_id  bigint primary key,
    server_id   bigint
);

create table if not exists info
(
    id                      int primary key not null default 1, -- enforced only equal to 1
    schema_version          int,
    constraint singleton    check (id = 1) -- enforce singleton table/row
);

insert into info (schema_version) values (1);
