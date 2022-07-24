import Vue from 'vue';
import Vuex from 'vuex';

// import axios from "axios";
import createPersistedState from 'vuex-persistedstate';

// import router from '@/router';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    element: {
      selected: '',
      validate: false,
    },

    date: {
      date: [],
      valid: false,
    },


    border: {
      data: [],
      valid: false,
      show: false,
    },
  },
  getters: {
  },

  mutations: {
    setElement: function(state, data) {
      state.element.selected = data.value;
      state.element.validate = data.valid;
    },
    setDates: function(state, data){
      state.date.date = [data.s, data.e];
      state.date.valid = data.valid;
    },
    setBorder: function(state, data){
      state.border.data = data.value;
      state.border.valid = data.valid;
    },

  },
  actions: {
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
