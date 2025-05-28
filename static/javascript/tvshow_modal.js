function setupTVShowModalEventListener() {
    document.getElementById("closeTVShowModalButton").addEventListener("click", () => {
        const tvShowModal = document.getElementById("tvShowModal");
        tvShowModal.classList.toggle("hidden");
    });
}
