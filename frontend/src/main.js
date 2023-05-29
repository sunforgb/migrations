import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import { loadFonts } from "./plugins/webfontloader";

loadFonts();

const app = createApp(App)
import { VDataTableServer } from "vuetify/labs/VDataTable";
app.component('VDataTableServer', VDataTableServer)
app.use(vuetify);
app.use(store);
app.use(router);

app.mount("#app");
