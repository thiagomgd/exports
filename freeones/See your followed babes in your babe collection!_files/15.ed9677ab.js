(window.webpackJsonp=window.webpackJsonp||[]).push([[15],{PzL6:function(t,e,s){"use strict";var a=s("SluN"),o=s("oCYn"),i=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"form-group filter-results-options ml-3 mr-1 mb-0"},[s("div",{staticClass:"select-wrapper select-wrapper-small select-wrapper--teasermode d-inline-flex align-items-center"},[s("label",{staticClass:"mb-1  color-text-dark position-absolute"},[s("icon",{attrs:{title:t.$store.state.translations[this.$translationLocale].display.switch,icon:"view_"+t.selectedMode,classes:"svg-icon-lg filter-view"}})],1),t._v(" "),s("select",{directives:[{name:"model",rawName:"v-model",value:t.selectedMode,expression:"selectedMode"}],staticClass:"form-control d-flex align-items-center",on:{change:[function(e){var s=Array.prototype.filter.call(e.target.options,(function(t){return t.selected})).map((function(t){return"_value"in t?t._value:t.value}));t.selectedMode=e.target.multiple?s:s[0]},t.updatePreference]}},t._l(t.options,(function(e){return s("option",{key:e.value,staticClass:"dropdown-item",domProps:{value:e.value}},[t._v("\n                "+t._s(e.text)+"\n            ")])})),0)])])};i._withStripped=!0;var r=s("yInD"),n={name:"setTeaserMode",data(){return{selectedMode:"text",options:[{value:"grid",text:this.$store.state.translations[this.$translationLocale].display.gridview},{value:"row",text:this.$store.state.translations[this.$translationLocale].display.rowview},{value:"text",text:this.$store.state.translations[this.$translationLocale].display.textview}]}},props:{mode:{type:String}},methods:{updatePreference(){const t={displayType:this.selectedMode},e=document.querySelectorAll("#search-result .js-grid");for(const t of e)t.classList.remove("teaser-mode--grid"),t.classList.remove("teaser-mode--row"),t.classList.remove("teaser-mode--text"),t.classList.add("teaser-mode--"+this.selectedMode);r.a.save("/my/displayType-toggle","displayType",t),this.$store.commit("UPDATE_TEASERMODE",this.selectedMode)}},mounted(){this.selectedMode=this.$props.mode,this.$store.commit("UPDATE_TEASERMODE",this.selectedMode)}},l=s("KHd+"),c=Object(l.a)(n,i,[],!1,null,null,null);c.options.__file="assets/base-theme/js/modules/filter-controls/setTeaserMode.vue";var d=c.exports,u=s("OIPd"),h=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{directives:[{name:"click-outside",rawName:"v-click-outside",value:t.clickOutside,expression:"clickOutside"}],staticClass:"sort-search  "},[s("div",{staticClass:" select-wrapper select-wrapper-small hand",on:{click:function(e){t.active=!t.active}}},[s("span",{staticClass:"sort-search__active-option mr-4 pr-3",attrs:{"data-test":"sort-search-active-option"}},["asc"===this.activeSortOrder?s("icon",{attrs:{title:t.$store.state.translations[this.$translationLocale].sort_search.ascending,icon:"trend-up",classes:"svg-icon-xs"}}):s("icon",{attrs:{icon:"trend-up",title:t.$store.state.translations[this.$translationLocale].sort_search.descending,classes:"svg-icon-xs rotate-180"}}),t._v("\n            "+t._s(this.selectedOption.key)+"\n        ")],1)]),t._v(" "),t.active?s("div",{staticClass:"sort-search__modal sort-search__modal--active filter-component"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.query,expression:"query"}],ref:"input",staticClass:"sort-search__input",attrs:{placeholder:t.$store.state.translations[this.$translationLocale].sort_search.find},domProps:{value:t.query},on:{input:[function(e){e.target.composing||(t.query=e.target.value)},t.setQuery],focus:t.focusInput}}),t._v(" "),s("ul",{staticClass:"sort-search__list"},t._l(t.filteredSortOptions,(function(e){return s("li",{key:e.key,staticClass:"sort-search__list-item",class:{"sort-search__list-item--active":e===t.preSelectedOption}},[s("a",{attrs:{href:e.url+t.sortOrder,"data-test":"sort-item-link"},on:{click:function(s){return s.preventDefault(),t.setSort(e)}}},[t._v(t._s(e.key)+" "),s("icon",{attrs:{icon:"check",classes:"svg-icon-sm icon-toggle"}})],1)])})),0),t._v(" "),s("div",{staticClass:"sort-search__meta"},[s("div",{staticClass:"toggler mr-2 d-inline-flex",class:{"toggler-right":"desc"===t.sortOrder}},[s("button",{staticClass:"toggle toggle-left",attrs:{type:"button"},on:{click:t.toggleSortOrder}},[s("icon",{attrs:{icon:"trend-up",classes:"svg-icon-sm icon-toggle"}})],1),t._v(" "),s("button",{staticClass:"toggle toggle-right",attrs:{type:"button"},on:{click:t.toggleSortOrder}},[s("icon",{attrs:{icon:"trend-up",classes:"svg-icon-sm icon-toggle"}})],1)]),t._v(" "),"desc"===t.sortOrder?s("span",[t._v(t._s(t.$store.state.translations[this.$translationLocale].sort_search.descending))]):s("span",[t._v(t._s(t.$store.state.translations[this.$translationLocale].sort_search.ascending))]),t._v(" "),s("button",{staticClass:"btn btn-primary self-align-end btn-block mt-3",attrs:{type:"button","data-test":"do-sort-button"},on:{click:t.activateSort}},[t._v(t._s(t.$store.state.translations[this.$translationLocale].sort_search.sort))])])]):t._e()])};h._withStripped=!0;var p=s("wouM"),m=s.n(p);o.default.use(m.a);var g={name:"sortShare",props:["sortOptions","activeSortOrder"],computed:{filteredSortOptions(){return this.sortOptions.filter(t=>-1!==t.key.toLocaleLowerCase().search(this.query.toLocaleLowerCase()))},currentSortUrl(){let t=this.preSelectedOption.url;return t=t.replace(/o=/g,"o="+this.sortOrder),t}},methods:{toggleSortOrder(){"asc"!==this.sortOrder?this.sortOrder="asc":this.sortOrder="desc"},focusInput(){const t=this.$refs.input.getBoundingClientRect(),e=window.pageYOffset||document.documentElement.scrollTop,s=document.querySelector(".js-site-nav").offsetHeight;window.matchMedia("(max-width: 992px)").matches&&window.setTimeout(()=>{window.scrollTo(0,t.top-s+e),document.body.scrollTop=t.top-s+e},200)},setQuery(t){this.query=t?t.target.value:this.query},setSort(t){this.preSelectedOption=t},clickOutside(){this.active=!1},activateSort(){this.selectedOption=this.preSelectedOption,window.location.href=this.currentSortUrl}},data:()=>({active:!1,query:"",sortOrder:"asc",selectedOption:{},preSelectedOption:{}}),mounted(){this.sortOrder=this.$props.activeSortOrder,this.selectedOption=this.$props.sortOptions.filter((function(t){return t.selected}))[0]||this.$props.sortOptions[0],this.preSelectedOption=this.selectedOption}},v=Object(l.a)(g,h,[],!1,null,null,null);v.options.__file="assets/base-theme/js/modules/filter-controls/sortSearch.vue";var f=v.exports,_=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[s("button",{staticClass:"btn btn-outline-secondary border-color-border d-flex align-items-center font-size-xs font-weight-light",attrs:{title:t.$store.state.translations[this.$translationLocale].save_search_dialog.title},on:{click:t.show}},[s("icon",{attrs:{icon:"star_border",classes:"svg-icon-sm mr-2",title:t.$store.state.translations[this.$translationLocale].save_search_dialog.title}}),t._v("\n        "+t._s(t.$store.state.translations[this.$translationLocale].save_search_dialog.title)+"\n    ")],1),t._v(" "),s("modal",{attrs:{name:"userSearch",height:"auto",classes:"bg-color-tertiary v-modal "}},[s("div",{staticClass:"d-flex flex-column p-4"},[s("h4",{staticClass:"border-bottom border-color-border border-width-1 pb-3 mb-3 w-100 font-weight-bold d-flex justify-content-between"},[t._v("\n                "+t._s(t.$store.state.translations[this.$translationLocale].save_search_dialog.title)+"\n                "),s("button",{staticClass:"icon-button",attrs:{"aria-label":t.$store.state.translations[this.$translationLocale].save_search_dialog.close},on:{click:function(e){return t.hide()}}},[s("icon",{attrs:{icon:"close",classes:"svg-icon-mlm",title:t.$store.state.translations[this.$translationLocale].save_search_dialog.close}})],1)]),t._v(" "),s("div",{directives:[{name:"show",rawName:"v-show",value:!t.added,expression:"!added"}]},[s("form",{on:{submit:t.saveSearch}},[s("div",{staticClass:"form-group mb-4"},[s("label",{staticClass:"font-weight-bold",attrs:{for:"name"}},[t._v(t._s(t.$store.state.translations[this.$translationLocale].save_search_dialog.name))]),t._v(" "),s("div",{staticClass:"d-flex flex-row mb-2"},[s("div",{staticClass:" d-flex align-items-center w-100 mr-2"},[s("input",{ref:"name",staticClass:"form-control font-size-sm font-weight-light w-60",attrs:{type:"text",required:"required",id:"name"}})])])]),t._v(" "),s("div",{staticClass:"form-group mb-4"},[s("label",{staticClass:"font-weight-bold",attrs:{for:"description"}},[t._v(t._s(t.$store.state.translations[this.$translationLocale].save_search_dialog.description))]),t._v(" "),s("div",{staticClass:"d-flex flex-row mb-2"},[s("div",{staticClass:" d-flex align-items-center w-100 mr-2"},[s("textarea",{ref:"description",staticClass:"form-control w-100",attrs:{rows:"3",id:"description"}})])])]),t._v(" "),s("div",{staticClass:"float-right"},[s("button",{staticClass:"btn btn-primary flex-1 btn btn-success",attrs:{title:t.$store.state.translations[this.$translationLocale].save_search_dialog.title,type:"submit"}},[t._v("\n                            "+t._s(t.$store.state.translations[this.$translationLocale].save_search_dialog.title)+"\n                        ")])])])]),t._v(" "),s("div",{directives:[{name:"show",rawName:"v-show",value:t.added,expression:"added"}]},[s("div",{staticClass:"pt-3"},[t._v("\n                    "+t._s(t.$store.state.translations[this.$translationLocale].save_search_dialog.search_saved)+"\n                ")])])])])],1)};_._withStripped=!0;var y=s("vDqi"),b=s.n(y);const w=new(s("vxF8").a);var S={name:"UserSearch",data:()=>({loaded:!1,added:!1}),props:{contentType:String,searchQuery:String,searchFilters:String,searchRanges:String,searchDateRanges:String,customerLocale:{type:String,default:"en"}},methods:{show(){this.$store.state.user?this.$modal.show("userSearch"):w.show()},hide(){this.$store.state.user?this.$modal.hide("userSearch"):w.show()},saveSearch(t){t.preventDefault(),this.$store.state.user?b.a.post("/my/search/add",{name:this.$refs.name.value,description:this.$refs.description.value,searchFilters:this.searchFilters,searchQuery:this.searchQuery,searchRanges:this.searchRanges,searchDateRanges:this.searchDateRanges,contentType:this.contentType}).then(t=>{this.added=!0,this.loading=!1}).catch(t=>{this.errorMessage=t.response.data.error,this.showError=!0,this.loading=!1}):w.show()}}},$=Object(l.a)(S,_,[],!1,null,null,null);$.options.__file="assets/base-theme/js/modules/filter-controls/UserSearch.vue";var C=$.exports,x=s("GIGG"),k=s.n(x),L=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"d-inline-block"},[s("div",{staticClass:"d-inline-block",on:{click:t.toggle}},[t._t("default")],2),t._v(" "),s("div",{staticClass:"pagination-modal",class:{"d-none":0==t.visible}},[s("div",{staticClass:"pagination-modal-title"},[t._v("\n            Go to page\n        ")]),t._v(" "),s("form",{staticClass:"pagination-modal-form",on:{submit:function(e){return e.preventDefault(),t.goToPage(e)}}},[s("div",{staticClass:"d-inline-flex"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.page,expression:"page"}],staticClass:"paging-control paging-control-input",attrs:{min:t.min,max:t.max,type:"number"},domProps:{value:t.page},on:{keyup:t.checkRange,input:function(e){e.target.composing||(t.page=e.target.value)}}}),t._v(" "),s("button",{staticClass:"paging-control paging-control-button",attrs:{type:"button"},on:{click:t.minus}},[t._v("-")]),t._v(" "),s("button",{staticClass:"paging-control paging-control-button",attrs:{type:"button"},on:{click:t.add}},[t._v("+")])]),t._v(" "),s("button",{staticClass:"btn btn-secondary d-inline-block ml-1",attrs:{type:"submit"}},[t._v("Go")])])])])};L._withStripped=!0;var O=s("IyZH"),E={name:"PageSelector",props:["min","current","max","url","track"],data:function(){return{page:1,visible:!1}},methods:{toggle(){this.visible=!this.visible,this.visible&&(this.addCLickListenerOnce(),this.track&&O.a.trackEvent(["paging","open pageselect",this.track],!0))},checkClickInside(t){this.$el.contains(t.target)?this.addCLickListenerOnce():this.visible&&this.toggle()},addCLickListenerOnce(){setTimeout(()=>{document.addEventListener("click",this.checkClickInside,{once:!0})},100)},add(){this.page<this.max&&this.page++},minus(){this.page>this.min&&this.page--},goToPage(){const t=this.url.replace("p=0","p="+this.page);window.location.href=t},checkRange(){this.page<this.min?this.page=this.min:this.page>this.max&&(this.page=this.max)}},mounted(){this.page=this.current}},A=Object(l.a)(E,L,[],!1,null,null,null);A.options.__file="assets/base-theme/js/modules/filter-controls/PageSelector.vue";var D=A.exports,P=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"form-group mr-1 mb-0"},[s("div",{staticClass:"select-wrapper select-wrapper-small d-inline-flex align-items-center"},[s("select",{directives:[{name:"model",rawName:"v-model",value:t.selectedDisplayAmount,expression:"selectedDisplayAmount"}],staticClass:"form-control d-flex align-items-center",on:{change:[function(e){var s=Array.prototype.filter.call(e.target.options,(function(t){return t.selected})).map((function(t){return"_value"in t?t._value:t.value}));t.selectedDisplayAmount=e.target.multiple?s:s[0]},t.updatePreference]}},t._l(t.options,(function(e){return s("option",{key:e.key,staticClass:"dropdown-item",attrs:{url:e.url},domProps:{value:e,selected:!0===e.selected}},[t._v("\n        "+t._s(e.key)+"\n      ")])})),0)]),t._v(" "),t.loading?s("loader"):t._e()],1)};P._withStripped=!0;var T={name:"setDisplayAmount",components:{Loader:s("PJnj").a},data:()=>({selectedDisplayAmount:"",loading:!1}),props:["options"],methods:{updatePreference(){const t={displayAmount:this.selectedDisplayAmount.key},e=r.a.save("/my/displayAmount","displayAmount",t);this.loading=!0,this.$store.commit("UPDATE_DISPLAY",this.selectedDisplayAmount.key),e.then?e.then(()=>{this.updateLocationHref()}):this.updateLocationHref()},updateLocationHref(){this.loading=!1,window.location.href=this.selectedDisplayAmount.url}},mounted(){this.selectedDisplayAmount=this.$props.options.filter((function(t){return t.selected}))[0]||this.$props.options[0],this.$store.commit("UPDATE_DISPLAY",this.selectedDisplayAmount)}},q=Object(l.a)(T,P,[],!1,null,null,null);q.options.__file="assets/base-theme/js/modules/filter-controls/setDisplayAmount.vue";var M=q.exports,j=s("aPjz");var B=class{constructor(){this.redirects=document.querySelectorAll("[data-redirect]"),this.selectElements=document.querySelectorAll(".js-select-redirect")}mount(){this.selectElements.forEach((function(t){t.addEventListener("change",t=>{t.target.selectedOptions[0].click()})}));const t=["click","touchstart"];this.redirects.forEach((function(e){t.forEach((function(t){e.addEventListener(t,t=>{t.preventDefault(),window.location.href=e.getAttribute("data-redirect")})}))}))}};s("Rnau");void 0!==window.preferences&&a.a.commit("UPDATE_TEASERMODE",window.preferences.teaserMode);e.a=()=>{(()=>{const t=document.getElementById("vue-user-search");if(t){o.default.use(k.a);new o.default({store:a.a,components:{UserSearch:C}}).$mount(t)}})(),(()=>{const t=document.getElementsByClassName("vue-teaser-mode");if(t)for(const e of t){new o.default({store:a.a,el:e,components:{TeaserMode:d}}).$mount(e)}})(),(()=>{const t=document.querySelectorAll(".vue-sort-search");t.length&&t.forEach(t=>{new o.default({store:a.a,data:{config:u.a},components:{SortSearch:f}}).$mount(t)})})(),(()=>{const t=document.querySelectorAll(".vue-page-selector");t.length&&t.forEach(t=>{new o.default({store:a.a,data:{config:u.a},components:{PageSelector:D}}).$mount(t)})})(),(()=>{const t=document.getElementsByClassName("vue-set-display-amount");if(t)for(const e of t){new o.default({store:a.a,el:e,components:{SetDisplayAmount:M}}).$mount(e)}})();(new j.a).mount();(new B).mount()}},Rnau:function(t,e,s){},aPjz:function(t,e,s){"use strict";var a=s("yInD"),o=s("/GhP");e.a=class{constructor(){document.querySelector('[data-component="toggle-filter-sidebar"]')&&(this.toggleFilterSidebar=document.querySelectorAll('[data-component="toggle-filter-sidebar"]'),this.mainButton=document.querySelector(".js-toggle-filter-main"),this.secondButton=document.querySelector(".js-toggle-filter-second"),this.footer=document.querySelector(".js-footer"),this.toggleClassName=["filter-sidebar-active","filter-sidebar-hidden"])}mount(){if(this.toggleFilterSidebar)for(let t=0;t<this.toggleFilterSidebar.length;t++){const e=this.toggleFilterSidebar[t];this.addEvents(e,document.querySelector(".filter-sidebar"),this.toggleClassName),this.addEvents(e,document.querySelector("body"),this.toggleClassName,!0),e.setAttribute("data-component","")}this.mainButton&&this.watchMainButton()}watchMainButton(){new o.a(this.footer,{},()=>{this.secondButton.classList.add("position-sticky-on-footer-line")},()=>{this.secondButton.classList.remove("position-sticky-on-footer-line")}).mount();new o.a(this.mainButton,{rootMargin:"-74px 0px 0px 0px"},()=>{this.secondButton.classList.add("d-none")},()=>{this.secondButton.classList.remove("d-none")}).mount()}addEvents(t,e,s,a=!1){t.addEventListener("click",()=>{const t=document.getElementsByClassName("toggle-filter-sidebar-button");for(let t=0;t<s.length;t++)e.classList.toggle(s[t]);if(document.getElementsByClassName("filter-sidebar-hidden").length>0)for(let e=0;e<t.length;e++)t[e].style.display="none";else for(let e=0;e<t.length;e++)t[e].style.display="inline";a&&this.savePreference(),window.onSidebarToggle&&window.onSidebarToggle()})}savePreference(){const t={state:!0};document.querySelector("body.filter-sidebar-hidden")&&(t.state=!1),a.a.save("/my/filter-toggle","filterDisplayed",t)}}}}]);