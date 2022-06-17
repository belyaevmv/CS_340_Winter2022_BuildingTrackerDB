from flask import Flask, render_template, json, redirect,jsonify
from flask import request

from flask_mysqldb import MySQL
from queries import DBQ

import os




app = Flask(__name__)




app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'

app.config['MYSQL_USER'] = 'cs340_belyaevm'

app.config['MYSQL_PASSWORD'] = '7233'

app.config['MYSQL_DB'] = 'cs340_belyaevm'

app.config['MYSQL_CURSORCLASS'] = "DictCursor"




mysql = MySQL(app)





# Routes


#------------------------------------------------------------------------------
# Main Pages
#------------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template("home.html")


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/buildings', methods=['POST','GET'])
def buildings():
    cur = mysql.connection.cursor()
    cur.execute(DBQ['b_query1'])
    data = cur.fetchall()

    return render_template("buildings.html", data = data)


@app.route('/floors')
def floors():
    cur = mysql.connection.cursor()
    cur.execute(DBQ['f_query1'])
    data = cur.fetchall()

    return render_template("floors.html", data = data)


@app.route('/rooms')
def rooms():
    cur = mysql.connection.cursor()
    cur.execute(DBQ['r_query1'])
    data = cur.fetchall()
    
    return render_template("rooms.html", data = data)


@app.route('/spacetypes')
def spacetypes():
    cur = mysql.connection.cursor()
    cur.execute(DBQ['st_query1'])
    data = cur.fetchall()
    
    return render_template("spacetypes.html", data = data)

@app.route('/departments')
def departments():
    cur = mysql.connection.cursor()
    cur.execute(DBQ['d_query1'])
    data = cur.fetchall()
    
    return render_template("departments.html", data = data)

@app.route('/accessories')
def accessories():
    cur = mysql.connection.cursor()
    cur.execute(DBQ['a_query1'])
    data = cur.fetchall()

    return render_template("accessories.html", data = data)

@app.route('/roomAccessories')
def room_accessories():
    cur = mysql.connection.cursor()
    cur.execute(DBQ['ra_query1'])
    data = cur.fetchall()

    return render_template("roomAccessories.html", data = data)


# ^^^ END MAIN
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Search Routes
#------------------------------------------------------------------------------

@app.route('/search_buildings', methods=['POST','GET'])
def search_buildings():
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        cur.execute(DBQ['b_query1'])
        table = cur.fetchall()
        return render_template("buildings_search.html", data = table)

    elif request.method == 'POST':
        # get values from form
        b_name = request.form['search_b_name']
        b_ad_num = request.form['search_b_address_number']
        b_ad_street = request.form['search_b_address_street']
        b_ad_state = request.form['search_b_address_state']
        b_ad_zip = request.form['search_b_address_zip']

        # concat with wild card
        b_name = "%" + b_name + "%"
        b_ad_num = "%" + b_ad_num + "%"
        b_ad_street = "%" + b_ad_street + "%"
        b_ad_state = "%" + b_ad_state + "%"
        b_ad_zip = "%" + b_ad_zip + "%"
        print(b_name, b_ad_num, b_ad_street, b_ad_state, b_ad_zip )
        data = (b_name, b_ad_num, b_ad_street, b_ad_state, b_ad_zip  ) 

        bs_query1 = """SELECT b.build_id, b.build_name, b.address_build_number,b.address_street, b.address_city, b.address_state, 
        IFNULL(b.address_zip, 'N/A'),  IFNULL(b.efficiency_factor,0)
        FROM buildings b
        WHERE b.build_name LIKE %s
        AND b.address_build_number LIKE %s
        AND b.address_street LIKE %s
        AND b.address_state LIKE %s
        AND b.address_zip LIKE %s
        GROUP BY b.build_id;"""

        cur.execute(bs_query1, data)    
        data=cur.fetchall() 

        return render_template("buildings.html", data = data)


# ^^^ END SEARCH
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Delete Routes
#------------------------------------------------------------------------------

