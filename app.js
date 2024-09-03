// Initialize Shiny
$(document).ready(function() {
    Shiny.initializeInputs();
    Shiny.bindAll();
});

// Load the Python Shiny app
fetch('app.py')
    .then(response => response.text())
    .then(code => {
        pyodide.runPython(code);
    });