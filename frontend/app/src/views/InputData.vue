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
      <br>
      <p>緯度経度の選択</p>
      <v-row>
        <base-map :pageName="pageName">
        </base-map>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import BaseMap from '@/components/BaseMap.vue';

import { mapActions } from 'vuex';
export default {
  name: "InputData",
  components: { BaseMap, },
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
    };
  },
  computed: {
  }, 
   
  methods: {
    ...mapActions([
      'postData',
    ]),

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
      // if (this.endDate.y && value > this.endDate.y){
      //   return '開始年が終了年より大きいです！'
      // }
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
      if (!value){ 
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
  },

  watch: {
    'element.select': function(){
      this.getMaxDate()
    },
  },

  async created(){
    this.getMaxDate()
  },
};
</script>