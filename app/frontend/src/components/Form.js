import React, {Component} from "react";
import axios from 'axios'
// require('dotenv').config()

class Form extends Component{
    constructor(props){
        super(props)

        this.state= {
            arrival : '',
            departure: ''
        }
    }

    handleDepartureChange = (event) => {
        this.setState({
            departure: event.target.value
        })
    }

    handleArrivalChange = (event) => {
        this.setState({
            arrival: event.target.value
        })
    }

    handleSubmit = event => {
        event.preventDefault()
        this.state.departure = "108 rue Perthuis, 92140 Clamart"
        this.state.arrival = "242 Rue du Faubourg Saint-Antoine, 75012 Paris"
        PostAddress('http://127.0.0.1:5000/prep_itineraries', this.state.departure, this.state.arrival)
    }

    render(){
        return(
            <form onSubmit={this.handleSubmit}>
                <div class="flexrow">
                    <div class="flexcolumn">
                        <input type='text' id='departure' class='inputbox' placeholder='Departure' onChange={this.handleDepartureChange} value={this.state.departure}/>
                        <input type='text' id='arrival' class='inputbox' placeholder='Arrival' onChange={this.handleArrivalChange} value={this.state.arrival}/>
                        <button class='btn btnspecs'>Send</button>
                    </div>
                </div>
            </form>
        )
    }
}

function PostAddress(url, departure, arrival){
    console.log(departure)
    console.log(arrival)
    axios.post(url, {
      departure: departure,
      arrival: arrival
    })
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
  }

export default Form