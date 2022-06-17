/* CS 340 - W22 Belyaev, Brinkly Step 5 Draft  */
/* FOr Data Manipulation, See project.sql for Data Defintion */

/*------------------------------------------------*/
/* ----------BUILDINGS TABLE AND QUERIES----------*/
/*------------------------------------------------*/


/*-------SELECT------ */
/* app.py line 56 b_query1  /buildings route */
SELECT b.build_id, b.build_name, b.address_build_number, b.address_street, b.address_city, b.address_state, 
    b.address_zip, IFNULL(SUM(f.floor_sqft), 0) AS gross_sf , IFNULL(SUM(r.room_sqft), 0) AS usable_sf, b.efficiency_factor
    FROM buildings b
    LEFT JOIN floors f on f.build_id = b.build_id
    LEFT JOIN rooms r on r.floor_id = f.floor_id
    GROUP BY b.build_id;

/* ------- Search -------- */
/* app.py line 179 bs_query1 /search_buildings */

SELECT b.build_id, b.build_name, b.address_build_number,b.address_street, b.address_city, b.address_state, 
    IFNULL(b.address_zip, 'N/A'),  IFNULL(b.efficiency_factor,0)
    FROM buildings b
    WHERE b.build_name LIKE %s
    AND b.address_build_number LIKE %s
    AND b.address_street LIKE %s
    AND b.address_state LIKE %s
    AND b.address_zip LIKE %s
    GROUP BY b.build_id;


/*-------DELETE------ */
/* app.py line 165 db_query1;  /delete_building route, confirm building deletion*/
SELECT b.build_name, COUNT(f.floor_id) AS floor, COUNT(r.room_id) AS room FROM buildings b
LEFT JOIN floors f on b.build_id = f.build_id
LEFT JOIN rooms r on r.floor_id = f.floor_id
WHERE b.build_id = %s;

/* app.py line 178 db_query2;  /delete_building route, delete building*/
DELETE FROM buildings WHERE build_id = %s ;

/*-------ADD NEW------ */
/* app.py line 306 ab_query1;  /add_new_building route  */
INSERT INTO buildings 
    (build_name, address_build_number, address_street, address_city, address_state, address_zip) 
    VALUES(%s, %s, %s, %s, %s, %s);

/*-------EDIT------ */
/* app.py line 609 eb_query1; /edit_building route, select building info for editing*/
SELECT build_id, build_name, address_build_number, address_street, address_city, address_state, 
        address_zip FROM buildings WHERE build_id = %s ;

/* app.py line 629 eb_query2; /edit_building route, set new values*/
UPDATE buildings SET build_name = %s, address_build_number = %s, 
    address_street = %s, address_city = %s, address_state = %s, address_zip = %s
    WHERE build_id = %s; 

/* app.py update_efficiency_factore(build_id) - Update efficiency factor after adding or updating floors or rooms tables */
/* app.py Line 372 b_query2; Calculate building gross_sf and usable_sf from build_id */
SELECT b.build_id, b.build_name, b.address_build_number, b.address_street, b.address_city, b.address_state, 
    b.address_zip, IFNULL(SUM(f.floor_sqft), 0) AS gross_sf , IFNULL(SUM(r.room_sqft), 0) AS usable_sf, b.efficiency_factor
    FROM buildings b
    LEFT JOIN floors f on f.build_id = b.build_id
    LEFT JOIN rooms r on r.floor_id = f.floor_id
    WHERE b.build_id = %s;

/* app.py Line 395 b_query3; update efficiency factore after calculation*/
UPDATE buildings SET efficiency_factor = %s WHERE build_id = %s;


/*------------------------------------------------*/
/* -----------FLOORS TABLE AND QUERIES------------*/
/*------------------------------------------------*/

/*-------SELECT------ */
/* app.py line 71 f_query1;  /floors route */
SELECT f.floor_id, f.floor_name, f.floor_sqft, b.build_name
FROM floors f INNER JOIN buildings b ON f.build_id = b.build_id
ORDER BY b.build_name, floor_name; 

/* 913 fb_query1 */
SELECT floor_id, floor_name FROM floors 
    WHERE build_id = %s; 

/*-------ADD------ */

/* app.py line 325 f_query1 /add_new_floor route - select building name and id for drop down menue*/
SELECT f.floor_id, f.floor_name, f.floor_sqft, b.build_name
    FROM floors f INNER JOIN buildings b ON f.build_id = b.build_id;

/* app.py line 328 f_query2 /add_new_floor route - select building name and id for drop down menue*/
SELECT build_id, build_name FROM buildings;

/* app.py line 351 f_query3 /add_new_floor route */
INSERT INTO floors (floor_name, floor_sqft, build_id) VALUES %s, %s, %s ;


/*-------EDIT------ */
/* 682 ef_query1 */
SELECT floor_id, floor_name, floor_sqft, build_id from floors
    WHERE floor_id = %s;

