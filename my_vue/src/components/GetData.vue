<template>
 
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'Footer',

    data: () => ({
      icons: [
        'mdi-facebook',
        'mdi-twitter',
        'mdi-linkedin',
        'mdi-instagram',
      ],
    }),

    methods: {
      getData: function(){
          axios.get('http://127.0.0.1:5000/api/comments').then(resp => {
          this.fd = resp.data; });
      }}}
</script>
