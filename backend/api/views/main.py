from flask import Blueprint, request
from api.models import sql_db, mongo_db
from api.core import create_response, serialize_list
import json

main = Blueprint("main", __name__)  # initialize blueprint


# function that is called when you visit /
@main.route("/")
def index():
    return "<h1>Hello World!</h1>"


@main.route("/insert", methods=["POST"])
def insert():
    data = request.json
    query = """
        INSERT INTO Professor (ID, name, department, rating_overall, rating_difficulty, rating_retake) VALUES ({}, "{}", "{}", {}, {}, {});
    """.format(
        int(data['recordId']),
        data['name'], 
        data['department'], 
        float(data['overallRating']), 
        float(data['overallDifficulty']), 
        float(data['overallRetake'])
    )
    
    with sql_db.get_db().cursor() as cursor:
        if cursor.execute(query):
            return create_response(message="Successfully inserted record")
        else:
            return create_response(status=500, message="Something went wrong")


@main.route("/update", methods=["PUT"])
def update():
    data = request.json
    
    if type(data['newVal']) == type(''):
        query = """
            UPDATE Professor
            SET {} = '{}'
            WHERE ID = {}
        """.format(data['key'], data['newVal'], int(data['recordId']))
    else:
        query = """
            UPDATE Professor
            SET {} = {}
            WHERE ID = {}
        """.format(data['key'], data['newVal'], int(data['recordId']))

    with sql_db.get_db().cursor() as cursor:
        if cursor.execute(query):
            return create_response(message="Successfully updated record")
        else:
            return create_response(status=500, message="Something went wrong")


@main.route("/delete", methods=["DELETE"])
def delete():
    deletion_id = request.json['recordId']
    print(deletion_id)
    query = """
        DELETE FROM Professor WHERE ID = {}
    """.format(int(deletion_id))

    with sql_db.get_db().cursor() as cursor:
        if cursor.execute(query):
            return create_response(message="Successfully deleted record")
        else:
            return create_response(status=500, message="Something went wrong")


@main.route("/search/<name>", methods=["GET"])
def search(name):
    prof_name = name
    query = """
        SELECT * FROM Professor WHERE name LIKE "%{}%";
    """.format(prof_name)

    with sql_db.get_db().cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

        serialized_results = []
        for res in results:
            serialized_results.append({
                "id": res[0],
                "name": res[1],
                "department": res[2],
                "rating_overall": res[3],
                "rating_difficulty": res[4],
                "rating_retake": res[5]
            })

        return create_response(data={"data": serialized_results})

@main.route("/saveschedule/<sched_name>", methods=["POST"])
def savesched(sched_name):
    data = request.json
    crn_strs = data['crns'].split(',')
    
    crns = []
    for c in crn_strs:
        crns.append(int(c))

    client = mongo_db.get_db()
    db = client['optiprof']
    sched_collection = db['schedules']

    contains_query = {
        "name": sched_name
    }

    if sched_collection.find_one(contains_query):
        update_query = {
            "$set": { "crns": crns }
        }
        sched_collection.update_one(contains_query, update_query)
    else:
        post = {
            "name": sched_name,
            "crns": crns
        }
        sched_collection.insert_one(post)

    return create_response(data={}) 

@main.route("/searchschedule/<key>", methods=["GET"])
def searchschedule(key):
    client = mongo_db.get_db()
    db = client['optiprof']
    sched_collection = db['schedules']
    result = sched_collection.find_one({"name": key}, {"_id": 0, "name": 0})
    if result:
        return create_response(data={"data": result["crns"]})
    else:
        return create_response(data={"data": []})

@main.route("/gpadata/<category>/<name>", methods=["GET"])
def gpadata(category, name):
    if category == 'department':
        query = """
            SELECT courseNumber, department, name, AVG(avgGPA) 
            FROM Course
            WHERE department = '{}' AND avgGPA > 0.0
            GROUP BY courseNumber, department, name
        """.format(name)

        with sql_db.get_db().cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

            serialized_results = []
            for res in results:
                serialized_results.append({
                    "courseNumber": res[0],
                    "department": res[1],
                    "courseName": res[2],
                    "avgGPA": res[3]
                })

            return create_response(data={"data": serialized_results})
    elif category == 'course':
        query = """
            SELECT pgpa.courseNumber, pgpa.courseDept, pgpa.courseName, pgpa.semesterTerm, p.name, pgpa.profGPA
            FROM ProfessorGPA pgpa JOIN Professor p ON pgpa.profID = p.ID
            WHERE pgpa.courseName = '{}' AND pgpa.profGPA > 0.0
        """.format(name)

        with sql_db.get_db().cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

            serialized_results = []
            for res in results:
                serialized_results.append({
                    "courseNumber": res[0],
                    "department": res[1],
                    "courseName": res[2],
                    "semesterTerm": res[3],
                    "name": res[4],
                    "avgGPA": res[5]
                })

            return create_response(data={"data": serialized_results})
    elif category == 'professor':
        query = """
            SELECT p.name, c.courseNumber, c.department, c.name, c.semesterTerm, c.avgGPA 
            FROM Professor p
            JOIN ProfessorGPA pgpa 
                ON p.ID = pgpa.profID
                AND p.name = '{}'
            JOIN Course c
                ON pgpa.courseNumber = c.courseNumber
                AND pgpa.courseDept = c.department
                AND pgpa.semesterTerm = c.semesterTerm
                AND pgpa.courseName = c.name
                AND c.avgGPA > 0.0
        """.format(name)

        with sql_db.get_db().cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

            serialized_results = []
            for res in results:
                serialized_results.append({
                    "professorName": res[0],
                    "courseNumber": res[1],
                    "department": res[2],
                    "courseName": res[3],
                    "semesterTerm": res[4],
                    "avgGPA": res[5]
                })

            return create_response(data={"data": serialized_results})

