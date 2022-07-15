import React, { useEffect, useState } from 'react';
import {Button} from './components/Button.js'
import Form from './components/Form.js'
import Itinerary from './components/Itinerary'
import GetRequest from './components/StandardRequest'
import Sketch from 'react-p5'

const SCALING_FACTOR = 0.8;
const CANVAS_SIZE = 1200*SCALING_FACTOR;
const STATION_SIZE = 5;
const STROKE_WEIGHT = 4;
const OFFSET_Y = 120
const OFFSET_X = 50

const BACK_URL = "http://127.0.0.1:5000"
const STATIONS_ENDPOINT = BACK_URL + "/stations"

// Main loop

function App() {
  const [data, setData] = useState({})
  let stations_data = GetRequest(STATIONS_ENDPOINT).stations

  let it = Itinerary()

  // SETUP

  const setup = (p5, canvasParentRef) => {
    p5.createCanvas(CANVAS_SIZE, CANVAS_SIZE).parent(canvasParentRef)
    p5.smooth();
  }

  // DRAW

  const draw = p5 => {
    p5.frameRate(2)
    let col = p5.color(20, 20, 20)
    p5.background(col)
    // p5.background(0, 0, 0, 0.6)
    p5.noFill()
    p5.stroke('#050054');
    p5.rect(0, 0, CANVAS_SIZE, CANVAS_SIZE)
    
    if (stations_data === undefined  || stations_data === undefined) {
      console.log("undefined")
      return
    }

    stations_data.forEach(line => {
      if(line.mode === "angles"){
        let c = p5.color(line.rgb[0], line.rgb[1], line.rgb[2])
        p5.stroke(c)
        
        for(let i = 0; i < line.x.length-1; i++){
          drawline(line.x[i], line.y[i], line.x[i+1], line.y[i+1], c, STROKE_WEIGHT)
        }
      }
      else{
        for(let i = 0; i < line.x.length-1; i++){
          // if(line.x[i] === "-") continue
          for(let i = 0; i < line.x.length-1; i++){
            drawcircle(line.x[i], line.y[i], STROKE_WEIGHT)
          }
        }
      }
    });

    if (it.status){
      for (const [j_id, journey] of Object.entries(it.itineraries)){
          for (const [s_id, sect] of Object.entries(journey.sections)){
          if(sect.mode === "Métro"){
            for(let i = 0; i < sect.angles.x.length-1; i++){
              drawline(sect.angles.x[i], sect.angles.y[i], sect.angles.x[i+1], sect.angles.y[i+1], p5.color(220, 220, 220), STROKE_WEIGHT * 3)
            }
          }
        }
        for (const [s_id, sect] of Object.entries(journey.sections)){
          if(sect.mode === "Métro"){
            for(let i = 0; i < sect.angles.x.length-1; i++){
              drawline(sect.angles.x[i], sect.angles.y[i], sect.angles.x[i+1], sect.angles.y[i+1], p5.color(0, 0, 0), STROKE_WEIGHT)
            }
          }
        }
        for (const [s_id, sect] of Object.entries(journey.sections)){
          if(sect.mode === "Métro"){
            for(let i = 0; i < sect.stations.x.length-1; i++){
              let c1 = i === 0 ? p5.color(255, 0, 0) : (i === sect.stations.x.length-2 ? p5.color(0, 155, 255) : p5.color(0, 0, 0))
              p5.stroke(c1)
              drawcircle(sect.stations.x[i], sect.stations.y[i], STROKE_WEIGHT*1.5)
            }
          }
        }
      }
    }

    function drawcircle(x, y, strokesize){
      p5.strokeWeight(strokesize)
      p5.circle(
        (x-OFFSET_X)*SCALING_FACTOR, 
        (y-OFFSET_Y)*SCALING_FACTOR, 
        STATION_SIZE*SCALING_FACTOR, 
        STATION_SIZE*SCALING_FACTOR)
    }

    function drawline(x1, y1, x2, y2, color, strokesize){
      p5.strokeWeight(strokesize)
      p5.stroke(color)
      p5.line(
      (x1-OFFSET_X)*SCALING_FACTOR, 
      (y1-OFFSET_Y)*SCALING_FACTOR, 
      (x2-OFFSET_X)*SCALING_FACTOR, 
      (y2-OFFSET_Y)*SCALING_FACTOR)
    }
  }

  const Al = (event) => {
    event.preventDefault();
    useEffect(() => {
      setData("test")
    }, "")
  }

  return (
  <div id="main">
    <Sketch setup={setup} draw={draw}/>

    <div id='userselect'>
      <div class='forms'>
        <Form class='address_form'/>
        {/* <form onSubmit={Al}>
          <div class="flexrow">
            <div class="flexcolumn">
              <input type='text' id='departure' class='inputbox' placeholder='Departure'/>
              <input type='text' id='arrival' class='inputbox' placeholder='Arrival'/>
              <button class='btn btnspecs'>Send</button>
            </div>
          </div>
        </form> */}
      </div>
    </div>
  </div>
  )
}

export default App;