@app.route('/delete_building/<int:build_id>', methods=['POST','GET'])
def delete_building(build_id, confirm = False):
    mydb = mysql.connection 
    cur = mydb.cursor()
    data = (build_id,)

    if request.method == 'GET':
        print("getting items to delete")
        cur.execute(DBQ['db_query1'], data)
        results = cur.fetchall()
        print(results)

        cur.execute(DBQ['b_query1'])
        table = cur.fetchall()
        return render_template("buildings_delete.html", build_id = build_id, results = results, data = table)

    elif request.method == 'POST':
        print(build_id, " - deleting item")
        result = cur.execute(DBQ['db_query2'], data)
        print(str(result) + "rows updated")
        mydb.commit()
        return redirect('/buildings')


@app.route('/delete_floor/<int:floor_id>', methods=['POST','GET'])
def delete_floor(floor_id):
    mydb = mysql.connection 
    cur = mydb.cursor()
    data = (floor_id,)

    if request.method == 'GET':
        print("getting items to delete")
        cur.execute(DBQ['df_query1'], data)
        results = cur.fetchall()
        print(results)
        cur.execute(DBQ['f_query1'])
        table = cur.fetchall()
        return render_template("floors_delete.html", floor_id=floor_id, results=results, data = table)

    elif request.method == 'POST':
        # get data for efficiency factor
        cur.execute(DBQ['bef_query4'], data)
        build_id = cur.fetchone()['build_id']

        # delete
        print(floor_id, " - deleting item")
        result = cur.execute(DBQ['df_query2'], data)
        print(str(result) + "rows updated")
        mydb.commit()

        # update efficiency factor
        update_efficiency_factor(build_id)

        return redirect('/floors')
    

@app.route('/delete_room/<int:room_id>')
def delete_room(room_id):
    mydb = mysql.connection 
    cur = mydb.cursor()
    data = (room_id,)

    cur.execute(DBQ['bef_query5'], data)
    build_id = cur.fetchone()['build_id']

    print(room_id, " - deleting item")
    result = cur.execute(DBQ['dr_query1'], data)
    print(str(result) + "rows updated")
    mydb.commit()

    #update efficiency factor
    update_efficiency_factor(build_id)
    return redirect('/rooms')


@app.route('/delete_spacetype/<int:spacetype_id>')
def delete_spacetype(spacetype_id):
    mydb = mysql.connection 
    cur = mydb.cursor()
    data = (spacetype_id,)
    print(spacetype_id, " - deleting item")

    result = cur.execute(DBQ['dsp_query1'], data)
    print(str(result) + "rows updated")
    mydb.commit()
    return redirect('/spacetypes')


@app.route('/delete_accessory/<int:accessory_id>')
def delete_accessory(accessory_id):
    mydb = mysql.connection 
    cur = mydb.cursor()
    data = (accessory_id,)
    print(accessory_id, " - deleting item")

    result = cur.execute(DBQ['da_query1'], data)
    print(str(result) + "rows updated")
    mydb.commit()
    return redirect('/accessories')


@app.route('/delete_department/<int:department_id>')
def delete_department(department_id):
    mydb = mysql.connection 
    cur = mydb.cursor()
    data = (department_id,)

    print(department_id, " - deleting item")

    result = cur.execute(DBQ['dd_query1'], data)
    print(str(result) + "rows updated")
    mydb.commit()
    return redirect('/departments')


@app.route('/delete_room_accessory/<int:room_accessory_id>')
def delete_room_accessory(room_accessory_id):
    mydb = mysql.connection 
    cur = mydb.cursor()
    data = (room_accessory_id,)

    print(room_accessory_id, " - deleting item")

    result = cur.execute(dra_query1, data)
    print(str(result) + "rows updated")
    mydb.commit()
    return redirect('/roomAccessories')

# ^^^ END DELETE
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Add Routes
#------------------------------------------------------------------------------


