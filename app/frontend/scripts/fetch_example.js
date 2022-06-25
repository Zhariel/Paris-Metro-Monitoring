const url = "http://127.0.0.1:5000/stations";

fetch(url)
    // .then(response => response.json())
    .then(data => {
        console.log(data)
    });
