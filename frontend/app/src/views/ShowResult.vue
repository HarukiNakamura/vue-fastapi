<template>
  <div id="app">
    <div>Mesh Data: {{ meshData }}</div>
  </div>
</template>

<script>
// import axios from "axios";

export default {
  name: "ShowResult",

  data() {
    return {
      metElement: '',
    };
  },
  computed: {
    meshData: function() {
        return this.$store.state.mesh.data
    }
  },
};
</script>