@app.route('/add_new_building', methods=['POST','GET'])
def add_new_building():

    mydb = mysql.connection 
    cur = mydb.cursor()
    cur.execute(DBQ['b_query1'])
    data = cur.fetchall()

    if request.method == "GET":
        return render_template('buildings_add.html', data = data)

    elif request.method == "POST":
        print('adding new building')

        b_name = request.form['building-name']
        b_number = request.form['building-address-number']
        b_street = request.form['building-address-street']
        b_city = request.form['building-address-city']
        b_state = request.form['building-address-state']
        b_zip = request.form['building-address-zip']

        print(b_name, b_number, b_street, b_city, b_state, b_zip)

        if b_zip == "" :
            b_zip = None
            print('b_zip is updated')

        data = (b_name, b_number, b_street, b_city, b_state, b_zip)

        cur.execute(DBQ['ab_query1'], data)
        mydb.commit()
        return redirect('/buildings')
    
    
@app.route('/add_new_floor', methods=['POST','GET'])
def add_new_floor():
    mydb = mysql.connection 
    cur = mydb.cursor()

    if request.method == 'GET':
        print('getting something')

        cur.execute(DBQ['f_query1'])
        data = cur.fetchall()

        cur.execute(DBQ['b_id_name_query'])
        buildings = cur.fetchall()

        return render_template("floors_add.html", data=data, buildings = buildings)

    elif request.method == 'POST':
        print('adding new floor')

        # get values from form
        f_name = request.form['floor_name']
        f_sqft = request.form['floor_sqft']
        f_building = request.form['build_id']

        data = (f_name, f_sqft, f_building)

        # run query
        cur.execute(DBQ['af_query1'], data)
        mydb.commit()

        # update building efficiency factor
        update_efficiency_factor(f_building)
    return redirect('/floors')


def update_efficiency_factor(build_id):
    print('updating efficiency')
    mydb = mysql.connection     
    cur = mydb.cursor()

    #get building to update and gross and usable sf
    building_id = (build_id,)
    cur.execute(DBQ['bef_query2'], building_id)
    data = cur.fetchone()
    print(data)

    gross_sf = data['gross_sf']
    usable_sf = data['usable_sf']

    #check for 0 division
    if gross_sf == 0 or gross_sf is None:
        efficiency_factor = 0
    else:
        efficiency_factor = usable_sf / gross_sf

    #update efficiency factor
    data = (efficiency_factor, build_id)

    result = cur.execute(DBQ['bef_query3'], data)
    mydb.commit()
    print(str(result) + "rows updated")
    


@app.route('/add_new_room', methods=['POST','GET'])
def add_new_room():
    mydb = mysql.connection 
    cur = mydb.cursor()

    if request.method == 'GET':
        print('getting something')

        cur.execute(DBQ['r_query1'])
        data = cur.fetchall()

        cur.execute(DBQ['f_id_name_query'])
        floors = cur.fetchall()

        cur.execute(DBQ['d_id_name_query'])
        departments = cur.fetchall()
        
        cur.execute(DBQ['st_id_name_query'])
        spacetypes = cur.fetchall()

        cur.execute(DBQ['b_id_name_query'])
        buildings = cur.fetchall()

        return render_template("rooms_add.html", data=data, floors = floors, departments = departments, spacetypes = spacetypes, buildings = buildings)

    elif request.method == 'POST':
        print('adding new room')

        # get values from form
        r_number = request.form['room_number']
        r_sqft = request.form['room_sqft']
        r_floor = request.form['floor_id']
        r_department = request.form['department_id']
        r_spacetype = request.form['spacetype_id']

        if r_department == "":
            r_department = None
        if r_spacetype == "":
            r_spacetype = None

        data = (r_number, r_sqft, r_floor, r_department,  r_spacetype)

        # run query
        cur.execute(DBQ['ar_query1'], data)
        mydb.commit()

        # update building efficiency factor
        r_floor = (r_floor,)
        cur.execute(DBQ['bef_query4'], r_floor)
        r_build_id = cur.fetchone()['build_id']
        update_efficiency_factor(r_build_id)

    return redirect('/rooms')


