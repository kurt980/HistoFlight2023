<template>
  <v-content>
    <v-data-table :headers="tableHeader" :items="flightData" :single-expand="singleExpand" :expanded.sync="expanded"
      item-key="flight_number" @item-expanded="onExpand" show-expand class="table">

      <template v-slot:item.time="{ item }">{{ item.departure_time }} - {{ item.arrival_time }}</template>
      <template v-slot:item.flight_number="{ item }">{{ item.flight_number }}</template>

      <template v-slot:item.avg_price="{ item }">
        ${{ item.avg_price }}
      </template>

      <template v-slot:item.ifstar="{ item }"> <v-icon v-if="item.is_cheap == 1" color="yellow">fas
          fa-star</v-icon></template>

      <template v-slot:item.logo="{ item }"><img :src="changeImgSource(item.flight_number)"
          style="width:50px;height:50px;"></template>

      <template v-slot:item.departure_arrival="{ item }">
        {{ item.departure_airport }} - {{ item.arrival_airport }}
      </template>

      <!-- <template v-slot:item.one_way>Nonstop</template> -->

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
          <br />
          <v-icon>mdi-seat-legroom-normal</v-icon>Average Legroom
          <br />
          <v-icon>mdi-signal-variant</v-icon>Free wifi available
          <br />
          <v-icon>mdi-power-plug-outline</v-icon>In-seat power outlet
          <br>
          <v-icon>mdi-cellphone-nfc</v-icon>Stream media to your device
        </td>
        <td>

            <canvas id="myChart" width="400" max_height="150"></canvas>



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
        { text: "", align: 'start', sortable: false, value: 'logo' },
        { text: "Flight Number", sortable: false, value: 'flight_number' },
        { text: "Time", sortable: false, value: "time" },
        // {text: "Departure Airport", value:'departure_airport'},
        // {text: "Arrival Airport", value:'arrival_airport'},
        { text: "Departure/Arrival", sortable: false, value: 'departure_arrival' },
        // { text: "", sortable: false, value: 'one_way' },
        { text: "Price", sortable: false, value: "avg_price" },
        { text: "Cheap", sortable: false, value: "ifstar" },
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
      axios.get('/api/ticket?flight_id=' + item.flight_id).then(resp => {
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

      axios.get('/api/getFlightsCheaperThanAvg?arrival_airport=' + aAbv + '&departure_airport=' + dAbv + '&departure_date=' + departDate).then(resp => {
        this.getTicketPrice(resp.data);
        this.createChartData(resp.data);
      });

    },
    getTicketPrice: function (fdata) {
      var b = fdata;

      for (let i = 0; i < b.length; i++) {
        var flight_id = b[i]["flight_id"];
        axios.get('/api/getFlightAvgPrice/' + flight_id).then(resp => {
          b[i]["avg_price"] = resp.data[0]["avg_price"].toFixed(2);

          this.flightData.push(b[i])

        });

      }

    },
    changeImgSource(flightNumber) {
      var UALogo = require("../assets/image/UA.jpg")
      var AALogo = require("../assets/image/AA.jpg")
      var NKLogo = require("../assets/image/spirit.jpg")
      var ASLogo = require("../assets/image/AS.jpg")
      var WNLogo = require("../assets/image/WN.jpg")
      var F9Logo = require("../assets/image/F9.jpg")
      var G4Logo = require("../assets/image/G4.jpg")
      var DLLogo = require("../assets/image/DL.jpg")
      var VXLogo = require("../assets/image/VX.jpg")
      var B6Logo = require("../assets/image/B6.jpg")
      var OOLogo = require("../assets/image/OO.jpg")
      var ACLogo = require("../assets/image/AC.jpg")
      var WSLogo = require("../assets/image/WS.jpg")
      var EVLogo = require("../assets/image/EV.jpg")
      var NKLogo = require("../assets/image/NK.jpg")
      var img = ""
      var company = flightNumber.substr(0, 2)
      console.log(company)
      if (company == "UA") {
        img = UALogo
      } else if (company == "AA") {
        img = AALogo
      } else if (company == "NK") {
        img = NKLogo
      } else if (company == "AS") {
        img = ASLogo
      } else if (company == "WN") {
        img = WNLogo
      } else if (company == "F9") {
        img = F9Logo
      } else if (company == "G4") {
        img = G4Logo
      } else if (company == "DL") {
        img = DLLogo
      } else if (company == "VX") {
        img = VXLogo
      } else if (company == "B6") {
        img = B6Logo
      } else if (company == "OO") {
        img = OOLogo
      } else if (company == "AC") {
        img = ACLogo
      } else if (company == "WS") {
        img = WSLogo
      } else if (company == "EV") {
        img = EVLogo
      } else if (company == "NK") {
        img = NKLogo
      }
      return img
    },
    createChartData(flight_id) {
      var d = []
      var temp = []
      axios.get('/api/ticket?flight_id=' + flight_id).then(resp => {
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
