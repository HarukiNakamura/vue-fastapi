<template>
  <base-view>
    <template v-slot:left-content>
      <v-row>
        <v-col cols="12" sm="9" md="8" lg="5" xl="4">
          <v-select
              v-model="element.select"
              clearable
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
        </v-col>
      </v-row>
      <br>
      <p>開始日</p>
      <v-form ref="formsd">
        <v-row>
          <v-col cols="5" sm="4" md="4" lg="3" xl="3">
            <v-text-field
              v-model="startDate.y"
              clearable
              label="年"
              outlined
              persistent-hint
              persistent-placeholder
              placeholder="1980"
              :rules="[sdateyRules]"
              validate-on-blur
              @blur="isSDate">
            </v-text-field>
          </v-col>
          <v-col cols="3" sm="3" md="3" lg="2" xl="2">
            <v-text-field
              v-model="startDate.m"
              clearable
              label="月"
              outlined
              persistent-hint
              persistent-placeholder
              placeholder="01"
              :rules="[sdatemRules]"
              validate-on-blur
              @blur="isSDate">
            </v-text-field>
          </v-col>
          <v-col cols="3" sm="3" md="3" lg="2" xl="2">
            <v-text-field
              v-model="startDate.d"
              clearable
              label="日"
              outlined
              persistent-hint
              persistent-placeholder
              placeholder="01"
              :rules="[sdatedRules]"
              validate-on-blur
              @blur="isSDate">
            </v-text-field>          
          </v-col>
        </v-row>
      </v-form>
      <br>
      <p>終了日</p>
      <v-form ref="formed">
        <v-row>        
          <v-col cols="5" sm="4" md="4" lg="3" xl="3">
            <v-text-field
              v-model="endDate.y"
              clearable
              label="年"
              outlined
              persistent-hint
              persistent-placeholder
              placeholder="1980"
              :rules="[edateyRules]"
              validate-on-blur
              @blur="isEDate">
            </v-text-field>
          </v-col>
          <v-col cols="3" sm="3" md="3" lg="2" xl="2">
            <v-text-field
              v-model="endDate.m"
              clearable
              label="月"
              outlined
              persistent-hint
              persistent-placeholder
              placeholder="01"
              :rules="[edatemRules]"
              validate-on-blur
              @blur="isEDate">
            </v-text-field>
          </v-col>
          <v-col cols="3" sm="3" md="3" lg="2" xl="2">
            <v-text-field
              v-model="endDate.d"
              clearable
              label="日"
              outlined
              persistent-hint
              persistent-placeholder
              placeholder="01"
              :rules="[edatedRules]"
              validate-on-blur
              @blur="isEDate">
            </v-text-field>          
          </v-col>
        </v-row>
      </v-form>
    </template>
    <template v-slot:right-content>
      <base-map :pageName="pageName">
        <template v-slot:map-content>
          <l-control position="bottomleft">
            <v-btn @click="changeSelectBy">
              <!-- <v-icon>{{ icon }}</v-icon> -->
              {{ btnmsg }}で範囲を指定する
            </v-btn>
          </l-control>
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
            <l-rectangle :bounds="[[border[0], border[2]], [border[1], border[3]]]" :l-style="rectangle.style"></l-rectangle>
          </template>          
        </template>
      </base-map>
    </template>
  </base-view>
      <!-- <v-btn @click="postData({metElement: element.select, 
                               date: [formatDate(startDate.y, startDate.m, startDate.d), formatDate(endDate.y, endDate.m, endDate.d)], 
                               border: border,})">Run Mesh</v-btn> -->
</template>


<script>
import BaseView from '@/components/BaseView.vue';
import BaseMap from '@/components/BaseMap.vue';
import { mapState, mapActions } from 'vuex';

import { LGeoJson, LRectangle, LControl, } from "vue2-leaflet";

