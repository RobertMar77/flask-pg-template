from flask import Flask, render_template, request, url_for;
import psycopg2;
from psycopg2.extras import RealDictCursor;
from sets import count_sets, search_sets, fav_sets, count_fav;
from util import safe_int;
import math;

conn = psycopg2.connect(
    "host=db dbname=postgres user=postgres password=postgres",
    cursor_factory=RealDictCursor);
app = Flask(__name__);

new_col_cmd = '''
alter table set
add column if not exists favorite boolean default false
''';

def update_fav(arg_name, arg_true):
    bool = "false";
    if (arg_true):
        bool = "true";
    return '''
    insert into set(''' + arg_name + ''')
    values(''' + bool + ''')
    where set_name = ""
    ''';

def get_conn():
    conn = psycopg2.connect(
    "host=db dbname=postgres user=postgres password=postgres",
    cursor_factory=RealDictCursor)
    return conn.cursor;

def set_fav(arg_name, arg_bool):
    cur = get_conn();
    with cur:
        update_fav(arg_name, arg_bool);

def do_nothing():
    return 0;


@app.route("/my-sets", methods = ["GET", "POST"])
def view_favorite_sets():
    with conn.cursor() as cur:
        results =fav_sets( cur  );

        count_fav_part=int(count_fav(cur))
        Total =(int)(count_fav_part)
        max=Total*0.15
        return render_template("my-sets.html",  results=results, max=max);

def set_favorite(arg_name):
    if arg_name != "":
        print(arg_name);
        with conn.cursor() as cur:
            cur.execute(f'''
            update set
            set favorite = true
            where cast(set.set_num as text) = %(arg)s
            ''', 
            {
                'arg': f"%{arg_name or ''}%",
            });


@app.route("/receipt", methods = ["GET", "POST"])
def view_favorite_sets_cost():
    with conn.cursor() as cur:
        results =fav_sets( cur  );

        count_fav_part=int(count_fav(cur))
        Total =(int)(count_fav_part)
        max=Total*0.15
        return render_template("receipt.html",  results=results, max=max);

def set_favorite(arg_name):
    if arg_name != "":
        print(arg_name);
        with conn.cursor() as cur:
            cur.execute(f'''
            update set
            set favorite = true
            where cast(set.set_num as text) = %(arg)s
            ''', 
            {
                'arg': f"%{arg_name or ''}%",
            });
            


@app.route("/sets", methods = ["GET", "POST"])
def search_sets_html():
    conn.autocommit = True;
    with conn.cursor() as cur:
        cur.execute(new_col_cmd);

    if request.method == "POST":
        tmp_name = request.form["favorite"];
        if tmp_name != "":
            with conn.cursor() as cur:
                cur.execute(f'''
                update set
                set favorite = true
                where cast(set.set_num as text) like %(arg)s
                ''', 
                {
                    'arg': f"%{tmp_name or ''}%",
                });
                conn.commit();
                print("Pancakes");
        tmp_name2 = request.form["nofavorite"];
        if tmp_name2 != "":
            with conn.cursor() as cur:
                cur.execute(f'''
                update set
                set favorite = false
                where cast(set.set_num as text) like %(arg)s
                ''', 
                {
                    'arg': f"%{tmp_name2 or ''}%",
                });
                conn.commit();
                print("Pancakes");
                

    set_name = request.args.get("set_name", "");
    theme_name = request.args.get("theme_name", "");
    page = safe_int(request.args.get("page"), 1);
    limit = safe_int(request.args.get("results_per_page"), 50);
    part_count_gte = safe_int(request.args.get("part_count_gte"), 0);
    part_count_lte = safe_int(request.args.get("part_count_lte"), 999999);


    sort_by = request.args.get("sort_by", "set_name");
    sort_dir = request.args.get("sort_dir", "asc");
    offset= (int(page) - 1) * int(limit);

    with conn.cursor() as cur:
        SORT_BY_PARAMS = set(["set_num", "set_name", "year", "theme_name", "part_count"]);
        SORT_DIR_PARAMS = set(["asc", "desc"]);
        
        if sort_dir not in SORT_DIR_PARAMS:
            sort_dir = "asc";
        if sort_by not in SORT_BY_PARAMS:
            sort_by = "theme_name";

        res = {};
        res["img1"] = url_for('static', filename='monument_flag.png');
        res["set_fav"] = set_favorite;

        count = count_sets(cur, set_name_contains= set_name, theme_name_contains =theme_name, part_count_gte=part_count_gte, part_count_lte=part_count_lte);
        results = search_sets(cur, set_name_contains= set_name, theme_name_contains =theme_name,  part_count_gte=part_count_gte, part_count_lte=part_count_lte, 
                            limit= limit, offset=offset, sort_by = sort_by, sort_dir = sort_dir);
        final_page = int(math.ceil(count / limit));
        
        return render_template("sets.html", count=count, results=results, set_name=set_name, theme_name=theme_name,
        page=page, limit=limit, part_count_gte = part_count_gte, 
        part_count_lte = part_count_lte, sort_by = sort_by, sort_dir = sort_dir, final_page=final_page, res=res);
       
        
