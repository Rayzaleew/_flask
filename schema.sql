drop table requests;
--drop table products;
--drop table users;
drop table feedback;

create table requests (
	id integer primary key autoincrement,
	created timestamp not null default current_time,
	place text not null,
	user text not null,
	content text not null,
	status text, 
	comment text

);

-- create table products (
-- 	id integer primary key autoincrement,
-- 	name text not null,
-- 	number integer CHECK(number > 0)
-- );

-- create table users (
-- 	id integer primary key autoincrement,
-- 	username text not null unique,
-- 	password_hash text not null,
-- 	user_role boolean not null,
-- 	phone_number text not null
-- );

create table feedback (
	id integer primary key autoincrement,
	request_id integer not null,
	feedback_text text not null,
	user_id integer,
	foreign key (user_id) references users (id)
);