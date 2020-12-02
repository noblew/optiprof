from flask_script import Manager
from api import create_app
from api.models import mongo_db, sql_db
from api.crawler import scrape_rmp_profs_mini, scrape_rmp_profs, scrape_courses, scrape_prof_gpas, scrape_sections

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
    profs = scrape_rmp_profs(school_name, sid, "rmp_data.json", sleep_max = 1.25, write_output = False)
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
    query = "SELECT * FROM Section WHERE courseNumber=241 AND courseDept='CS' LIMIT 10;"
    with sql_db.get_db().cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        print(results)
    # res = scrape_prof_gpas('api/crawler/uiuc-gpa-dataset.csv')
    # print(res)

@manager.command
def test_select_section():
    query = "SELECT * FROM Section WHERE courseNumber = 411 AND courseDept = 'CS';"
    with sql_db.get_db().cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        print(results)

@manager.command
def test_select_teaches():
    query = "SELECT * FROM Teaches LIMIT 100;"
    with sql_db.get_db().cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        print(results)

@manager.command
def load_courses():
    courses = scrape_courses('api/crawler/uiuc-gpa-dataset.csv', 'University of Illinois at Urbana - Champaign')

    stmt = """
        INSERT IGNORE INTO Course (courseNumber, university, department, semesterTerm, name, avgGPA)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    with sql_db.get_db().cursor() as cursor:
        cursor.executemany(stmt, courses)


@manager.command
def load_prof_gpas():
    # reformat response to insert into temporary table
    prof_gpas = scrape_prof_gpas('api/crawler/uiuc-gpa-dataset.csv')
    reformatted_prof_gpas = []
    for cnum, cdept, csem, cinstructor, title, cgpa in prof_gpas:
        reformatted_prof_gpas.append((cinstructor, cnum, cdept, csem, title, cgpa))

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
                courseName VARCHAR(255),
                cumulativeGPA REAL
            );
        """)

    stmt = """
        INSERT INTO ProfTemp (name, courseNum, courseDept, courseSem, courseName, cumulativeGPA)
        VALUES (%s, %s, %s, %s, %s, %s)
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
                pgpa.courseName as courseName,
                pgpa.cumulativeGPA as cumulativeGPA
            FROM Professor p JOIN ProfTemp pgpa ON p.name = pgpa.name;
        """)

        cursor.execute("""
            INSERT INTO ProfessorGPA (profID, courseNumber, courseDept, semesterTerm, courseName, profGPA)
            SELECT ID, courseNum, courseDept, courseSem, courseName, cumulativeGPA
            FROM pgpa_joined;
        """)

        cursor.execute("""
            DROP TEMPORARY TABLE IF EXISTS pgpa_joined;
        """)

        cursor.execute("""
            DROP TEMPORARY TABLE IF EXISTS ProfTemp;
        """)

