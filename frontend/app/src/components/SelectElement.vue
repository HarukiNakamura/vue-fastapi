<template>
  <div>
    <v-row>
      <v-col cols="12" sm="9" md="8" lg="7" xl="6">
        <v-select
            v-model="element.select"
            autofocus
            clearable
            item-text="ele"
            item-value="text"
            :items="element.choices"
            label="気象要素"
            persistent-hint
            persistent-placeholder
            placeholder="日平均気温"
            :rules="[eleRules]">
          <!-- <template v-slot:append-outer><v-icon v-bind:color="element.iconColor">mdi-checkbox-marked-circle</v-icon></template> -->
        </v-select>
      </v-col>
    </v-row>    
  </div>
</template>

<script>
import { mapMutations, } from 'vuex';

export default {
  name: "SelectElement",
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
    };
  },

  computed: { 
  },

  methods: {
    ...mapMutations(['setElement',]),

    eleRules: function(value){
      this.element.iconColor = '';
      this.element.valid = false;
      if (!value){
        this.setElement({value: value, valid:this.element.valid})
        return '気象要素を選択して下さい！';
      } else {
        this.element.iconColor = 'green';
        this.element.valid = true;
        this.setElement({value: value, valid:this.element.valid})
        return true;
      }
    },    
  },
};
</script>

<style>
</style>