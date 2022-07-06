<template>
  <v-app>
    <!-- <v-navigation-drawer app permanent width="5%"></v-navigation-drawer> -->
    <!-- <v-app-bar app>
      <v-toolbar-title>App Bar</v-toolbar-title>
    </v-app-bar> -->
    <v-main>
      <v-container fill-height fluid>
        <v-layout wrap>
          <v-col cols="12" sm="12" md="6" lg="7" xl="7">
            <slot name="left-content"></slot>
          </v-col>
          <v-col cols="12" sm="12" md="6" lg="5" xl="5" class="map-wrapper">
            <slot name="right-content"></slot>
          </v-col>
        </v-layout>
      </v-container>
    </v-main>
    <!-- <v-footer app>
      Footer
    </v-footer> -->
  </v-app>
</template>

<script>

export default {
  name: "BaseView",
  data() {
    return {
    };
  },

  computed: {
  },

  methods: {
  },

  watch: {
  },
};
</script>

<style>
.map-wrapper {
  position: relative;
}
</style>