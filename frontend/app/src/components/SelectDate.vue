<template>
  <div>
    <p>開始日</p>
    <v-form ref="formsd">
      <v-row>
        <v-col cols="5" sm="4" md="4" lg="4" xl="3">
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
            @input="startDate.y=zenkakuToHankaku(startDate.y)"
            @blur="dateValidation">
          </v-text-field>
        </v-col>
        <v-col cols="3" sm="3" md="3" lg="3" xl="2">
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
            @input="startDate.m=zenkakuToHankaku(startDate.m)"
            @blur="dateValidation">
          </v-text-field>
        </v-col>
        <v-col cols="3" sm="3" md="3" lg="3" xl="2">
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
            @input="startDate.d=zenkakuToHankaku(startDate.d)"
            @blur="dateValidation">
          </v-text-field>
        </v-col>
        <!-- <v-col cols="1" sm="1" md="1" lg="1" xl="1">
          <v-input>
            <template v-slot:append><v-icon v-bind:color="startDate.iconColor">mdi-checkbox-marked-circle</v-icon></template>
          </v-input>
          <v-icon v-bind:color="startDate.iconColor">mdi-checkbox-marked-circle</v-icon>
        </v-col> -->
      </v-row>
    </v-form>
    <br>
    <p>終了日</p>
    <v-form ref="formed">
      <v-row>        
        <v-col cols="5" sm="4" md="4" lg="4" xl="3">
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
            @input="endDate.y=zenkakuToHankaku(endDate.y)"
            @blur="dateValidation">
          </v-text-field>
        </v-col>
        <v-col cols="3" sm="3" md="3" lg="3" xl="2">
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
            @input="endDate.m=zenkakuToHankaku(endDate.m)"
            @blur="dateValidation">
          </v-text-field>
        </v-col>
        <v-col cols="3" sm="3" md="3" lg="3" xl="2">
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
            @input="endDate.d=zenkakuToHankaku(endDate.d)"
            @blur="dateValidation">
          </v-text-field>          
        </v-col>
      </v-row>
    </v-form>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";

