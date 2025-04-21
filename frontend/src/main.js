import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";

axios.defaults.withCredentials = true;
axios.defaults.baseURL = "http://127.0.0.1:5000";

createApp(App).use(router).mount("#app");
