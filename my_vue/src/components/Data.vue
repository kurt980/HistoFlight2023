<template>
    <v-content>
        <v-simple-table class="table">
            <template v-slot:default>
                <thead>
                <tr>
                    <th>Flights ({{flightData.length}})</th>
                    <th>Departure City</th>
                    <th>Arrival City</th>
                    <th>Travel Time</th>
                    <th>Departure Date</th>
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
                    <td>{{ flight.travel_time }}</td>
                    <td>{{ flight.departure_date }}</td>
                    <td>{{ flight.avg_Price }}</td>
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
      }
    },
    created(){
      console.log(this.$route.query.items);
      this.getData();
      // this.getTicketPrice();
    },
    methods: {
      getData: function(){
        // if (this.$route.query.items.avgPrice == true){
        //   // console.log("True");
        //     axios.get(url+'/api/getFlightsCheaperThanAvg?arrival_airport=LAX&departure_airport=ORD&limit=10').then(resp => {
        //       this.flightData = resp.data;
        //   });
        // }else{
          // console.log("False")
          // http://127.0.0.1:5000/api/flight?arrival_airport=LAX&departure_airport=ORD&limit=2
        axios.get(url+'/api/flight?arrival_airport=LAX&departure_airport=ORD&limit=10').then(resp => {
            // this.flightData = resp.data;
            console.log("resp",resp.data);
            return resp.data
            // this.getTicketPrice(resp.data);
        })
        .then(resp => {
            console.log(resp)
            this.getTicketPrice(resp.data);
        })
        ;
      },
      getTicketPrice:function(fdata){       
        var b = fdata;
        console.log("fdata", fdata);

        for (let i = 0; i < b.length; i++) {
          var flight_id = b[i]["flight_id"];
          // console.log(flight_id);
          axios.get(url+'/api/getFlightAvgPrice/'+flight_id).then(resp => {
            // console.log(resp.data[0]["avg_price"]);
            b[i]["avg_Price"] = resp.data[0]["avg_price"].toString();
            // console.log(b)
            // console.log(this.flightData);
          });
        }
        // console.log(b);
        this.flightData = b;
        console.log(this.flightData);
      },

    }
}
</script>

<style>

.table{
    padding-left: 20%;
    padding-right: 20%;

}

</style>
