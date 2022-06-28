<template>
  <div id="app">
    <v-col cols="12">
      <l-map ref="map" style="height: 600px; width: 800px;" :options="map.options" :center="map.center" :maxBounds="map.maxBounds" :zoom="map.zoom" :minZoom="map.minZoom" @mousedown="mapMousedown($event)" @mousemove="mapMousemove($event)" @mouseup="mapMouseup($event)">
        <l-control-layers position="topright"></l-control-layers>
        <l-tile-layer v-for="tileProvider in tileProviders" :key="tileProvider.name" :name="tileProvider.name" :visible="tileProvider.visible" :url="tileProvider.url" :attribution="tileProvider.attribution" layer-type="base"/>
        <l-rectangle :bounds="[[s, w], [n, e]]" :l-style="rectangle.style"></l-rectangle>
        <l-control position="bottomleft" >
        <v-btn @click="btn">
        {{ message }}
        </v-btn>
        </l-control>
      </l-map>
    </v-col>
    <v-col cols="3">
      <v-text-field v-model="s" label="南端緯度" outlined persistent-placeholder></v-text-field>
      <v-text-field v-model="n" label="北端緯度" outlined persistent-placeholder></v-text-field>
      <v-text-field v-model="w" label="西端経度" outlined persistent-placeholder></v-text-field>
      <v-text-field v-model="e" label="東端経度" outlined persistent-placeholder></v-text-field>
    </v-col>
  </div>
</template>

<script>
import { latLngBounds } from "leaflet";
import { LMap, LTileLayer, LControlLayers, LRectangle, LControl, } from "vue2-leaflet";


export default {
  name: "InputData",
  components: { LMap, LTileLayer, LControlLayers, LRectangle, LControl, },
  data() {
    return {
      isMousedowned: false,

      s: '',
      n: '',
      w: '',
      e: '',

      message: 'Draw Rectangle', 

      map: {
        options: {
          preferCanvas: true,
          dragging: true,
          // doubleClickZoom: false,
        },
        center: [35.693825, 139.703356],
        maxBounds: latLngBounds([
          [23, 120],
          [46, 150]
        ]),
        zoom: 6,
        minZoom: 4,
        inertia: false
      },
      tileProviders: [
        {
          name: '標準地図',
          visible: false,
          url: 'https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png',
          attribution:
            '&copy; <a target="_blank" href="https://maps.gsi.go.jp/development/ichiran.html">地理院タイル</a>',
        },
        {
          name: '淡色地図',
          visible: true,
          url: 'https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png',
          attribution:
            '&copy; <a target="_blank" href="https://maps.gsi.go.jp/development/ichiran.html">地理院タイル</a>',
        },
        {
          name: '白地図',
          visible: false,
          url: 'https://cyberjapandata.gsi.go.jp/xyz/blank/{z}/{x}/{y}.png',
          attribution:
            '&copy; <a target="_blank" href="https://maps.gsi.go.jp/development/ichiran.html">地理院タイル</a>'
        }
      ],


      rectangle: {
        style: {weight: 2, color: "#232323", opacity: 1, fillColor: "#55FF00", fillOpacity: 0.7}
      }, 
    };
  },
  computed: {
  }, 
   
  methods: {

    mapMousedown(event){
      if (!this.map.options.dragging){
        this.isMousedowned = true
        this.s = event.latlng.lat
        this.n = event.latlng.lat
        this.w = event.latlng.lng
        this.e = event.latlng.lng
      }
    },

    mapMousemove(event){
      if (!this.map.options.dragging){
        if (this.isMousedowned){
          if (event.latlng.lat <= this.s){
            this.s = event.latlng.lat
          } else {
            this.n = event.latlng.lat
          }
          if (event.latlng.lng <= this.w){
            this.w = event.latlng.lng
          } else {
          this.e = event.latlng.lng
          }
        }
      }
    },

    mapMouseup(event){
      if (!this.map.options.dragging){
        if (this.isMousedowned){
          if (event.latlng.lat <= this.s){
            this.s = event.latlng.lat
          } else {
            this.n = event.latlng.lat
          }
          if (event.latlng.lng <= this.w){
            this.w = event.latlng.lng
          } else {
          this.e = event.latlng.lng
          }
        }
        this.isMousedowned = false
      }
    },

    btn(){
      if (this.map.options.dragging){
        this.$refs.map.mapObject.dragging.disable()
        this.map.options.dragging = false
        this.message = "Move Map"
      } else {
        this.$refs.map.mapObject.dragging.enable()
        this.map.options.dragging = true
        this.message = "Draw Rectangle"
      }
    }
  },
  
  async created(){
  },
};
</script>
