<template>
  <div id="app">
    <v-col cols="12">
      <l-map ref="map" style="height: 600px; width: 800px;" :options="map.options" :center="map.center" :maxBounds="map.maxBounds" :zoom="map.zoom" :minZoom="map.minZoom" @mousedown="mapMousedown($event)" @mousemove="mapMousemove($event)" @mouseup="mapMouseup($event)">
      <l-control-layers position="topright"></l-control-layers>
      <l-tile-layer v-for="tileProvider in tileProviders" :key="tileProvider.name" :name="tileProvider.name" :visible="tileProvider.visible" :url="tileProvider.url" :attribution="tileProvider.attribution" layer-type="base"/>
      <template v-if="pageName==='inputData'">
        <l-geo-json v-if="selectBy==='prefecture'" ref="myGeoJson" :geojson="prefecture.data" :options="prefectureOptions" :options-style="prefecture.style"></l-geo-json>
        <template v-else-if="selectBy==='rectangle'">
          <l-control position="bottomleft">
            <v-tooltip right>
              <template v-slot:activator="{ on, attrs }">
                <v-btn v-bind="attrs" v-on="on" @click="controlMapDraggable">
                  <v-icon>{{ icon }}</v-icon>
                </v-btn>
              </template>
              <span>{{ message }}</span>
            </v-tooltip>
          </l-control>
          <l-rectangle :bounds="[[s, w], [n, e]]" :l-style="rectangle.style"></l-rectangle>
        </template>
      </template>
      <template v-else-if="pageName==='showResult'">
      </template>
      </l-map>
      <v-btn v-if="pageName==='inputData'" @click="changeSelectBy">{{ btnmsg }}で範囲を指定する</v-btn>
    </v-col>
    <v-col v-if="pageName==='inputData'" cols="4">
      <p v-if="selectBy==='prefecture'">選択した都道府県：{{ prefectureName }}</p>
      <p v-else-if="selectBy==='rectangle'">手動での入力も可能です。</p>
      <v-text-field v-model="s" label="南端緯度" outlined :readonly="readonly"></v-text-field>
      <v-text-field v-model="n" label="北端緯度" outlined :readonly="readonly"></v-text-field>
      <v-text-field v-model="w" label="西端経度" outlined :readonly="readonly"></v-text-field>
      <v-text-field v-model="e" label="東端経度" outlined :readonly="readonly"></v-text-field>
    </v-col>
  </div>
</template>

<script>
import { latLngBounds } from "leaflet";
import { LMap, LTileLayer, LControlLayers, LGeoJson, LRectangle, LControl, } from "vue2-leaflet";


export default {
  name: "InputData",
  components: { LMap, LTileLayer, LControlLayers, LGeoJson, LRectangle, LControl, },
  props: {'pageName': String,},
  data() {
    return {
      prefectureName: '',
      initialLat: '',
      initialLng: '',
      s: '',
      n: '',
      w: '',
      e: '',
      selectBy: 'prefecture',
      btnmsg: '矩形',
      readonly: true,
      icon: 'mdi-vector-rectangle',
      message: '領域を選択する',
      
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

      prefecture: {
        data: null, 
        style: {weight: 2, color: "#232323", opacity: 1, fillColor: "#55FF00", fillOpacity: 0.2},
        show: true,
      },

      rectangle: {
        style: {weight: 2, color: "#232323", opacity: 1, fillColor: "#55FF00", fillOpacity: 0.7}
      }, 
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
    changeSelectBy(){
      if (this.selectBy === "prefecture"){
        this.selectBy = "rectangle"
        this.btnmsg = "都道府県"
        this.readonly = false
      } else {
        this.prefectureName = ''
        this.$refs.map.mapObject.dragging.enable()
        this.map.options.dragging = true
        this.selectBy = "prefecture"
        this.btnmsg = "矩形"
        this.readonly = true
      }
    },

    geojsonClick(event){
      this.$refs.myGeoJson.mapObject.resetStyle()
      const layer = event.target
      layer.setStyle({fillOpacity: 0.7})
      this.prefectureName = layer.feature.properties.name
      const bounds = layer.getBounds()
      this.s = bounds._southWest.lat
      this.n = bounds._northEast.lat
      this.w = bounds._southWest.lng
      this.e = bounds._northEast.lng
    },

    controlMapDraggable(){
      if (this.map.options.dragging){
        this.$refs.map.mapObject.dragging.disable()
        this.icon = "mdi-arrow-all"
        this.message = '地図を移動する'
        this.map.options.dragging = false
      } else {
        this.$refs.map.mapObject.dragging.enable()
        this.icon = "mdi-vector-rectangle"
        this.message = '領域を選択する'
        this.map.options.dragging = true
      }
    },

    mapMousedown(event){
      if (!this.map.options.dragging){
        this.isMousedowned = true
        this.initialLat = event.latlng.lat
        this.initialLng = event.latlng.lng
        this.s = event.latlng.lat
        this.n = event.latlng.lat
        this.w = event.latlng.lng
        this.e = event.latlng.lng
      }
    },

    mapMousemove(event){
      if (!this.map.options.dragging){
        if (this.isMousedowned){
          if (event.latlng.lat >= this.initialLat){
            this.n = event.latlng.lat
          } else {
            this.s = event.latlng.lat
          }
          if (event.latlng.lng >= this.initialLng){
            this.e = event.latlng.lng
          } else {
            this.w = event.latlng.lng
          }
        }
      }
    },

    mapMouseup(event){
      if (!this.map.options.dragging){
        if (this.isMousedowned){
          if (event.latlng.lat >= this.initialLat){
            this.n = event.latlng.lat
          } else {
            this.s = event.latlng.lat
          }
          if (event.latlng.lng >= this.initialLng){
            this.e = event.latlng.lng
          } else {
            this.w = event.latlng.lng
          }
        }
        this.isMousedowned = false
      }
    },
  },
  
  async created(){
    const response = await fetch('http://localhost/prefectures.geojson');
    this.prefecture.data = await response.json();
  },
};
</script>
