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
  const size = 1225;
  
  // health();

  useEffect(()=>{
    axios.get('http://127.0.0.1:5000/stations').then(response => {
      console.log("SUCCESS", response)
      setData(response)
    }).catch(error => {
      console.log(error)
    })
  }, [])

  let stations = data.data

  ///////////////////

  const setup = (p5, canvasParentRef) => {
    p5.createCanvas(size, size).parent(canvasParentRef)
  }

  const draw = p5 => {
    p5.background(214, 222, 255)
    // p5.rect(0, 0, size, size)
    
    
    if (stations === undefined  || stations.stations === undefined) return
    stations.stations.array.forEach(element => {
      console.log("a")
      p5.rect(0, 0, size, size)
    })
  }

  return <Sketch setup={setup} draw={draw} />
}

export default App;

