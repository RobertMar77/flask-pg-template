from psycopg2.extensions import cursor

# valid sort params for search_sets function
SORT_BY_PARAMS = set(["set_name", "year",
                     "theme_name", "part_count"])
# valid sort direction parameters for search_sets function
SORT_DIR_PARAMS = set(["asc", "desc"])


def search_sets(cur: cursor,
                set_name_contains: str,
                theme_name_contains: str,
                part_count_gte: int,
                part_count_lte: int,
                limit: int,
                offset: int,
                sort_by: str,
                sort_dir: str) -> list[dict[str, str]]:
    """
    Search the sets table with the given parameters
    """

    # these values can't easily be parameterized into the sql query, so we need to sanitize them
    # before interoplating them to protect against SQL injection
    assert int(limit) >= 0
    assert int(offset) >= 0
    assert sort_by in SORT_BY_PARAMS
    assert sort_dir in SORT_DIR_PARAMS

    cur.execute(f"""
select s.name as set_name,
    s.set_num,
    s.year,
    t.name as theme_name,
    s.num_parts as part_count,
    s.favorite
from set s
    inner join theme t on s.theme_id = t.id
where lower(s.name) like lower(%(set_name_param)s)
    and lower(t.name) like lower(%(theme_name_param)s)
    and s.num_parts >= %(part_count_gte_param)s
    and s.num_parts <= %(part_count_lte_param)s
order by {sort_by} {sort_dir}
limit {limit}
offset {offset}
    """, {
        'set_name_param': f"%{set_name_contains or ''}%",
        'theme_name_param': f"%{theme_name_contains or ''}%",
        'part_count_gte_param': int(part_count_gte),
        'part_count_lte_param': int(part_count_lte),
    })
    return list(cur)


def count_sets(cur: cursor,
               set_name_contains: str,
               theme_name_contains: str,
               part_count_gte: int,
               part_count_lte: int) -> list[dict[str, str]]:
    cur.execute("""
select count(*)
from set s
    inner join theme t on s.theme_id = t.id
where lower(s.name) like lower(%(set_name_param)s)
    and lower(t.name) like lower(%(theme_name_param)s)
    and s.num_parts >= %(part_count_gte_param)s
    and s.num_parts <= %(part_count_lte_param)s
    """, {
        'set_name_param': f"%{set_name_contains or ''}%",
        'theme_name_param': f"%{theme_name_contains or ''}%",
        'part_count_gte_param': int(part_count_gte),
        'part_count_lte_param': int(part_count_lte),
    })
    return cur.fetchone()['count']
