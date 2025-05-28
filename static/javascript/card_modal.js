function setupCardModalEventListener() {
    const cards = document.querySelectorAll(".card");

    cards.forEach(card => {
        card.addEventListener("click", function (event) {
            const id = card.getAttribute("data-id");
            const type = card.getAttribute("data-type");

            if (type === "movie") {
                fetch(`/streaming/movies/${id}/details/`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error("Network response was not ok");
                        }
                        return response.json();
                    })
                    .then(data => {
                        const movieModal = document.getElementById("movieModal");
                        document.getElementById("movieTitle").innerHTML = data.title;
                        document.getElementById("moviePoster").src = data.poster;
                        document.getElementById("movieOverview").innerHTML = data.overview;
                        document.getElementById("movieWatchURL").href = `/streaming/movies/${data.id}/watch/`

                        const releaseDateStr = data.release_date; // Ex: "2020-01-15"
                        if (releaseDateStr) {
                            const dateObj = new Date(releaseDateStr);
                            const options = { day: 'numeric', month: 'long', year: 'numeric' };
                            document.getElementById("movieReleaseDate").innerHTML = dateObj.toLocaleDateString('fr-FR', options);
                        } else {
                            document.getElementById("movieReleaseDate").innerHTML = "Date inconnue"; // Au cas où la date n'est pas fournie
                        }

                        movieModal.classList.toggle("hidden");
                    })
                    .catch(error => {
                        console.error("Fetch error:", error);
                    });
            }
            else if (type === "tv_show") {
                fetch(`/streaming/tvshows/${id}/details/`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error("Network response was not ok");
                        }
                        return response.json();
                    })
                    .then(data => {
                        const tvShowModal = document.getElementById("tvShowModal");
                        const tvshow_name = data.name;
                        document.getElementById("tvShowTitle").innerHTML = tvshow_name;
                        document.getElementById("tvShowPoster").src = data.poster;
                        document.getElementById("tvShowOverview").innerHTML = data.overview;

                        const releaseDateStr = data.first_air_date; // Ex: "2020-01-15"
                        if (releaseDateStr) {
                            const dateObj = new Date(releaseDateStr);
                            const options = { day: 'numeric', month: 'long', year: 'numeric' };
                            document.getElementById("tvShowReleaseDate").innerHTML = dateObj.toLocaleDateString('fr-FR', options);
                        } else {
                            document.getElementById("tvShowReleaseDate").innerHTML = "Date inconnue"; // Au cas où la date n'est pas fournie
                        }

                        document.getElementById("containerTitle").innerHTML = "Saisons";
                        const seasonContainer = document.getElementById("tvShowSeasonsContainer");
                        seasonContainer.innerHTML = "";
                        data.seasons.forEach(season => {
                            const li = document.createElement("li");
                            li.className = "season bg-slate-700 rounded-md p-2 hover:bg-slate-600 transition-colors flex justify-center items-center space-x-4";
                            li.dataset.id = season.id;
                            li.innerHTML = `
                                        <img src="${season.poster}" class="h-24 w-auto" />
                                        <div>
                                            <div class="flex justify-between items-center">
                                                <span class="font-medium text-slate-200">${season.name ? season.name : `Saison ${season.season_number}`}</span>
                                                <span class="text-slate-400">${season.episodes.length} épisodes</span>
                                            </div>
                                            <p class="text-slate-300 text-xs mt-1">${season.overview || "Aucune description."}</p>
                                        </div>
                                    `;
                            seasonContainer.appendChild(li);
                        });

                        const seasons = document.querySelectorAll(".season");
                        seasons.forEach(season => {
                            season.addEventListener("click", () => {
                                const season_id = season.dataset.id;
                                fetch(`/streaming/tvshows/seasons/${season_id}/details/`)
                                    .then(response => {
                                        if (!response.ok) {
                                            throw new Error("Network response was not ok");
                                        }
                                        return response.json();
                                    })
                                    .then(data => {
                                        console.log(data);
                                        const name = data.name;
                                        if (name === null) {
                                            document.getElementById("tvShowTitle").innerHTML = `${tvshow_name} - Saison ${data.season_number}`;
                                        }
                                        else {
                                            document.getElementById("tvShowTitle").innerHTML = `${tvshow_name} - ${name} - Saison ${data.season_number}`;
                                        }

                                        document.getElementById("tvShowPoster").src = data.poster;

                                        const releaseDateStr = data.air_date; // Ex: "2020-01-15"
                                        if (releaseDateStr) {
                                            const dateObj = new Date(releaseDateStr);
                                            const options = { day: 'numeric', month: 'long', year: 'numeric' };
                                            document.getElementById("tvShowReleaseDate").innerHTML = dateObj.toLocaleDateString('fr-FR', options);
                                        } else {
                                            document.getElementById("tvShowReleaseDate").innerHTML = "Date inconnue"; // Au cas où la date n'est pas fournie
                                        }

                                        document.getElementById("tvShowOverview").innerHTML = data.overview;
                                        document.getElementById("containerTitle").innerHTML = "Épisodes";
                                        const episodeContainer = document.getElementById("tvShowSeasonsContainer");
                                        episodeContainer.innerHTML = "";
                                        data.episodes.forEach(episode => {
                                            const airDate = episode.air_date; // Ex: "2020-01-15"
                                            let airString = "";
                                            if (airDate) {
                                                const dateObj = new Date(airDate);
                                                const options = { day: 'numeric', month: 'long', year: 'numeric' };
                                                airString = dateObj.toLocaleDateString('fr-FR', options);
                                            } else {
                                                airString = "Date inconnue";
                                            }
                                            const li = document.createElement("li");
                                            li.className = "bg-slate-700 rounded-md p-2 hover:bg-slate-600 transition-colors flex justify-center items-center space-x-4";
                                            li.innerHTML = `
                                                <a href="/streaming/tvshows/episodes/${episode.id}/watch/">
                                                    <img src="${episode.thumbnail}" class="h-24 w-auto" />
                                                    <div>
                                                        <div class="flex flex-col md:flex-row md:justify-between md:items-center">
                                                            <span class="font-medium text-slate-200">Épisode ${episode.episode_number} ${episode.name ?` - ${episode.name}` : ""}</span>
                                                            <span class="text-slate-400">${airString}</span>
                                                        </div>
                                                        <p class="text-slate-300 text-xs mt-1">${episode.overview || "Aucune description."}</p>
                                                    </div>
                                                </a>
                                            `;
                                            episodeContainer.appendChild(li);
                                        });
                                    })
                                    .catch(error => {
                                        console.error("Fetch error:", error);
                                    });
                            });
                        });
                        tvShowModal.classList.toggle("hidden");
                    })
                    .catch(error => {
                        console.error("Fetch error:", error);
                    });
            }
        });
    });
}