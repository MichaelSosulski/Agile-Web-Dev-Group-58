function submitFilmData(data) {
    //add film data to hidden form inputs
	addFilmForm.elements["release_year"].value = data.release_year;
	addFilmForm.elements["director"].value = data.directorName;
	addFilmForm.elements["genres"].value = data.genres;
	addFilmForm.elements["run_time"].value = data.runTime;
	addFilmForm.elements["plot"].value = data.plot;
	addFilmForm.elements["poster_url"].value = data.poster;

	//change user title to api response's film title
	addFilmForm.elements["film_title"].value = data.filmTitle;

	//submit form
	addFilmForm.submit();
}

function getFilmData(filmId) {
	const filmDataRequest = {
		async: true,
		crossDomain: true,
		url: 'https://graph.imdbapi.dev/v1?query={title(id:"' + filmId + '"){primary_title,start_year,runtime_minutes,plot,genres,posters{url},directors:credits(first:1,categories:["director"]){name{display_name}}}}',
		method: 'GET',
		dataType : 'json',
		headers: {},
		success: function (response) {
			const filmResponse = response.data.title;
            const filmData = {
            filmTitle: filmResponse.primary_title,
			release_year: filmResponse.start_year,
			directorName: filmResponse.directors[0].name.display_name,
			genres: filmResponse.genres,
			runTime: filmResponse.runtime_minutes,
			plot: filmResponse.plot,
			poster: filmResponse.posters[0].url
            };
            submitFilmData(filmData);
		},
		error: function (response) {
			console.error("Error getting film data.")
			console.error("Response Text:", response.responseText);;
			}
	}
	
	$.ajax(filmDataRequest);
	};

function getFilm(filmTitle, year) {
	const filmIdRequest = {
		async: true,
		crossDomain: true,
		url: 'https://imdb.iamidiotareyoutoo.com/search?q=' + filmTitle + ' ' + year,
		method: 'GET',
		dataType : 'json',
		headers: {},
		success: function (response) {
			getFilmData(response.description[0]["#IMDB_ID"])
		},
		error: function (response) {
			console.error("Error getting film id.")
			console.error("Response Text:", response.responseText);;
			}
	}
	
	$.ajax(filmIdRequest);
	};

const addFilmForm = document.forms["addFilmForm"];

//event listener for when the user clicks submit on the form
addFilmForm.addEventListener("submit", function(e) {
	e.preventDefault(); //Prevents form submission

	inputTitle = addFilmForm.elements["film_title"].value;
	inputYear = addFilmForm.elements["release_year"].value;
	getFilm(inputTitle, inputYear);
})