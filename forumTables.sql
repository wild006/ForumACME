CREATE TABLE IF NOT EXISTS USER(
	id INTEGER NOT NULL AUTO_INCREMENT,
	nom varchar(50) NOT NULL, 
	prenom varchar(50), 
	username varchar(100), 
	passwd varchar(255), 
	mail varchar(120),  
	PRIMARY KEY ( id ))ENGINE = innoDB CHARACTER SET utf8 COLLATE utf8_general_ci;
	
CREATE TABLE IF NOT EXISTS SUJET(
	id INTEGER NOT NULL AUTO_INCREMENT, 
	nom varchar(50), 
	date DATETIME, 
	user varchar(100), 
	parent INTEGER REFERENCES SUJET(id), 
	PRIMARY KEY ( id ))ENGINE = innoDB CHARACTER SET utf8 COLLATE utf8_general_ci;
	
CREATE TABLE IF NOT EXISTS MESSAGE(
	id INTEGER NOT NULL AUTO_INCREMENT,
	texte varchar(1337),
	date DATETIME,
	reponse INTEGER REFERENCES MESSAGE(id),
	user varchar(100),
	sujet INTEGER REFERENCES SUJET(id),
	PRIMARY KEY(id))ENGINE = innoDB CHARACTER SET utf8 COLLATE utf8_general_ci;
	
	
	
