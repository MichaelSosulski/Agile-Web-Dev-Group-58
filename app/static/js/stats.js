document.addEventListener("DOMContentLoaded", function () {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

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

    // Send chart to friend button handler
    document.getElementById("sendChart").addEventListener("click", function () {
        const recipientSelect = document.getElementById('recipientSelect');
        const recipientId = recipientSelect.value;  // get selected friend user_id

        // Convert Plotly chart to image
        Plotly.toImage('genreChart', { format: 'png', width: 700, height: 500 })
            .then(function (dataUrl) {
                // Send POST request to /send_chart with imageData and recipient_id
                fetch('/send_chart', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken  // Include CSRF token for security
                    },
                    body: JSON.stringify({
                        imageData: dataUrl,
                        recipient_id: recipientId
                    })
                })
                // Handle the server's response
                .then(response => response.json())
                .then(data => alert(data.message))
                .catch(error => console.error('Error:', error));
            });
    });
});