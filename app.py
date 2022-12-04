from flask import Flask, render_template, request
import psycopg2
from psycopg2.extras import RealDictCursor
from sets import count_sets, search_sets
from util import safe_int
import math

conn = psycopg2.connect(
    "host=db dbname=postgres user=postgres password=postgres",
    cursor_factory=RealDictCursor)
app = Flask(__name__)


@app.route("/sets")
def search_sets_html():
    set_name= request.args.get("set_name", "")
    theme_name= request.args.get("theme_name", "")
    page= safe_int(request.args.get("page"), 1)
    limit=safe_int(request.args.get("results_per_page"), 50)
    part_count_gte = safe_int(request.args.get("part_count_gte"), 0)
    part_count_lte = safe_int(request.args.get("part_count_lte"), 999999)
    sort_by = request.args.get("sort_by", "set_name")
    sort_dir = request.args.get("sort_dir", "asc")
    offset= (int(page) - 1) * int(limit)
    with conn.cursor() as cur:
        SORT_BY_PARAMS = set(["set_num", "set_name", "year", "theme_name", "part_count"])
        SORT_DIR_PARAMS = set(["asc", "desc"])
        
        if sort_dir not in SORT_DIR_PARAMS:
            sort_dir = "asc"
        if sort_by not in SORT_BY_PARAMS:
            sort_by = "theme_name"


        count = count_sets(cur, set_name_contains= set_name, theme_name_contains =theme_name, part_count_gte=part_count_gte, part_count_lte=part_count_lte)
        results= search_sets(cur, set_name_contains= set_name, theme_name_contains =theme_name,  part_count_gte=part_count_gte, part_count_lte=part_count_lte, 
                            limit= limit, offset=offset, sort_by = sort_by, sort_dir = sort_dir)     
        final_page =int(math.ceil(count/limit))
        
        return render_template("sets.html", count=count, results=results, set_name=set_name, theme_name=theme_name,
        page=page, limit=limit, part_count_gte = part_count_gte, 
        part_count_lte = part_count_lte, sort_by = sort_by, sort_dir = sort_dir, final_page=final_page)
       
        


