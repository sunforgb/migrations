/* eslint-disable no-console */
<template>
  <v-app :style="{background: backColor }">
    <v-main>
      <HeaderTop></HeaderTop>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import HeaderTop from "./components/HeaderTop.vue"
export default {
  name: "App",
  components: {
    HeaderTop
  },
  data: () => ({
  }),
  computed: {
    backColor() {
      return this.$store.state.back_color
    }
  }
};
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
