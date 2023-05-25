(function(){/*

 Copyright The Closure Library Authors.
 SPDX-License-Identifier: Apache-2.0
*/
'use strict';var f;function aa(a){var b=0;return function(){return b<a.length?{done:!1,value:a[b++]}:{done:!0}}}
function g(){var a=ba,b="undefined"!=typeof Symbol&&Symbol.iterator&&a[Symbol.iterator];if(b)return b.call(a);if("number"==typeof a.length)return{next:aa(a)};throw Error(String(a)+" is not an iterable or ArrayLike");}
var ca="function"==typeof Object.create?Object.create:function(a){function b(){}
b.prototype=a;return new b},h;
if("function"==typeof Object.setPrototypeOf)h=Object.setPrototypeOf;else{var k;a:{var da={a:!0},l={};try{l.__proto__=da;k=l.a;break a}catch(a){}k=!1}h=k?function(a,b){a.__proto__=b;if(a.__proto__!==b)throw new TypeError(a+" is not extensible");return a}:null}var m=h,n=this||self;
function q(a){a=a.split(".");for(var b=n,c=0;c<a.length;c++)if(b=b[a[c]],null==b)return null;return b}
function r(a,b){a=a.split(".");var c=n;a[0]in c||"undefined"==typeof c.execScript||c.execScript("var "+a[0]);for(var d;a.length&&(d=a.shift());)a.length||void 0===b?c[d]&&c[d]!==Object.prototype[d]?c=c[d]:c=c[d]={}:c[d]=b}
;function t(){this.s=this.s;this.B=this.B}
t.prototype.s=!1;t.prototype.dispose=function(){this.s||(this.s=!0,this.G())};
t.prototype.G=function(){if(this.B)for(;this.B.length;)this.B.shift()()};var u=n.window,v,w,x=(null==u?void 0:null==(v=u.yt)?void 0:v.config_)||(null==u?void 0:null==(w=u.ytcfg)?void 0:w.data_)||{};r("yt.config_",x);function y(a,b){return a in x?x[a]:b}
;function z(a,b){a=A(a);return void 0===a&&void 0!==b?b:Number(a||0)}
function A(a){var b=y("EXPERIMENTS_FORCED_FLAGS",{})||{};return void 0!==b[a]?b[a]:y("EXPERIMENT_FLAGS",{})[a]}
;var ea=z("web_emulated_idle_callback_delay",300),B=1E3/60-3,ba=[8,5,4,3,2,1,0];
function C(a){a=void 0===a?{}:a;t.call(this);this.i=[];this.h={};this.D=this.g=0;this.C=this.l=!1;this.u=[];this.A=this.F=!1;for(var b=g(),c=b.next();!c.done;c=b.next())this.i[c.value]=[];this.j=0;this.N=a.timeout||1;this.o=B;this.m=0;this.H=this.R.bind(this);this.M=this.T.bind(this);this.J=this.O.bind(this);this.K=this.P.bind(this);this.L=this.S.bind(this);if(b=!!window.requestIdleCallback&&!!window.cancelIdleCallback)b=A("disable_scheduler_requestIdleCallback"),b=!("string"===typeof b&&"false"===
b?0:b);this.I=b;(this.v=!1!==a.useRaf&&!!window.requestAnimationFrame)&&document.addEventListener("visibilitychange",this.H)}
C.prototype=ca(t.prototype);C.prototype.constructor=C;if(m)m(C,t);else for(var D in t)if("prototype"!=D)if(Object.defineProperties){var E=Object.getOwnPropertyDescriptor(t,D);E&&Object.defineProperty(C,D,E)}else C[D]=t[D];function F(a,b){var c=Date.now();G(b);b=Date.now()-c;a.l||(a.o-=b)}
function H(a,b,c,d){++a.D;if(10===c)return F(a,b),a.D;var e=a.D;a.h[e]=b;a.l&&!d?a.u.push({id:e,priority:c}):(a.i[c].push(e),a.C||a.l||(0!==a.g&&I(a)!==a.m&&J(a),a.start()));return e}
function K(a){a.u.length=0;for(var b=5;0<=b;b--)a.i[b].length=0;a.i[8].length=0;a.h={};J(a)}
function I(a){if(a.i[8].length){if(a.A)return 4;if(!document.hidden&&a.v)return 3}for(var b=5;b>=a.j;b--)if(0<a.i[b].length)return 0<b?!document.hidden&&a.v?3:2:1;return 0}
function L(a){var b=q("yt.logging.errors.log");b&&b(a)}
function G(a){try{a()}catch(b){L(b)}}
function M(a){for(var b=g(),c=b.next();!c.done;c=b.next())if(a.i[c.value].length)return!0;return!1}
f=C.prototype;f.P=function(a){var b=void 0;a&&(b=a.timeRemaining());this.F=!0;N(this,b);this.F=!1};
f.T=function(){N(this)};
f.O=function(){O(this)};
f.S=function(a){this.A=!0;var b=I(this);4===b&&b!==this.m&&(J(this),this.start());N(this,void 0,a);this.A=!1};
f.R=function(){document.hidden||O(this);this.g&&(J(this),this.start())};
function O(a){J(a);a.l=!0;for(var b=Date.now(),c=a.i[8];c.length;){var d=c.shift(),e=a.h[d];delete a.h[d];e&&G(e)}P(a);a.l=!1;M(a)&&a.start();a.o-=Date.now()-b}
function P(a){for(var b=0,c=a.u.length;b<c;b++){var d=a.u[b];a.i[d.priority].push(d.id)}a.u.length=0}
function N(a,b,c){a.A&&4===a.m&&a.g||J(a);a.l=!0;b=Date.now()+(b||a.o);for(var d=a.i[5];d.length;){var e=d.shift(),p=a.h[e];delete a.h[e];if(p)try{p(c)}catch(ja){L(ja)}}for(d=a.i[4];d.length;)c=d.shift(),e=a.h[c],delete a.h[c],e&&G(e);d=a.F?0:1;d=a.j>d?a.j:d;if(!(Date.now()>=b)){do{a:{c=a;e=d;for(p=3;p>=e;p--)for(var U=c.i[p];U.length;){var V=U.shift(),W=c.h[V];delete c.h[V];if(W){c=W;break a}}c=null}c&&G(c)}while(c&&Date.now()<b)}a.l=!1;P(a);a.o=B;M(a)&&a.start()}
f.start=function(){this.C=!1;if(0===this.g)switch(this.m=I(this),this.m){case 1:var a=this.K;this.g=this.I?window.requestIdleCallback(a,{timeout:3E3}):window.setTimeout(a,ea);break;case 2:this.g=window.setTimeout(this.M,this.N);break;case 3:this.g=window.requestAnimationFrame(this.L);break;case 4:this.g=window.setTimeout(this.J,0)}};
function J(a){if(a.g){switch(a.m){case 1:var b=a.g;a.I?window.cancelIdleCallback(b):window.clearTimeout(b);break;case 2:case 4:window.clearTimeout(a.g);break;case 3:window.cancelAnimationFrame(a.g)}a.g=0}}
f.G=function(){K(this);J(this);this.v&&document.removeEventListener("visibilitychange",this.H);t.prototype.G.call(this)};var Q=q("yt.scheduler.instance.timerIdMap_")||{},R=z("kevlar_tuner_scheduler_soft_state_timer_ms",800),S=0,T=0;function X(){var a=q("ytglobal.schedulerInstanceInstance_");if(!a||a.s)a=new C(y("scheduler")||{}),r("ytglobal.schedulerInstanceInstance_",a);return a}
function fa(){Y();var a=q("ytglobal.schedulerInstanceInstance_");a&&(a&&"function"==typeof a.dispose&&a.dispose(),r("ytglobal.schedulerInstanceInstance_",null))}
function Y(){K(X());for(var a in Q)Q.hasOwnProperty(a)&&delete Q[Number(a)]}
function ha(a,b,c){if(!c)return c=void 0===c,-H(X(),a,b,c);var d=window.setTimeout(function(){var e=H(X(),a,b);Q[d]=e},c);
return d}
function ia(a){var b=X();F(b,a)}
function ka(a){var b=X();if(0>a)delete b.h[-a];else{var c=Q[a];c?(delete b.h[c],delete Q[a]):window.clearTimeout(a)}}
function Z(a){var b=q("ytcsi.tick");b&&b(a)}
function la(){Z("jse");ma()}
function ma(){window.clearTimeout(S);X().start()}
function na(){var a=X();J(a);a.C=!0;window.clearTimeout(S);S=window.setTimeout(la,R)}
function oa(){window.clearTimeout(T);T=window.setTimeout(function(){Z("jset");pa(0)},R)}
function pa(a){oa();var b=X();b.j=a;b.start()}
function qa(a){oa();var b=X();b.j>a&&(b.j=a,b.start())}
function ra(){window.clearTimeout(T);var a=X();a.j=0;a.start()}
;q("yt.scheduler.initialized")||(r("yt.scheduler.instance.dispose",fa),r("yt.scheduler.instance.addJob",ha),r("yt.scheduler.instance.addImmediateJob",ia),r("yt.scheduler.instance.cancelJob",ka),r("yt.scheduler.instance.cancelAllJobs",Y),r("yt.scheduler.instance.start",ma),r("yt.scheduler.instance.pause",na),r("yt.scheduler.instance.setPriorityThreshold",pa),r("yt.scheduler.instance.enablePriorityThreshold",qa),r("yt.scheduler.instance.clearPriorityThreshold",ra),r("yt.scheduler.initialized",!0));}).call(this);
