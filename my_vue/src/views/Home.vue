<template>
  <v-content>
    <hero/>
    <SearchBar/>
  </v-content>
</template>

<script>



import Hero from '../components/Hero.vue'
import SearchBar from '../components/Search.vue'
export default {
  name: 'Home',
  components: { 
  Hero,
  SearchBar
},

}

</script>