/* 688 ef_query2 */
SELECT build_id, build_name from buildings

/* 702  ea_query2*/
UPDATE floors SET floor_name = %s, floor_sqft = %s, build_id = %s 
    WHERE floor_id = %s;




/*-------DELETE------ */
/* app.py line 191 df_query1  /delete_floor method GET */
SELECT b.build_name, f.floor_id, f.floor_name, COUNT(r.room_id) AS room FROM floors f
        INNER JOIN buildings b on b.build_id = f.build_id
        INNER JOIN rooms r on r.floor_id = f.floor_id
        WHERE f.floor_id=%s;

/* app.py line 204 df_query2  /delete_floor method POST */
DELETE FROM `floors` WHERE `floors`.`floor_id` = %s;


/*------------------------------------------------*/
/* ------------ROOMS TABLE AND QUERIES------------*/
/*------------------------------------------------*/

/*-------SELECT------ */
/* app.py line 83 r_query1 /rooms route */
SELECT r.room_id, st.spacetype_name, r.room_num, r.room_sqft, d.department_name, f.floor_name, b.build_name FROM rooms r
    INNER JOIN floors f on f.floor_id = r.floor_id
    INNER JOIN buildings b on f.build_id = b.build_id
    LEFT JOIN departments d on r.department_id = d.department_id
    LEFT JOIN spacetypes st on r.spacetype_id = st.spacetype_id
    ORDER BY b.build_name, f.floor_name, r.room_num;

/* 935  rf_query1 */
SELECT room_id, room_num FROM rooms 
    WHERE floor_id = %s; 

/*-------ADD------ */
/* app.py line 408 under /add_new_room method query 1*/
SELECT r.room_id, r.room_num, r.room_sqft, d.department_name, f.floor_name, b.build_name FROM rooms r
    INNER JOIN floors f on f.floor_id = r.floor_id
    INNER JOIN buildings b on f.build_id = b.build_id
    LEFT JOIN departments d on r.department_id = d.department_id;


/* app.py line 413 under /add_new_room method GET query 2*/
SELECT  floor_id, floor_name FROM floors ORDER BY floor_name;

/* app.py line 415 under /add_new_room method GET query 3*/
SELECT department_id, department_name FROM departments;

/* app.py line 416 under /add_new_room GET method r_query4 */
SELECT spacetype_id, spacetype_name FROM spacetypes;

/* 418 r_query5 GET*/
SELECT  build_id, build_name FROM buildings ORDER BY build_name;

/* app.py line 454 under add_new_room POST method r_rquery4 */
INSERT INTO rooms (room_num, room_sqft, floor_id, department_id) VALUES (%s, %s, %s, %s);

/* app.py line 466 under add_new_room POST method r_rquery5 */
SELECT b.build_id FROM buildings b INNER JOIN floors f ON f.build_id = b.build_id 
    WHERE f.floor_id = %s


/*-------EDIT------ */
/* where is this one? did it get replaced??? */
SELECT f.floor_id, f.floor_name, f.build_id, b.build_name from floors f 
INNER JOIN buildings b on f.build_id = b.build_id WHERE f.floor_id = %s;

/* 721  er_query1 */
SELECT r.room_id, r.room_num, r.room_sqft, r.department_id, r.spacetype_id, r.floor_id, f.floor_name, b.build_id, b.build_name 
        FROM rooms r
        INNER JOIN floors f on f.floor_id = r.floor_id
        INNER JOIN buildings b on b.build_id = f.build_id
        WHERE room_id = %s ;

/* 730 er_query2 */
SELECT department_id, department_name FROM departments;

/* 735 er_query3 */
SELECT spacetype_id, spacetype_name FROM spacetypes;

/* 740  er_query4 */
SELECT build_id, build_name FROM buildings;

/* 757  er_query5*/
UPDATE rooms SET room_num = %s, room_sqft = %s, department_id = %s, spacetype_id = %s, floor_id = %s 
        WHERE room_id = %s;

/*-------DELETE------ */

/* line 217 under /delete_room/ dr_query1 */
DELETE FROM rooms WHERE room_id = %s;


/*------------------------------------------------*/
/* ---------DEPARTMENTS TABLE AND QUERIES-------- */
/*------------------------------------------------*/

/*-------SELECT------ */
/* app.py line 110 st_query1  /departments */
SELECT d.department_id, d.department_name, d.department_chair_name, d.department_contact_num, d.department_contact_email,
    d.current_dept_size, d.projected_dept_size, IFNULL(SUM(r.room_sqft), 0) AS department_sf
    FROM departments d LEFT JOIN rooms r on r.department_id = d.department_id GROUP BY d.department_id;


/*-------ADD------ */
/* line 546  ad_query1  /add_new_department  post*/
INSERT INTO departments (department_name, department_chair_name, department_contact_num, department_contact_email,
    current_dept_size, projected_dept_size) 
    VALUES %s, %s, %s, %s, %s, %s ;



