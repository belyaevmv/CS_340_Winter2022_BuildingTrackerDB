/* CS 340 - W22 Belyaev, Brinkly Step 5 Draft  */
/* for Data Definition, see DML_Queries.sql for data manipulation */

<<<<<<< HEAD
SET FOREIGN_KEY_CHECKS=0;

/*------------------------------------------------*/
/* ----------BUILDINGS TABLE AND QUERIES----------*/
/*------------------------------------------------*/

CREATE TABLE buildings (
    build_id INT(11) AUTO_INCREMENT NOT NULL, 
    build_name VARCHAR(255) NOT NULL UNIQUE, 
    address_build_number VARCHAR(255) NOT NULL,
    address_street VARCHAR(255) NOT NULL, 
    address_city VARCHAR(255) NOT NULL, 
    address_state VARCHAR(2) NOT NULL,
    address_zip INT, 
    efficiency_factor DEC(3,2) DEFAULT NULL,
    CONSTRAINT zip_length CHECK (address_zip >=10000 AND address_zip <= 99999),
    PRIMARY KEY(build_id)
    ) engine=innodb;


/* Insert data buildings table*/
INSERT INTO buildings 
    (build_name, address_build_number, address_street, address_city, address_state, address_zip) 
    VALUES("big building", "12", "wide street", "Atlanta", "GA", 30253);


/*------------------------------------------------*/
/* -----------FLOORS TABLE AND QUERIES------------*/
/*------------------------------------------------*/

CREATE TABLE floors (
    floor_id INT(11) AUTO_INCREMENT NOT NULL, 
    floor_name VARCHAR(3) NOT NULL, 
    floor_sqft INT NOT NULL,
    build_id INT NOT NULL,
    CONSTRAINT one_floor UNIQUE (build_id, floor_name),
    PRIMARY KEY(floor_id),
    FOREIGN KEY(build_id) REFERENCES buildings(build_id) ON DELETE CASCADE
    ) engine=innodb;


INSERT INTO floors (floor_name, floor_sqft, build_id) VALUES
    (1, 11000, 1),
    (2, 11000, 1),
    (3, 11000, 1);


/*------------------------------------------------*/
/* ------------ROOMS TABLE AND QUERIES------------*/
/*------------------------------------------------*/

CREATE TABLE rooms (
    room_id INT(11) AUTO_INCREMENT NOT NULL, 
    room_num VARCHAR(10) NOT NULL, 
    room_sqft INT NOT NULL,
    floor_id INT NOT NULL,
    department_id INT,
    spacetype_id INT,
    PRIMARY KEY(room_id),
    FOREIGN KEY(floor_id) REFERENCES floors(floor_id) ON DELETE CASCADE,
    FOREIGN KEY(department_id) REFERENCES departments(department_id) ON DELETE SET NULL,
    FOREIGN KEY(spacetype_id) REFERENCES spacetypes(spacetype_id) ON DELETE SET NULL,
    CONSTRAINT room_floor UNIQUE (room_num, floor_id)
    ) engine=innodb;


INSERT INTO rooms (room_num, room_sqft, floor_id, department_id, spacetype_id) VALUES
    ("101", 100, 1, 1, 1),
    ("102", 200, 1, 1, 1),
    ("103", 300, 1, 2, 2),
    ("201", 100, 1, 3, 2),
    ("201A", 100, 1, 3, 2),
    ("202", 100, 1, 3, 1);

/*------------------------------------------------*/
/* ---------DEPARTMENTS TABLE AND QUERIES-------- */
/*------------------------------------------------*/

CREATE TABLE departments (
    department_id INT(11) AUTO_INCREMENT NOT NULL, 
    department_name VARCHAR(100) NOT NULL UNIQUE, 
    department_chair_name VARCHAR(250) NOT NULL,
    department_contact_num INT NOT NULL, 
    department_contact_email VARCHAR(250) NOT NULL,
    current_dept_size INT,
    projected_dept_size INT,
    CONSTRAINT contact_num_length CHECK (department_contact_num >=1000000000 AND department_contact_num <= 9999999999),
    PRIMARY KEY(department_id)
    ) engine=innodb;


