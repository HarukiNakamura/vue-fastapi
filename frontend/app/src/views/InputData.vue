<template>
  <div id="app">
    <v-container fluid>
      <v-row>
        <v-col cols="3">
          <v-select
                    v-model="element.select"
                    hint="気象要素を選択して下さい。"
                    item-text="ele"
                    item-value="text"
                    :items="element.choices"
                    label="気象要素"
                    persistent-hint
                    persistent-placeholder
                    placeholder="日平均気温" 
                    :rules="[eleRules]">
            <template v-slot:append-outer><v-icon v-bind:color="element.iconColor">mdi-checkbox-marked-circle</v-icon></template>
          </v-select>
          <!-- <div>Your choice: {{ element.select }}</div> -->
          <!-- <div>Limit Date: {{ dateRange.max }}</div> -->
        </v-col>
      </v-row>
      <br>
      <p>開始日</p>
      <v-row>
        <v-col cols="3">
          <v-text-field 
            v-model="startDate.y"
            clearable
            hint="開始年を入力して下さい。"
            label="年"
            outlined
            persistent-hint
            persistent-placeholder
            placeholder="1980"
            :rules="[sdateyRules]"
            validate-on-blur>
          </v-text-field>
        </v-col>
        <v-col cols="2">
          <v-text-field 
            v-model="startDate.m"
            clearable
            hint="開始月を入力して下さい。"
            label="月"
            outlined
            persistent-hint
            persistent-placeholder
            placeholder="01"
            :rules="[sdatemRules]"
            validate-on-blur>
          </v-text-field>
        </v-col>
        <v-col cols="2">
          <v-text-field 
            v-model="startDate.d"
            clearable
            hint="開始日を入力して下さい。"
            label="日"
            outlined
            persistent-hint
            persistent-placeholder
            placeholder="01"
            :rules="[sdatedRules]"
            validate-on-blur>
          </v-text-field>          
        </v-col>
      </v-row>
      <br>
      <p>終了日</p>
      <v-row>
        <v-col cols="3">
          <v-text-field 
            v-model="endDate.y"
            clearable
            hint="終了年を入力して下さい。"
            label="年"
            outlined
            persistent-hint
            persistent-placeholder
            placeholder="1980"
            :rules="[edateyRules]"
            validate-on-blur>
          </v-text-field>
        </v-col>
        <v-col cols="2">
          <v-text-field 
            v-model="endDate.m"
            clearable
            hint="終了月を入力して下さい。"
            label="月"
            outlined
            persistent-hint
            persistent-placeholder
            placeholder="01"
            :rules="[edatemRules]"
            validate-on-blur>
          </v-text-field>
        </v-col>
        <v-col cols="2">
          <v-text-field 
            v-model="endDate.d"
            clearable
            hint="終了日を入力して下さい。"
            label="日"
            outlined
            persistent-hint
            persistent-placeholder
            placeholder="01"
            :rules="[edatedRules]"
            validate-on-blur>
          </v-text-field>          
        </v-col>
      </v-row>
      <v-row>
        <BaseMap>
        </BaseMap>
      </v-row>
      <v-row>
        <AnotherMap>
        </AnotherMap>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { latLngBounds } from 'leaflet';
// import { LMap, LTileLayer, LControlLayers, LMarker, LRectangle, LGeoJson} from "vue2-leaflet";
import BaseMap from '../components/BaseMap.vue';
import AnotherMap from '../components/AnotherMap.vue';

