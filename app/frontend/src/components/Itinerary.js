import Request from './StandardRequest'
import { useState, useEffect, } from 'react';
import axios from 'axios'

const BACK_URL = "http://127.0.0.1:5000"
const ITINERARIES_ENDPOINT = BACK_URL + "/itineraries"

function Itinerary(){
    const [data, setData] = useState({})
  
    useEffect(() => {
      axios.get(ITINERARIES_ENDPOINT)
        .then(response => {
        console.log("SUCCESS", response.data)
        setData(response.data)
      }).catch(error => {
        console.log(error)
      })
    }, [])

    return data
}

export default Itinerary;
