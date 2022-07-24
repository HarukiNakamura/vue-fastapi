<template>
  <base-view>
    <template v-slot:full-content>
      <loading :active="isLoading" :can-cancel="true" :is-full-page="true"/>
    </template>
    <template v-slot:left-content>
      <select-element>
      </select-element>
      <br>
      <select-date>
      </select-date>
      <br>
      <p>緯度経度の選択：地図から選択して下さい。</p>
      <v-row>
        <v-col cols="6" sm="5" md="5" lg="5" xl="4">
          <v-text-field
            v-model="border.data[0]"
            label="南端緯度"
            outlined
            persistent-hint
            persistent-placeholder
            placeholder="36.00"
            readonly>
          </v-text-field>
        </v-col>
        <v-col cols="6" sm="5" md="5" lg="5" xl="4">
          <v-text-field
            v-model="border.data[1]"
            label="北端緯度"
            outlined
            persistent-hint
            persistent-placeholder
            placeholder="38.00"
            readonly>
          </v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" sm="5" md="5" lg="5" xl="4">
          <v-text-field
            v-model="border.data[2]"
            label="西端経度"
            outlined
            persistent-hint
            persistent-placeholder
            placeholder="136.00"
            readonly>
          </v-text-field>
        </v-col>
        <v-col cols="6" sm="5" md="5" lg="5" xl="4">
          <v-text-field
            v-model="border.data[3]"
            label="東端経度"
            outlined
            persistent-hint
            persistent-placeholder
            placeholder="138.00"
            readonly>
          </v-text-field>
        </v-col>                
      </v-row>
      <v-btn @click="postData" :disabled="buttonDeactivate">Run Mesh</v-btn>
    </template>
    <template v-slot:right-content>
      <base-map ref="basemap" :pageName="pageName">
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
            <l-rectangle v-if="border.valid" :bounds="[[border.data[0], border.data[2]], [border.data[1], border.data[3]]]" :l-style="rectangle.style"></l-rectangle>
          </template>          
        </template>
      </base-map>
    </template>
  </base-view>
</template>


<script>
import BaseView from '@/components/BaseView.vue';
import BaseMap from '@/components/BaseMap.vue';
import SelectElement from '@/components/SelectElement.vue';
import SelectDate from '@/components/SelectDate.vue';

import axios from "axios";
import { mapState, mapMutations, } from 'vuex';
import { LGeoJson, LRectangle, LControl, } from "vue2-leaflet";

import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';