@app.route('/add_new_spacetype', methods=['POST','GET'])
def add_new_spacetype():
    mydb = mysql.connection 
    cur = mydb.cursor()

    if request.method == 'GET':
        cur.execute(DBQ['st_query1'])
        table = cur.fetchall()
        return render_template("spacetypes_add.html", data = table)

    elif request.method == 'POST':
        print('adding new spacetype')
        print(request.form)

        st_name = request.form['spacetype_name']
        st_description = request.form['spacetype_description']
        st_max_occupancy = request.form['spacetype_max_occupancy']

        data = (st_name, st_description, st_max_occupancy)

        cur.execute(DBQ['ast_query1'], data)
        mydb.commit()
        return redirect('/spacetypes')


@app.route('/add_new_accessory', methods=['POST','GET'])
def add_new_accessory():
    mydb = mysql.connection 
    cur = mydb.cursor()

    if request.method == 'GET':
        cur.execute(DBQ['a_query1'])
        data = cur.fetchall()
        return render_template("accessories_add.html", data = data)

    elif request.method == 'POST':
        print('adding new accessory')
        print(request.form)

        a_name = request.form['accessory_name']
        a_description = request.form['accessory_description']

        if a_description == "":
            a_description = None

        data = (a_name, a_description)
        cur.execute(DBQ['aa_query1'], data)
        mydb.commit()
        return redirect('/accessories')

@app.route('/add_new_department', methods=['POST','GET'])
def add_new_department():
    mydb = mysql.connection 
    cur = mydb.cursor()

    if request.method == 'GET':
        cur.execute(DBQ['d_query1'])
        table = cur.fetchall()
        return render_template("departments_add.html", data = table)

    elif request.method == 'POST':
        print('adding new department')

        d_name = request.form['department_name']
        d_chair_name = request.form['department_chair_name']
        d_contact_num = request.form['department_contact_num']
        d_contact_email = request.form['department_contact_email']
        d_current_size = request.form['department_current_size']
        d_projected_size = request.form['department_projected_size']

        data = (d_name, d_chair_name, d_contact_num, d_contact_email, d_current_size, d_projected_size)

        cur.execute(DBQ['ad_query1'], data)
        mydb.commit()
        return redirect('/departments')

@app.route('/add_new_room_accessory', methods=['POST','GET'])
def add_new_room_accessory():
    mydb = mysql.connection 
    cur = mydb.cursor()

    if request.method == 'GET':
        cur. execute(DBQ['ra_query1'])
        table = cur.fetchall()

        cur.execute(DBQ['b_id_name_query'])
        buildings = cur.fetchall()

        cur.execute(DBQ['a_id_name_query'])
        accessories = cur.fetchall()

        return render_template("roomAccessories_add.html", buildings = buildings, accessories = accessories, data = table)

    elif request.method == 'POST':
        print('adding new room accessory')
        print(request.form)

        ra_room = request.form['room_id']
        ra_accessory = request.form['accessory_id']
        ra_accessory_qty = request.form['accessory_qty']

        data = (ra_room, ra_accessory, ra_accessory_qty)
        
        cur.execute(DBQ['ara_query1'], data)
        mydb.commit()
        return redirect('/roomAccessories')

#------------------------------------------------------------------------------
#  ^^^ END ADD ROUTES


#------------------------------------------------------------------------------
# Edit Routes
#------------------------------------------------------------------------------

