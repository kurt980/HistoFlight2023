
<template>
  <v-app id="inspire">
    <div ref='vantaRef'>

      <v-content>
        <v-container class="fill-height" fluid>
          <v-row align="center" justify="center">
            <v-col cols="12" sm="8" md="8">
              <v-card class="elevation-12">
                <v-window v-model="step">
                  <v-window-item :value="1">
                    <v-row>
                      <v-col cols="12" md="8">

                        <v-card-text class="mt-12">
                          <h1 class="text-center display-2 blue--text text--lighten-2">HistoFlight</h1>
                          <div class="text-center mt-4">

                          </div>
                          <v-form>
                            <v-text-field label="User Name" name="User Name" prepend-icon="mdi-account" type="text"
                              color="blue lighten-2" v-model="user_name" />

                            <v-text-field id="password" label="Password" name="password" prepend-icon="mdi-lock"
                              type="password" color="blue lighten-2" v-model="password" />
                          </v-form>
                          <h3 class="text-center mt-4">Forgot your password ?</h3>
                        </v-card-text>
                        <div class="text-center mt-3">
                          <v-btn rounded color="blue lighten-2" dark @click="signin">SIGN IN</v-btn>

                          <v-dialog  v-model="failure_dialog" persistent max-width="300">
                            <v-card >
                              <v-card-title class="text-h5">
                                Incorrect information
                              </v-card-title>
                              <v-card-text>The user name or password you entered is incorrect. Please try it again.</v-card-text>
                              <v-divider></v-divider>
                              <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="primary" text @click="failure_dialog = false">
                                  Close
                                </v-btn>
                              </v-card-actions>
                            </v-card>
                          </v-dialog>


                        </div>
                        <p></p>
                      </v-col>
                      <v-col cols="12" md="4" class="blue lighten-2">
                        <v-card-text class="white--text mt-12">
                          <h1 class="text-center display-1">Hello, Friend!</h1>
                          <h5 class="text-center">Enter your personal details and start journay with us</h5>
                        </v-card-text>
                        <div class="text-center">
                          <v-btn rounded outlined dark @click="step++">SIGN UP</v-btn>
                        </div>
                      </v-col>
                    </v-row>
                  </v-window-item>
                  <v-window-item :value="2">
                    <v-row class="fill-height">
                      <v-col cols="12" md="4" class="blue lighten-2">
                        <v-card-text class="white--text mt-12">
                          <h1 class="text-center display-1">Welcome Back!</h1>
                          <h5 class="text-center">To Keep connected with us please login with your personnel info</h5>
                        </v-card-text>
                        <div class="text-center">
                          <v-btn rounded outlined dark @click="step--">Sign in</v-btn>
                        </div>
                      </v-col>

                      <v-col cols="12" md="8">
                        <v-card-text class="mt-12">
                          <h1 class="text-center display-2 blue--text text--lighten-2">Create Account</h1>
                          <div class="text-center mt-4">
                          </div>
                          <v-form>
                            <v-text-field label="User Name" name="User Name" prepend-icon="mdi-account" type="text"
                              color="blue lighten-2" v-model="user_name" />
                            <v-text-field label="Email" name="Email" prepend-icon="mdi-email" type="text"
                              color="blue lighten-2" v-model="email" />

                            <v-text-field id="password" label="Password" name="password" prepend-icon="mdi-lock"
                              type="password" color="blue lighten-2" v-model="password" />
                          </v-form>
                        </v-card-text>
                        <div class="text-center mt-n5">
                          <v-btn rounded color="blue lighten-2" dark @click="signup">SIGN UP</v-btn>
                        </div>
                        <p></p>
                      </v-col>
                    </v-row>
                  </v-window-item>
                </v-window>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-content>
      <br> <br> <br>
    </div>

  </v-app>
</template>

<script>
import CLOUDS from "../../vanta/dist/vanta.clouds.min"
import axios from "axios"
export default {
  name: 'Login',
  data: () => ({
    failure_dialog: false,
    step: 1
  }),
  props: {
    source: String
  },
  mounted() {
    this.vantaEffect = CLOUDS({
      el: this.$refs.vantaRef
    })
  },
  beforeDestroy() {
    if (this.vantaEffect) {
      this.vantaEffect.destroy()
    }
  },
  created() {
    if (sessionStorage.token) {
      this.$router.push('/myaccount')
    }
  },
  methods: {

    signin() {
      axios.post('http://127.0.0.1:5000/auth/login', {}, {
        auth: {
          username: this.user_name,
          password: this.password
        }
      }).then(response => {
        console.log(response);
        // console.log(response.data);
        sessionStorage.token = response.data.token
        console.log(sessionStorage)

        this.$router.push('/myaccount')
      }).catch(error => {
        console.log(error);

        this.failure_dialog = true

      });
    },

    signup() {
      let body = {
        user_name: this.user_name,
        email: this.email,
        password: this.password
      }
      // console.log(body)
      axios.post('http://127.0.0.1:5000/auth/signup', body)
        .then(response => {
          console.log(response);
          sessionStorage.token = response.data.token
          this.$router.push('/myaccount')
        })
    },

  }
};
</script>