export default {
  name: "SelectDate",
  data() {
    return {
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
      },
      endDate: {
        y: '',
        m: '',
        d: '',
        iconColor: '',
        yvalid: false,
        mvalid: false,
        dvalid: false,
      },
    };
  },

  computed: {
    ...mapState(['element']),
  },

  methods: {
    ...mapMutations(['setDates',]),

    zenkakuToHankaku: function(value){
      if (value){
        value = value.replace(/[０-９]/g, function(s) {return String.fromCharCode(s.charCodeAt(0) - 0xFEE0);});
      }
      return value
    },    
    
    formatDate: function(y, m, d){
      return y + '-' + m + '-' + d
    },

    getMaxDate: function(){
      let date = new Date();
      const plusNine = ['OPR', 'GSR', 'DLR', 'RH', 'WIND', 'SD', 'SWE', 'SFW'];
      if (plusNine.includes(this.element.selected)){
        date.setDate(date.getDate() + 9);
      } else {
        date.setDate(date.getDate() + 26);
      }
      this.dateRange.max = date;
    },

    sdateyRules: function(value){
      this.startDate.yvalid = false;
      if (!value){
        return '開始年を入力して下さい！';
      }
      const regex = /\d{4}/;
      if ( !regex.test(value) || value.length > 4){
        return '開始年は数字4桁で入力して下さい！';
      }
      if (this.dateRange.min.getFullYear() > value ||
          this.dateRange.max.getFullYear() < value ){
        return `開始年は${this.dateRange.min.getFullYear()}年から${this.dateRange.max.getFullYear()}年の間で入力して下さい！`;
      }
      this.startDate.y = value;
      if (this.startDate.m && this.startDate.d){
        const date = new Date(this.startDate.y, this.startDate.m - 1, this.startDate.d)
        const month = date.getMonth() + 1
        if (this.startDate.m != month) {
          return '存在しない日付です。'
        }
      }
      if (this.startDate.m && this.startDate.d && this.endDate.y && this.endDate.m && this.endDate.d){
        const s = this.startDate.y + this.startDate.m + this.startDate.d;
        const e = this.endDate.y + this.endDate.m + this.endDate.d;
        if (s > e){
          return '終了日は開始日以前の値にして下さい。'
        }
      }
      this.startDate.yvalid = true;
      return true;
    },

    sdatemRules: function(value){
      this.startDate.mvalid = false;
      if (!value){
        return '開始月を入力して下さい！';
      }
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
      if (this.startDate.y && this.startDate.d){
        const date = new Date(this.startDate.y, this.startDate.m - 1, this.startDate.d)
        const month = date.getMonth() + 1
        if (this.startDate.m != month) {
          return '存在しない日付です。'
        }
      }
      if (this.startDate.y && this.startDate.d && this.endDate.y && this.endDate.m && this.endDate.d){
        const s = this.startDate.y + this.startDate.m + this.startDate.d;
        const e = this.endDate.y + this.endDate.m + this.endDate.d;
        if (s > e){
          return '終了日は開始日以前の値にして下さい。'
        }
      }      
      this.startDate.mvalid = true;
      return true;
    },

    sdatedRules: function(value){
      this.startDate.dvalid = false;
      if (!value){
        return '開始日を入力して下さい！';
      }
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
      this.startDate.d = value;    
      if (this.startDate.y && this.startDate.m){
        const date = new Date(this.startDate.y, this.startDate.m - 1, this.startDate.d)
        const month = date.getMonth() + 1
        if (this.startDate.m != month) {
          return '存在しない日付です。'
        }
      }
      if (this.startDate.y && this.startDate.m && this.endDate.y && this.endDate.m && this.endDate.d){
        const s = this.startDate.y + this.startDate.m + this.startDate.d;
        const e = this.endDate.y + this.endDate.m + this.endDate.d;
        if (s > e){
          return '終了日は開始日以前の値にして下さい。'
        }
      }
      this.startDate.dvalid = true;
      return true;
    },

    edateyRules: function(value){
      this.endDate.yvalid = false;
      if (!value){
        return '終了年を入力して下さい！';
      }
      const regex = /\d{4}/;
      if ( !regex.test(value) || value.length > 4){
        return '終了年は数字4桁で入力して下さい！';
      }
      if (this.dateRange.min.getFullYear() > value ||
          this.dateRange.max.getFullYear() < value ){
        return `終了年は${this.dateRange.min.getFullYear()}年から${this.dateRange.max.getFullYear()}年の間で入力して下さい！`;
      }
      if (this.endDate.m && this.endDate.d){
        const date = new Date(value, this.endDate.m - 1, this.endDate.d)
        const month = date.getMonth() + 1
        if (this.endDate.m != month) {
          return '存在しない日付です。'
        }
      }
      if (this.startDate.y && this.startDate.m && this.startDate.d && this.endDate.m && this.endDate.d){
        const s = this.startDate.y + this.startDate.m + this.startDate.d;
        const e = value + this.endDate.m + this.endDate.d;
        if (s > e){
          return '終了日は開始日以前の値にして下さい。'
        }
      }
      this.endDate.y = value;
      this.endDate.yvalid = true;
      return true;
    },

    edatemRules: function(value){
      this.endDate.mvalid = false;      
      if (!value){
        return '終了月を入力して下さい！';
      }
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
        const date = new Date(this.endDate.y, value - 1, this.endDate.d)
        const month = date.getMonth() + 1
        if (this.endDate.m != month) {
          return '存在しない日付です。'
        }
      }
      if (this.startDate.y && this.startDate.m && this.startDate.d && this.endDate.y && this.endDate.d){
        const s = this.startDate.y + this.startDate.m + this.startDate.d;
        const e = this.endDate.y + value + this.endDate.d;
        if (s > e){
          return '終了日は開始日以前の値にして下さい。'
        }
      }
      this.endDate.m = value;
      this.endDate.mvalid = true;
      return true;
    },

    edatedRules: function(value){
      this.endDate.dvalid = false;
      if (!value){
        return '終了日を入力して下さい！';
      }
      const regex = /\d{1,2}/;
      if ( !regex.test(value) || value.length > 2){
        return '終了月は数字2桁で入力して下さい！';
      }
      const days = [...Array(31)].map((_, i) => i + 1)
      value = ('0' + value).slice(-2);
      if ( !days.includes(Number(value)) ){
        return '終了日は1 ~ 31の数字で入力して下さい！'
      }
      if ((this.endDate.y == this.dateRange.max.getFullYear()) && (this.endDate.m == this.dateRange.max.getMonth()+1) && (value > this.dateRange.max.getDate())) {
        return `${this.dateRange.max.getFullYear()}年${this.dateRange.max.getMonth()+1}月${this.dateRange.max.getDate()}日までのデータが取得可能です。`
      }
      if (this.endDate.y && this.endDate.m){
        const date = new Date(this.endDate.y, this.endDate.m - 1, value)
        const month = date.getMonth() + 1
        if (this.endDate.m != month) {
          return '存在しない日付です。'
        }
      }
      if (this.startDate.y && this.startDate.m && this.startDate.d && this.endDate.m && this.endDate.d){
        const s = this.startDate.y + this.startDate.m + this.startDate.d;
        const e = this.endDate.y + this.endDate.m + this.endDate.d;
        if (s > e){
          return '終了日は開始日以前の値にして下さい。'
        }
      }      
      this.endDate.d = value;
      this.endDate.dvalid = true;
      return true;
    },

    dateValidation: function(){
      let svalid;
      let evalid;
      if (this.startDate.y && this.startDate.m && this.startDate.d){
        svalid = this.$refs.formsd.validate()
      }
      if (this.endDate.y && this.endDate.m && this.endDate.d){
        evalid = this.$refs.formed.validate()
      }
      let valid;
      let s;
      let e;
      if (svalid && evalid) {
        valid = true;
        s = this.formatDate(this.startDate.y, this.startDate.m, this.startDate.d);
        e = this.formatDate(this.endDate.y, this.endDate.m, this.endDate.d);

      } else {
        valid = false;
        s = ''
        e = ''
      }
      this.setDates({s: s, e: e, valid: valid})
    }, 
  },

  watch: {
    'element.selected': function(){
      this.getMaxDate();
      this.dateValidation();
    }
  },

  created(){
    this.getMaxDate()
  },
};
</script>

<style>
</style>