from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import csv
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CSV_FILE = "movies.csv"

@app.get("/movies")
def get_movies(director: str = Query("", alias="q")):
    try:
        if not os.path.exists(CSV_FILE):
            return JSONResponse(status_code=404, content={"error": "CSV file not found"})

        with open(CSV_FILE, "r") as f:
            reader = csv.DictReader(f)
            movies = [row for row in reader if director.lower() in row["Director"].lower()] 
            return movies

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/movies")
def add_movie(movie: dict):
    try:
        
        if "title" not in movie or "director" not in movie:
            return JSONResponse(
                status_code=400,
                content={"error": "Missing required keys: 'title' and/or 'director'"}
            )

        if not os.path.exists(CSV_FILE):
            return JSONResponse(status_code=404, content={"error": "CSV file not found"})
        
        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([movie["title"], movie["director"]])

        return {"message": "Movie added successfully"}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
