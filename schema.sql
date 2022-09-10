drop table requests;

create table requests (
	id integer primary key autoincrement,
	created timestamp not null default current_time,
	user text not null,
	content text not null,
	status text 

);