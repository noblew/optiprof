from flask_script import Manager
from api import create_app
from api.models import mongo_db, sql_db

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
            CREATE TABLE IF NOT EXISTS ProfessorGPA (
                profID INT,
                courseNumber INT,
                courseDept VARCHAR(255),
                studentCount INT,
                profGPA REAL,
                FOREIGN KEY (courseNumber, courseDept) REFERENCES Course (courseNumber, department)
                    ON DELETE SET NULL
                    ON UPDATE CASCADE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Course (
                courseNumber INT,
                department VARCHAR(255),
                name VARCHAR(255),
                avgGPA REAL,
                PRIMARY KEY (courseNumber, department)
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

        # existence check for trigger
        cursor.execute("""
            DROP TRIGGER IF EXISTS gpaUpdate;
        """)

        cursor.execute("""
            CREATE TRIGGER gpaInsert
                AFTER INSERT ON ProfessorGPA
                    FOR EACH ROW
                BEGIN
                    DECLARE newAvg REAL DEFAULT 0.0;
                    IF (EXISTS(
                        SELECT c.courseNumber, c.department 
                        FROM Course c
                        WHERE c.courseNumber = new.courseNumber AND c.department = new.courseDept
                    )) THEN
                        SET newAvg = SELECT AVG(profGPA * studentCount) FROM ProfessorGPA GROUP BY courseNumber, courseDept;
                        UPDATE Course c SET avgGPA = newAvg WHERE c.courseNumber = new.courseNumber AND c.department = new.courseDept;
                    END IF;
                END;
        """)

        cursor.execute("""
            CREATE TRIGGER gpaUpdate
                AFTER UPDATE ON ProfessorGPA
                    FOR EACH ROW
                BEGIN
                    DECLARE newAvg REAL DEFAULT 0.0;
                    IF (EXISTS(
                        SELECT c.courseNumber, c.department 
                        FROM Course c
                        WHERE c.courseNumber = new.courseNumber AND c.department = new.courseDept
                    )) THEN
                        SET newAvg = SELECT AVG(profGPA * studentCount) FROM ProfessorGPA GROUP BY courseNumber, courseDept;
                        UPDATE Course c SET avgGPA = newAvg WHERE c.courseNumber = new.courseNumber AND c.department = new.courseDept;
                    END IF;
                END;
        """)


if __name__ == "__main__":
    manager.run()
