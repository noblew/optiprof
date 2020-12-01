from .scrape_rmp_profs import scrape_rmp_profs
from .scrape_rmp_profs_mini import scrape_rmp_profs_mini
from .scrape_gpa import scrape_courses, scrape_prof_gpas
from .scrape_section import scrape_sections

__all__ = [
    "scrape_rmp_profs", 
    "scrape_rmp_profs_mini", 
    "scrape_courses",
    "scrape_prof_gpas",
    "scrape_sections"
]

# You must import all of the new functions you create in the crawler folder here