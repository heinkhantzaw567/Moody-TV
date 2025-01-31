document.addEventListener("DOMContentLoaded", () => {
    const body = document.querySelector(".body");
    const posters = document.querySelectorAll(".poster");
    const poster_hein = document.querySelector(".poster-hein");
    const backButton = document.getElementById("backButton"); // Ensure this is defined once
    
    posters.forEach((poster) => {
        const watchlistbutton = poster.querySelector(".watchlistbutton");
        const imageclick = poster.querySelector(".posterimg");
        console.log(imageclick)
        imageclick.addEventListener('click',()=>{
            if (imageclick && watchlistbutton)
                {
                    // Fetch the data-movie attribute from the button
                    let movieData = watchlistbutton.dataset.movie;
        
                    // Use backticks for the fetch URL to interpolate movieData
                    fetch(`/get-movie/${movieData}`)
                        .then((response) => {
                            if (!response.ok) {
                                throw new Error(`HTTP error! Status: ${response.status}`);
                            }
                            return response.json();
                        })
                        .then((movie) => {
                            // Ensure body is defined, and replace the content with the movie details
                            
                            body.style.display = "none"; // Hide the current content
                            const Html = `
                                <div class="container">
                                    <img src="${movie.Poster}" alt="${movie.Title} Poster" class="poster-detail">
                                    <div class="content">
                                        <h1 class="title">${movie.Title}</h1>
                                        <div class="details">
                                            <span><strong>Release Date:</strong> ${movie.Released}</span>
                                            <span><strong>Genre:</strong> ${movie.Genre}</span>
                                            <span><strong>Director:</strong> ${movie.Director}</span>
                                            <span><strong>Actors:</strong> ${movie.Actors}</span>
                                            <span><strong>Rating:</strong> ${movie.Rated}</span>
                                        </div>
                                        <p class="description">${movie.Plot}</p>
                                        <div class="cta">
                                            <a href="${movie.youtubeurl[0]}" target="_blank">Watch Trailer</a>
                                        </div>
                                    </div>
                                </div>`;
                            poster_hein.innerHTML = Html; // Inject the generated HTML into the body
                            backButton.style.display = "inline"; // Show the back button
                        })
                        .catch((error) => {
                            console.error("Error fetching movie data:", error.message);
                        });
                } else {
                    console.error("Watchlist button not found!");
                }
        })
        watchlistbutton.addEventListener('click', ()=>{
            
            let movieData = watchlistbutton.dataset.movie;
            fetch(`/get-movie/${movieData}`)
                .then((response) => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then((movie) => {
                    // Step 2: Post to watchlist
                    return fetch('/watchlist/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(movie),
                    });
                })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error(`Failed to add to watchlist. Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then((result) => {
                    // Handle successful response
                    console.log('Movie added to watchlist:', result);
                    watchlistbutton.style.display ="none"
                })

            })


            
        })
        
        


        
    

    // Back Button Functionality
    backButton.addEventListener("click", () => {
        body.style.display = "block"; // Show the main content
        poster_hein.innerHTML = ""; // Clear the movie details section
        backButton.style.display = "none"; // Hide the back button
    });

});