<template>
  <v-content>
    <Hero/>
    <br>
    <SearchBar/>
  </v-content>
</template>

<script>



import Hero from '../components/Hero.vue'
import SearchBar from '../components/Flight_Search.vue'
export default {
  name: 'Home',
  components: { 
  Hero,
  SearchBar
},

}

</script>
