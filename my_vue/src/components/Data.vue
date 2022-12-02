<template>
  <v-content>
      <!-- <div>
        <v-card
          flat
          color="transparent"
        >
          <v-subheader>Min and max default slider</v-subheader>

          <v-card-text>
            <v-row>
              <v-col class="pr-4">
                <v-slider
                  v-model="slider"
                  class="align-center"
                  :max="max"
                  :min="min"
                  hide-details
                >
                  <template v-slot:append>
                    <v-text-field
                      v-model="slider"
                      class="mt-0 pt-0"
                      hide-details
                      single-line
                      type="number"
                      style="width: 60px"
                    ></v-text-field>
                  </template>
                </v-slider>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </div> -->
      <!-- <v-simple-table class="table">
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
      </v-simple-table> -->
      <v-data-table
        :headers="tableHeader"
        :items="flightData"
        :single-expand="singleExpand"
        :expanded.sync="expanded"
        item-key="flight_number"
        show-expand
        class="table"
      >
        <template v-slot:item.time="{ item }">{{ item.departure_time }} - {{ item.arrival_time }}</template>

        <template v-slot:item.avg_price="{ item }">${{ item.avg_price }}</template>

        <template v-slot:item.logo="{ item }"><img :src="changeImgSource(item.flight_number)" style="width:50px;height:50px;"></template>
        

        <template v-slot:item.travel_time="{ item }">
          {{ item.travel_time }}
          <p>{{ item.departure_airport }} - {{ item.arrival_airport }}</p>
        </template>

        <template v-slot:item.one_way>Nonstop</template>

        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Flight Table</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-switch
              v-model="singleExpand"
              label="Single expand"
              class="mt-2"
            ></v-switch>
          </v-toolbar>
        </template>
        <!-- <template v-slot:expanded-item="{ item }">
          <td>
            <p>More info about {{ item.flight_id }}</p>
          </td>
            <td>
              <v-subheader>Current Price Range</v-subheader>

              <v-card-text>
                <v-slider
                  v-model="f"
                  :tick-labels="ticksLabels"
                  v-bind="{max, tickLabels}"
                  tick-size="0"
                ></v-slider>
              </v-card-text>
            </td> -->
            <!-- <v-slider
              v-model="ex3.val"
              :label="ex3.label"
              :thumb-color="ex3.color"
              thumb-label="always"
              :tick-labels="tickLabels"
            ></v-slider> -->
          
        <!-- </template> -->
        <template v-slot:expanded-item="{ item }">
          <td>
            <!-- <v-range-slider
              :tick-labels="flightTicksLabels"
              :value="[0, 1]"
              min="0"
              max="1"
              ticks="always"
              vertical
              disabled
                            
            >
               <template v-slot:thumb-label="props">
                <v-icon dark>
                  {{ flightTicksLabels(props.value) }}
                </v-icon>
              </template> -->
              
            <!-- </v-range-slider> -->
            <p>Travel time</p>
            {{item.flight_number}}
          </td>
          
          <!-- <td>
              <v-subheader>Current Price Range</v-subheader>

              <v-card-text>
                <v-slider
                  v-model="f"
                  :tick-labels="ticksLabels"
                  v-bind="{max, tickLabels}"
                  tick-size="0"
                ></v-slider>
              </v-card-text>
          </td> -->
          <td>
            {{item.flight_number}}
            <!-- {{item.chart_data}} -->
          </td>
          <td>
            <canvas id="myChart1" width="400" height="400" v-bind="createChart(item.chart_data)"></canvas>
            <!-- " -->
          </td>
          
        </template>
      </v-data-table>
      <!-- <v-card
        class="mx-auto text-center"
        color="cyan"
        dark
        max-width="800"
      >
        <v-card-text>
          <v-sheet color="rgba(0, 0, 0, .12)">
            <v-sparkline
              :value="value"
              color="white"
              height="100"
              padding="14"
              stroke-linecap="round"
              smooth
              label-size="5"
              auto-line-width="true"
            >
              <template v-slot:label="item">
                ${{ item.value }}
              </template>
            </v-sparkline>
          </v-sheet>
        </v-card-text>

        <v-card-text>
          <div class="text-h4 font-weight-thin">
            Range of Flight Prices
          </div>
        </v-card-text>

        <v-divider></v-divider>

         <v-card-actions class="justify-center">
          <v-btn
            block
            text
          >
            Go to Report
          </v-btn>
        </v-card-actions> --> 
      <!-- </v-card>  -->
      
      <canvas id="myChart" width="400" height="400"></canvas>
      <canvas id="myChart1" width="400" height="400"></canvas>
      <h1>hi</h1>
  </v-content>
