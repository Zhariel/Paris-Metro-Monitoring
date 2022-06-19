import React, { useEffect, useState } from 'react';
import axios from 'axios'
import Sketch from 'react-p5'

function health(){
  axios.get('http://127.0.0.1:5000/health').then(response => {
    console.log("SUCCESS", response)
  }).catch(error => {
    console.log(error)
  })
}

// Main loop

function App() {
  const [data, setData] = useState({})
  const size = 1250;
  const station_size = 5;
  
  // health();

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/stations').then(response => {
      console.log("SUCCESS", response.data)
      setData(response.data)
    }).catch(error => {
      console.log(error)
    })
  }, [])

  ///////////////////

  const setup = (p5, canvasParentRef) => {
    p5.createCanvas(size, size).parent(canvasParentRef)
  }

  const draw = p5 => {
    p5.background(214, 222, 255)
    // p5.rect(0, 0, size, size)

    console.log(data.stations)
      
    if (data.stations === undefined  || data.stations === undefined) {
      console.log("undefined")
      return
    }

    data.stations.forEach(line => {
      if(line.mode === "angles"){
        for(let i = 0; i < line.x.length-1; i++){
          p5.line(line.x[i]-50, line.y[i]-50, line.x[i+1]-50, line.y[i+1]-50)
        }
      }

      // p5.circle(line.x[i]-50, line.y[i]-50, station_size, station_size)
    });
  }

  return <Sketch setup={setup} draw={draw} />
}

export default App;

