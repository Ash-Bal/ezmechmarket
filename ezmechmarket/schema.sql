drop table if exists posts;
drop table if exists images;
drop table if exists album;

create table posts (
    id integer primary key AUTOINCREMENT,
    title text not NULL,
    url text not NULL,
    body text not NULL,
    created timestamp not NULL
);

create table images (
    id integer primary key AUTOINCREMENT,
    title text not NULL,
    image_url text not NULL,
    created timestamp not NULL default CURRENT_TIMESTAMP
);


create table album (
    id integer primary key AUTOINCREMENT,
    title text not NULL,
    album_url text not NULL
);