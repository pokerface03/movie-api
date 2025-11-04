from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
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
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        movies = [row for row in reader if director.lower() in row["Director"].lower()]
    return movies

@app.post("/movies")
def add_movie(movie: dict):
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([movie["title"], movie["director"]])
    return {"message": "Movie added successfully"}
