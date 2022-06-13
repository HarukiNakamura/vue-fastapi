<template>
  <div id="app">
    <div>
      {{ message }}
      <br>      
    </div>
    <div>
      <label>meshの有無</label>
      <input id="checkbox" v-model="mesh.show" type="checkbox">
      <button @click="runMesh">Show Result</button>
      <l-map ref="map" style="height: 400px; width: 600px;" :options="map.options" :center="map.center" :maxBounds="map.maxBounds" :zoom="map.zoom" :minZoom="map.minZoom">
        <l-control-layers position="topright"></l-control-layers>
        <l-tile-layer v-for="tileProvider in tileProviders" :key="tileProvider.name" :name="tileProvider.name" :visible="tileProvider.visible" :url="tileProvider.url" :attribution="tileProvider.attribution" layer-type="base"/>
        <l-geo-json v-if="mesh.show" :geojson="mesh.data" :options="meshOptions" :options-style="mesh.style"></l-geo-json>
      </l-map>
    </div>
    <button onclick="location.href='/'">入力画面に戻る</button>
  </div>
</template>

<script>
import { latLngBounds } from "leaflet";
import { LMap, LTileLayer, LControlLayers, LGeoJson} from "vue2-leaflet";

import axios from "axios";

export default {
  name: "ShowResult",

  components: { LMap, LTileLayer, LControlLayers, LGeoJson},
  data() {
    return {
      
      map: {
        options: {
          preferCanvas: true,
          // doubleClickZoom: false,
        },
        center: [35.693825, 139.703356],
        maxBounds: latLngBounds([
          [23, 120],
          [46, 150]
        ]),
        zoom: 8,
        minZoom: 4,
        inertia: false
      },

      tileProviders: [
        {
          name: '標準地図',
          visible: false,
          url: 'https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png',
          attribution:
            '&copy; <a target="_blank" href="http://osm.org/copyright">地理院タイル</a>',
        },
        {
          name: '淡色地図',
          visible: true,
          url: 'https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png',
          attribution:
            '&copy; <a target="_blank" href="http://osm.org/copyright">地理院タイル</a>',
        },
      ],

      mesh: {
        data: null,
        style: {weight: 0, color: "#000000", opacity: 0, fillColor: "#3a2f4d", fillOpacity: 1},
        show: false,
      },

      message: '',
    };
  },

  computed: {
    meshOptions() {
      return {
        onEachFeature: this.meshOnEachFeatureFunction
      };
    }, 
    meshOnEachFeatureFunction() {
      return (feature, layer) => {
        layer.options.fillColor = feature.properties.fillcolor;  
        layer.bindTooltip(
          "<div>メッシュ番号:" + feature.properties.meshcode + 
          "</div><div>気象データ: " + feature.properties.eledata + 
          "</div>", { permanent: false, sticky: true }
        );
      };
    },
  },

  mounted () {
    axios.get('http://localhost:3000/api/result')
    .then(response => (this.message = response))
  },

  methods: {
    async runMesh() {
      const response = await fetch('http://localhost/meshdata.geojson');
      this.mesh.data = await response.json();
      this.mesh.show = true;
    },
  },
};
</script>


<!-- <style>
</style> -->