export default {
  name: "InputData",
  components: { BaseView, BaseMap, LGeoJson, LRectangle, LControl, },
  data() {
    return {
      pageName: 'inputData',

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

    selectBy: 'prefecture',
    btnmsg: '矩形',
    readonly: true,
    draggable: true,
    icon: 'mdi-vector-rectangle',
    message: '領域を選択する',

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
    ...mapState(['border']),

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
  },

  methods: {
    ...mapActions([
      'postData',
    ]),

    formatDate: function(y, m, d){
      return y + '-' + m + '-' + d
    },

    eleRules: function(value){
      if (!value){
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
      if (!value){
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
      if (this.startDate.m && this.startDate.d){
        const date = new Date(this.startDate.y, this.startDate.m - 1, this.startDate.d)
        const month = date.getMonth() + 1
        if (this.startDate.m != month) {
          return '存在しない日付です。'
        }
      }
      this.startDate.y = value;
      this.startDate.yvalid = true;
      return true;
    },

    sdatemRules: function(value){
      if (!value){
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
      if (this.startDate.y && this.startDate.d){
        const date = new Date(this.startDate.y, this.startDate.m - 1, this.startDate.d)
        const month = date.getMonth() + 1
        if (this.startDate.m != month) {
          return '存在しない日付です。'
        }
      }
      this.startDate.m = value;
      this.startDate.mvalid = true;
      return true;
    },

    sdatedRules: function(value){
      if (!value){
        return '開始日を入力して下さい！';
      }
      value = value.replace(/[０-９]/g, function(s) {return String.fromCharCode(s.charCodeAt(0) - 0xFEE0);});
      const regex = /\d{1,2}/;
      if ( !regex.test(value) || value.length > 2){
        return '開始月は数字2桁で入力して下さい！';
      }
      const days = [...Array(31)].map((_, i) => i + 1)
      value = ('0' + value).slice(-2);
      if ( !days.includes(Number(value)) ){
        return '開始日は1 ~ 31の数字で入力して下さい！'
      }
      if ((this.startDate.y == this.dateRange.max.getFullYear()) && (this.startDate.m == this.dateRange.max.getMonth()+1) && (value > this.dateRange.max.getDate())) {
        return `${this.dateRange.max.getFullYear()}年${this.dateRange.max.getMonth()+1}月${this.dateRange.max.getDate()}日までのデータが取得可能です。`
      }
      if (this.startDate.y && this.startDate.m){
        const date = new Date(this.startDate.y, this.startDate.m - 1, this.startDate.d)
        const month = date.getMonth() + 1
        if (this.startDate.m != month) {
          return '存在しない日付です。'
        }
      }      
      this.startDate.d = value;
      this.startDate.dvalid = true;
      return true;
    },

    isSDate: function(){
      if (this.startDate.y && this.startDate.m && this.startDate.d){
        this.$refs.formsd.validate()
      }
    },


    edateyRules: function(value){
      if (!value){
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
      if (this.endDate.m && this.endDate.d){
        const date = new Date(this.endDate.y, this.endDate.m - 1, this.endDate.d)
        const month = date.getMonth() + 1
        if (this.endDate.m != month) {
          return '存在しない日付です。'
        }
      }       
      this.endDate.y = value;
      this.endDate.yvalid = true;
      return true;
    },

    edatemRules: function(value){
      if (!value){
        return '終了月を入力して下さい！';
      }
      value = value.replace(/[０-９]/g, function(s) {return String.fromCharCode(s.charCodeAt(0) - 0xFEE0);});
      const regex = /\d{1,2}/;
      if ( !regex.test(value) || value.length > 2){
        return '終了月は数字2桁で入力して下さい！';
      }
      const months = [...Array(12)].map((_, i) => i + 1);
      value = ('0' + value).slice(-2);
      if ( !months.includes(Number(value)) ){
        return '終了月は1 ~ 12の数字で入力して下さい！'
      }
      if ((this.endDate.y == this.dateRange.max.getFullYear()) && (value > this.dateRange.max.getMonth() + 1)) {
        return `${this.dateRange.max.getFullYear()}年${this.dateRange.max.getMonth()+1}月${this.dateRange.max.getDate()}日までのデータが取得可能です。`
      }
      if (this.endDate.y && this.endDate.d){
        const date = new Date(this.endDate.y, this.endDate.m - 1, this.endDate.d)
        const month = date.getMonth() + 1
        if (this.endDate.m != month) {
          return '存在しない日付です。'
        }
      }        
      this.endDate.m = value;
      this.endDate.mvalid = true;
      return true;
    },

    edatedRules: function(value){
      if (!value){
        return '終了日を入力して下さい！';
      }
      value = value.replace(/[０-９]/g, function(s) {return String.fromCharCode(s.charCodeAt(0) - 0xFEE0);});
      const regex = /\d{1,2}/;
      if ( !regex.test(value) || value.length > 2){
        return '終了月は数字2桁で入力して下さい！';
      }
      const days = [...Array(31)].map((_, i) => i + 1)
      value = ('0' + value).slice(-2);
      if ( !days.includes(Number(value)) ){
        return '終了日は1 ~ 31の数字で入力して下さい！'
      }
      if ((this.endDate.y == this.dateRange.max.getFullYear()) && (this.startDate.m == this.dateRange.max.getMonth()+1) && (value > this.dateRange.max.getDate())) {
        return `${this.dateRange.max.getFullYear()}年${this.dateRange.max.getMonth()+1}月${this.dateRange.max.getDate()}日までのデータが取得可能です。`
      }
      if (this.endDate.y && this.endDate.m){
        const date = new Date(this.endDate.y, this.endDate.m - 1, this.endDate.d)
        const month = date.getMonth() + 1
        if (this.endDate.m != month) {
          return '存在しない日付です。'
        }
      }        
      this.endDate.d = value;
      this.endDate.dvalid = true;
      return true;
    },

    isEDate: function(){
      if (this.endDate.y && this.endDate.m && this.endDate.d){
        this.$refs.formed.validate()
      }
    },    

    // 開始日 <= 終了日のバリデーション
    // 気象要素が変更された場合に取得範囲が変わり、その際のバリデーション
    // y,m,dがすべてvalid=trueになったら、アイコンの色とvalidをtruにする。
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

    controlMapDraggable: function(){
      if (this.draggable){
        console.log(Object.keys(this.$children))
        // this.$refs.map.mapObject.dragging.disable()
        this.icon = "mdi-arrow-all"
        this.message = '地図を移動する'
        this.draggable = false
      } else {
        // this.$refs.map.mapObject.dragging.enable()
        this.icon = "mdi-vector-rectangle"
        this.message = '領域を選択する'
        this.draggable = true
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
