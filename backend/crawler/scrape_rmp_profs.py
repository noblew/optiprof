
def scrape_rmp_profs(school_name, sid, output_file, sleep_max = 0, write_output = False):

    init_rmp_url = "https://www.ratemyprofessors.com/filter/professor/?department=&institution=" + school_name + "&page=1&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(sid)

    initial_req = requests.get(init_rmp_url)
    initial_page = json.loads(initial_req.content)
    res_total = initial_page["searchResultsTotal"]
    n_per_page = len(initial_page["professors"])

    request_count = math.ceil(res_total // n_per_page)
    page_idx = 1

    proflist = []

    for i in range(1,request_count + 1):
        time.sleep(random.random() * sleep_max)
        rmp_url = "https://www.ratemyprofessors.com/filter/professor/?department=&institution=" + school_name + "&page=" + str(page_idx) + "&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(sid)
        curr_req = requests.get(rmp_url)
        curr_page = json.loads(curr_req.content)
        proflist = proflist + curr_page["professors"]
        print("got page ", page_idx)
        page_idx += 1

    if(write_output):
        with open('output_file', 'w') as outfile:
            json.dump(proflist, outfile)
    
    return proflist
            
school_name = "University+Of+Illinois+at+Urbana+-+Champaign"
sid = 1112

profs = scrape_rmp_profs(school_name, sid, "rmp_data.json", sleep_max = 1, write_output = True)