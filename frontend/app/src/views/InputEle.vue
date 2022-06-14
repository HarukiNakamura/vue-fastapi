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
      <button @click="postMet">run mesh</button>
    </div>
    <div>{{ s }}</div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "InputEle",

  data() {
    return {
      metElement: '',
      s: '',
    };
  },
  
  methods: {
    postMet: function() {
      axios.post('http://localhost:3000/api/input', {
        metEle: this.metElement
      })
      .then((response) => {
        //this.$store.mesh.data = response.data;
        this.s = response.data;
        })
      .catch((err) => {
        console.log(err);
      });
    },
  },
};
</script>

<!-- <style>
</style> -->