import csv

gpa_idx_map = {
    0: 4.0,
    1: 4.0,
    2: 3.67,
    3: 3.33,
    4: 3.00,
    5: 2.67,
    6: 2.33,
    7: 2.00,
    8: 1.67,
    9: 1.33,
    10: 1.00,
    11: 0.67,
    12: 0.00
}

def scrape_courses(dataset_path, university):
    with open(dataset_path, 'r') as dataset:
        csv_reader = csv.reader(dataset, delimiter=',')
        next(csv_reader) # skip header

        course_data = []
        for row in csv_reader:
            # course num, university name, course department/subject, semester/term, title, avg GPA 
            meta_data = row[4], university, row[3], row[2], row[5], 0.0
            course_data.append(meta_data)

        return course_data


def scrape_prof_gpas(dataset_path):
    with open(dataset_path, 'r') as dataset:
        csv_reader = csv.reader(dataset, delimiter=',')
        next(csv_reader) # skip header

        prof_data = []
        for row in csv_reader:
            # if professor exists
            if row[20]:
                # course num, course department/subject, semester/term, instructor
                meta_data = row[4], row[3], row[2], row[20], calculate_gpa(row[6:19])
                prof_data.append(meta_data)
        
        return prof_data


def calculate_gpa(gpa_arr):
    int_gpa_arr = list(map(int, gpa_arr))
    total_gpa_hrs = 0.0
    for idx, ct in enumerate(int_gpa_arr):
        total_gpa_hrs += ct * gpa_idx_map[idx]
    
    return round(total_gpa_hrs / sum(int_gpa_arr), 2)
