import { createStore } from "vuex";

const store = createStore({
  state: {
    back_color: "#343537",
    migr_access_token: " ",
    user_type: " ",
    email: " "
  },
  getters: {
    getAccessToken(state) {
      return state.migr_access_token
    },
    getEmail(state) {
      return state.email
    },
    getUserType(state) {
      return state.user_type
    }
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem("migrTheme") == "light") {
        state.back_color = "#d3cccc";
      } else {
        state.back_color = "#343537";
      }
      let token = localStorage.getItem('migr_access_token')
      if (token){
        state.migr_access_token = token
      } else {
        state.migr_access_token = ""
      }
      let user_type = localStorage.getItem('user_type')
      if (user_type) {
        state.user_type = user_type
      } else {
        state.user_type = ""
      }
      let email = localStorage.getItem('email')
      if (email) {
        state.email = email
      } else {
        state.email = ""
      }
    },
    setBackColor(state, value) {
      state.back_color = value;
    },
    setAccess (state, access) {
      state.migr_access_token = access
      localStorage.setItem("migr_access_token", access)
    },
    delAccess (state) {
      state.migr_access_token = ""
      localStorage.removeItem("migr_access_token")
    },
    setUserType (state, user_type) {
      state.user_type = user_type
      localStorage.setItem("user_type", user_type)
    },
    setEmail (state, email) {
      state.email = email
      localStorage.setItem("email", email)
    }
  },
  actions: {},
  modules: {},
});

export default store;
