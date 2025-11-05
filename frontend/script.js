const API_URL = "http://127.0.0.1:8000/movies";

document.getElementById("searchBtn").addEventListener("click", searchMovies);
document.getElementById("addBtn").addEventListener("click", addMovie);

async function searchMovies() {
    const query = document.getElementById("searchInput").value.trim();
    const response = await fetch(`${API_URL}?q=${encodeURIComponent(query)}`);
    const movies = await response.json();
    displayMovies(movies);
}

async function addMovie() {
    const title = document.getElementById("movieTitle").value.trim();
    const director = document.getElementById("movieDirector").value.trim();

    if (!title || !director) return alert("Please fill in both fields.");

    const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, director })
    });

    console.log(JSON.stringify({ title, director }))

    if (response.ok) {
        const result = await response.json();
        alert("" + result.message);

        // Clear fields
        document.getElementById("movieTitle").value = "";
        document.getElementById("movieDirector").value = "";

        // Refresh movie list
        searchMovies();
    } else {
        alert("Failed to add movie. Server error.");
    }

    document.getElementById("movieTitle").value = "";
    document.getElementById("movieDirector").value = "";
    searchMovies(); // refresh results
}

function displayMovies(movies) {
    const container = document.getElementById("results");
    container.innerHTML = "";

    if (movies.length === 0) {
        container.innerHTML = "<p>No movies found.</p>";
        return;
    }

    movies.forEach(movie => {
        const div = document.createElement("div");
        div.className = "movie-item";
        div.textContent = `Title:${movie.title} - Director:${movie.director}`;
        container.appendChild(div);
    });
}
