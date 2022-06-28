<template>
  <div id="app">
    <v-col cols="12">
      <l-map ref="map" style="height: 600px; width: 800px;" :options="map.options" :center="map.center" :maxBounds="map.maxBounds" :zoom="map.zoom" :minZoom="map.minZoom" >
        <l-control-layers position="topright"></l-control-layers>
        <l-tile-layer v-for="tileProvider in tileProviders" :key="tileProvider.name" :name="tileProvider.name" :visible="tileProvider.visible" :url="tileProvider.url" :attribution="tileProvider.attribution" layer-type="base"/>
        <l-geo-json ref="myGeoJson" :geojson="prefecture.data" :options="prefectureOptions" :options-style="prefecture.style"></l-geo-json>
        <!-- <l-rectangle :bounds="[[s, w], [n, e]]" :l-style="rectangle.style"></l-rectangle> -->
      </l-map>
    </v-col>
    <v-col cols="4">
      <p>選択した都道府県：{{ selectedPrefectureName }}</p>
    </v-col>
    <v-col cols="3">
      <v-text-field v-model="s" label="南端緯度" outlined readonly persistent-placeholder></v-text-field>
      <v-text-field v-model="n" label="北端緯度" outlined readonly persistent-placeholder></v-text-field>
      <v-text-field v-model="w" label="西端経度" outlined readonly persistent-placeholder></v-text-field>
      <v-text-field v-model="e" label="東端経度" outlined readonly persistent-placeholder></v-text-field>
    </v-col>
  </div>
</template>

<script>
import { latLngBounds } from "leaflet";
import { LMap, LTileLayer, LControlLayers, LGeoJson, } from "vue2-leaflet";

// import { mapActions } from 'vuex';
export default {
  name: "InputData",
  // components: { LMap, LTileLayer, LControlLayers, LMarker, LRectangle, LGeoJson},
  components: { LMap, LTileLayer, LControlLayers, LGeoJson, },
  data() {
    return {
      s: '',
      n: '',
      w: '',
      e: '',
      selectedPrefectureName: '',

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
          url: 'https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png',
          attribution:
            '&copy; <a target="_blank" href="https://maps.gsi.go.jp/development/ichiran.html">地理院タイル</a>',
        }
      ],

      prefecture: {
        data: null, 
        style: {weight: 2, color: '#232323' , opacity: 1, fillColor: '#55FF00', fillOpacity: 0.2},
      },

      // rectangle: {
      //   style: {weight: 2, color: "#232323", opacity: 1, fillColor: "#FFFFFF", fillOpacity: 1.0}
      // },

    };
  },

  computed: {
    prefectureOptions() {
      return {
        onEachFeature: this.prefectureOnEachFeatureFunction
      };
    },
    prefectureOnEachFeatureFunction() {
      return (feature, layer) => {
        layer.bindTooltip(
          "<div>都道府県:" + feature.properties.name + 
          "</div><div>都道府県番号: " + feature.properties.pref + 
          "</div>", { permanent: false, sticky: true }
        );
        layer.on({'click': this.geojsonClick,})
      };
    },
  }, 
   
  methods: {
    geojsonClick(event){
      this.$refs.myGeoJson.mapObject.resetStyle()
      const layer = event.target
      layer.setStyle({fillOpacity: 0.7})
      this.selectedPrefectureName = layer.feature.properties.name
      const bounds = layer.getBounds()
      this.s = bounds._southWest.lat
      this.n = bounds._northEast.lat
      this.w = bounds._southWest.lng
      this.e = bounds._northEast.lng
    },
  },

  async created(){
    const response = await fetch('http://localhost/prefectures.geojson');
    this.prefecture.data = await response.json();
  },
};
</script>