// Load data and create visualizations
fetch('processed_data.json')
    .then(response => response.json())
    .then(data => {
        createMap(data);
        createTypeChart(data);
        createTimeline(data);
    });

function createMap(data) {
    // Use Plotly.js to create the map visualization
    // ...
}

function createTypeChart(data) {
    // Use Plotly.js to create the type chart
    // ...
}

function createTimeline(data) {
    // Use Plotly.js to create the timeline
    // ...
}

// Add functions to handle filtering and updating visualizations
// ...