import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'

import axios from 'axios';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

Vue.config.productionTip = false;
Vue.prototype.$axios = axios;

// leafletのアイコンが表示されないので、その対処。
// https://github.com/vue-leaflet/Vue2Leaflet/issues/96
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
