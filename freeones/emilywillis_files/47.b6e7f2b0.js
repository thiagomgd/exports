(window.webpackJsonp=window.webpackJsonp||[]).push([[47],{FXSp:function(t,e,o){"use strict";o.r(e);var i=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("form",{attrs:{id:"comment-form"}},[t.errors.comment?o("p",{staticClass:"help is-danger"},[t._v("Please don't leave blank comments")]):t._e(),t._v(" "),o("div",{staticClass:"mb-2 mb-md-3 d-flex flex-row border-bottom border-width-1 pb-2 pb-md-3 border-color-border position-relative"},[o("input-with-emoji",{attrs:{name:"comment"},on:{submit:t.processForm},model:{value:t.comment,callback:function(e){t.comment=e},expression:"comment"}})],1)])};i._withStripped=!0;var s=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",{staticClass:"w-100 input-with-emoji"},[o("picker",{directives:[{name:"click-outside",rawName:"v-click-outside",value:t.closeEmojiPicker,expression:"closeEmojiPicker"},{name:"show",rawName:"v-show",value:t.showEmojiPicker,expression:"showEmojiPicker"}],attrs:{title:"Pick your emoji...",emoji:"point_up",set:"twitter",native:!1},on:{select:t.addEmoji}}),t._v(" "),o("input",{ref:"bodyinput",staticClass:"textarea w-100 color-text-dark",attrs:{name:t.name,type:"text",placeholder:"Write your comment here..."},domProps:{value:t.value},on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.$emit("submit")},input:function(e){return t.$emit("input",e.target.value)}}}),t._v(" "),o("button",{staticClass:"emoji-trigger input-emoticon-selector color-text-dark",class:{triggered:t.showEmojiPicker},attrs:{type:"button"},on:{mousedown:function(e){return e.preventDefault(),t.toggleEmojiPicker(e)}}},[o("icon",{attrs:{icon:"smile-regular",classes:"svg-icon-ml"}})],1),t._v(" "),t.value.trim().length?o("button",{staticClass:"input-with-emoji-submit color-text-dark",attrs:{type:"button"},on:{click:function(e){return t.$emit("submit")}}},[o("icon",{attrs:{icon:"paper-plane-regular",classes:"svg-icon-ml"}})],1):t._e()],1)};s._withStripped=!0;var n=o("sEf9"),r=o("wouM"),m=o.n(r);o("oCYn").default.use(m.a);var c={name:"InputWithEmoji",components:{Picker:n.Picker},props:{value:{type:String,default:""},name:{type:String}},data:()=>({showEmojiPicker:!1}),mounted(){},methods:{closeEmojiPicker(t){"function"==typeof t.target.className.match&&(t.target.className.match(/\bfa-smile\b/)&&!t.target.className.match(/\bemoji-trigger\b/)||(this.showEmojiPicker=!1))},toggleEmojiPicker(){this.showEmojiPicker=!this.showEmojiPicker},addEmoji(t){this.showEmojiPicker=!1;const e=this.$refs.bodyinput,o=e.selectionEnd,i=this.value.substring(0,e.selectionStart),s=this.value.substring(e.selectionStart),n=i+t.colons+" "+s;this.$emit("input",n),e.focus(),this.$nextTick(()=>{e.selectionEnd=o+t.colons.length+1})}}},a=o("KHd+"),l=Object(a.a)(c,s,[],!1,null,null,null);l.options.__file="assets/base-theme/js/modules/comments/InputWithEmoji.vue";var u=l.exports,p=o("vDqi"),h=o.n(p),d={name:"CommentForm",components:{InputWithEmoji:u},props:{typeId:String,type:String},data:()=>({comment:"",errors:{comment:!1}}),mounted(){},methods:{processForm:function(){if(this.errors.comment=""===this.comment,!this.errors.comment){let t="";for(let e=0;e<this.comment.length;e++)(this.comment.charCodeAt(e)<=127||this.comment.charCodeAt(e)>=160&&this.comment.charCodeAt(e)<=255)&&(t+=this.comment.charAt(e));h.a.post(`/comments/${this.type}/${this.typeId}/add`,{body:t,_csrf:this.csrfToken}).then(t=>{this.$emit("comment-added",t.data.comment),this.comment=""}).catch(t=>{console.log(t)})}}}},v=Object(a.a)(d,i,[],!1,null,null,null);v.options.__file="assets/base-theme/js/modules/comments/CommentForm.vue";e.default=v.exports}}]);