@main.route('/getSection/<crn>', methods=["GET"])
def get_section(crn):
    query = """
        SELECT 
            sectionID, 
            courseNumber, 
            courseDept, 
            semesterTerm, 
            courseName, 
            startTime,
            endTime,
            instructor
        FROM Section
        WHERE sectionID = {}
    """.format(int(crn))

    with sql_db.get_db().cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()[0]

        serialized_result = {
                "crn": results[0],
                "courseNumber": results[1],
                "department": results[2],
                "semesterTerm": results[3],
                "courseName": results[4],
                "startTime": results[5],
                "endTime": results[6],
                "professorName": results[7]
            }

        return create_response(data={"data": serialized_result})

def day_overlap(first, second):
    for day in first:
        if day in second:
            return True
    return False

def time_to_int(time):
    temp = time.split(' ')[0].split(':')
    ret = int(temp[0])*100 + int(temp[1])
    if 'P' in time:
        ret += 1200
    return ret

def time_overlap(firstStart, firstEnd, secondStart, secondEnd):
    first_start = time_to_int(firstStart)
    first_end = time_to_int(firstEnd)
    second_start = time_to_int(secondStart)
    second_end = time_to_int(secondEnd)

    return not (first_start < second_start and first_end < second_start) or (second_start < first_start and second_end < first_start)

@main.route("/schedule/<criteria>", methods=["POST"])
def generate_schedule(criteria):
    # parse course list into a string of comma separated courses
    desired_courses = request.json.get('courses', '').split(',')

    # make flaas from criteria
    prof_quality = 0
    prof_difficulty = 0
    course_gpa = 0

    if criteria == "quality":
        prof_quality = 1
    elif criteria == "difficulty":
        prof_difficulty = 1
    elif criteria == "gpa":
        course_gpa = 1
    else:
        prof_quality = 1
        prof_difficulty = 1
        course_gpa = 1

    optimal_schedule = []
    conflict_times = []

    for desired_course in desired_courses:
        course_info = desired_course.split(' ')
        department = course_info[0]
        course_number = course_info[1]
        # print(course_info)
        query = """
            SELECT * FROM Section WHERE courseNumber = {} and courseDept = "{}";
        """.format(int(course_number), department)
        
        with sql_db.get_db().cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            # print(results)

            augmented_results = []
            for res in results:
                # print(res)
                criteria_rating = 0
                if course_gpa:
                    query = """
                        SELECT AVG(profGPA) FROM ProfessorGPA WHERE courseNumber = {} and courseDept = "{}" and profID = (SELECT profID FROM Teaches WHERE sectionID = {});
                    """.format(int(res[1]), res[2], int(res[0]))

                    with sql_db.get_db().cursor() as cursor2:
                        cursor2.execute(query)
                        results2 = cursor2.fetchall()
                        criteria_rating += results2[0][0]
                        # print("After course gpa: " + str(criteria_rating))

                if prof_quality or prof_difficulty:
                    query = """
                        SELECT rating_overall, rating_difficulty FROM Professor WHERE ID = (SELECT profID FROM Teaches WHERE sectionID = {});
                    """.format(int(res[0]))
                    
                    with sql_db.get_db().cursor() as cursor2:
                        cursor2.execute(query)
                        results2 = cursor2.fetchall()

                        if prof_quality:
                            criteria_rating += results2[0][0]
                            # print("After prof quality: " + str(criteria_rating))
                        if prof_difficulty:
                            criteria_rating -= results2[0][1]
                            # print("After prof difficulty: " + str(criteria_rating))
                
                augmented_results.append((res, criteria_rating))
            
            augmented_results.sort(key = lambda x: x[1])

            i = 0
            while i < len(conflict_times):
                if day_overlap(conflict_times[i][2], augmented_results[0][0][7]) and time_overlap(conflict_times[i][0], conflict_times[i][1], augmented_results[0][0][5], augmented_results[0][0][6]):
                    augmented_results.pop(0)
                    if not augmented_results:
                        return []
                    i = 0
                i += 1

            optimal_schedule.append(augmented_results[0][0][0])
            conflict_times.append((augmented_results[0][0][5], augmented_results[0][0][6], augmented_results[0][0][7]))

    return create_response(data={"data": optimal_schedule})
