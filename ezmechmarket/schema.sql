drop table if exists posts;
drop table if exists images;

create table posts (
    id integer primary key AUTOINCREMENT,
    title text not NULL,
    url text not NULL,
    body text not NULL
);

create table images (
    id integer primary key AUTOINCREMENT,
    title text not NULL,
    image_url text not NULL
);


