<template>
  <l-map
    id="map"
    ref="map"
    :options="map.options"
    :center="map.center"
    :maxBounds="map.maxBounds"
    :zoom="map.zoom"
    :minZoom="map.minZoom"
    :maxZoom="map.maxZoom"
    @mousedown="mapMousedown($event)"
    @mousemove="mapMousemove($event)"
    @mouseup="mapMouseup($event)">
    <l-control-layers position="topright"></l-control-layers>
    <l-tile-layer
      v-for="tileProvider in tileProviders"
      :key="tileProvider.name"
      :name="tileProvider.name"
      :visible="tileProvider.visible"
      :url="tileProvider.url"
      :attribution="tileProvider.attribution"
      layer-type="base"/>
      <slot name="map-content"></slot>
  </l-map>
</template>

<script>
import L from 'leaflet';
import { LMap, LTileLayer, LControlLayers, } from "vue2-leaflet";
import { mapState, mapMutations, } from 'vuex';

export default {
  name: 'BaseMap',
  components: { LMap, LTileLayer, LControlLayers, },
  props: {
    'pageName': String,
    },
  data() {
    return {
      page: '',

      map: {
        options: {
          preferCanvas: true,
          dragging: true,
          // doubleClickZoom: false,
        },
        center: [35.693825, 139.703356],
        maxBounds: [[23, 120],[46, 150]],
        zoom: 6,
        minZoom: 5,
        maxZoom: 12,
        inertia: false,
      },

      isMousedowned: false,
      initialLat: '',
      initialLng: '',
      s: '',
      n: '',
      w: '',
      e: '',      

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
    }
  },

  computed: {
    ...mapState(['border']),
  },

  methods: {
    ...mapMutations(['setBorder',]),

    mapMousedown: function(event){
      if (this.pageName==="inputData" && !this.$refs.map.mapObject.dragging._enabled){
        this.initialLat = event.latlng.lat
        this.initialLng = event.latlng.lng
        this.s = event.latlng.lat
        this.n = event.latlng.lat
        this.w = event.latlng.lng
        this.e = event.latlng.lng
        this.isMousedowned = true
        this.setBorder({value:[this.s, this.n, this.w, this.e], valid:true})
      }
    },
    mapMousemove: function(event){
      if (this.pageName==="inputData" && this.isMousedowned ){
        event.latlng.lat >= this.initialLat ? this.n = event.latlng.lat : this.s = event.latlng.lat
        event.latlng.lng >= this.initialLng ? this.e = event.latlng.lng : this.w = event.latlng.lng
        this.setBorder({value:[this.s, this.n, this.w, this.e], valid:true})
      }
    },
    mapMouseup: function(event){
      if (this.pageName==="inputData" && this.isMousedowned){
        event.latlng.lat >= this.initialLat ? this.n = event.latlng.lat : this.s = event.latlng.lat
        event.latlng.lng >= this.initialLng ? this.e = event.latlng.lng : this.w = event.latlng.lng
        this.setBorder({value:[this.s, this.n, this.w, this.e], valid:true})
        this.isMousedowned = false
      }
    },        
  },

  mounted(){
    if (this.border.data.length){
      this.$refs.map.mapObject.fitBounds(L.latLngBounds([this.border.data[0],this.border.data[2]], [this.border.data[1],this.border.data[3]]))
    }
  },  
}
</script>

<style>
/* .map-wrapper {
  position: relative;
} */

#map {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  min-height: 400px;
}
</style>