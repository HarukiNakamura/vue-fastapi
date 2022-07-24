<template>
  <div id="app">
    <base-view>
      <template v-slot:left-content>
        AAA
      </template>
      <template v-slot:right-content>
        <base-map ref="basemap" :pageName="pageName">
          <template v-slot:map-content>
          </template>
        </base-map>
      </template>
    </base-view>
  </div>
</template>

<script>
import { mapState, } from 'vuex';
import L from 'leaflet';

import * as PIXI from "pixi.js";
import "leaflet-pixi-overlay";

import BaseView from '@/components/BaseView.vue';
import BaseMap from '@/components/BaseMap.vue';

export default {
  name: "ShowResult",
  components: { BaseView, BaseMap, },
  props: {'meshdata': Object,},
  data() {
    return {
      pageName: 'showResult',
      mesh: '',
      i: 0
    };
  },

  computed: {
    ...mapState(['border']),
    // meshOptions() {
    //   return {
    //     onEachFeature: this.meshOnEachFeatureFunction
    //   };
    // }, 
    // meshOnEachFeatureFunction() {
    //   return (feature, layer) => {
    //     layer.options.fillColor = feature.properties.fillcolor;  
    //     layer.bindTooltip(
    //       "<div>メッシュ番号:" + feature.properties.meshcode + 
    //       "</div><div>気象データ: " + feature.properties.eledata + 
    //       "</div>", { permanent: false, sticky: true }
    //     );
    //   };
    // } 
  }, 
   
  methods: {
    drawMesh: function(){
      let i = this.i
      let mesh = this.mesh;

      let pixiContainer = new PIXI.Container();
      let pixiGraphics = new PIXI.Graphics();
      pixiContainer.addChild(pixiGraphics)
      let pixiLayer = (function() {
        let firstDraw = true
        return L.pixiOverlay(function(utils) {
          // let zoom = utils.getMap().getZoom();
          let project = utils.latLngToLayerPoint;
          let container = utils.getContainer();
          let renderer = utils.getRenderer();
          let gl = renderer.gl;
          // let scale = utils.getScale();
          
          if (firstDraw){
            (function(){
              if (renderer.type === PIXI.RENDERER_TYPE.WEBGL) {
                gl.blendFunc(gl.ONE, gl.ZERO);
                // document.querySelector('#webgl').style.display = 'block';
              } else {
                document.body.removeChild(document.querySelector('#webgl'));
              }
              Object.keys(mesh).forEach(function(key){
                let border = mesh[key].border
                let color = '0x'+ mesh[key].fillColor[i].slice(1,7)
                let alpha = 0.8
                let projectedBorder = border.map(function(xy) {return project(xy);})
                let s = projectedBorder[0].x
                let w = projectedBorder[0].y
                let n = projectedBorder[1].x
                let e = projectedBorder[1].y
                let width = n - s
                let height = e - w
                let rectangle = new PIXI.Rectangle(n, w, width, height)
                pixiGraphics.beginFill(color, alpha)
                pixiGraphics.drawShape(rectangle)
                pixiGraphics.endFill();
              })
              mesh = null                 
            })()
          }            
          utils.getMap().on('click', function(e) {
            console.log(e.latlng)
          });
          firstDraw = false;
          renderer.render(container);
        },pixiContainer, {destroyInteractionManager: true}) 
      })();
      pixiLayer.addTo(this.$refs.basemap.$refs.map.mapObject);
      
      // let ticker = PIXI.Ticker.shared
      // ticker.minFPS = 1
      // ticker.maxFPS = 1
      // ticker.add(function(delta) {
      //   pixiLayer.redraw({type: 'redraw', delta: delta});
      // });
      // ticker.stop();
      // this.$refs.map.mapObject.on('zoomanim', pixiLayer.redraw, pixiLayer);
    },    
  },
  
  created(){
    this.mesh = this.meshdata;
  },
  mounted(){
    //  $refsでmapObjectにアクセスするにはmouted以降でないとダメ
    this.drawMesh()
  }
};
</script>