@app.route('/edit_building/<int:build_id>', methods=['POST','GET'])
def edit_building(build_id):
    mydb = mysql.connection 
    cur = mydb.cursor()
    data = (build_id,)

    if request.method == 'GET':
        print('Getting building to edit')
        cur.execute(DBQ['eb_query1'], data)
        build_to_edit = cur.fetchone()
        print(build_to_edit)

        if build_to_edit == None:
            return "Building is not found"

        cur.execute(DBQ['b_query1'])
        table = cur.fetchall()

        return render_template("buildings_edit.html", build_to_edit = build_to_edit, data = table)

    elif request.method == 'POST':
        print ('Updating Building')
        print(request.form)
        b_name = request.form['edit_building_name']
        b_number = request.form['edit_building_address_number']
        b_street = request.form['edit_building_address_street']
        b_city = request.form['edit_building_address_city']
        b_state = request.form['edit_building_address_state']
        b_zip = request.form['edit_building_address_zip']

        if b_zip == "" :
            b_zip = None
            print('b_zip is updated')

        data = (b_name, b_number, b_street, b_city, b_state, b_zip, build_id)
        print(data)
        result = cur.execute(DBQ['eb_query2'], data)
        mydb.commit()
        print(str(result) + "rows updated")
        return redirect('/buildings')
    

@app.route('/edit_accessory/<int:accessory_id>', methods=['POST','GET'])
def edit_accessory(accessory_id):
    mydb = mysql.connection 
    cur = mydb.cursor()
    cur.execute(DBQ['a_query1'])
    table = cur.fetchall()
    data = (accessory_id,)

    if request.method == 'GET':
        print('Getting accessory to edit')
        cur.execute(DBQ['ea_query1'], data)
        accessory_to_edit = cur.fetchone()
        print(accessory_to_edit)

        if accessory_to_edit == None:
            return "Accessory is not found"
        return render_template("accessories_edit.html", accessory_to_edit = accessory_to_edit, data = table)

    elif request.method == 'POST':
        print ('Updating Accessory')
        print(request.form)
        a_name = request.form['edit_accessory_name']
        a_description = request.form['edit_accessory_description']

        if a_description == "" or a_description == "N/A" or a_description == "n/a":
            a_description = None

        data = (a_name, a_description, accessory_id )
        print(data)
        result = cur.execute(DBQ['ea_query2'], data)
        mydb.commit()
        print(str(result) + "rows updated")
        return redirect('/accessories')


@app.route('/edit_floor/<int:floor_id>', methods=['POST','GET'])
def edit_floor(floor_id):
    mydb = mysql.connection 
    cur = mydb.cursor()
    floor_id = (floor_id,)

    if request.method == 'GET':
        print('Getting floor to edit') 
        cur.execute(DBQ['ef_query1'], floor_id)
        floor_to_edit = cur.fetchone()

        cur.execute(DBQ['b_id_name_query'])
        buildings = cur.fetchall()

        cur.execute(DBQ['f_query1'])
        table = cur.fetchall()

        if floor_to_edit == None:
            return "Floor is not found"
        return render_template("floors_edit.html", data = table, floor_to_edit = floor_to_edit, buildings = buildings)

    elif request.method == 'POST':

        print ('Updating Floor')
        print(request.form)
        f_name = request.form['edit_floor_name']
        f_sqft = request.form['edit_floor_sqft']
        f_building = request.form['edit_build_id']

        data = (f_name, f_sqft,f_building, floor_id )
        print(data)
        result = cur.execute(DBQ['ef_query2'], data)
        mydb.commit()
        print(str(result) + "rows updated")

        # update building efficiency factor
        print('updating ef factor')
        update_efficiency_factor(f_building)

        # get build_id from floor_id to check how many times 
        # efficiency factor needs to be updated
        cur.execute(DBQ['bef_query4'], floor_id)
        og_build_id = cur.fetchone()['build_id']
        print(og_build_id)

        if og_build_id != f_building:
            print('updating ef factor again')
            update_efficiency_factor(og_build_id)

        return redirect('/floors')


