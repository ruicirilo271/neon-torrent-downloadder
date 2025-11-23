async function searchMovies() {
    const q = document.getElementById("query").value.trim();
    const results = document.getElementById("results");

    if (!q) {
        results.innerHTML = "<p>❗ Escreva algo para pesquisar.</p>";
        return;
    }

    results.innerHTML = "<p>🔎 A procurar filmes...</p>";

    const res = await fetch(`/search?q=${encodeURIComponent(q)}`);
    const data = await res.json();

    if (data.error) {
        results.innerHTML = `<p>⚠ Erro: ${data.error}</p>`;
        return;
    }

    results.innerHTML = "";

    data.forEach(movie => {
        const card = document.createElement("div");
        card.className = "card";

        card.innerHTML = `
            <img src="${movie.medium_cover_image}">
            <h3>${movie.title}</h3>
            <a class="torrent-btn" href="/movie/${movie.id}">
                📄 Ver detalhes
            </a>
        `;

        results.appendChild(card);
    });
}


/* ===== DETALHES DO FILME ===== */
async function loadMovieDetails() {
    if (typeof movieId === "undefined") return;

    const res = await fetch(`/api/details/${movieId}`);
    const data = await res.json();

    const movie = data.data.movie;
    const box = document.getElementById("movieDetails");

    let torrentsHtml = "";
    movie.torrents.forEach(t => {
        torrentsHtml += `
            <a class="torrent-btn" href="${t.url}" target="_blank">
                📥 Torrent ${t.quality} (${t.size})
            </a>
            <a class="torrent-btn" href="magnet:?xt=urn:btih:${t.hash}" target="_blank">
                🧲 Magnet ${t.quality}
            </a>
        `;
    });

    box.innerHTML = `
        <h1 class="title">${movie.title}</h1>
        <img class="cover" src="${movie.large_cover_image}">
        
        <p><strong>Ano:</strong> ${movie.year}</p>
        <p><strong>Rating:</strong> ⭐ ${movie.rating}</p>
        <p><strong>Duração:</strong> ${movie.runtime} min</p>
        <p><strong>Géneros:</strong> ${movie.genres.join(", ")}</p>

        <h2 class="subtitle">Sinopse</h2>
        <p>${movie.description_full}</p>

        <h2 class="subtitle">Downloads</h2>
        ${torrentsHtml}
    `;

    loadSuggestions();
}


/* ===== SUGESTÕES ===== */
async function loadSuggestions() {
    const res = await fetch(`/api/suggestions/${movieId}`);
    const data = await res.json();

    const list = data.data.movies || [];
    const container = document.getElementById("suggestions");

    container.innerHTML = "";

    list.forEach(movie => {
        const card = document.createElement("div");
        card.className = "card";

        card.innerHTML = `
            <img src="${movie.medium_cover_image}">
            <h3>${movie.title}</h3>
            <a class="torrent-btn" href="/movie/${movie.id}">
                📄 Ver detalhes
            </a>
        `;

        container.appendChild(card);
    });
}

document.addEventListener("DOMContentLoaded", loadMovieDetails);
