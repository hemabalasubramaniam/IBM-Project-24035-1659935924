import ibm_db

import ConZon_Mail_config
from ConZon_Db_connection import execution, Prepare_db, execution_immediate


def admin_login_verification(name, password):
    query = "Select mail_id,password from admin_profile where mail_id = ?"
    prep_stmt = Prepare_db(query)
    ibm_db.bind_param(prep_stmt, 1, name)
    execution(prep_stmt)
    res = ibm_db.fetch_both(prep_stmt)
    if res is False:
        return 'Account Not Found 😞'
    else:
        if password == res[1]:
            return True
        else:
            return 'Password is Incorrect 🙁'


def admin_register(name, passwords, req_id):
    if req_id == '2002':
        query = "Select mail_id from admin_profile where mail_id =?;"
        prep_stmt = Prepare_db(query)
        ibm_db.bind_param(prep_stmt, 1, name)
        execution(prep_stmt)
        res = ibm_db.fetch_both(prep_stmt)
        if res is not False:
            return "⚠️Account is already available"
        else:
            query = "INSERT INTO admin_profile (mail_id,password,Hospital_ID) VALUES (?,?,?)"
            prep_stmt = Prepare_db(query)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, passwords)
            ibm_db.bind_param(prep_stmt, 3, req_id)
            execution(prep_stmt)
            ConZon_Mail_config.assing_mail('ConZo Account Creation', 'Account was successfully Created', name)
            return True

    else:
        return "Hospital ID is Incorrect 😟"


def dashboard_data():
    query = 'Select * from containment_details LIMIT 5'
    stmt = execution_immediate(query)
    dictionary = ibm_db.fetch_both(stmt)
    employee = []
    while dictionary != False:
        content = {}
        content = {'ID': dictionary[0], 'Name': dictionary[1], 'City': dictionary[2], 'Latitude': dictionary[3],
                   'Longitude': dictionary[4], 'Address': dictionary[5]}
        employee.append(content)
        content = {}
        dictionary = ibm_db.fetch_both(stmt)
    return employee


def dashboard_data_add(name, city, latitude, longitude, address):
    query = "Select address from containment_details where address = ?"
    prep_stmt = Prepare_db(query)
    ibm_db.bind_param(prep_stmt, 1, address)
    execution(prep_stmt)
    res = ibm_db.fetch_both(prep_stmt)
    if res is not False:
        return False  # "Patient Already Inserted"
    else:
        execute = "INSERT INTO containment_details (name, city, latitude, longitude, address) VALUES (?,?,?,?,?)"
        prep_stmt = Prepare_db(execute)
        ibm_db.bind_param(prep_stmt, 1, name)
        ibm_db.bind_param(prep_stmt, 2, city)
        ibm_db.bind_param(prep_stmt, 3, latitude)
        ibm_db.bind_param(prep_stmt, 4, longitude)
        ibm_db.bind_param(prep_stmt, 5, address)
        execution(prep_stmt)
        return False  # "Patient Added"


def dashboard_data_process(data):
    try:
        res_data = []
        row_len = len(data)
        col_len = len(data[0])
        for colCnt in range(col_len):
            for rowCnt in range(row_len):
                res_data.insert(rowCnt, data[rowCnt][colCnt])
            dashboard_data_add(res_data[0], res_data[1], res_data[2], res_data[3], res_data[4])
            res_data.clear()
        return True
    except():
        return False


def dashboard_data_delete(data):
    try:
        col_len = len(data[0])
        for colCnt in range(col_len):
            query = "DELETE FROM containment_details WHERE Address = ?"
            prep_stmt = Prepare_db(query)
            ibm_db.bind_param(prep_stmt, 1, data[4][colCnt])
            execution(prep_stmt)
        return True
    except():
        return False


def containmentZone():
    query = 'select COUNT(*) from containment_details'
    result = execution_immediate(query)
    res = ibm_db.fetch_both(result)
    return res[0]


def containmentZone_withoutCommon():
    query = 'select COUNT(DISTINCT LATITUDE) from containment_details'
    result = execution_immediate(query)
    res = ibm_db.fetch_both(result)
    return res[0]


print(dashboard_data())