// import axios from "axios";
import { mapActions } from 'vuex';
export default {
  name: "InputData",
  // components: { LMap, LTileLayer, LControlLayers, LMarker, LRectangle, LGeoJson },
  components: { BaseMap, AnotherMap },
  data() {
    return {
      element: {
        choices: [{ele: '日平均気温', text: 'TMP_mea'},
                  {ele: '日最高気温', text: 'TMP_max'},
                  {ele: '日最低気温', text: 'TMP_min'},
                  {ele: '降水量', text: 'APCP'},
                  {ele: '1mm以上の降水の有無', text: 'OPR'},
                  {ele: '日照時間', text: 'SSD'},
                  {ele: '全天日射量', text: 'GSR'},
                  {ele: '下向き長波放射量', text: 'DLR'},
                  {ele: '日平均相対湿度', text: 'RH'},
                  {ele: '日平均風速', text: 'WIND'},
                  {ele: '積雪深', text: 'SD'},
                  {ele: '積雪相当水量', text: 'SWE'},
                  {ele: '日降雪相当水量', text: 'SFW'},
                 ],
        select: '',
        iconColor: '',
        valid: false
      },

      limitDate: '',
      dateRange: {min: new Date(1980, 0, 1), max: ''},

      startDate: {
        y: '',
        m: '',
        d: '',
        iconColor: '',
        yvalid: false,
        mvalid: false,
        dvalid: false,
        valid: false
      },

      endDate: {
        y: '',
        m: '',
        d: '',
        iconColor: '',
        yvalid: false,
        mvalid: false,
        dvalid: false,
        valid: false
      },


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

    eleRules: function(value){
      if (!!value == false){
        return '気象要素を選択して下さい！';
      } else {
        this.element.iconColor = 'green';
        this.element.valid = true;
        return true;
      }
    },

    getMaxDate: function(){
      let date = new Date();
      const plusNine = ['OPR', 'GSR', 'DLR', 'RH', 'WIND', 'SD', 'SWE', 'SFW'];
      if (plusNine.includes(this.element.select)){
        date.setDate(date.getDate() + 9);
      } else {
        date.setDate(date.getDate() + 26);
      }
      this.dateRange.max = date;
    },

    sdateyRules: function(value){
      if (!!value == false){
        return '開始年を入力して下さい！';
      }
      value = value.replace(/[０-９]/g, function(s) {return String.fromCharCode(s.charCodeAt(0) - 0xFEE0);});
      const regex = /\d{4}/;
      if ( !regex.test(value) || value.length > 4){
        return '開始年は数字4桁で入力して下さい！';
      }
      if (this.dateRange.min.getFullYear() > value || 
          this.dateRange.max.getFullYear() < value ){
        return `開始年は${this.dateRange.min.getFullYear()}年から${this.dateRange.max.getFullYear()}年の間で入力して下さい！`;
      }
      // if (this.endDate.y && value > this.endDate.y){
      //   return '開始年が終了年より大きいです！'
      // }
      this.startDate.y = value;
      this.startDate.yvalid = true;
      return true;
    },

    sdatemRules: function(value){
      if (!!value == false){
        return '開始月を入力して下さい！';
      }
      value = value.replace(/[０-９]/g, function(s) {return String.fromCharCode(s.charCodeAt(0) - 0xFEE0);});
      const regex = /\d{1,2}/;
      if ( !regex.test(value) || value.length > 2){
        return '開始月は数字2桁で入力して下さい！';
        // 'a2'とかがpassしてしまう。次のvalidationで引っかかるので取り敢えず、このまま。
      }
      const months = [...Array(12)].map((_, i) => i + 1)
      value = ('0' + value).slice(-2);
      if ( !months.includes(Number(value)) ){
        return '開始月は1 ~ 12の数字で入力して下さい！'
      }
      if ((this.startDate.y == this.dateRange.max.getFullYear()) && (value > this.dateRange.max.getMonth() + 1)) {
        return `${this.dateRange.max.getFullYear()}年${this.dateRange.max.getMonth()+1}月${this.dateRange.max.getDate()}日までのデータが取得可能です。`
      }
      this.startDate.m = value;
      this.startDate.mvalid = true;
      return true;
    },

    sdatedRules: function(value){
      if (!!value == false){
        return '開始日を入力して下さい！';
      }
      value = value.replace(/[０-９]/g, function(s) {return String.fromCharCode(s.charCodeAt(0) - 0xFEE0);});
      const regex = /\d{1,2}/;
      if ( !regex.test(value) || value.length > 2){
        return '開始月は数字2桁で入力して下さい！';
        // 'a2'とかがpassしてしまう。次のvalidationで引っかかるので取り敢えず、このまま。
      }
      const days = [...Array(31)].map((_, i) => i + 1)
      value = ('0' + value).slice(-2);
      if ( !days.includes(Number(value)) ){
        return '開始日は1 ~ 31の数字で入力して下さい！'
      }
      if ((this.startDate.y == this.dateRange.max.getFullYear()) && (this.startDate.m == this.dateRange.max.getMonth()+1) && (value > this.dateRange.max.getDate())) {
        return `${this.dateRange.max.getFullYear()}年${this.dateRange.max.getMonth()+1}月${this.dateRange.max.getDate()}日までのデータが取得可能です。`
      }
      this.startDate.d = value;
      this.startDate.dvalid = true;
      return true;
    },

    edateyRules: function(value){
      if (!!value == false){
        return '終了年を入力して下さい！';
      }
      value = value.replace(/[０-９]/g, function(s) {return String.fromCharCode(s.charCodeAt(0) - 0xFEE0);});
      const regex = /\d{4}/;
      if ( !regex.test(value) || value.length > 4){
        return '終了年は数字4桁で入力して下さい！';
      }
      if (this.dateRange.min.getFullYear() > value || 
          this.dateRange.max.getFullYear() < value ){
        return `終了年は${this.dateRange.min.getFullYear()}年から${this.dateRange.max.getFullYear()}年の間で入力して下さい！`;
      }
      this.endDate.y = value;
      this.endDate.yvalid = true;
      return true;
    },

    edatemRules: function(value){
      if (!!value == false){
        return '終了月を入力して下さい！';
      }
      value = value.replace(/[０-９]/g, function(s) {return String.fromCharCode(s.charCodeAt(0) - 0xFEE0);});
      const regex = /\d{1,2}/;
      if ( !regex.test(value) || value.length > 2){
        return '終了月は数字2桁で入力して下さい！';
      }
      const months = [...Array(12)].map((_, i) => i + 1)
      value = ('0' + value).slice(-2);
      if ( !months.includes(Number(value)) ){
        return '終了月は1 ~ 12の数字で入力して下さい！'
      }
      if ((this.endDate.y == this.dateRange.max.getFullYear()) && (value > this.dateRange.max.getMonth() + 1)) {
        return `${this.dateRange.max.getFullYear()}年${this.dateRange.max.getMonth()+1}月${this.dateRange.max.getDate()}日までのデータが取得可能です。`
      }
      this.endDate.m = value;
      this.endDate.mvalid = true;
      return true;
    },

    edatedRules: function(value){
      if (!!value == false){
        return '終了日を入力して下さい！';
      }
      value = value.replace(/[０-９]/g, function(s) {return String.fromCharCode(s.charCodeAt(0) - 0xFEE0);});
      const regex = /\d{1,2}/;
      if ( !regex.test(value) || value.length > 2){
        return '終了月は数字2桁で入力して下さい！';
        // 'a2'とかがpassしてしまう。次のvalidationで引っかかるので取り敢えず、このまま。
      }
      const days = [...Array(31)].map((_, i) => i + 1)
      value = ('0' + value).slice(-2);
      if ( !days.includes(Number(value)) ){
        return '終了日は1 ~ 31の数字で入力して下さい！'
      }
      if ((this.endDate.y == this.dateRange.max.getFullYear()) && (this.startDate.m == this.dateRange.max.getMonth()+1) && (value > this.dateRange.max.getDate())) {
        return `${this.dateRange.max.getFullYear()}年${this.dateRange.max.getMonth()+1}月${this.dateRange.max.getDate()}日までのデータが取得可能です。`
      }
      this.endDate.d = value;
      this.endDate.dvalid = true;
      return true;
    },

    // その日付が存在するかどうか、のバリデーション
    // 開始日 <= 終了日のバリデーション
    // 気象要素が変更された場合に取得範囲が変わり、その際のバリデーション
    // y,m,dがすべてvalid=trueになったら、アイコンの色とvalidをtruにする。


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

  watch: {
    'element.select': function(){
      this.getMaxDate()
    },
  },

  async created(){
    this.getMaxDate()
    const response = await fetch('http://localhost/prefectures.geojson');
    this.prefecture.data = await response.json();
  },
};
</script>