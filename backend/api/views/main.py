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
        INSERT INTO Professor (name, department, rating_overall, rating_difficulty, rating_retake) VALUES ("{}", "{}", {}, {}, {});
    """.format(
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
    query = """
        DELETE FROM Professor WHERE ID = {}
    """.format(int(deletion_id))

    with sql_db.get_db().cursor() as cursor:
        if cursor.execute(query):
            return create_response(message="Successfully deleted record")
        else:
            return create_response(status=500, message="Something went wrong")


@main.route("/search", methods=["GET"])
def search():
    prof_name = request.json['name']
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
