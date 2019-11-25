create table users(
    id serial,
    user_login varchar(255) not null,
    pass varchar(255) not null,
    comment text
);

insert into users (user_login, pass, comment) values ('god', 'admin', 'yeah')
