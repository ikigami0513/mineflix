function setupMovieModalEventListener() {
    document.getElementById("closeMovieModalButton").addEventListener("click", () => {
        const movieModal = document.getElementById("movieModal");
        movieModal.classList.toggle("hidden");
    });
}