<template>
  <div id="app">
    <base-map :pageName="pageName">
    </base-map>
  </div>
</template>

<script>
import BaseMap from '@/components/BaseMap.vue';

export default {
  name: "ShowResult",
  components: { BaseMap, },
  data() {
    return {
      pageName: 'showResult',
    };
  },

  computed: {
  }, 
   
  methods: {
  },
  
  async created(){
  },
};
</script>
