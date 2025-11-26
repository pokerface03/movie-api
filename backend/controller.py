from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import psycopg2
from psycopg2.extras import RealDictCursor
import redis
from dotenv import load_dotenv
import os
import json
from logger import get_logger
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client

logger = get_logger() 

app = FastAPI()

apm_config = {
    'SERVICE_NAME': 'movie-api',
    'SERVER_URL': 'http:192.168.1.122//:8200',
    'ENVIRONMENT': 'production',
}

apm = make_apm_client(apm_config)
app.add_middleware(ElasticAPM, client=apm)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()  # Load .env file

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

db_conn = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "port": DB_PORT,
}

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.get("/movies")
def get_movies(director: str = Query("", alias="q")):
    try:
        logger.info(f"GET /movies?q={director}")

        #redis cache search
        key = f"movies:{director.lower()}"
        cached = redis_client.get(key)

        if cached:
            logger.info(f"CACHE HIT for director={director}")
            return json.loads(cached)
        else:
            logger.info(f"CACHE MISS for director={director}")

        #postgress set up 
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

        #result store in redis
        redis_client.set(key, json.dumps(movies), ex=60)  

        print(movies)
        cur.close()
        conn.close()

        logger.info(f"CACHE MISS for director={director}")

        return movies
    
    except Exception as e:
        logger.error(f"Error in get_movies: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/movies")
def add_movie(movie: dict):
    try:
        logger.info(f"POST /movies body={movie}")

        conn = psycopg2.connect(**db_conn)
        cur = conn.cursor()
        
        if "title" not in movie or "director" not in movie:
            logger.warning("Invalid payload")
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

        #redis clear cache for matched patterns
        pattern = f"movies:{movie['director'].lower()}*"
        for key in redis_client.scan_iter(pattern):
            redis_client.delete(key)

        logger.info("Movie added successfully")

        return {"message": "Movie added successfully"}

    except Exception as e:
        logger.error(f"Error in add_movie: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})