@app.route('/edit_room/<int:room_id>', methods=['POST','GET'])
def edit_room(room_id):
    mydb = mysql.connection 
    cur = mydb.cursor()
    data = (room_id,)

    if request.method == 'GET':
        print('Getting room to edit')
        cur.execute(DBQ['r_query1'])
        table = cur.fetchall()

        cur.execute(DBQ['er_query1'], data)
        room_to_edit = cur.fetchone()

        cur.execute(DBQ['d_id_name_query'])
        departments = cur.fetchall()

        cur.execute(DBQ['st_id_name_query'])
        spacetypes = cur.fetchall()

        cur.execute(DBQ['b_id_name_query'])
        buildings = cur.fetchall()

        if room_to_edit == None:
            return "Room is not found"
        return render_template("rooms_edit.html", data = table, room_to_edit = room_to_edit, 
        departments = departments, spacetypes=spacetypes, buildings = buildings)

    elif request.method == 'POST':
        print ('Updating Room')
        print(request.form)
        r_num = request.form['edit_room_num']
        r_sqft = request.form['edit_room_sqft']
        r_dept = request.form['edit_dept_id']
        r_spacetype = request.form['edit_spacetype_id']
        r_floor = request.form['edit_floor_id']

        if r_spacetype == "":
            r_spacetype = None
        if r_dept == "":
            r_dept = None

        data = (r_num, r_sqft, r_dept, r_spacetype, r_floor, room_id )
        print(data)
        result = cur.execute(DBQ['er_query2'], data)
        mydb.commit()
        print(str(result) + "rows updated")

        # update building efficiency factor
        r_floor = (r_floor,)
        cur.execute(DBQ['bef_query4'], r_floor)
        r_build_id = cur.fetchone()['build_id']
        update_efficiency_factor(r_build_id)

        # check if room moved from one building to another
        data = (room_id,)
        cur.execute(DBQ['bef_query5'], data)
        og_build_id = cur.fetchone()['build_id']
        if og_build_id != r_build_id:
            update_efficiency_factor(og_build_id)
        return redirect('/rooms')


@app.route('/edit_spacetypes/<int:spacetype_id>', methods=['POST','GET'])
def edit_spacetypes(spacetype_id):
    mydb = mysql.connection 
    cur = mydb.cursor()
    data = (spacetype_id,)

    if request.method == 'GET':
        print('Getting spacetypes to edit')
        ea_query1 = """SELECT spacetype_id, spacetype_name, spacetype_description, max_occupancy FROM spacetypes WHERE spacetype_id = %s ;""" 
        cur.execute(ea_query1, data)
        spacetypes_to_edit = cur.fetchone()
        print(spacetypes_to_edit)

        cur.execute(DBQ['st_query1'])
        table = cur.fetchall()

        if spacetypes_to_edit == None:
            return "Spacetype is not found"
        return render_template("spacetypes_edit.html", spacetypes_to_edit = spacetypes_to_edit, data = table)
    
    elif request.method == 'POST':
        print ('Updating Spacetypes')
        print(request.form)
        s_name = request.form['edit_spacetypes_name']
        s_description = request.form['edit_spacetypes_description']
        s_occupancy = request.form['edit_max_occupancy']

        ea_query2 = """UPDATE spacetypes SET spacetype_name = %s, spacetype_description = %s, max_occupancy = %s
        WHERE spacetype_id = %s;"""

        data = (s_name, s_description, s_occupancy, spacetype_id )
        print(data)
        result = cur.execute(ea_query2, data)
        mydb.commit()
        print(str(result) + "rows updated")
        return redirect('/spacetypes')

@app.route('/edit_department/<int:department_id>', methods=['POST','GET'])
def edit_department(department_id):
    mydb = mysql.connection 
    cur = mydb.cursor()
    data = (department_id,)

    if request.method == 'GET':
        print('Getting departments to edit')

        cur.execute(DBQ['ed_query1'], data)
        department_to_edit = cur.fetchone()
        cur.execute(DBQ['d_query1'])
        table = cur.fetchall()

        if department_to_edit == None:
            return "Department is not found"
        return render_template("departments_edit.html", data =table, department_to_edit = department_to_edit)

    elif request.method == 'POST':
        print ('Updating Departments')

        d_name = request.form['edit_department_name']
        d_chair_name = request.form['edit_department_chair_name']
        d_contact_num = request.form['edit_department_contact_num']
        d_contact_emal = request.form['edit_department_contact_email']
        d_curr_size = request.form['edit_current_dept_size']
        d_proj_size = request.form['edit_projected_dept_size']

        data = (d_name, d_chair_name, d_contact_num, d_contact_emal, d_curr_size, d_proj_size, department_id )

        result = cur.execute(DBQ['ed_query2'], data)
        mydb.commit()

        print(str(result) + "rows updated")
        return redirect('/departments')


