from flask_script import Manager
from api import create_app
from api.models import mongo_db, sql_db
from api.crawler import scrape_rmp_profs_mini, scrape_rmp_profs, scrape_courses, scrape_prof_gpas

# sets up the app
app = create_app()

manager = Manager(app)


@manager.command
def runserver():
    app.run(debug=True, host="0.0.0.0", port=5000)


@manager.command
def runworker():
    app.run(debug=False)


@manager.command
def load_profs():
    school_name = "University+Of+Illinois+at+Urbana+-+Champaign"
    sid = 1112
    with sql_db.get_db().cursor() as cursor:
        cursor.execute("""
            INSERT INTO University VALUES ("University Of Illinois at Urbana - Champaign");
        """)

    # profs = scrape_rmp_profs_mini(school_name, sid, "rmp_data_mini.json", sleep_max = 1.5, write_output = False)
    profs = scrape_rmp_profs(school_name, sid, "rmp_data.json", sleep_max = 1.5, write_output = False)
    tuple_prof_data = []
    for prof in profs:
        tuple_prof_data.append((
            prof['tid'],
            '{} {}'.format(prof['tFname'], prof['tLname']),
            prof['tDept'],
            prof['overall_rating'],
            prof['difficulty'],
            prof['would_take_again_pct']
        ))
    
    stmt = """
        INSERT INTO Professor (ID, name, department, rating_overall, rating_difficulty, rating_retake) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    with sql_db.get_db().cursor() as cursor:
        cursor.executemany(stmt, tuple_prof_data)


@manager.command
def test_select():
    query = "SELECT * FROM Professor;"
    with sql_db.get_db().cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        print(len(results), results)
    # res = scrape_prof_gpas('api/crawler/uiuc-gpa-dataset.csv')
    # print(res)


@manager.command
def load_courses():
    courses = scrape_courses('api/crawler/uiuc-gpa-dataset.csv', 'University of Illinois at Urbana - Champaign')
    courses = list(set(courses))

    stmt = """
        INSERT INTO Course (courseNumber, university, department, semesterTerm, name, avgGPA)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    with sql_db.get_db().cursor() as cursor:
        cursor.executemany(stmt, courses)


@manager.command
def load_prof_gpas():
    # reformat response to insert into temporary table
    prof_gpas = scrape_prof_gpas('api/crawler/uiuc-gpa-dataset.csv')
    reformatted_prof_gpas = []
    for cnum, cdept, csem, cinstructor, cgpa in prof_gpas:
        reformatted_prof_gpas.append(cinstructor, cnum, cdept, csem, cgpa)

    with sql_db.get_db().cursor() as cursor:
        cursor.execute("""
            DROP TEMPORARY TABLE IF EXISTS ProfTemp;
        """)

        cursor.execute("""
            CREATE TEMPORARY TABLE IF NOT EXISTS ProfTemp (
                name VARCHAR(255),
                courseNum INT,
                courseDept VARCHAR(255),
                courseSem VARCHAR(255),
                cumulativeGPA REAL,
                PRIMARY KEY(name)
            );
        """)

    stmt = """
        INSERT INTO ProfTemp (name, courseNum, courseDept, courseSem, cumulativeGPA)
        VALUES (%s, %s, %s, %s, %s)
    """

    with sql_db.get_db().cursor() as cursor:
        cursor.executemany(stmt, reformatted_prof_gpas)
        cursor.execute("""
            DROP TEMPORARY TABLE IF EXISTS pgpa_joined;
        """)  

        # join with professor table to get the professor id
        cursor.execute("""
            CREATE TEMPORARY TABLE IF NOT EXISTS pgpa_joined
            SELECT 
                p.ID as ID, 
                p.name as name, 
                pgpa.courseNum as courseNum,
                pgpa.courseDept as courseDept,
                pgpa.courseSem as courseSem,
                pgpa.cumulativeGPA as cumulativeGPA
            FROM Professor p JOIN ProfTemp pgpa ON p.name = pgpa.name;
        """)

        cursor.execute("""
            INSERT INTO ProfessorGPA (profID, courseNumber, courseDept, semesterTerm, profGPA)
            SELECT ID, courseNum, courseDept, courseSem, cumulativeGPA
            FROM pgpa_joined;
        """)


