import Vue from 'vue'
import Vuex from 'vuex'

import axios from "axios"
import createPersistedState from 'vuex-persistedstate'

import router from '@/router'

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
      state.mesh.show = true
    },

  },
  actions: {
    postData: function({commit}, inputData) {
      axios.post('http://localhost:3000/api/result', {
        inputData: inputData
      })
      .then((response) => {
        commit('setData', response.data)
        // ここにローディングの処理を入れる。
        // actionsにrouter.pushを入れるのは、アンチパターンな気もするが、
        // 現状は外に方法がわからないので、この方法を採用する。
        router.push('/result')  
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

