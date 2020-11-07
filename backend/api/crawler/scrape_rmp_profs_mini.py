def scrape_rmp_profs_mini(school_name, sid, output_file, sleep_max = 1, write_output = False):

    #get first json object response with count of profs and output length per req
    init_rmp_url = "https://www.ratemyprofessors.com/filter/professor/?department=&institution=" + school_name + "&page=1&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(sid)

    initial_req = requests.get(init_rmp_url)
    initial_page = json.loads(initial_req.content)
    res_total = initial_page["searchResultsTotal"]
    n_per_page = len(initial_page["professors"])

    request_count = math.ceil(res_total // n_per_page)
    page_idx = 1

    proflist = []

    #get basic prof json objects
    for i in range(1,10):
        time.sleep(random.random() * sleep_max)
        rmp_url = "https://www.ratemyprofessors.com/filter/professor/?department=&institution=" + school_name + "&page=" + str(page_idx) + "&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(sid)
        curr_req = requests.get(rmp_url)
        curr_page = json.loads(curr_req.content)
        proflist = proflist + curr_page["professors"]
        print("got page ", page_idx)
        page_idx += 1
    
    #get additional prof attributes from individual prof pages
    for prof in proflist:
        time.sleep(random.random() * sleep_max)
        prof_id = prof["tid"]
        prof_page_url = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + str(prof_id)
        prof_req = requests.get(prof_page_url)
        prof_page = BeautifulSoup(prof_req.content, 'html.parser')
        stats = prof_page.findAll("div", {"class" : lambda L: L and L.startswith('FeedbackItem__FeedbackNumber-uof32n-1')})
        prof["would_take_again_pct"] = -1
        prof["difficulty"] = -1
        for s in stats:
            if(s.contents[0][-1] == "%"):
                prof["would_take_again_pct"] = int(s.contents[0][:-1])
            else:
                prof["difficulty"] = float(s.contents[0])
        print("got prof ", prof["tLname"])

    #write to output json file
    if(write_output):
        with open(output_file, 'w') as outfile:
            json.dump(proflist, outfile)
    
    return proflist

school_name = "University+Of+Illinois+at+Urbana+-+Champaign"
sid = 1112

mini = scrape_rmp_profs_mini(school_name, sid, "rmp_data_mini.json", sleep_max = 1.5, write_output = True)