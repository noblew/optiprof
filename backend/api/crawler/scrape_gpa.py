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

        course_data = set()
        for row in csv_reader:
            # course num, university name, course department/subject, semester/term, title, avg GPA 
            meta_data = row[4], university, row[3], row[2], row[5], 0.0
            course_data.add(meta_data)

        return list(course_data)


def scrape_prof_gpas(dataset_path):
    with open(dataset_path, 'r') as dataset:
        csv_reader = csv.reader(dataset, delimiter=',')
        next(csv_reader) # skip header

        prof_data = []
        for row in csv_reader:
            # if professor exists
            if row[20]:
                # course num, course department/subject, semester/term, instructor, title, gpa
                meta_data = row[4], row[3], row[2], parse_prof_name(row[20]), row[5], calculate_gpa(row[6:19])
                prof_data.append(meta_data)
        
        # calculate cumulative professor gpas if professor has taught the same course multiple times
        prof_sorted_data = sorted(prof_data, key=lambda x: (x[3], x[0], x[1], x[2], x[4]))
        return calculate_prof_gpa(prof_sorted_data)


def parse_prof_name(full_name):
    split_name = full_name.split(', ')
    last_name = split_name[0]
    first_name = split_name[1].split(' ')[0]
    return '{} {}'.format(first_name, last_name)


def calculate_gpa(gpa_arr):
    int_gpa_arr = list(map(int, gpa_arr))
    total_gpa_hrs = 0.0
    for idx, ct in enumerate(int_gpa_arr):
        total_gpa_hrs += ct * gpa_idx_map[idx]
    
    return round(total_gpa_hrs / sum(int_gpa_arr), 2)


def calculate_prof_gpa(sorted_gpa_arr):
    result = []

    # consolidate gpas of professors that have taught the same course multiple times a semester
    idx = 0
    while idx < len(sorted_gpa_arr):
        result.append(sorted_gpa_arr[idx])
        it_idx = idx + 1
        if idx >= len(sorted_gpa_arr) - 1:
            break

        while it_idx < len(sorted_gpa_arr):
            onum, odept, osem, oinstructor, title, ogpa = result[-1]
            cnum, cdept, csem, cinstructor, title, cgpa = sorted_gpa_arr[it_idx]

            # if current course and professor is the same, add the gpas together
            if cnum == onum and odept == cdept and osem == csem and oinstructor == cinstructor and title == title:
                result[-1] = (onum, odept, osem, oinstructor, title, ogpa + cgpa)
            else:
                idx = it_idx
                break

            it_idx += 1
        
        if it_idx >= len(sorted_gpa_arr):
            break
    
    # total count of the number of times a professor has taught a course
    prof_course_ct = {}
    for cnum, cdept, csem, cinstructor, title, _ in sorted_gpa_arr:
        key = (cnum, cdept, csem, cinstructor, title)
        if key in prof_course_ct:
            prof_course_ct[key] += 1
        else:
            prof_course_ct[key] = 1

    # calculate final average gpa
    for i in range(len(result)):
        cnum, cdept, csem, cinstructor, title, cgpa = result[i]
        result[i] = (
            cnum, 
            cdept, 
            csem, 
            cinstructor, 
            title,
            round(cgpa / prof_course_ct[(cnum, cdept, csem, cinstructor, title)], 2)
        )
    
    return result
