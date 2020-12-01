from flask import Blueprint, request
from api.models import sql_db, mongo_db
from api.core import create_response, serialize_list

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


@main.route("/gpadata/<category>/<name>")
def gpadata(category, name):
    if category == 'department':
        query = """
            SELECT courseNumber, semesterTerm, name, avgGPA 
            FROM Course
            WHERE department = '{}' AND avgGPA > 0.0
        """.format(name)

        with sql_db.get_db().cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

            serialized_results = []
            for res in results:
                serialized_results.append({
                    "courseNumber": res[0],
                    "semesterTerm": res[1],
                    "name": res[2],
                    "avgGPA": res[3]
                })

            return create_response(data={"data": serialized_results})
    elif category == 'course':
        query = """
            SELECT pgpa.courseNumber, pgpa.courseName, pgpa.semesterTerm, p.name, pgpa.profGPA
            FROM ProfessorGPA pgpa JOIN Professor p ON pgpa.profID = p.ID
            WHERE pgpa.courseName = '{}'
        """.format(name)

        with sql_db.get_db().cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

            serialized_results = []
            for res in results:
                serialized_results.append({
                    "courseNumber": res[0],
                    "courseName": res[1],
                    "semesterTerm": res[2],
                    "name": res[3],
                    "avgGPA": res[4]
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