@manager.command
def load_sections():

    sections = scrape_sections('api/crawler/2020-sp.csv')

    with sql_db.get_db().cursor() as cursor:
        cursor.execute("""
            DROP TEMPORARY TABLE IF EXISTS SectionTemp;
        """)

        cursor.execute("""
            CREATE TEMPORARY TABLE IF NOT EXISTS SectionTemp (
                sectionID INT,
                courseNumber INT,
                courseDept VARCHAR(255),
                semesterTerm VARCHAR(255),
                courseName VARCHAR(255),
                startTime VARCHAR(255),
                endTime VARCHAR(255),
                daysOfWeek VARCHAR(255),
                instructor VARCHAR(255)
            );
        """)

    stmt = """ 
        INSERT INTO SectionTemp (sectionID, courseNumber, courseDept, semesterTerm, courseName, startTime, endTime, daysOfWeek, instructor)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    with sql_db.get_db().cursor() as cursor:
        cursor.executemany(stmt, sections)
        cursor.execute("""
            DROP TEMPORARY TABLE IF EXISTS sec_crs_joined;
        """)

        cursor.execute("""
            CREATE TEMPORARY TABLE IF NOT EXISTS sec_crs_joined
            SELECT 
                Stemp.sectionID as sectionID, 
                C.courseNumber as courseNumber, 
                C.department as courseDept,
                C.semesterTerm as semesterTerm,
                C.name as courseName,
                Stemp.startTime as startTime,
                Stemp.endTime as endTime,
                Stemp.daysOfWeek as daysOfWeek,
                Stemp.instructor as instructor
            FROM Course C JOIN SectionTemp Stemp ON 
                C.semesterTerm = Stemp.semesterTerm AND
                C.name = Stemp.courseName AND
                C.department = Stemp.courseDept AND
                C.courseNumber = Stemp.courseNumber;
        """)

        cursor.execute("""
            INSERT IGNORE INTO Section (sectionID, courseNumber, courseDept, semesterTerm, courseName, startTime, endTime, daysOfWeek, instructor)
            SELECT sectionID, courseNumber, courseDept, semesterTerm, courseName, startTime, endTime, daysOfWeek, instructor
            FROM sec_crs_joined;
        """)

        cursor.execute("""
            DROP TEMPORARY TABLE IF EXISTS sec_crs_joined;
        """)

        cursor.execute("""
            DROP TEMPORARY TABLE IF EXISTS SectionTemp;
        """)

@manager.command
def load_teaches():
    with sql_db.get_db().cursor() as cursor:

        cursor.execute("""
            DROP TEMPORARY TABLE IF EXISTS sec_prof_joined;
        """)

        cursor.execute("""
            DROP TEMPORARY TABLE IF EXISTS prof_name_fix;
        """)

        cursor.execute("""
            CREATE TEMPORARY TABLE IF NOT EXISTS prof_name_fix
            SELECT
                *,
                SUBSTRING(S.instructor, 1, 1) AS firstInitial,
                SUBSTRING(S.instructor, 3, 30) AS lastname
            FROM Section S
        """)  

        cursor.execute("""
            CREATE TEMPORARY TABLE IF NOT EXISTS sec_prof_joined
            SELECT
                S.sectionID as sectionID,
                P.ID as profID
            FROM Professor P JOIN prof_name_fix S ON
                P.name LIKE CONCAT(S.firstInitial, '%', S.lastname)
        """)

        test_query = 'SELECT * FROM sec_prof_joined LIMIT 20'
        cursor.execute(test_query)
        result = cursor.fetchall()
        print(result)

        cursor.execute(""" 
            INSERT IGNORE INTO Teaches (sectionID, profID)
            SELECT sectionID, profID
            FROM sec_prof_joined
        """)

        cursor.execute("""
            DROP TEMPORARY TABLE IF EXISTS sec_prof_joined;
        """)

        cursor.execute("""
            DROP TEMPORARY TABLE IF EXISTS prof_name_fix;
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

        # cursor.execute("""
        #     DROP TABLE IF EXISTS Section;
        # """)

        cursor.execute("""
            DROP TABLE IF EXISTS WorksFor;
        """)

        # cursor.execute("""
        #     DROP TABLE IF EXISTS Teaches;
        # """)
    
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
                PRIMARY KEY (courseNumber, department, semesterTerm, name),
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
                courseName VARCHAR(255),
                profGPA REAL,
                FOREIGN KEY (profID) REFERENCES Professor (ID)
                    ON DELETE SET NULL
                    ON UPDATE CASCADE,
                FOREIGN KEY (courseNumber, courseDept, semesterTerm, courseName) REFERENCES Course (courseNumber, department, semesterTerm, name)
                    ON DELETE SET NULL
                    ON UPDATE CASCADE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Section (
                sectionID INT,
                courseNumber INT,
                courseDept VARCHAR(255),
                semesterTerm VARCHAR(255),
                courseName VARCHAR(255),
                startTime VARCHAR(255),
                endTime VARCHAR(255),
                daysOfWeek VARCHAR(255),
                instructor VARCHAR(255),
                PRIMARY KEY (sectionID),
                FOREIGN KEY (courseNumber, courseDept, semesterTerm, courseName) REFERENCES Course (courseNumber, department, semesterTerm, name)
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
            DROP TRIGGER IF EXISTS gpaInsert;
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
