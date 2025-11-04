from fastapi import FastAPI, Query
import csv
import os

app = FastAPI()

CSV_FILE = "movies.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "director"])

@app.get("/movies")
def get_movies(director: str = Query("", alias="director")):
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        movies = [row for row in reader if director.lower() in row["director"].lower()]
    return movies

@app.post("/movies")
def add_movie(movie: dict):
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([movie["title"], movie["director"]])
    return {"message": "Movie added successfully"}
