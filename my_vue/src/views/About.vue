<template>
  <v-content>
    <div class="staticHero">
      <v-img 
            src="../assets/image/aboutus.jpeg"
            height="400">
        <v-row align="end" class="lightbox white--text pa-2 fill-height">
          <v-col>
            <v-container>
              <div class="headline">About Us</div>
            </v-container>
          </v-col>
        </v-row>
      </v-img>
    </div>

    <div class="block">
      <v-container>
        <p>
          We are the team of Pepsi in CS411 Database System. Welcome to use this application for searching historical Flight Price!
        </p>
      </v-container>
    </div>

    <div class="block">
      <v-container>
        <h2 class="text-center">Our Teams</h2>
        <v-row>
          <v-col v-for="item in items" :key="item.id" class="d-flex child-flex">
            <v-card flat tile class="mx-auto">
              <v-img :src="item.src" aspect-ratio="1" class="grey lighten-2"  ></v-img>
              <v-card-text class="text--primary text-center">
                <div class="title">{{ item.name }}</div>
                <p>{{ item.title }}</p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </v-content>
</template>

<script> 
  export default {
    name: 'About',

    data() {
    return {
      items: [
        {
          id: 1,
          src: require("../assets/image/team1.webp"),
          name: 'Yilun Fu',
          title: 'Front-end web developer'
        },
        {
          id: 2,
          src: require("../assets/image/team2.jpg"),
          name: 'Weikun Wu',
          title: 'Back-end Engineer'
        },
        {
          id: 3,
          src: require("../assets/image/team3.jpg"),
          name: 'Chengyan Ji',
          title: 'SQL Supporter'
        },       
        {
          id: 4,
          src: require("../assets/image/team4.jpg"),
          name: 'Henry Wang',
          title: 'software Engineer'
        }
      ]
    };
  }
  }
</script>
