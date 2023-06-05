/* eslint-disable no-console */
<template>
  <v-app-bar density="comfortable">
    <v-spacer></v-spacer>
    <span align="center"> Автоматизированная система миграционного учета!</span>
    <v-spacer></v-spacer>
    <v-btn v-if="logged_in"> Здравствуйте, {{ username }} </v-btn>
    <LoginUser v-if="!logged_in"></LoginUser>
    <v-btn v-if="logged_in" @click="logOut()"> Выход </v-btn>
    <v-btn variant="text" @click="changeTheme"> 
        Сменить тему
    </v-btn>
  </v-app-bar>
</template>
<script>
import { useTheme } from "vuetify";
import LoginUser from "./Login.vue";
import axios from 'axios';
export default {
  name: "HeaderTop",
  components: {
    LoginUser,
  },
  data() {
    return {
      logged_in: false,
      email: ''
    }
  },
  theme: undefined,
  methods: {
    changeTheme (){
        this.$options.theme.global.name.value = this.$options.theme.current.value.dark ? 'light' : 'dark'
        localStorage.setItem("migrTheme", this.$options.theme.global.name.value)
        if (this.$options.theme.global.name.value == 'light') {
            this.$store.commit('setBackColor', '#d3cccc')
        } else {
            this.$store.commit('setBackColor', '#343537')
        }
    },
    logOut (){
      localStorage.removeItem('migr_access_token');
      localStorage.removeItem('email');
      localStorage.removeItem('user_type');
      location.reload();
      this.$router.push('/');
    }
  },
  beforeCreate (){
    axios.defaults.baseURL = 'http://185.231.153.231:8000'
    if (this.$store.getters.getAccessToken){
      axios.defaults.headers.common['Authorization'] = 'JWT ' + this.$store.getters.getAccessToken
      axios.get('/api/users/me/').then((response) => {
        if (response.data.email){
          this.logged_in = true
          this.email = response.data.email
        }
      }).catch(error => {
        this.logged_in = false
        console.log("Not authorized");
        console.log(error);
      })
    }
  },
  created (){
      this.$options.theme = useTheme()
      if (localStorage.getItem("migrTheme")){
          this.$options.theme.global.name.value = localStorage.getItem("migrTheme")
      }
  },
  computed: {
    username (){
      return this.email.split('@')[0]
    }
  }
};
</script>