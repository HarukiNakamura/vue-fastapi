import Vue from 'vue'
import Vuex from 'vuex'

import axios from "axios"
import createPersistedState from 'vuex-persistedstate'

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
    setData: function(state, data) {
      state.mesh.data = data
    },

  },
  actions: {
    postMet: function({commit}, metElement) {
      axios.post('http://localhost:3000/api/result', {
        metEle: metElement
      })
      .then((response) => {
        commit('setData', response.data)
      })
      .catch((err) => {
        console.log(err);
      });
    },
  },
  modules: {
  },
  plugins: [createPersistedState(
    { // ストレージのキーを指定
      key: 'vuewithfastapi',
      // ストレージの種類を指定
      storage: window.sessionStorage
    }
  )]
})

