<template>
    <div class="searchbar">
        <v-form>
            <v-container>
                <v-row>
                    <v-col
                        class="d-flex"
                        cols="8"
                        sm="4"
                    >
                        <v-select
                            v-model="departureCity"
                            :items="cities"
                            label="Departure City"
                            outlined
                            required
                            >
                        </v-select>
                    </v-col>
                    <v-col
                        class="d-flex"
                        cols="8"
                        sm="4"
                    >
                        <v-select
                            v-model="arrivalCity"
                            :items="cities"
                            label="Where To?"
                            outlined
                            required
                            >
                        </v-select>
                    </v-col>
                    <v-col
                        class="d-flex"
                        cols="4"
                        sm="2"
                    >
                        <p>Departure Date</p>
                        <input type="date" class="calender" v-model="departureDate">
                    </v-col>
                    <v-col
                        class="d-flex"
                        cols="4"
                        sm="2"
                    >   
                        <p>Return Date</p>
                        <input type="date" class="calender" v-model="returnDate">
                    </v-col>

                </v-row>
                <v-row>
                    <v-col class="searchbtn">
                        <v-btn rounded color="accent" @click="goToResults">Search 
                            <v-icon
                            right
                            dark
                            >
                            fas fa-search
                            </v-icon> 
                        </v-btn>
                    </v-col>
                    <v-checkbox
                        v-model="avgPrice"
                        label="Find Tickets lower than Avg price"
                        ></v-checkbox>
                </v-row>
            </v-container>
        </v-form>
    </div>
 
</template>

<script>
import { ref } from "vue";
// import { EventBus } from "../event-bus";

let input = ref("");
// const cities = ["Chicago", "Los Angeles", "New York City"]
// function filterCity() {
//   return cities.filter((city) =>
//     city.toLowerCase().includes(input.value.toLowerCase())
//   );
// }

var ddate = changeTimeZone();
var retdate = new Date();
retdate.setDate(retdate.getDate() + 5);

function changeTimeZone(addDate = 0){
    var d = new Date();
    d.setDate(d.getDate() + addDate);
    var year = d.toLocaleString("en-US", { year: "numeric", timeZone: 'America/Chicago' });
    var month = d.toLocaleString("en-US", { month: "2-digit", timeZone: 'America/Chicago' });
    var day = d.toLocaleString("en-US", { day: "2-digit", timeZone: 'America/Chicago' });

    var formattedDate = year + "-" + month + "-" + day;
    return formattedDate
}


    export default{
        data(){
            return {
            userInput: {},
            departureCity: null,
            arrivalCity: null,
            departureDate : changeTimeZone(),
            returnDate : changeTimeZone(5),
            avgPrice: 0,
            cities: [
                'Chicago',
                'Los Angeles',
                'Chicago'
            ],
            }
        },
        methods:{
            goToResults: function(){
                this.urlParams();
                console.log(this.userInput);
                this.$router.push({
                   path: '/results',
                   query:{
                    items: this.userInput
                   }
                });
            },
            urlParams: function(){
                this.userInput = {
                    departureCity: this.departureCity, 
                    arrivalCity: this.arrivalCity,
                    departureDate: this.departureDate,
                    returnDate: this.returnDate,
                    avgPrice: this.avgPrice,
                    };
            }
        }
        
    }

</script>

<style>

.calender{
    border: 1px solid #888;
    border-radius: 0.25em;
    width: 150px;
    height: 55px;
}

.searchbtn{
  height: 10em;
  display: flex;
  align-items: center;
  justify-content: center
}

</style>

