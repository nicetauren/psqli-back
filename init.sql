drop table solves;
drop table challenges;
drop table posts;
drop table admin;
drop table users;
drop table maker;

create table users
	(ID		    SERIAL not null,
	 name		varchar(20) NOT NULL,
	 nickname   varchar(15) NULL,
	 loginId    varchar(15) NOT NULL,
	 password   char(64) NOT NULL,
	 score      INT NULL,
	 primary key (ID)
	);

create table admin
	(ID	        SERIAL not null, 
	 name		varchar(20) NOT NULL,
	 nickname   varchar(15) NULL,
	 loginId    varchar(15) NOT NULL,
	 password   char(64) NOT NULL,
	 primary key (ID)
	);

create table maker
	(ID	        SERIAL not null, 
	 name		varchar(20) NOT NULL,
	 nickname   varchar(15) NULL,
	 loginId    varchar(15) NOT NULL,
	 password   char(64) NOT NULL,
	 primary key (ID)
	);

create table challenges
	(ID           SERIAL not null,
	title         varchar(20) NOT NULL,
	subscription  varchar(200) NULL,
	score         INT NOT NULL,
	answer        varchar(30) NOT NULL,
	mid           INT NOT NULL,
	 primary key (ID),
	 FOREIGN KEY (mid) REFERENCES maker ON DELETE SET null
	);

create table solves
	(ID         SERIAL not null,
	uid         INT NOT NULL,
	cid         INT NOT NULL,
	correctness boolean NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (uid) REFERENCES users ON DELETE SET NULL,
	FOREIGN KEY (cid) REFERENCES challenges ON DELETE SET NULL
	);

create table posts
	(ID           SERIAL not null,
	title         varchar(20) NOT NULL,
	subscription  varchar(200) NULL,
	aid           INT NOT NULL,
	 primary key (ID),
	 FOREIGN KEY (aid) REFERENCES admin ON DELETE SET null
	);

