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
  const SCALING_FACTOR = 0.9;
  const CANVAS_SIZE = 1250*SCALING_FACTOR;
  const STATION_SIZE = 5;
  const STROKE_WEIGHT = 4;
  const OFFSET_Y = 120
  const OFFSET_X = 60
  
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
    p5.createCanvas(CANVAS_SIZE, CANVAS_SIZE).parent(canvasParentRef)
    p5.smooth();
  }

  const draw = p5 => {
    let col = p5.color(0, 0, 0)
    p5.background(col)
    // p5.background(0, 0, 0, 0.6)
    p5.noFill()
    p5.stroke('#050054');
    p5.rect(0, 0, CANVAS_SIZE, CANVAS_SIZE)
    
    if (data.stations === undefined  || data.stations === undefined) {
      console.log("undefined")
      return
    }

    data.stations.forEach(line => {
      if(line.mode === "angles"){
        let c = p5.color(line.rgb[0], line.rgb[1], line.rgb[2])
        p5.strokeWeight(STROKE_WEIGHT)
        p5.stroke(c)
        
        for(let i = 0; i < line.x.length-1; i++){
          p5.line(
            (line.x[i]-OFFSET_X)*SCALING_FACTOR, 
            (line.y[i]-OFFSET_Y)*SCALING_FACTOR, 
            (line.x[i+1]-OFFSET_X)*SCALING_FACTOR, 
            (line.y[i+1]-OFFSET_Y)*SCALING_FACTOR)
        }
      }
      else{
        for(let i = 0; i < line.x.length-1; i++){
          // if(line.x[i] === "-") continue
          p5.circle(
            (line.x[i]-OFFSET_X)*SCALING_FACTOR, 
            (line.y[i]-OFFSET_Y)*SCALING_FACTOR, 
            STATION_SIZE*SCALING_FACTOR, 
            STATION_SIZE*SCALING_FACTOR)
        }
      }
    });
  }

  return (
  <>
    <Sketch setup={setup} draw={draw} />
    {/* <div class="background"></div> */}
  </>
  )
}

export default App;

