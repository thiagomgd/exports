(window.webpackJsonp=window.webpackJsonp||[]).push([[5],{rPx6:function(t,e,s){"use strict";var o=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("modal",{attrs:{name:"problemReport",height:"auto",classes:"v-modal bg-color-tertiary"}},[s("div",{staticClass:" d-flex flex-column p-4"},[s("h4",{staticClass:"border-bottom border-color-border border-width-1 pb-3 mb-3 w-100 font-weight-bold d-flex justify-content-between"},[t._v("\n      "+t._s(t.$store.state.translations[this.$translationLocale].problem_report_dialog["report_"+t.type])+"\n      "),s("button",{staticClass:"icon-button",attrs:{title:t.$store.state.translations[this.$translationLocale].problem_report_dialog.close,"aria-label":t.$store.state.translations[this.$translationLocale].problem_report_dialog.close},on:{click:function(e){return t.hide()}}},[s("icon",{attrs:{icon:"close",classes:"svg-icon-mlm"}})],1)]),t._v(" "),s("div",{directives:[{name:"show",rawName:"v-show",value:!t.reported,expression:"!reported"}]},[s("form",[s("div",{staticClass:"form-group mb-4"},[s("label",{staticClass:"font-weight-bold"},[t._v("\n            "+t._s(t.$store.state.translations[this.$translationLocale].problem_report_dialog[t.type])+"\n          ")]),t._v(" "),"link"===t.type?s("div",[s("a",{staticClass:"inline-link",attrs:{target:"_blank",href:t.meta}},[t._v(t._s(t.title))])]):s("div",[t._v("\n            "+t._s(t.title)+"\n          ")])]),t._v(" "),s("div",{staticClass:"form-group mb-4"},[s("label",{staticClass:"font-weight-bold"},[t._v("\n            "+t._s(t.$store.state.translations[this.$translationLocale].problem_report_dialog.reason)+"\n          ")]),t._v(" "),s("div",{staticClass:" mb-2"},[s("div",{staticClass:" align-items-center w-100 mr-2"},t._l(t.reportReasons,(function(e){return s("div",{key:e.value,staticClass:"form-check"},[s("label",{staticClass:"form-check-label"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.reason,expression:"reason"}],staticClass:"form-check-input ml-0",attrs:{type:"radio",name:"reportReason"},domProps:{value:e.value,checked:t._q(t.reason,e.value)},on:{change:function(s){t.reason=e.value}}}),t._v("\n                  "+t._s(e.value)+"\n                ")])])})),0)])]),t._v(" "),s("div",{directives:[{name:"show",rawName:"v-show",value:"Other"===t.reason,expression:"reason === 'Other'"}],staticClass:"form-group mb-4"},[s("label",{staticClass:"font-weight-bold",attrs:{for:"report-comment-description"}},[t._v(t._s(t.$store.state.translations[this.$translationLocale].problem_report_dialog.reason))]),t._v(" "),s("div",{staticClass:"d-flex flex-row mb-2"},[s("div",{staticClass:"d-flex align-items-center w-100"},[s("textarea",{ref:"comment",staticClass:"form-control w-100",attrs:{rows:"3",id:"report-comment-description"}})])])]),t._v(" "),s("div",{directives:[{name:"show",rawName:"v-show",value:!t.isLoggedIn,expression:"!isLoggedIn"}],staticClass:"form-group mb-4"},[s("div",[s("label",{directives:[{name:"show",rawName:"v-show",value:t.submitterInfoMissing,expression:"submitterInfoMissing"}],staticClass:"font-weight-bold danger"},[t._v("\n              "+t._s(t.$store.state.translations[this.$translationLocale].problem_report_dialog.name_email_required)+"\n            ")])]),t._v(" "),s("label",{staticClass:"font-weight-bold",attrs:{for:"submitterName"}},[t._v("\n            "+t._s(t.$store.state.translations[this.$translationLocale].problem_report_dialog.name)+"\n          ")]),t._v(" "),s("div",{staticClass:"d-flex flex-row mb-2"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.submitterName,expression:"submitterName"}],staticClass:"form-control font-size-sm font-weight-light",attrs:{type:"text",required:"",id:"submitterName"},domProps:{value:t.submitterName},on:{input:function(e){e.target.composing||(t.submitterName=e.target.value)}}})]),t._v(" "),s("label",{staticClass:"font-weight-bold",attrs:{for:"email"}},[t._v("\n            "+t._s(t.$store.state.translations[this.$translationLocale].problem_report_dialog.email)+"\n          ")]),t._v(" "),s("div",{staticClass:"d-flex flex-row mb-2"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.email,expression:"email"}],staticClass:"form-control font-size-sm font-weight-light",attrs:{type:"email",required:"",id:"email"},domProps:{value:t.email},on:{input:function(e){e.target.composing||(t.email=e.target.value)}}})])]),t._v(" "),s("div",{staticClass:"float-right"},[s("button",{staticClass:"btn btn-outline-white",attrs:{type:"button"},on:{click:function(e){return t.hide()}}},[t._v("\n            "+t._s(t.$store.state.translations[this.$translationLocale].problem_report_dialog.cancel)+"\n          ")]),t._v(" "),s("button",{staticClass:"btn btn-primary flex-1",attrs:{type:"button"},on:{click:function(e){return t.postProblemReport()}}},[t._v("\n            "+t._s(t.$store.state.translations[this.$translationLocale].problem_report_dialog.report)+"\n          ")])])])]),t._v(" "),s("div",{directives:[{name:"show",rawName:"v-show",value:t.reported,expression:"reported"}]},[s("div",{staticClass:"pt-3"},[t._v("\n        "+t._s(t.$store.state.translations[this.$translationLocale].problem_report_dialog.reported)+"\n      ")])])])])};o._withStripped=!0;var a=s("vDqi"),r=s.n(a),i=s("h6/w"),n={name:"ProblemReportModal",data:()=>({showAddPlaylist:!1,loaded:!1,reported:!1,reason:"",comment:!1,typeId:null,type:null,title:null,isLoggedIn:!1,meta:"",reportReasons:[],submitterInfoMissing:!1,submitterName:"",email:""}),methods:{show(t,e,s,o,a){this.typeId=t,this.type=e,this.title=s,this.meta=o,this.isLoggedIn=a,this.getProblemReportReasons()},hide(t){this.$modal.hide("problemReport")},getProblemReportReasons(){r.a.get("/problem-report/reasons/"+this.type).then(t=>{this.reportReasons=t.data.reportReasons,this.reason=this.reportReasons[0].value,this.$modal.show("problemReport")}).catch(t=>{this.error=!0,i.a.error(t.message,t)})},postProblemReport(){this.loading=!0;const t=this.submitterName.trim(),e=this.email.trim();this.isLoggedIn||0!==t.length&&0!==e.length?r.a.post("/problem-report/add",{typeId:this.typeId,type:this.type,reason:this.reason,comment:this.$refs.comment.value,submitterName:t,email:e}).then(t=>{this.loading=!1,this.reported=!0}).catch(t=>{this.errorMessage=t.response.data.error,this.showError=!0,this.loading=!1}):this.submitterInfoMissing=!0}},mounted:function(){this.$eventHub.$on("showModal",this.show),this.$eventHub.$on("hideModal",this.hide),this.$el.parentElement.removeAttribute("id")}},l=s("KHd+"),m=Object(l.a)(n,o,[],!1,null,null,null);m.options.__file="assets/base-theme/js/components/problem-report/ProblemReportModal.vue";e.a=m.exports}}]);