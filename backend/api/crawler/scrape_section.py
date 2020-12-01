import csv

def scrape_sections(csv_path):
    with open(csv_path, 'r',  encoding="utf8") as data:
        csv_reader = csv.reader(data, delimiter = ',')
        next(csv_reader)

        sections = set()

        for row in csv_reader:
            section_data = row[11], row[4], row[3], row[2], row[5], row[18], row[19], row[20], row[23]
            sections.add(section_data)

        print(len(sections), " sections from data added")
        return list(sections)

        
"""
CSV SCHEMA

0   Year
1   Term
2   YearTerm
3   Subject
4   Number
5   Name
6   Description
7   Credit Hours
8   Section Info
9   Degree Attributes
10   Schedule Information
11   CRN
12   Section
13   Status Code
14   Part of Term
15   Section Status
16   Enrollment Status
17   Type
18   Start Time
19   End Time
20   Days of Week
21   Room
22   Building
23   Instructors
"""

"""
Section Shema:

sectionID INT,
courseNumber INT,
courseDept VARCHAR(255),
semesterTerm VARCHAR(255),
courseName VARCHAR(255),
startTime VARCHAR(255),
endTime VARCHAR(255),
daysOfWeek VARCHAR(255),
instructor VARCHAR(255)
"""