import csv

def scrape_sections(csv_path):
    with open(csv_path, 'r') as data:
        csv_reader = csv.reader(data, delimiter = ',')
        next(csv_reader)

        sections = []
        for row in csv_reader:
            section_data = row[11], row[4], row[3], row[1], row[5], row[21], row[22], row[23], row[26]
            sections.append(section_data)

        return sections

        
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
15   Section Title
16   Section Credit Hours
17   Section Status
18   Enrollment Status
19   Type
20   Type Code
21   Start Time
22   End Time
23   Days of Week
24   Room
25   Building
26   Instructors
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
"""