@app.route('/edit_room_accessory/<int:room_accessory_id>', methods=['POST','GET'])
def edit_room_accessory(room_accessory_id):
    mydb = mysql.connection 
    cur = mydb.cursor()
    data = (room_accessory_id,)

    if request.method == 'GET':
        print('Getting room_accessory to edit')
        cur.execute(DBQ['ra_query1'])
        table = cur.fetchall()

        cur.execute(DBQ['era_query1'], data)
        room_accessory_to_edit = cur.fetchone()

        cur.execute(DBQ['a_id_name_query'])
        accessories = cur.fetchall()
 
        cur.execute(DBQ['b_id_name_query'])
        buildings = cur.fetchall()
        print(buildings)

        cur.execute(DBQ['f_id_name_query'])
        floors = cur.fetchall()
        print(floors)

        data = (room_accessory_to_edit['floor_id'],)
        cur.execute(DBQ['era_query5'], data)
        rooms = cur.fetchall()
        print(rooms)

        if room_accessory_to_edit == None:
            return "Room is not found"

        return render_template("roomAccessories_edit.html", data = table,
            room_accessory_to_edit = room_accessory_to_edit, buildings = buildings, 
            floors = floors, rooms = rooms, accessories = accessories)

    elif request.method == 'POST':
        print ('Updating Room_Accessory')
        print(request.form)
        ra_room = request.form['edit_room_id']
        ra_accessory = request.form['edit_accessory_id']
        ra_accessory_qty = request.form['edit_accessory_qty']


        era_query6 = """UPDATE roomaccessory SET room_id = %s, accessory_id = %s, accessory_qty = %s 
        WHERE room_accessory_id = %s;"""

        data = (ra_room, ra_accessory, ra_accessory_qty, room_accessory_id )
        print(data)
        result = cur.execute(era_query6, data)
        mydb.commit()
        print(str(result) + "rows updated")
        return redirect('/roomAccessories')


#Floors in rooms dependent drop down
@app.route('/floors/<int:build_id>', methods=['POST','GET'])
def floors_in_building(build_id):
    mydb = mysql.connection 
    cur = mydb.cursor()
    data = (build_id,)
    print("getting floors from buildng")
    fb_query1 = """SELECT floor_id, floor_name FROM floors 
    WHERE build_id = %s; """

    cur.execute(fb_query1, data)
    floors = cur.fetchall()

    floor_array = []
    for f in floors:
        floor_obj = {}
        floor_obj['id'] = f['floor_id']
        floor_obj['name'] = f['floor_name']
        floor_array.append(floor_obj)

    return jsonify({'floors': floor_array})

#Rooms in Floors dependent drop down
@app.route('/rooms/<int:floor_id>', methods=['POST','GET'])
def rooms_in_floors(floor_id):
    mydb = mysql.connection 
    cur = mydb.cursor()
    data = (floor_id,)
    print("getting rooms from floors")
    rf_query1 = """SELECT room_id, room_num FROM rooms 
    WHERE floor_id = %s; """

    cur.execute(rf_query1, data)
    rooms = cur.fetchall()

    room_array = []
    for r in rooms:
        room_obj = {}
        room_obj['id'] = r['room_id']
        room_obj['number'] = r['room_num']
        room_array.append(room_obj)

    return jsonify({'rooms': room_array})




# Listener

if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted

    app.run(port=9842, debug=True)