INSERT INTO departments (department_name, department_chair_name, department_contact_num, department_contact_email,
    current_dept_size, projected_dept_size) VALUES
    ("Computer Science", "Bill Gates", 6788761111, "gates@bill.ms", 100, 1000),
    ("English Literature", "William Shakespeare", 5192821212, "bshakes@highnmighty.edu", 2, 15),
    ("Physics", "Albert Enstien", 3605551234, "al_u238@losalamos.gov", 99, 98);

/*------------------------------------------------*/
/* ---------SPACETYPES TABLE AND QUERIES ---------*/
/*------------------------------------------------*/

CREATE TABLE spacetypes (
    spacetype_id INT(11) AUTO_INCREMENT NOT NULL, 
    spacetype_name VARCHAR(50) NOT NULL, 
    spacetype_description VARCHAR(250) NOT NULL,
    max_occupancy INT, 
    PRIMARY KEY(spacetype_id)
    ) engine=innodb;


INSERT INTO spacetypes (spacetype_name, spacetype_description, max_occupancy) VALUES
    ("Office",  "Generic Office Space", 1),
    ("PhysicsLab", "Physics Lab space", 20),
    ("CSLobby", "Computer Science Main Lobby", NULL);



/*------------------------------------------------*/
/* ------- ACCESSORIES TABLE AND QUERIES ---------*/
/*------------------------------------------------*/

CREATE TABLE accessories (
    accessory_id INT(11) AUTO_INCREMENT NOT NULL, 
    accessory_name VARCHAR(250) UNIQUE NOT NULL,
    accessory_desc VARCHAR(250),
    PRIMARY KEY(accessory_id)
    ) engine=innodb;
	
INSERT INTO accessories (accessory_name, accessory_desc) VALUES
    ("Projector", "Epson LS 300"),
    ("Sink", "Dual, hot/cold"),
    ("Lecturn", "Portable w/ AV connections"),
    ("Cabinet", "Base, fixed" );


/*------------------------------------------------*/
/* ---- JOINT ROOMACCESSORY TABLE AND QUERIES ----*/
/*------------------------------------------------*/

CREATE TABLE roomaccessory (
    room_accessory_id INT(11) AUTO_INCREMENT NOT NULL, 
    room_id INT(11) NOT NULL, 
    accessory_id INT(11) NOT NULL,
	accessory_qty INT(11) NOT NULL,	
    PRIMARY KEY(room_accessory_id),
    FOREIGN KEY(room_id) REFERENCES rooms(room_id) ON DELETE CASCADE,
    FOREIGN KEY (accessory_id) REFERENCES accessories(accessory_id) ON DELETE CASCADE
    ) engine=innodb;

INSERT INTO roomaccessory (room_id, accessory_id, accessory_qty) VALUES
    (1,1,1),
    (1,2,2),
    (2,4,2),
	(3,3,1);




/* obsoleted with roomaccessory joint table above*/
/*------------------------------------------------*/
/* -JOINT SPACETYPE-DEPARTMENTS TABLE AND QUERIES-*/
/*------------------------------------------------*/

CREATE TABLE spacetype_dept (
    spacetype_dept_id INT(11) AUTO_INCREMENT NOT NULL, 
    department_id INT(11), 
    spacetype_id INT(11) NOT NULL, 
    PRIMARY KEY(spacetype_dept_id),
    FOREIGN KEY(department_id) REFERENCES departments(department_id) ON DELETE SET NULL,
    FOREIGN KEY (spacetype_id) REFERENCES spacetypes(spacetype_id)
    ) engine=innodb;

    INSERT INTO spacetype_dept (department_id,spacetype_id) VALUES
    (2,1),
    (3,2),
    (2,3);
    
