import { createApp } from "vue";
import App from "./App.vue";
import axios from "axios";
import VueAxios from "vue-axios";
import VueCookies from "vue3-cookies";
import { createStore } from "vuex";

const store = createStore({
  state() {
    return {
      authorized_user: null,
    };
  },
  mutations: {
    login(state, username) {
      state.authorized_user = username;
    },
    logout(state) {
      state.authorized_user = null;
    },
  },
});

createApp(App)
  .use(VueAxios, axios)
  .use(store)
  .use(VueCookies, {
    expireTimes: "30d",
    path: "/",
    domain: "",
    secure: false,
  })
  .mount("#app");
