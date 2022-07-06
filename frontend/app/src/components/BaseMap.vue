<template>
  <l-map
    id="map"
    ref="map"
    :options="map.options"
    :center="map.center"
    :maxBounds="map.maxBounds"
    :zoom="map.zoom"
    :minZoom="map.minZoom"
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
import { latLngBounds } from "leaflet";
// import { LMap, LTileLayer, LControlLayers, LGeoJson, LRectangle, LControl, } from "vue2-leaflet";
import { LMap, LTileLayer, LControlLayers, } from "vue2-leaflet";
import { mapMutations, } from 'vuex';

export default {
  name: 'BaseMap',
  components: { LMap, LTileLayer, LControlLayers, },
  props: {'pageName': String,},
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
        maxBounds: latLngBounds([
          [23, 120],
          [46, 150]
        ]),
        zoom: 6,
        minZoom: 4,
        inertia: false
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
  },


  methods: {
    ...mapMutations(['setBorder',]),

    mapMousedown: function(event){
      if (this.pageName==="inputData"){
        this.initialLat = event.latlng.lat
        this.initialLng = event.latlng.lng
        this.s = event.latlng.lat
        this.n = event.latlng.lat
        this.w = event.latlng.lng
        this.e = event.latlng.lng
        this.isMousedowned = true
        this.setBorder([this.s, this.n, this.w, this.e])
      }
    },
    mapMousemove: function(event){
      if (this.pageName==="inputData" && this.isMousedowned ){
        event.latlng.lat >= this.initialLat ? this.n = event.latlng.lat : this.s = event.latlng.lat
        event.latlng.lng >= this.initialLng ? this.e = event.latlng.lng : this.w = event.latlng.lng
        this.setBorder([this.s, this.n, this.w, this.e])
      }
    },
    mapMouseup: function(event){
      if (this.pageName==="inputData" && this.isMousedowned){
        event.latlng.lat >= this.initialLat ? this.n = event.latlng.lat : this.s = event.latlng.lat
        event.latlng.lng >= this.initialLng ? this.e = event.latlng.lng : this.w = event.latlng.lng
        this.setBorder([this.s, this.n, this.w, this.e])
        this.isMousedowned = false
      }
    },        
    // mapMousedown: function(event){
    //   if (!this.map.options.dragging){
    //     this.isMousedowned = true
    //     this.initialLat = event.latlng.lat
    //     this.initialLng = event.latlng.lng
    //     this.s = event.latlng.lat
    //     this.n = event.latlng.lat
    //     this.w = event.latlng.lng
    //     this.e = event.latlng.lng
    //     this.setBorder([this.s, this.n, this.w, this.e])
    //   }
    // },

    // mapMousemove: function(event){
    //   if (!this.map.options.dragging){
    //     if (this.isMousedowned){
    //       if (event.latlng.lat >= this.initialLat){
    //         this.n = event.latlng.lat
    //       } else {
    //         this.s = event.latlng.lat
    //       }
    //       if (event.latlng.lng >= this.initialLng){
    //         this.e = event.latlng.lng
    //       } else {
    //         this.w = event.latlng.lng
    //       }
    //       this.setBorder([this.s, this.n, this.w, this.e])
    //     }
    //   }
    // },

    // mapMouseup: function(event){
    //   if (!this.map.options.dragging){
    //     if (this.isMousedowned){
    //       if (event.latlng.lat >= this.initialLat){
    //         this.n = event.latlng.lat
    //       } else {
    //         this.s = event.latlng.lat
    //       }
    //       if (event.latlng.lng >= this.initialLng){
    //         this.e = event.latlng.lng
    //       } else {
    //         this.w = event.latlng.lng
    //       }
    //       this.setBorder([this.s, this.n, this.w, this.e])
    //     }
    //     this.isMousedowned = false
    //   }
    // }, 
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
}
</style> -->
<!-- <template>
  <div id="app">
    <v-col cols="12">
      <v-btn v-if="pageName==='inputData'" @click="changeSelectBy">{{ btnmsg }}で範囲を指定する</v-btn>
      <div class="map-wrapper">
      <l-map id="map" ref="map" style="height: 600px; width: 800px;" :options="map.options" :center="map.center" :maxBounds="map.maxBounds" :zoom="map.zoom" :minZoom="map.minZoom" @mousedown="mapMousedown($event)" @mousemove="mapMousemove($event)" @mouseup="mapMouseup($event)">
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
        <l-geo-json v-if="mesh.show" :geojson="mesh.data[i].geojson" :options="meshOptions" :options-style="mesh.style"></l-geo-json>
      </template>
      </l-map>
      </div>
      <v-slider v-if="pageName==='showResult'"
                v-model="i"
                :max="Object.keys(mesh.data).length - 1"
                label="日付選択"
                step="1"
                thumb-label
                :thumb-size="60"
                tick>
                 <template v-slot:thumb-label="{ value }">{{ Object.values(mesh.data).map(x => x.time)[value] }}</template>
                </v-slider>
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

import { mapState, mapMutations, } from 'vuex';

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

      i: 0,

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
    ...mapState(['mesh']),
    prefectureOptions: function(){
      return {
        onEachFeature: this.prefectureOnEachFeatureFunction
      };
    },
    prefectureOnEachFeatureFunction: function() {
      return (feature, layer) => {
        layer.bindTooltip(
          "<div>都道府県:" + feature.properties.name +
          "</div><div>都道府県番号: " + feature.properties.pref +
          "</div>", { permanent: false, sticky: true }
        );
        layer.on({'click': this.geojsonClick,})
      };
    },
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

  methods: {
    ...mapMutations(['setBorder',]),

    changeSelectBy: function(){
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

    geojsonClick: function(event){
      this.$refs.myGeoJson.mapObject.resetStyle()
      const layer = event.target
      layer.setStyle({fillOpacity: 0.7})
      this.prefectureName = layer.feature.properties.name
      const bounds = layer.getBounds()
      this.s = bounds._southWest.lat
      this.n = bounds._northEast.lat
      this.w = bounds._southWest.lng
      this.e = bounds._northEast.lng
      this.setBorder([this.s, this.n, this.w, this.e])
    },

    controlMapDraggable: function(){
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

    mapMousedown: function(event){
      if (!this.map.options.dragging){
        this.isMousedowned = true
        this.initialLat = event.latlng.lat
        this.initialLng = event.latlng.lng
        this.s = event.latlng.lat
        this.n = event.latlng.lat
        this.w = event.latlng.lng
        this.e = event.latlng.lng
        this.setBorder([this.s, this.n, this.w, this.e])
      }
    },

    mapMousemove: function(event){
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
          this.setBorder([this.s, this.n, this.w, this.e])
        }
      }
    },

    mapMouseup: function(event){
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
          this.setBorder([this.s, this.n, this.w, this.e])
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

<style>
.map-wrapper {
  position: relative;
}

#map {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}
</style> -->