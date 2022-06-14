import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    mesh: {
      data: null,
      style: {weight: 0, color: "#000000", opacity: 0, fillColor: "#3a2f4d", fillOpacity: 1},
      show: false,
    },
  },
  getters: {
  },
  mutations: {
    // postMet: function(state) {
    //   axios.post('http://localhost:3000/api/input', {
    //     metEle: this.metElement
    //   })
    //   .then((response) => {
    //     state.mesh.data = response.data;
    //   })
    //   .catch((err) => {
    //     console.log(err);
    //   });
    // },
  },
  actions: {
  },
  modules: {
  }
})
