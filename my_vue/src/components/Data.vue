<template>
  <v-content>
    <v-data-table :headers="tableHeader" :items="flightData" :single-expand="singleExpand" :expanded.sync="expanded"
      item-key="flight_number" @item-expanded="onExpand" show-expand class="table">

      <template v-slot:item.time="{ item }">{{ item.departure_time }} - {{ item.arrival_time }}</template>
      <template v-slot:item.avg_price="{ item }">
          ${{ item.avg_price }} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <v-icon v-if="item.is_cheap==1" color="yellow" >fas fa-star</v-icon>
        </template>
      <template v-slot:item.logo="{ item }"><img :src="changeImgSource(item.flight_number)"
          style="width:50px;height:50px;"></template>

      <template v-slot:item.travel_time="{ item }">
        {{ item.travel_time }}
        <p>{{ item.departure_airport }} - {{ item.arrival_airport }}</p>
      </template>

      <template v-slot:item.one_way>Nonstop</template>

      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Flight Table</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-switch v-model="singleExpand" label="Single expand" class="mt-2"></v-switch>
        </v-toolbar>
      </template>

      <!-- </template> -->
      <template v-slot:expanded-item="{ item }">
        <!-- {{content}} -->
        <td>
          <br></br>
            <v-icon>mdi-seat-legroom-normal</v-icon>Average Legroom
            <br></br>
            <v-icon>mdi-signal-variant</v-icon>Free wifi available
            <br></br>
            <v-icon>mdi-power-plug-outline</v-icon>In-seat power outlet
            <br></br>
            <v-icon>mdi-cellphone-nfc</v-icon>Stream media to your device
        </td>
        <td>
          <canvas id="myChart" width="400" height="400"></canvas>
        </td>

      </template>
    </v-data-table>

    <!-- <canvas id="myChart" width="400" height="400"></canvas> -->
    <!-- <canvas id="myChart" width="400" height="400"></canvas> -->
  </v-content>
</template>
<script>
import Chart from 'chart.js';
import axios from 'axios';


var url = "http://127.0.0.1:5000";

export default {
  props: ['items'],
  data() {
    return {
      flightData: [],
      content: "",
      value: [],
      cityAbv:
      {
        "Chicago": "ORD",
        "Los Angeles": "LAX",
        "San Francisco": "SFO",
      },
      singleExpand: false,
      tableHeader: [
        // {text: "Flight Number",align: 'start',sortable: false, value:'flight_number'},
        { text: "Logo", align: 'start', sortable: false, value: 'logo' },
        { text: "", sortable: false, value: "time" },
        // {text: "Departure Airport", value:'departure_airport'},
        // {text: "Arrival Airport", value:'arrival_airport'},
        { text: "", sortable: false, value: 'travel_time' },
        { text: "", sortable: false, value: 'one_way' },
        { text: "", sortable: false, value: "avg_price" },
        { text: '', value: 'data-table-expand' }
      ],
    }
  },

  created() {
    console.log(this.$route.query.items);
    this.getData();

    // console.log(document.getElementById('myChart'))
  },
  methods: {
    onExpand({ item }) {
      axios.get(url + '/api/ticket?flight_id=' + item.flight_id).then(resp => {
        let d = resp.data
        let temp = []
        for (let i = 0; i < d.length; i++) {

          temp.push({
            "label": d[i]["purchase_date"],
            "value": d[i]["price"]
          })

          temp.sort((a, b) => (a.label > b.label) ? 1 : ((b.label > a.label) ? -1 : 0))
        }
        item["chart_data"] = temp;
        this.mountGraph(item)
      });
    },
    mountGraph(item) {
      console.log("mounted")
      const t = item.chart_data
      const ctx = document.getElementById('myChart');
      console.log("ctx", ctx)
      var labels = []
      var d = []
      for (let i = 0; i < t.length; i++) {
        labels.push(t[i]["label"])
        d.push(t[i]["value"])
      }
      // const labels = ['Jan', 'Feb', 'Mar', 'Feb','Feb','Feb','Feb'];
      const data = {
        labels: labels,
        datasets: [{
          label: 'Price',
          data: d,
          fill: false,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        }]
      };

      const myChart = new Chart(ctx, {
        type: 'line',
        data: data
      });
      console.log("ctx", ctx)
      myChart;
      this.createChart();
    },
    getData: function () {
      var aAbv = this.cityAbv[this.$route.query.items.arrivalCity] || "ORD";
      var dAbv = this.cityAbv[this.$route.query.items.departureCity] || "LAX";
      var departDate = this.$route.query.items.departureDate;
      
      axios.get(url+'/api/getFlightsCheaperThanAvg?arrival_airport='+aAbv+'&departure_airport='+dAbv+'&departure_date='+departDate).then(resp => {
          this.getTicketPrice(resp.data);
          this.createChartData(resp.data);
      });

    },
    getTicketPrice: function (fdata) {
      var b = fdata;

      for (let i = 0; i < b.length; i++) {
        var flight_id = b[i]["flight_id"];
        axios.get(url + '/api/getFlightAvgPrice/' + flight_id).then(resp => {
          b[i]["avg_price"] = resp.data[0]["avg_price"].toFixed(2);

          this.flightData.push(b[i])

        });

      }

    },
    changeImgSource(flightNumber) {
      // var UALogo = require("../assets/image/UA.jpg")
      // var AALogo = require("../assets/image/AA.jpg")
      // var NKLogo = require("../assets/image/spirit.jpg")
      // var img = ""
      // var company = flightNumber.substr(0, 2)
      // // console.log(company)
      // if (company == "UA"){
      //   img = UALogo
      //  }else if (company == "AA"){
      //   img = AALogo
      // } else if (company == "NK"){
      //   img = NKLogo
      // }
      // return img
    },
    createChartData(flight_id) {
      var d = []
      var temp = []
      axios.get(url + '/api/ticket?flight_id=' + flight_id).then(resp => {
        d = resp.data
        var cdata;
        for (let i = 0; i < d.length; i++) {

          temp.push({
            "label": d[i]["purchase_date"],
            "value": d[i]["price"]
          })

          temp.sort((a, b) => (a.label > b.label) ? 1 : ((b.label > a.label) ? -1 : 0))
          // console.log(temp);

          var labels = []
          var value = []
          for (let y = 0; y < temp.length; y++) {
            labels.push(temp[y]["label"])
            value.push(temp[y]["value"])
          }

          cdata = {
            labels: labels,
            datasets: [{
              label: 'Price',
              data: value,
              fill: false,
              borderColor: 'rgb(75, 192, 192)',
              tension: 0.1
            }]
          };

        }
        console.log("cdata " + cdata)
      });
    },
    createChart(data) {
      const ctx = document.getElementById('myChart1');

      var labels = []
      var value = []
      for (let y = 0; y < data.length; y++) {
        labels.push(data[y]["label"])
        value.push(data[y]["value"])
      }

      const cdata = {
        labels: labels,
        datasets: [{
          label: 'Price',
          data: value,
          fill: false,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        }]
      };
      console.log(labels)
      console.log(cdata)
      const myChart = new Chart(ctx, {
        type: 'line',
        data: data
      });
      // console.log(ctx)
      myChart;
    }
  },
}
</script>

<style>
.table {
  padding-left: 20%;
  padding-right: 20%;

}
</style>
