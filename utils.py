import sqlite3
from collections import Counter


class DbConnect:
    # with sqlite3.connect('netflix.db') as connection:
    #     cur = connection.cursor()
    #     cur.execute("")

    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def __del__(self):
        self.cur.close()
        self.con.close()

def get_by_title(title):
    db_connect = DbConnect('netflix.db')
    db_connect.cur.execute(
        f"""
        SELECT title, country, release_year, listed_in, description
        FROM netflix
        WHERE title LIKE '%{title}%'
        order by release_year desc limit 1
        """)
    result = db_connect.cur.fetchone()
    return {
		"title": result[0],
		"country": result[1],
		"release_year": result[2],
		"genre": result[3],
		"description": result[4]
}

def get_by_ages(year1, year2):
    db_connect = DbConnect('netflix.db')
    query = f"""
             SELECT title, release_year
             FROM netflix
             WHERE release_year BETWEEN {year1} AND {year2}
             LIMIT 100
             """
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
	                        "release_year": movie[1]})
    return result_list

def movies_by_rating(rating):
    db_connect = DbConnect('netflix.db')
    rating_parameters = {
        "children": "'G'",
        "family": "'G', 'PG', 'PG-13'",
        "adult": "'R', 'NC-17'"
    }

    query = f"""SELECT title, rating, description
              FROM netflix
              WHERE rating in ({rating_parameters[rating]})"""
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({
	 "title": movie[0],
	 "rating": movie[1],
	 "description": movie[2]
	})
    return result_list

def get_top_by_genre(genre):
    db_connect = DbConnect('netflix.db')
    query = f"""
    SELECT title, description
    FROM netflix
    WHERE listed_in LIKE '%{genre}%'
    ORDER BY release_year DESC 
    LIMIT 10;
    """
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({
        "title": movie[0],
        "description": movie[1]
        })
    return result_list

def two_actors(actor1, actor2):
    db_connect = DbConnect('netflix.db')
    query = f"""
    SELECT `cast`
    FROM netflix
    WHERE `cast` LIKE '%{actor1}%' AND `cast` LIKE '%{actor2}%';
    """
    result = db_connect.cur.execute(query)
    actor_list = []
    for cast in result:
        actor_list.extend(cast[0].split(', '))
    counter = Counter(actor_list)
    result_list = []
    for actor, count in counter.items():
        if actor not in [actor1, actor2] and count > 2:
            result_list.append(actor)
    return result_list

def search_movie_by_param(type, year, genre):
    db_connect = DbConnect('netflix.db')
    query = f"""
    SELECT title, description
    FROM netflix
    WHERE type = '{type}' 
    AND release_year = '{year}' 
    AND listed_in LIKE '%{genre}%'
    """
    result = db_connect.cur.execute(query)
    result_list = []
    for movie in result:
        result_list.append({'title': movie[0],
                            'description': movie[1]})
    return result_list


# cast_partners('Rose McIver', 'Ben Lamb')
print(search_movie_by_param('TV Show', '2005', 'Dramas'))