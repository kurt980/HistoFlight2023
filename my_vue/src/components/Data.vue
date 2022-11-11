<template>
    <v-content>
        <v-simple-table class="table">
            <template v-slot:default>
                <thead>
                <tr>
                    <th>Flights ({{flightData.length}})</th>
                    <th>Departure City</th>
                    <th>Arrival City</th>
                    <th>Departure Date</th>
                    <th>Departure Time</th>
                    <th>Arrival Date</th>
                    <th>Arrival Time</th>
                    <th>Price</th>
                </tr>
                </thead>
                <tbody>
                <tr
                    v-for="(flight,index) in flightData"
                    :key="index"
                >
                    <td>{{ flight.flight_number }}</td>
                    <td>{{ flight.departure_airport }}</td>
                    <td>{{ flight.arrival_airport }}</td>
                    <td>{{ flight.departure_date }}</td>
                    <td>{{ flight.departure_time }}</td>
                    <td>{{ flight.arrival_date }}</td>
                    <td>{{ flight.arrival_time }}</td>
                    <td>${{ flight.avg_Price }}</td>
                </tr>
                </tbody>
            </template>
        </v-simple-table>
    </v-content>
</template>
<script>
import axios from 'axios'

var url = "http://127.0.0.1:5000";

export default{
    props:['items'],
    data () {
      return {
        flightData: [],
        cityAbv: 
          {"Chicago": "ORD",
          "Los Angeles": "LAX",
          "San Francisco": "SFO",
          }
      }
    },
    created(){
      console.log(this.$route.query.items);
      this.getData();
    },
    methods: {
      getData: function(){
        var aAbv = this.cityAbv[this.$route.query.items.arrivalCity] || "ORD";
        var dAbv = this.cityAbv[this.$route.query.items.departureCity] || "LAX";
        var departDate = this.$route.query.items.departureDate;
        if (this.$route.query.items.avgPrice == true){
            axios.get(url+'/api/getFlightsCheaperThanAvg?arrival_airport='+aAbv+'&departure_airport='+dAbv+'&departure_date='+departDate).then(resp => {
              this.getTicketPrice(resp.data);
          });
        }else{
          axios.get(url+'/api/flight?arrival_airport='+aAbv+'&departure_airport='+dAbv+'&limit=10').then(resp => {
              this.getTicketPrice(resp.data);
          });
        }
      },
      getTicketPrice:function(fdata){       
        var b = fdata;

        for (let i = 0; i < b.length; i++) {
          var flight_id = b[i]["flight_id"];
          axios.get(url+'/api/getFlightAvgPrice/'+flight_id).then(resp => {
            b[i]["avg_Price"] = resp.data[0]["avg_price"].toFixed(2);
            this.flightData.push(b[i])
          });
        }
      },
    },
}
</script>

<style>

.table{
    padding-left: 20%;
    padding-right: 20%;

}

</style>
