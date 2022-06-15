<template>
  <div id="app">
    <select v-model="metElement">
      <option value="TMP_mea">日平均気温</option>
      <option value="TMP_max">日最高気温</option>
      <option value="TMP_min">日最低気温</option>
    </select>
    <p>Your Choice: {{ metElement }}</p>
    <br>
    <div>
      <button @click="postMet" onclick="location.href='/result'">run mesh</button>
    </div>
  </div>
</template>

<script>
// import axios from "axios";

export default {
  name: "InputEle",

  data() {
    return {
      metElement: '',
    };
  },
  
  methods: {
    postMet: function() {
      this.$store.dispatch('postMet', this.metElement)
    }
  },
};
</script>
