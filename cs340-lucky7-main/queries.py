DBQ = {

   # took out from between address_zip and b.efficiency_factor
   # IFNULL(SUM(f.floor_sqft), 0) AS gross_sf , IFNULL(SUM(r.room_sqft), 0) AS usable_sf,
   #  LEFT JOIN floors f on f.build_id = b.build_id
   #  LEFT JOIN rooms r on r.floor_id = f.floor_id
   'b_query1' : """
   SELECT b.build_id, b.build_name, b.address_build_number,b.address_street, b.address_city, b.address_state, 
   IFNULL(b.address_zip, 'N/A'),  IFNULL(b.efficiency_factor,0)
   FROM buildings b
   ORDER BY b.build_id;
   """ ,

   'f_query1' : """
   SELECT f.floor_id, f.floor_name, f.floor_sqft, b.build_name
   FROM floors f INNER JOIN buildings b ON f.build_id = b.build_id
   ORDER BY b.build_name, floor_name;
   """,

   'r_query1' : """
   SELECT r.room_id, IFNULL(st.spacetype_name, 'N/A'), r.room_num, r.room_sqft, 
   IFNULL(d.department_name, 'N/A'), f.floor_name, b.build_name FROM rooms r
   INNER JOIN floors f on f.floor_id = r.floor_id
   INNER JOIN buildings b on f.build_id = b.build_id
   LEFT JOIN departments d on r.department_id = d.department_id
   LEFT JOIN spacetypes st on r.spacetype_id = st.spacetype_id
   ORDER BY b.build_name, f.floor_name, r.room_num;
   """,

   'd_query1' : """
   SELECT d.department_id, d.department_name, d.department_chair_name, d.department_contact_num, d.department_contact_email,
   d.current_dept_size, d.projected_dept_size, IFNULL(SUM(r.room_sqft), 0) AS department_sf
   FROM departments d LEFT JOIN rooms r on r.department_id = d.department_id GROUP BY d.department_id ORDER BY d.department_name;
   """,

   'st_query1' : """
   SELECT * FROM spacetypes ORDER BY spacetype_name ;
   """,

   'a_query1' : """
   SELECT accessory_id, accessory_name, IFNULL(accessory_desc, 'N/A') as 'accessory_desc' 
   FROM accessories ORDER BY accessory_name ASC;
   """,

   'ra_query1' : """
   SELECT b.build_name, f.floor_name, r.room_num, st.spacetype_name, 
   a.accessory_name, ra.accessory_qty,  ra.room_accessory_id
   FROM roomaccessory ra 
   INNER JOIN rooms r on ra.room_id = r.room_id
   INNER JOIN floors f on r.floor_id = f.floor_id
   INNER JOIN buildings b on f.build_id = b.build_id
   LEFT JOIN accessories a on ra.accessory_id = a.accessory_id
   LEFT JOIN spacetypes st on r.spacetype_id = st.spacetype_id
   ORDER BY b.build_name ASC, f.floor_name ASC, r.room_num ASC;
   """,

   # GENERAL SELECT QUERIES FOR FORM VALUES

   'b_id_name_query' : """
   SELECT build_id, build_name FROM buildings ORDER BY build_name;
   """,

   'f_id_name_query' : """
   SELECT floor_id, floor_name FROM floors ORDER BY floor_name;
   """ ,

   'st_id_name_query' : """
   SELECT spacetype_id, spacetype_name FROM spacetypes ORDER BY spacetype_name;
   """ ,

   'd_id_name_query' : """
   SELECT department_id, department_name FROM departments;
   """, 

   'a_id_name_query' : """
   SELECT accessory_id, accessory_name FROM accessories ORDER BY accessory_name;
   """ ,

   # Building Efficiency factor
   'bef_query2' : """
   SELECT b.build_id, b.build_name, b.address_build_number, b.address_street,b.address_city, b.address_state, 
   b.address_zip, IFNULL(SUM(f.floor_sqft), 0) AS gross_sf , IFNULL(SUM(r.room_sqft), 0) AS usable_sf, b.efficiency_factor
   FROM buildings b
   LEFT JOIN floors f on f.build_id = b.build_id
   LEFT JOIN rooms r on r.floor_id = f.floor_id
   WHERE b.build_id = %s;""",

   'bef_query3' : """
   UPDATE buildings SET efficiency_factor = %s WHERE build_id = %s;
   """,

   'bef_query4' : """
   SELECT b.build_id FROM buildings b
   INNER JOIN floors f ON f.build_id = b.build_id
   WHERE f.floor_id = %s;
   """,

   'bef_query5' : """
   SELECT b.build_id FROM buildings b
   INNER JOIN floors f ON f.build_id = b.build_id
   INNER JOIN rooms r ON r.floor_id = f.floor_id
   WHERE r.room_id = %s;
   """,

   # ADD QUERIES
   'ab_query1' : """
   INSERT INTO buildings 
   (build_name, address_build_number, address_street, address_city, address_state, address_zip) 
   VALUES(%s, %s, %s, %s, %s, %s);
   """,

   'af_query1' : """
   INSERT INTO floors (floor_name, floor_sqft, build_id) VALUES (%s, %s, %s);
   """,

   "ar_query1" : """
   INSERT INTO rooms (room_num, room_sqft, floor_id, department_id, spacetype_id) VALUES ( %s, %s, %s, %s, %s ) ;
   """,

   'ara_query1' : """
   INSERT INTO roomaccessory (room_id, accessory_id, accessory_qty) 
   VALUES(%s, %s, %s);
   """,

   'ast_query1' : """
   INSERT INTO spacetypes 
   (spacetype_name, spacetype_description, max_occupancy) 
   VALUES(%s, %s, %s);
   """,

   'ad_query1' : """
   INSERT INTO departments (department_name, 
   department_chair_name, department_contact_num, department_contact_email,
   current_dept_size, projected_dept_size) 
   VALUES(%s, %s, %s, %s, %s, %s);
   """,

   'aa_query1' : """
   INSERT INTO accessories (accessory_name, accessory_desc) VALUES(%s, %s);
   """,

   # EDIT QUERIES
   'eb_query1' : """
   SELECT build_id, build_name, address_build_number, address_street, address_city, address_state, 
   address_zip FROM buildings WHERE build_id = %s ;
   """ ,

   'eb_query2' : """
   UPDATE buildings SET build_name = %s, address_build_number = %s, 
   address_street = %s, address_city = %s, address_state = %s, address_zip = %s
   WHERE build_id = %s;
   """,

   'ef_query1' : """
   SELECT floor_id, floor_name, floor_sqft, build_id from floors
   WHERE floor_id = %s;
   """,

   'ef_query2' : """
   UPDATE floors SET floor_name = %s, floor_sqft = %s, build_id = %s 
   WHERE floor_id = %s;""",
   
   'ed_query1' : """
   SELECT department_id, department_name, department_chair_name, department_contact_num,
   department_contact_email, current_dept_size, projected_dept_size FROM departments 
   WHERE department_id = %s ;
   """ ,
   
   'ed_query2' : """
   UPDATE departments SET department_name = %s, department_chair_name = %s, department_contact_num = %s,
   department_contact_email = %s, current_dept_size = %s, projected_dept_size = %s WHERE department_id = %s;
   """,

   'era_query1' : """
   SELECT ra.room_id, f.floor_id, f.floor_name, b.build_id, 
   ra.accessory_id, ra.accessory_qty, ra.room_accessory_id
   FROM roomaccessory ra
   INNER JOIN rooms r on r.room_id = ra.room_id
   INNER JOIN floors f on f.floor_id = r.floor_id
   INNER JOIN buildings b on b.build_id = f.build_id
   WHERE room_accessory_id = %s ;
   """ ,

   'era_query5' : """
   SELECT room_id, room_num FROM rooms WHERE floor_id = %s ORDER BY room_num;
   """,

   'er_query1' : """
   SELECT r.room_id, r.room_num, r.room_sqft, r.department_id, r.spacetype_id, r.floor_id, f.floor_name, b.build_id, b.build_name 
   FROM rooms r
   INNER JOIN floors f on f.floor_id = r.floor_id
   INNER JOIN buildings b on b.build_id = f.build_id
   WHERE room_id = %s ;
   """ ,

   'er_query2' : """
   UPDATE rooms SET room_num = %s, room_sqft = %s, department_id = %s, spacetype_id = %s, floor_id = %s 
   WHERE room_id = %s;
   """,

   'ea_query1' : """
   SELECT accessory_id, accessory_name, IFNULL(accessory_desc, 'N/A') as 'accessory_desc' FROM accessories WHERE accessory_id = %s ;
   """ ,

   'ea_query2' : """
   UPDATE accessories SET accessory_name = %s, accessory_desc = %s 
   WHERE accessory_id = %s;
   """,

   #delete
   'db_query1' : """
   SELECT b.build_name, COUNT(f.floor_id) AS floor, COUNT(r.room_id) AS room FROM buildings b
   LEFT JOIN floors f on b.build_id = f.build_id
   LEFT JOIN rooms r on r.floor_id = f.floor_id
   WHERE b.build_id=%s;
   """,

   'db_query2' : """
   DELETE FROM buildings WHERE build_id = %s ;
   """,

   'df_query1' : """
   SELECT b.build_name, f.floor_id, f.floor_name, COUNT(r.room_id) AS room FROM floors f
   INNER JOIN buildings b on b.build_id = f.build_id
   INNER JOIN rooms r on r.floor_id = f.floor_id
   WHERE f.floor_id=%s;
   """,

   'df_query2' : """
   DELETE FROM floors WHERE floor_id = %s ;
   """,

   'dr_query1' : """
   DELETE FROM rooms WHERE room_id = %s ;
   """,

   'dsp_query1' : """
   DELETE FROM spacetypes WHERE spacetype_id = %s 
   """,

   'da_query1' : """
   DELETE FROM accessories WHERE accessory_id = %s ;
   """,

   'dd_query1' : """
   DELETE FROM departments WHERE department_id = %s ;
   """,

   'dra_query1' : """
   DELETE FROM roomaccessory WHERE room_accessory_id = %s ;
   """
}