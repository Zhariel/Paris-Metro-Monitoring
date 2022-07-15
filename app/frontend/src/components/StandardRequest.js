import { useState, useEffect, } from 'react';
import axios from 'axios'

function GetRequest(url){
    const [data, setData] = useState({})
  
    useEffect(() => {
      axios.get(url).then(response => {
        console.log("SUCCESS", response.data)
        setData(response.data)
      }).catch(error => {
        console.log(error)
      })
    }, [])

    return data
}

export default GetRequest;