<template>
  <v-content>
    <div class="staticMyComment">
      <v-img src="../assets/image/myhisto.jpg" height="400">
        <v-row align="end" class="lightbox white--text pa-2 fill-height">
          <v-col>
            <v-container>
              <div class="headline">My Histo</div>
            </v-container>
          </v-col>
        </v-row>
      </v-img>
    </div>

    <v-main>
      <v-container>
        <v-row>
          <v-col cols="5">
            <v-row justify="center">
              <v-col cols="12" sm="8">
                <v-card>

                  <v-toolbar color="blue lighten-2" dark>

                    <v-toolbar-title>My Histo</v-toolbar-title>
                  </v-toolbar>
                  <v-spacer></v-spacer>
                  <v-list>
                    <v-list-item>
                      <v-list-item-action>
                        <v-icon>mdi-account</v-icon>
                      </v-list-item-action>

                      <v-list-item-content>
                        <v-list-item-title v-html="username"></v-list-item-title>
                      </v-list-item-content>

                    </v-list-item>

                    <v-divider inset></v-divider>

                    <v-divider inset></v-divider>

                    <v-list-item>
                      <v-list-item-action>
                        <v-icon>mdi-email</v-icon>
                      </v-list-item-action>

                      <v-list-item-content>
                        <v-list-item-title v-html="email"></v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>

                    <v-divider inset></v-divider>
                    <p>
                    <div class="text-center">
                      <v-btn class="ma-2 white--text" :loading="loading2" :disabled="loading2" color="grey"
                        @click="logout">
                        Log out
    
                      </v-btn>
                    </div>

                  </v-list>


                </v-card>
              </v-col>
            </v-row>
          </v-col>

          <v-col>
            <v-sheet min-height="70vh" rounded="lg">
              <!--  -->

              <v-card max-width="800" class="mx-auto">
                <v-toolbar color="blue lighten-2" dark>

                  <v-toolbar-title>My Comments</v-toolbar-title>

                  <v-spacer></v-spacer>
                </v-toolbar>

                <v-list three-line>
                  <template v-for="(item, index) in items">
                    <v-subheader v-if="item.header" :key="item.header" v-text="item.header"></v-subheader>

                    <v-divider v-else-if="item.divider" :key="index" :inset="item.inset"></v-divider>

                    <v-list-item v-else :key="item.comment_id">

                      <v-list-item-content>
                        <v-list-item-title v-html="item.airline"></v-list-item-title>
                        <v-list-item-subtitle v-html="item.text"></v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                  </template>
                </v-list>
              </v-card>
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-content>
</template>

<script>
import axios from 'axios'
export default {
  name: "test",
  created() {
    console.log(sessionStorage.token)
    this.get_user()

  },
  data: () => ({
    username: "",
    email: "",
    items: [],

  }),
  methods: {
    get_user() {
      axios.get('http://127.0.0.1:5000/auth/user', {
        headers: {
          "x-access-tokens": sessionStorage.token
        }
      }).then(response => {
        console.log("response", response.data.message)
        if (response.data.message === 'token is expired'
          || response.data.message === 'token is invalid') {
          sessionStorage.removeItem('token')
          this.$router.push('/login')
        }
        console.log("response ", response)
        this.username = response.data.user_name;
        this.email = response.data.email;
        axios.get('http://127.0.0.1:5000/api/comment?user_name=' + response.data.user_name).then(resp => {
          console.log(resp)
          console.log(resp.data)
          resp.data.forEach(comment => {
            this.items.push(comment)
            this.items.push({ divider: true, inset: true })
          })
          this.items.pop()
        })
      })
    },
    logout(){
      sessionStorage.removeItem('token')
      this.$router.push('/login')
    }

  }
}


</script>