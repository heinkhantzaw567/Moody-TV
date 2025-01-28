document.addEventListener("DOMContentLoaded",()=>{
    const body = document.querySelector(".body")
    const posters = document.querySelectorAll(".poster");
    const poster_hein = document.querySelector(".poster-hein");
    const backButton = document.getElementById("backButton");
    posters.forEach((poster) =>{
        const image = poster.querySelector(".movie_poster");
        const title = poster.querySelector(".poster-title");
        const remove = poster.querySelector(".remove-watchlist-animated");
        if (image && title)
            
            {
                let movieData = title.innerHTML
                image.addEventListener('click', ()=>{
                    fetch(`${movieData}`)
                    .then((response) => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! Status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then((movie) => {
                        console.log(movie[0])
                        let hein = movie[0].trailer.length
                        console.log(hein)
                        let zaw = movie[0].trailer.substring(2,movie[0].trailer.length-2)
                        console.log(zaw)
                        // Ensure body is defined, and replace the content with the movie[0] details
                        body.style.display = "none"; // Hide the current content
                        const Html = `
                            <div class="container-detail">
                                <img src="${movie[0].poster}" alt="${movie[0].Title} Poster" class="poster-detail">
                                <div class="content">
                                    <h1 class="title">${movie[0].title}</h1>
                                    <div class="details">
                                        <span><strong>Release Date:</strong> ${movie[0].released}</span>
                                        <span><strong>Genre:</strong> ${movie[0].Genre}</span>
                                        <span><strong>Director:</strong> ${movie[0].Director}</span>
                                        <span><strong>Actors:</strong> ${movie[0].Actors}</span>
                                        <span><strong>Rating:</strong> ${movie[0].rated}</span>

                                    </div>
                                    <p class="description">${movie[0].plot}</p>
                                    <div class="cta">
                                        <a href="${zaw}" target="_blank">Watch Trailer</a>
                                    </div>
                                </div>
                            </div>`;
                        poster_hein.innerHTML = Html; // Inject the generated HTML into the body
                        backButton.style.display = "inline"; // Show the back button
                    })
                    .catch((error) => {
                        console.error("Error fetching movie data:", error.message);
                    });
                })

            }
            else {
                console.error("Watchlist button not found!");
            }
        if(remove)
        {
            remove.addEventListener('click',()=>{
                let movieData = title.innerText.trim();
                 
                fetch(`${movieData}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                
                })

                .then((response) => response.json())
                .then((data) => {
                    if (data.message) {
                        // alert("Movie removed successfully!");
                        poster.innerHTML = "";
                    } else {
                        // alert(data.error || "Error removing movie");
                    }
                })
                .catch((error) => console.error("Error:", error));
                poster.innerHTML =""
            });
            
        }
    })
    backButton.addEventListener("click", () => {
        body.style.display = "block"; // Show the main content
        poster_hein.innerHTML = ""; // Clear the movie details section
        backButton.style.display = "none"; // Hide the back button
    });

})