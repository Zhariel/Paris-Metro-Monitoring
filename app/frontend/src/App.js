import React, { useEffect, useState } from 'react';
import axios from 'axios'

function App() {
  const [data, setData] = useState([{}])

  useEffect(()=>{
    axios.get('http://127.0.0.1:5000/stations').then(response => {
      console.log("SUCCESS", response)
      setData(response)
    }).catch(error => {
      console.log(error)
    })
    },[])

  return (
    <>
    </>
  )
}

export default App