/*-------EDIT------ */
/* 809 ea_query1 */
SELECT department_id, department_name, department_chair_name, department_contact_num,
            department_contact_email, current_dept_size, projected_dept_size FROM departments WHERE department_id = %s ;

/* 829  ea_query2 */
UPDATE departments SET department_name = %s, department_chair_name = %s, department_contact_num = %s,
            department_contact_email = %s, current_dept_size = %s, projected_dept_size = %s WHERE department_id = %s;

/*-------DELETE------ */
/* 259 dd_query1 */
DELETE FROM departments WHERE department_id = %s;



/*------------------------------------------------*/
/* ---------SPACETYPES TABLE AND QUERIES ---------*/
/*------------------------------------------------*/

/*-------SELECT------ */
/*app.py line 99 st_query1, /spacetypes */
SELECT * FROM spacetypes;

/*-------ADD------ */
/* app.py line 491 ast_query1, /add_spacetypes */
INSERT INTO spacetypes (spacetype_name, spacetype_description, max_occupancy) 
VALUES %s, %s, %s ;

/*-------EDIT------ */
/* 776  ea_query1 */
SELECT spacetype_id, spacetype_name, spacetype_description, max_occupancy FROM spacetypes WHERE spacetype_id = %s ;

/* 791  ea_query2 */
UPDATE spacetypes SET spacetype_name = %s, spacetype_description = %s, max_occupancy = %s
        WHERE spacetype_id = %s;

/*-------DELETE------ */
/* 231  dsp_query1*/
DELETE FROM spacetypes WHERE spacetype_id = %s;


/*------------------------------------------------*/
/* ---------ACCESSOREIS TABLE AND QUERIES ---------*/
/*------------------------------------------------*/

/*-------SELECT------ */
/*app.py line 123 a_query1, /accessories */
SELECT * FROM accessories;

/*-------ADD------ */
/* app.py line 517 aa_query1, /add_new_accessory */
INSERT INTO accessories (accessory_name, accessory_desc) 
VALUES %s, %s ;

/*-------EDIT------ */
/* 649  ea_query1 */
SELECT accessory_id, accessory_name, accessory_desc FROM accessories WHERE accessory_id = %s ;

/* 639  ea_query2 */
UPDATE accessories SET accessory_name = %s, accessory_desc = %s 
    WHERE accessory_id = %s;

/*-------DELETE------ */
/* 245  da_query1 */
DELETE FROM accessories WHERE accessory_id = %s;


/*------------------------------------------------*/
/* JOINT ROOMACCESSORIES TABLE AND QUERIES*/
/*------------------------------------------------*/

/*-------SELECT------ */
/* app.py line 134 ra_query1 */
SELECT b.build_name, f.floor_name, r.room_num, st.spacetype_name, 
    a.accessory_name, ra.accessory_qty,  ra.room_accessory_id
    FROM roomaccessory ra 
    INNER JOIN rooms r on ra.room_id = r.room_id
    INNER JOIN floors f on r.floor_id = f.floor_id
    INNER JOIN buildings b on f.build_id = b.build_id
    LEFT JOIN accessories a on ra.accessory_id = a.accessory_id
    LEFT JOIN spacetypes st on r.spacetype_id = st.spacetype_id
    ORDER BY b.build_name ASC, f.floor_name ASC, r.room_num ASC;

/*-------ADD------ */

/* 565 'GET'ra_query1*/
SELECT build_id, build_name from buildings

/* 566 ra_query2 */
SELECT accessory_id, accessory_name from accessories

/* 584 ra_query3 */
INSERT INTO roomAccessory (room_id, accessory_id, accessory_qty ) VALUES(%s, %s, %s);

/*-------EDIT------ */
/* 848 era_query1 */
SELECT ra.room_id, f.floor_id, f.floor_name, b.build_id, 
        ra.accessory_id, ra.accessory_qty, ra.room_accessory_id
        FROM roomaccessory ra
        INNER JOIN rooms r on r.room_id = ra.room_id
        INNER JOIN floors f on f.floor_id = r.floor_id
        INNER JOIN buildings b on b.build_id = f.build_id
        WHERE room_accessory_id = %s
        ;

/* 860 a_id_name_query */
SELECT accessory_id, accessory_name FROM accessories ORDER BY accessory_name;

/* 865 b_id_name_query */
SELECT build_id, build_name FROM buildings ORDER BY build_name;

/* 870 f_id_name_query  */
SELECT floor_id, floor_name FROM floors ORDER BY floor_name;

/* 875 era_query5 */
SELECT room_id, room_num FROM rooms WHERE floor_id = %s ORDER BY room_num;

/* 895 era_query6 */
UPDATE roomAccessory SET room_id = %s, accessory_id = &s, accessory_qty = %s ) WHERE room_accessory_id = %s ;

/*-------DELETE------ */
/* 273 dra_query1 */
DELETE FROM roomAccessory WHERE room_accessory_id = %s ;
