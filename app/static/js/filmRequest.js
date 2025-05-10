function submitFilmData(data) {
    //Disable submit button, add film data to hidden form inputs, submit to server
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
			const filmResponse = response.data;
            const filmData = {
            filmTitle: filmResponse.title,
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

function getFilm(filmTitle) {
	const filmIdRequest = {
		async: true,
		crossDomain: true,
		url: 'https://imdb.iamidiotareyoutoo.com/search?q=' + filmTitle,
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