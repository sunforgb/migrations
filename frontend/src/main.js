/* eslint-disable */
import { createApp } from "vue";
import 'vuetify/styles';
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import { loadFonts } from "./plugins/webfontloader";
import Axios from "axios";
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

Axios.defaults.baseUrl = 'http://185.231.153.231:8000'

loadFonts();

const app = createApp(App);
import { VDataTableServer } from "vuetify/labs/VDataTable";
app.component("VDataTableServer", VDataTableServer);
app.component("VueDatePicker", VueDatePicker)
store.commit('initializeStore');
if (localStorage.getItem("migr_access_token")){
    Axios.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem("migr_access_token")
}
// Axios.defaults.headers.common['Authorization'] = 'JWT ' + store.getters.getAccessToken
app.use(vuetify);
app.use(store);
app.use(router);

app.mount("#app");
