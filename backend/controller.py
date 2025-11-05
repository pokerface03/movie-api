from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_conn = {
    "dbname": "movies_db",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432",
}


@app.get("/movies")
def get_movies(director: str = Query("", alias="q")):
    try:

        conn = psycopg2.connect(**db_conn)
        cur = conn.cursor(cursor_factory=RealDictCursor)

        if director:
            query = """
                SELECT id, title, director
                FROM movies
                WHERE LOWER(director) LIKE %s;
            """
            cur.execute(query, (f"%{director.lower()}%",))
        else:
            raise Exception("director: paramenter not found")
        
        movies = cur.fetchall()
        print(movies)
        cur.close()
        conn.close()

        return movies
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/movies")
def add_movie(movie: dict):
    try:

        conn = psycopg2.connect(**db_conn)
        cur = conn.cursor()
        
        if "title" not in movie or "director" not in movie:
            return JSONResponse(
                status_code=400,
                content={"error": "Missing required keys: 'title' and/or 'director'"}
            )

        query = """
            INSERT INTO movies (title, director)
            VALUES (%s, %s);
        """

        cur.execute(query, (movie["title"], movie["director"]))

        conn.commit()

        cur.close()
        conn.close()

        return {"message": "Movie added successfully"}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
