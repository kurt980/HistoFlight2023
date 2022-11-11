<template>
  <v-content>
    <Comment_post/>
    <br>
    <Comments_output/>
  </v-content>
</template>

<script>
import Comment_post from '../components/Comment_post.vue'
import Comments_output from '../components/Comments_output.vue'

export default {
  name: 'Comments',
  components: { 
  Comment_post,
  Comments_output
},
}
</script>
