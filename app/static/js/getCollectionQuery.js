const serverDomain = "http://127.0.0.1:5000";
const serverRoute = "/get_film/";
const rmRoute = "/rm_film";
const favRoute = "/fav_film";
const searchBox = document.getElementById("searchFilm");
const filmBox = document.getElementById("filmData");


let searchTerm = '';
let timeoutId;

function clearChildren(parent) {
        parent.innerHTML = "";
}

function getUserFilmInfo(search) {
    if (!search) {
        clearChildren(filmBox);
        return;
    }
    const url = `${serverDomain}${serverRoute}${encodeURIComponent(search)}`;

    $.ajax({
        url: url,
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            clearChildren(filmBox);

            if (data && data.length > 0) {
                data.forEach(film => {
                    console.log(film);
                    //Populate posterDiv
                    const posterDiv = document.createElement("div");
                    posterDiv.classList.add("col-md-2");
                    const posterImg = document.createElement("img");
                    posterImg.src = film.poster;
                    posterImg.alt = "poster of " + film.title;
                    posterDiv.appendChild(posterImg);
                    filmBox.appendChild(posterDiv);
                    //Populate filmDiv
                    const filmDiv = document.createElement("div");
                    filmDiv.classList.add("col-md-5");
                    filmDiv.innerHTML = `
                        <h3>${film.title} (${film.release_year})</h3>
                        <p>Director: ${film.director}</p>
                        <p>Genres: ${film.genres}</p>
                        <p>Run Time: ${parseInt (film.run_time/60)}hr ${parseInt (film.run_time%60)} min</p>
                        <p>${film.plot}</p>
                    `;
                    filmBox.appendChild(filmDiv);
                    //favourite button
                    const favBtn = document.createElement("btn");
                    favBtn.type = "button";
                    favBtn.classList.add("btn");
                    favBtn.classList.add("btn-info");
                    favBtn.innerText = "favourite";
                    filmDiv.appendChild(favBtn);
                    $(favBtn).click(function(){
                        $.post(serverDomain + favRoute,
                        {
                            id: film.movie_id
                        },
                        function(data, status){
                        console.log("Status: " + status);
                        });
                    }); 
                    //delete button
                    const deleteBtn = document.createElement("btn");
                    deleteBtn.type = "button";
                    deleteBtn.classList.add("btn");
                    deleteBtn.classList.add("btn-danger");
                    deleteBtn.innerText = "remove";
                    filmDiv.appendChild(deleteBtn);
                    //Populate userDiv
                    const userDiv = document.createElement("div");
                    userDiv.classList.add("col-md-5")
                    userDiv.innerHTML = `<br>
                        <p>Status: ${film.category}</p>
                        <p>Watch Date: ${film.watch_date}</p>
                        <p>Rating: ${film.rating}/5</p>
                        <p>Review: ${film.review}</p>
                    `;
                    filmBox.appendChild(userDiv);

                });
            } else {
                filmBox.innerHTML += `<p>No films found matching "${search}".</p>`;
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error("Error: ${textStatus}, ${errorThrown}");
            clearChildren(filmBox);
        }
    });
}

function handleSearchChange(event) {
    searchTerm = event.target.value;

    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
        if (searchTerm) {
            getUserFilmInfo(searchTerm);
        } else {
            clearChildren(filmBox);
        }
    }, 300);
}

searchBox.addEventListener("input", handleSearchChange);