export default {
  name: "InputData",
  components: { BaseView, BaseMap, SelectElement, SelectDate, LGeoJson, LRectangle, LControl, Loading, },
  data() {
    return {
      pageName: 'inputData',
      isLoading: false,

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

      prefectureBorder: {
        '北海道': [41.350, 45.533, 139.327, 145.998],
        '青森県': [40.217, 41.558, 139.490, 141.685],
        '岩手県': [38.742, 40.458, 140.652, 142.073],
        '宮城県': [37.767, 39.008, 140.265, 141.685],
        '秋田県':	[38.867, 40.517, 139.690, 140.998],
        '山形県':	[37.733, 39.217, 139.515, 140.648],
        '福島県':	[36.783, 37.983, 139.165, 141.048],
        '茨城県':	[35.733, 36.950, 139.690, 140.860],
        '栃木県':	[36.192, 37.158, 139.327, 140.298],
        '群馬県':	[35.983, 37.067, 138.390, 139.673],
        '埼玉県':	[35.750, 36.292, 138.702, 139.910],
        '千葉県':	[34.892, 36.108, 139.740, 140.885],
        '東京都':	[34.675, 35.900, 138.940, 139.923],
        '神奈川県':	[35.125, 35.675, 138.915, 139.835],
        '新潟県':	[36.733, 38.558, 137.627, 139.898],
        '富山県':	[36.267, 36.983, 136.765, 137.773],
        '石川県':	[36.067, 37.858, 136.240, 137.373],
        '福井県':	[35.342, 36.300, 135.440, 136.835],
        '山梨県':	[35.167, 35.975, 138.177, 139.135],
        '長野県':	[35.192, 37.033, 137.315, 138.748],
        '岐阜県':	[35.133, 36.467, 136.277, 137.660],
        '静岡県': [34.567, 35.650, 137.465, 139.185],
        '愛知県':	[34.567, 35.425, 136.665, 137.848],
        '三重県': [33.717, 35.258, 135.852, 136.998],
        '滋賀県':	[34.783, 35.708, 135.765, 136.460],
        '京都府':	[34.700, 35.783, 134.852, 136.060],
        '大阪府':	[34.267, 35.058, 135.090, 135.748],
        '兵庫県':	[34.150, 35.675, 134.252, 135.473],
        '奈良県':	[33.858, 34.783, 135.540, 136.235],
        '和歌山県':	[33.425, 34.392, 135.002, 136.023],
        '鳥取県': [35.050, 35.617, 133.127, 134.523],
        '島根県': [34.300, 36.358, 131.665, 133.398],
        '岡山県':	[34.292, 35.358, 133.265, 134.423],
        '広島県': [34.025, 35.108, 132.027, 133.473],
        '山口県': [33.708, 34.800, 130.765, 132.498],
        '徳島県': [33.533, 34.258, 133.652, 134.823],
        '香川県': [34.008, 34.567, 133.440, 134.448],
        '愛媛県': [32.883, 34.308, 132.002, 133.698],
        '高知県': [32.700, 33.892, 132.477, 134.323],
        '福岡県': [32.992, 34.250, 130.027, 131.198],
        '佐賀県': [32.950, 33.625, 129.727, 130.548],
        '長崎県': [31.983, 34.733, 128.102, 130.398],
        '熊本県': [32.092, 33.200, 129.940, 131.335],
        '大分県': [32.708, 33.742, 130.815, 132.185],
        '宮崎県': [31.350, 32.842, 130.702, 131.885],
        '鹿児島県': [28.750, 32.317, 128.965, 131.210],
        '沖縄県': [24.042, 27.892, 122.927, 131.335]
      }
    };
  },

  computed: {
    ...mapState(['element', 'date', 'border']),

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

    buttonDeactivate: function(){
      if (this.element.validate && this.date.valid && this.border.valid){
        return false
      }
      return true
    }
  },

  methods: {
    ...mapMutations(['setBorder',]),

    changeSelectBy: function(){
      if (this.selectBy === "prefecture"){
        this.selectBy = "rectangle"
        this.btnmsg = "都道府県"
        this.readonly = false
      } else {
        // this.prefectureName = ''
        // ここ、もう少しスマートに書けないだろうか。
        this.$refs.basemap.$refs.map.mapObject.dragging.enable()
        this.selectBy = "prefecture"
        this.btnmsg = "矩形"
        this.readonly = true
      }
    },    

    controlMapDraggable: function(){
      if (this.draggable){
        this.$refs.basemap.$refs.map.mapObject.dragging.disable()
        this.icon = "mdi-arrow-all"
        this.message = '地図を移動する'
        this.draggable = false
      } else {
        this.$refs.basemap.$refs.map.mapObject.dragging.enable()
        this.icon = "mdi-vector-rectangle"
        this.message = '領域を選択する'
        this.draggable = true
      }
    },

    geojsonClick: function(event){
      this.$refs.myGeoJson.mapObject.resetStyle()
      const layer = event.target
      layer.setStyle({fillOpacity: 0.7})
      const prefectureName = layer.feature.properties.name
      const border = this.prefectureBorder[prefectureName]
      this.setBorder({value:border, valid:true})
    },    

    postData: function(){
      this.isLoading = true;
      axios.post('http://localhost:3000/api/result',
      {
        inputData:
        {metElement: this.element.selected,
        date: this.date.date,
        border: this.border.data}
      }
      )
      .then((response) => {
        this.isLoading = false;
        this.$router.push({name: 'ShowResult', params: {meshdata: response.data}});
      })
      .catch((err) => {
        this.isLoading = false;
        console.log(err);
      })
    },
  },

  watch: {
  },

  async created(){
    const response = await fetch('http://localhost/prefectures.geojson');
    this.prefecture.data = await response.json();
  },
};

</script>