@manager.command
def recreate_db():
    """
    Drops existing database and data and creates a fresh database.
    Note this should only be run once in production.
    """
    with sql_db.get_db().cursor() as cursor:
        # cursor.execute("""
        #     DROP DATABASE IF EXISTS optiprof;
        # """)

        cursor.execute("""
            DROP TABLE IF EXISTS ProfessorGPA;
        """)

        cursor.execute("""
            DROP TABLE IF EXISTS Section;
        """)

        cursor.execute("""
            DROP TABLE IF EXISTS Course;
        """)

        cursor.execute("""
            DROP TABLE IF EXISTS WorksFor;
        """)

        cursor.execute("""
            DROP TABLE IF EXISTS University;
        """)

        cursor.execute("""
            DROP TABLE IF EXISTS Teaches;
        """)
    
    createschema()


def createschema():
    """
    Creates SQL Schema in remote AWS instance. Uses existence checks
    in the case that this command is run multiple times.
    """
    with sql_db.get_db().cursor() as cursor:
        cursor.execute("""
            CREATE DATABASE IF NOT EXISTS optiprof;
        """)

        cursor.execute("""
            USE optiprof;
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Professor (
                ID INT,
                name VARCHAR(255),
                department VARCHAR(255),
                rating_overall REAL,
                rating_difficulty REAL,
                rating_retake REAL,
                PRIMARY KEY (ID)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS University (
                name VARCHAR(255),
                PRIMARY KEY (name)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Course (
                courseNumber INT,
                university VARCHAR(255),
                department VARCHAR(255),
                semesterTerm VARCHAR(255),
                name VARCHAR(255),
                avgGPA REAL,
                PRIMARY KEY (courseNumber, department, semesterTerm),
                FOREIGN KEY (university) REFERENCES University (name)
                    ON DELETE SET NULL
                    ON UPDATE CASCADE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ProfessorGPA (
                profID INT,
                courseNumber INT,
                courseDept VARCHAR(255),
                semesterTerm VARCHAR(255),
                profGPA REAL,
                FOREIGN KEY (courseNumber, courseDept, semesterTerm) REFERENCES Course (courseNumber, department, semesterTerm)
                    ON DELETE SET NULL
                    ON UPDATE CASCADE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Section (
                sectionID INT,
                courseNumber INT,
                startTime TIME,
                endTime TIME,
                PRIMARY KEY (sectionID),
                FOREIGN KEY (courseNumber) REFERENCES Course (courseNumber)
                    ON DELETE SET NULL
                    ON UPDATE CASCADE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Teaches (
                sectionID INT,
                profID INT,
                PRIMARY KEY (sectionID)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS WorksFor (
                university VARCHAR(255),
                profID INT,
                FOREIGN KEY (university) REFERENCES University (name)
                    ON DELETE SET NULL
                    ON UPDATE CASCADE,
                FOREIGN KEY (profID) REFERENCES Professor (ID)
                    ON DELETE SET NULL
                    ON UPDATE CASCADE
            );
        """)

        # existence check for trigger
        cursor.execute("""
            DROP TRIGGER IF EXISTS gpaUpdate;
        """)

        # after insert, write SQL query to figure out average after group by
        cursor.execute("""
            CREATE TRIGGER gpaInsert
                AFTER INSERT ON ProfessorGPA
                    FOR EACH ROW
                BEGIN
                    DECLARE newAvg REAL DEFAULT 0.0;
                    IF (EXISTS(
                        SELECT c.courseNumber, c.department, c.semesterTerm
                        FROM Course c
                        WHERE c.courseNumber = new.courseNumber AND c.department = new.courseDept AND c.semesterTerm = new.semesterTerm
                    )) THEN
                        SET newAvg = (
                            SELECT AVG(profGPA) 
                            FROM ProfessorGPA pgpa
                            WHERE pgpa.courseNumber = new.courseNumber AND pgpa.courseDept = new.courseDept AND pgpa.semesterTerm = new.semesterTerm
                            GROUP BY courseNumber, courseDept, semesterTerm
                        );
                        UPDATE Course c SET avgGPA = newAvg WHERE c.courseNumber = new.courseNumber AND c.department = new.courseDept AND c.semesterTerm = new.semesterTerm;
                    END IF;
                END;
        """)


if __name__ == "__main__":
    manager.run()