</template>
<script>
import Chart from 'chart.js';
import axios from 'axios';


var url = "http://127.0.0.1:5000";

export default{
  props:['items'],
  data () {
    return {
      flightData: [],

      value:[],
      cityAbv: 
        {"Chicago": "ORD",
        "Los Angeles": "LAX",
        "San Francisco": "SFO",
        },
      // min: -50,
      max: 2,
      // slider: 40,
      singleExpand: false,
      tableHeader: [
        // {text: "Flight Number",align: 'start',sortable: false, value:'flight_number'},
        {text: "Logo", align: 'start', sortable: false, value:'logo' },
        {text: "",sortable: false, value:"time"},
        // {text: "Departure Airport", value:'departure_airport'},
        // {text: "Arrival Airport", value:'arrival_airport'},
        {text: "", sortable: false, value:'travel_time'},
        {text: "", sortable: false, value:'one_way'},
        {text: "", sortable: false, value:"avg_price"},
        { text: '', value: 'data-table-expand' }
      ],
      // ticksLabels:[
      //   '0',
      //   '163.5',
      //   '200',
      // ],
      // datacollection:{
      //   // labels:
      // }
    }
  },
  mounted(){
//       console.log("mounted")
    const t = [ { "label": "2022-11-01", "value": 206 }, { "label": "2022-11-02", "value": 232 }, { "label": "2022-11-03", "value": 218 }, { "label": "2022-11-04", "value": 228 }, { "label": "2022-11-05", "value": 220 }, { "label": "2022-11-06", "value": 235 }, { "label": "2022-11-07", "value": 256 }, { "label": "2022-11-08", "value": 231 }, { "label": "2022-11-09", "value": 277 }, { "label": "2022-11-11", "value": 171 }, { "label": "2022-11-13", "value": 168 }, { "label": "2022-11-14", "value": 168 }, { "label": "2022-11-15", "value": 169 }, { "label": "2022-11-16", "value": 198 }, { "label": "2022-11-17", "value": 252 }, { "label": "2022-11-18", "value": 293 } ]
    const ctx = document.getElementById('myChart');

    var labels = []
    var d = []
    for(let i = 0;i<t.length;i++){
      labels.push(t[i]["label"])
      d.push(t[i]["value"])
    }
// const labels = ['Jan', 'Feb', 'Mar', 'Feb','Feb','Feb','Feb'];
const data = {
labels: labels,
datasets: [{
label: 'My First Dataset',
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
console.log(ctx)
myChart;
this.createChart();
  },
  created(){
    console.log(this.$route.query.items);
    this.getData();

    // console.log(document.getElementById('myChart'))
  },
  methods: {
    getData: function(){
      var aAbv = this.cityAbv[this.$route.query.items.arrivalCity] || "ORD";
      var dAbv = this.cityAbv[this.$route.query.items.departureCity] || "LAX";
      var departDate = this.$route.query.items.departureDate;
      // if (this.$route.query.items.avgPrice == true){
      //     axios.get(url+'/api/getFlightsCheaperThanAvg?arrival_airport='+aAbv+'&departure_airport='+dAbv+'&departure_date='+departDate).then(resp => {
      //       this.getTicketPrice(resp.data);
      //   });
      // }else{
        axios.get(url+'/api/flight?arrival_airport='+aAbv+'&departure_airport='+dAbv+'&departure_date='+departDate).then(resp => {
          this.getTicketPrice(resp.data);
          this.createChartData(resp.data);
        });
      // }
    },
    getTicketPrice:function(fdata){       
      var b = fdata;
      // var set = new Set();
      console.log(fdata);
      for (let i = 0; i < b.length; i++) { 
        var flight_id = b[i]["flight_id"];
        axios.get(url+'/api/getFlightAvgPrice/'+flight_id).then(resp => {
          b[i]["avg_price"] = resp.data[0]["avg_price"].toFixed(2);
          // b[i]["chart_data"] = this.createChartData(flight_id);
          // console.log("b" + b[i]["chart_data"])

          var d = []
          var temp = []
          var cdata;
          axios.get(url+'/api/ticket?flight_id='+flight_id).then(resp => {
              d = resp.data
              
              for (let i = 0;i<d.length;i++){

                temp.push({
                  "label": d[i]["purchase_date"],
                  "value": d[i]["price"]
                })
                
                temp.sort((a,b) => (a.label > b.label) ? 1 : ((b.label > a.label) ? -1 : 0))
                // console.log(temp);
                
                // var labels = []
                // var value = []
                // for (let y = 0;y<temp.length;y++){
                //   labels.push(temp[y]["label"])
                //   value.push(temp[y]["value"])
                // }

                // cdata = {
                //     labels: labels,
                //     datasets: [{
                //       label: 'Price',
                //       data: value,
                //       fill: false,
                //       borderColor: 'rgb(75, 192, 192)',
                //       tension: 0.1
                //     }]
                //   };
              }
              b[i]["chart_data"] = temp;
              console.log(b[i])
              this.flightData.push(b[i])
            });
            
            


          // console.log(b[i])
          
          // set.add(parseFloat(resp.data[0]["avg_price"].toFixed(2)))
          // console.log(set)
          // this.value = Array.from(set).sort(function(a, b){return a - b});
          // console.log(this.value)

          // this.setDataCollection(b)
          
        });
        
      }
      
    },
    // setDataCollection:function(fdata){
    //   var flabel = [];
    //   var pricedata = [];
    //   // {
    //   //   data: [86, 114, 106, 106, 107, 111, 133, 221, 783, 2478],
    //   //     label: "Africa",
    //   //     borderColor: "#3e95cd",
    //   //     fill: false
    //   // }
    //   for (let i = 0; i<this.flightData.length;i++){
    //     flabel.push(this.flightData[i]["flight_number"])
    //     pricedata.push(parseFloat(this.flightData[i]["avg_price"]))
    //   }
    //   this.datacollection = {
    //     labels: flabel,
    //     datasets: [{
    //       data: pricedata,
    //       label: "",
    //       borderColor: "#3e95cd",
    //       fill: false
    //     }]
    //   }
    // },
    changeImgSource(flightNumber){
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
    createChartData(flight_id){
      // var b = fdata;
      // console.log(fdata);
      // for (let i = 0; i < b.length; i++) { 
      //   var flight_id = b[i]["flight_id"];
      var d = []
      var temp = []
      axios.get(url+'/api/ticket?flight_id='+flight_id).then(resp => {
          d = resp.data
          var cdata;
          for (let i = 0;i<d.length;i++){

            temp.push({
              "label": d[i]["purchase_date"],
              "value": d[i]["price"]
            })
            
            temp.sort((a,b) => (a.label > b.label) ? 1 : ((b.label > a.label) ? -1 : 0))
            // console.log(temp);
            
            var labels = []
            var value = []
            for (let y = 0;y<temp.length;y++){
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
          // return cdata;
          // this.createChart(cdata);
          // b[i]["chart_data"] = cdata;
          // this.flightData.push(b[i])
        });

      // }
    },
    createChart(data){
      // console.log()
      // console.log("cc " + data)
      const ctx = document.getElementById('myChart1');

// const labels = ['Jan', 'Feb', 'Mar', 'Feb','Feb','Feb','Feb'];
// const data = {
// labels: labels,
// datasets: [{
//   label: 'My First Dataset',
//   data: [65, 59, 80, 81, 56, 55, 40],
//   fill: false,
//   borderColor: 'rgb(75, 192, 192)',
//   tension: 0.1
// }]
// };

var labels = []
var value = []
for (let y = 0;y<data.length;y++){
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

.table{
  padding-left: 20%;
  padding-right: 20%;

}

</style>
