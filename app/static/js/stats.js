document.addEventListener("DOMContentLoaded", function () {
    // 1. Top Genres - Pie Chart
    const genreData = [{
        values: chartGenreValues,
        labels: chartGenres,
        type: 'pie'
    }];
    Plotly.newPlot('genreChart', genreData, {
        title: 'Your Top Genres'
    });

    // 2. Watch Time - Bar Chart
    const watchTimeData = [{
        x: ['Total Watch Time'],
        y: [chartWatchTime],
        type: 'bar',
        marker: { color: 'green' }
    }];
    Plotly.newPlot('watchTimeChart', watchTimeData, {
        title: 'Watch Time (Minutes)',
        yaxis: { title: 'Minutes' }
    });

    // 3. Watched Films - Bar Chart
    const watchedData = [{
        x: watchedTitles,
        y: watchedRatings,
        type: 'bar',
        marker: { color: 'blue' }
    }];
    Plotly.newPlot('watchedFilmsChart', watchedData, {
        title: 'Your Watched Films and Ratings',
        yaxis: { title: 'Rating', dtick: 1 },
        xaxis: { title: 'Film Title' }
    });

    // 4. Favourite Directors - Bar Chart
    const directorData = [{
        x: directorNames,
        y: directorFreqs,
        type: 'bar',
        marker: { color: 'red' }
    }];
    Plotly.newPlot('directorChart', directorData, {
        title: 'Favourite Directors',
        xaxis: { title: 'Director' },
        yaxis: { title: 'Number of Films Watched', dtick: 1 }
    });
});
