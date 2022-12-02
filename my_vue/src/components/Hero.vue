<template>

    
    <div class="heroBlock">
      <v-carousel hide-delimiter-background cycle>
        <v-carousel-item
        v-for="(item,i) in items"
        :key="i"
        :src="item.src"
        reverse-transition="slide-y-transition"
        transition="slide-y-transition"
        >
          <v-row
            class="fill-height title"
            align="center"
            justify="center"
          >
            <div>
             {{ item.title }}
            </div>
          </v-row>
      </v-carousel-item>
      </v-carousel>
    </div>
 

</template>

<script>
  export default {
    name: 'Hero',

    data () {
      return {
        items: [
          {
            src: require('../assets/image/carousel1.webp'),
            title:"Easy to check the price",
            height:"400"
          },
          {
            src: require('../assets/image/carousel2.webp'),
            title:"Buy ticket at low price",
            height:"400"
          },
          {
            src: require('../assets/image/carousel5.jpg'),
            title:"Historical data is useful",
            height:"400"
          }
        ],
      }
    },
    
  }
</script>
