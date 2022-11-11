(window.webpackJsonp=window.webpackJsonp||[]).push([[52],{tLey:function(t,e,a){"use strict";a.r(e);var s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{directives:[{name:"show",rawName:"v-show",value:t.valid,expression:"valid"}],class:["pt-3","pb-2","filter-component",{"d-none":!t.hasPurposeVisibility}],attrs:{id:"refineFilter-"+t.facetName}},[a("toggle",{attrs:{index:t.index,name:t.$store.state.translations[this.$translationLocale].key_name[t.facetName],"is-refined":this.isRefined,advancedSearch:t.advancedSearch}},[a("a",{staticClass:"w-100",attrs:{href:"#",rel:"nofollow"},on:{click:function(t){t.stopPropagation(),t.preventDefault()}}},[a("vue-slider",{ref:"slider",attrs:{"tooltip-formatter":function(e){return t.formatter(e)},min:parseFloat(t.min),max:parseFloat(t.max),reverse:!1,tooltip:"active",enableCross:!1,lazy:t.lazy,interval:t.interval},on:{"drag-end":function(e){t.manualUpdate(t.$refs.slider.getValue())}},nativeOn:{click:function(e){return t.manualUpdate(e)}},model:{value:t.currentValue,callback:function(e){t.currentValue=e},expression:"currentValue"}})],1),t._v(" "),a("div",{directives:[{name:"show",rawName:"v-show",value:!t.hideInputFields,expression:"!hideInputFields"}],staticClass:"mt-2 pb-3 w-100 "},[a("a",{attrs:{href:"#",rel:"nofollow"},on:{click:function(t){t.stopPropagation(),t.preventDefault()}}},[a("input",{ref:"minInput",staticClass:"w-30 border-none p-2 font-size-xs",attrs:{type:"number",min:t.minValue,max:t.maxValue},domProps:{value:t.currentValue[0]},on:{change:function(e){return t.update("min")}}}),t._v(" "),a("input",{ref:"maxInput",staticClass:"w-30 border-none p-2 font-size-xs",attrs:{type:"number",min:t.minValue,max:t.maxValue},domProps:{value:t.currentValue[1]},on:{change:function(e){return t.update("max")}}})]),t._v(" "),a("span",{staticClass:"pl-2 w-40 d-inline"},[t._v(t._s(t.formatValue))]),t._v(" "),a("div",[t.isRefined?a("a",{staticClass:"btn btn-lg btn-link text-underline",attrs:{href:"#",rel:"nofollow"},on:{click:function(e){return e.preventDefault(),t.reset(e)}}},[t._v("\n                  "+t._s(t.$store.state.translations[this.$translationLocale].advanced_search.reset_filter)+"\n                ")]):t._e()])])])],1)};s._withStripped=!0;var i=a("SXG0"),r=a.n(i),n=a("sBL/"),o=a.n(n),u=a("MG4b"),l=a("maDl"),m=a("IyZH"),c=a("h6/w"),h=a("kC9S"),p=a("oCYn"),f={mixins:[u.a,l.a],name:"Slider",components:{vueSlider:r.a,Toggle:h.a},props:{facetName:String,index:Number,hideInputFields:Boolean,format:String,formatValue:String,purpose:Object,precision:{type:Number,default:0},interval:{type:Number,default:1},advancedSearch:{type:Boolean,default:!1},customerLocale:{type:String,default:"en"}},data:()=>({componentKey:0,lazy:!0,init:!1,currentValue:[],minValue:!1,maxValue:!1}),computed:{valid:function(){return!isNaN(this.min)&&!isNaN(this.max)&&null!==this.min&&null!==this.max&&void 0!==this.min&&void 0!==this.max&&this.min!==this.max},min:{get:function(){let t=this.minValue;return this.minValue||(this.$store.state.aggregations[this.facetName]?t=parseFloat(this.$store.state.aggregations[this.facetName].min).toFixed(this.precision):c.a.warn("Aggregations missing for "+this.facetName)),t},set:function(t){this.minValue=t}},max:{get:function(){let t=this.maxValue;return this.maxValue||this.$store.state.aggregations[this.facetName]&&(t=parseFloat(this.$store.state.aggregations[this.facetName].max).toFixed(this.precision)),t},set:function(t){this.maxValue=t}}},methods:{manualUpdate(t){m.a.trackEvent(["track-filter",this.$options._componentTag,this.facetName],!0),this.currentValue=this.$refs.slider.getValue(),this.$store.commit("UPDATE_RANGE",{facet:this.facetName,range:this.currentValue}),this.$store.dispatch("CALL_API",this.$eventHub)},formatter:function(t){const e=t%3600,a=Math.floor(t/3600),s=Math.floor(e/60),i=e%60;switch(this.format){case"h:m:s":return("00"+a).substr(-2)+":"+("00"+s).substr(-2)+":"+("00"+i).substr(-2);case"m:s":return~~(t/60)+":"+(t%60<10?"0":"")+t%60;case"display_percentage":return t+"%";case"append":return t+this.formatValue;default:return t=parseFloat(t),this.precision>0&&(t=t.toFixed(this.precision)),t}},update:o()((function(t){"max"===t&&Number(this.$refs.maxInput.value)>Number(this.max)&&(this.$refs.maxInput.value=Number(this.max)),"min"===t&&Number(this.$refs.minInput.value)<Number(this.min)&&(this.$refs.minInput.value=Number(this.min)),"min"===t&&parseFloat(this.$refs.minInput.value)>=parseFloat(this.min)&&parseFloat(this.$refs.minInput.value)<=parseFloat(this.currentValue[1])&&(this.currentValue[0]=parseFloat(this.$refs.minInput.value).toFixed(this.precision)),"max"===t&&parseFloat(this.$refs.maxInput.value)<=parseFloat(this.max)&&parseFloat(this.$refs.maxInput.value)>=parseFloat(this.currentValue[0])&&(this.currentValue[1]=parseFloat(this.$refs.maxInput.value).toFixed(this.precision)),p.default.set(this.currentValue,0,this.currentValue[0]),p.default.set(this.currentValue,1,this.currentValue[1]),this.mutate()}),230),mutate(t=!0){this.$store.commit("UPDATE_RANGE",{facet:this.facetName,range:this.currentValue}),this.$refs.slider&&this.$refs.slider.setValue(this.currentValue),t&&this.$store.dispatch("CALL_API",this.$eventHub)}},mounted(){void 0!==this.$store.state.base_ranges[this.facetName]?this.currentValue=this.$store.state.base_ranges[this.facetName]:void 0!==this.$store.state.ranges[this.facetName]?this.currentValue=this.$store.state.ranges[this.facetName]:void 0!==this.$store.state.aggregations[this.facetName]&&(this.currentValue=[parseFloat(this.$store.state.aggregations[this.facetName].min).toFixed(this.precision),parseFloat(this.$store.state.aggregations[this.facetName].max).toFixed(this.precision)])}},d=a("KHd+"),v=Object(d.a)(f,s,[],!1,null,null,null);v.options.__file="assets/base-theme/js/modules/filters/Slider.vue";e.default=v.exports}}]);