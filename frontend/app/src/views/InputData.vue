<template>
  <div id="app">
    <select v-model="inputData.metElement">
      <option value="TMP_mea">日平均気温</option>
      <option value="TMP_max">日最高気温</option>
      <option value="TMP_min">日最低気温</option>
      <option value="APCP">降水量</option>
      <option value="OPR">1mm以上の降水の有無</option>
      <option value="SSD">日照時間</option>
      <option value="GSR">全天日射量</option>
      <option value="DLR">下向き長波放射量</option>
      <option value="RH">日平均相対湿度</option>
      <option value="WIND">WIND</option>
      <option value="SD">積雪深</option>
      <option value="SWE">積雪相当水量</option>
      <option value="SFW">日降雪相当水量</option>
      <option value="PTMP">予報気温の確からしさ</option>
    </select>
    <p>Your Choice: {{ inputData.metElement }}</p>
    <input v-model="inputData.date[0]" type="date" min="1980-01-01" max="2022-06-16">
    <input v-model="inputData.date[1]" type="date" min="1980-01-01" max="2022-06-16">
    <div>
      <label for="checkbox">県境の有無</label>
      <input id="checkbox" v-model="prefecture.show" type="checkbox">
    </div>
    <l-map ref="map" style="height: 400px; width: 600px;" :options="map.options" :center="map.center" :maxBounds="map.maxBounds" :zoom="map.zoom" :minZoom="map.minZoom" @click="addMarker($event), borderMarker(), countClick()" >
    <!-- counterLimitの制限を越えたら、マーカーを全削除するようにする? -->
      <l-control-layers position="topright"></l-control-layers>
      <l-tile-layer v-for="tileProvider in tileProviders" :key="tileProvider.name" :name="tileProvider.name" :visible="tileProvider.visible" :url="tileProvider.url" :attribution="tileProvider.attribution" layer-type="base"/>
      <l-marker v-for="(marker, index) in markers" :lat-lng="marker" v-bind:key="index" @click="removeMarker(index), borderMarker()"></l-marker>
      <l-rectangle v-if="markers.length" :bounds="[[inputData.border[0], inputData.border[2]], [inputData.border[1], inputData.border[3]]]" :l-style="rectangle.style"></l-rectangle>
      <l-geo-json v-if="prefecture.show" :geojson="prefecture.data" :options="prefectureOptions" :options-style="prefecture.style"></l-geo-json>
    </l-map>
    <div>
      南端緯度: {{ inputData.border[0] }}<br>
      北端緯度: {{ inputData.border[1] }}<br>
      西端経度: {{ inputData.border[2] }}<br>
      東端経度: {{ inputData.border[3] }}<br>
    </div>    
    <div>
      <button @click="postData(inputData)">run mesh</button>
    </div>
  </div>
</template>

<script>
import { latLngBounds } from "leaflet";
import { LMap, LTileLayer, LControlLayers, LMarker, LRectangle, LGeoJson} from "vue2-leaflet";
// import axios from "axios";
import { mapActions } from 'vuex';

export default {
  name: "InputData",

  components: { LMap, LTileLayer, LControlLayers, LMarker, LRectangle, LGeoJson},

  data() {
    return {
      counter: 0,
      counterLimit: 10,

      inputData: {
        metElement: '',
        date: [],
        border: [],
      },

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

      markers: [],

      rectangle: {
        style: {fillColor: 'red', fillOpacity: 0.5, color: 'black', weight: 2}
      },

      prefecture: {
        data: null, 
        style: {weight: 2, color: "#000000", opacity: 1, fillColor: "#4072B3", fillOpacity: 0.2},
        show: true,
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
      };
    },
  }, 
   
  methods: {
    ...mapActions([
      'postData',
    ]),

    addMarker: function(event) {
      this.markers.push(event.latlng);
    },

    countClick: function() {
      this.counter ++;
      if (this.counter > this.counterLimit){
        alert("これ以上マーカーを打てません。");
        this.removeAllMarker();
      }
    },

    removeMarker: function(index) {
      this.markers.splice(index, 1);
      this.counter --;
      if (this.counter === 0){
        this.inputData.border = [];
      }
    },

    removeAllMarker: function() {
      this.markers = [];
      this.inputData.border = [];
      this.counter = 0;
    },

    borderMarker: function() {
      if (this.markers.length){
        let m_lat = 10000;
        let M_lat = 0;
        let m_lng = 10000;
        let M_lng = 0;
        for (let i=0; i<this.markers.length; i++){
          m_lat = Math.min(m_lat, this.markers[i].lat);
          M_lat = Math.max(M_lat, this.markers[i].lat);
          m_lng = Math.min(m_lng, this.markers[i].lng);
          M_lng = Math.max(M_lng, this.markers[i].lng);
          this.inputData.border[0] = m_lat;
          this.inputData.border[1] = M_lat;
          this.inputData.border[2] = m_lng;
          this.inputData.border[3] = M_lng;
        }
      } 
    },
  },
  async created(){
    const response = await fetch('http://localhost/prefectures.geojson');
    this.prefecture.data = await response.json();
  },
};
</script>
