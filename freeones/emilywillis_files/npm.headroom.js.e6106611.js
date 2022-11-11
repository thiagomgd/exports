(window.webpackJsonp=window.webpackJsonp||[]).push([["npm.headroom.js"],{e0Yc:function(t,o,n){var i,e,s;
/*!
 * headroom.js v0.9.4 - Give your page some headroom. Hide your header until you need it
 * Copyright (c) 2017 Nick Williams - http://wicky.nillia.ms/headroom.js
 * License: MIT
 */!function(n,r){"use strict";e=[],void 0===(s="function"==typeof(i=function(){var t={bind:!!function(){}.bind,classList:"classList"in document.documentElement,rAF:!!(window.requestAnimationFrame||window.webkitRequestAnimationFrame||window.mozRequestAnimationFrame)};function o(t){this.callback=t,this.ticking=!1}function n(t){return t&&"undefined"!=typeof window&&(t===window||t.nodeType)}function i(t,o){var e;o=function t(o){if(arguments.length<=0)throw new Error("Missing arguments in extend function");var i,e,s=o||{};for(e=1;e<arguments.length;e++){var r=arguments[e]||{};for(i in r)"object"!=typeof s[i]||n(s[i])?s[i]=s[i]||r[i]:s[i]=t(s[i],r[i])}return s}(o,i.options),this.lastKnownScrollY=0,this.elem=t,this.tolerance=(e=o.tolerance)===Object(e)?e:{down:e,up:e},this.classes=o.classes,this.offset=o.offset,this.scroller=o.scroller,this.initialised=!1,this.onPin=o.onPin,this.onUnpin=o.onUnpin,this.onTop=o.onTop,this.onNotTop=o.onNotTop,this.onBottom=o.onBottom,this.onNotBottom=o.onNotBottom}return window.requestAnimationFrame=window.requestAnimationFrame||window.webkitRequestAnimationFrame||window.mozRequestAnimationFrame,o.prototype={constructor:o,update:function(){this.callback&&this.callback(),this.ticking=!1},requestTick:function(){this.ticking||(requestAnimationFrame(this.rafCallback||(this.rafCallback=this.update.bind(this))),this.ticking=!0)},handleEvent:function(){this.requestTick()}},i.prototype={constructor:i,init:function(){if(i.cutsTheMustard)return this.debouncer=new o(this.update.bind(this)),this.elem.classList.add(this.classes.initial),setTimeout(this.attachEvent.bind(this),100),this},destroy:function(){var t=this.classes;for(var o in this.initialised=!1,t)t.hasOwnProperty(o)&&this.elem.classList.remove(t[o]);this.scroller.removeEventListener("scroll",this.debouncer,!1)},attachEvent:function(){this.initialised||(this.lastKnownScrollY=this.getScrollY(),this.initialised=!0,this.scroller.addEventListener("scroll",this.debouncer,!1),this.debouncer.handleEvent())},unpin:function(){var t=this.elem.classList,o=this.classes;!t.contains(o.pinned)&&t.contains(o.unpinned)||(t.add(o.unpinned),t.remove(o.pinned),this.onUnpin&&this.onUnpin.call(this))},pin:function(){var t=this.elem.classList,o=this.classes;t.contains(o.unpinned)&&(t.remove(o.unpinned),t.add(o.pinned),this.onPin&&this.onPin.call(this))},top:function(){var t=this.elem.classList,o=this.classes;t.contains(o.top)||(t.add(o.top),t.remove(o.notTop),this.onTop&&this.onTop.call(this))},notTop:function(){var t=this.elem.classList,o=this.classes;t.contains(o.notTop)||(t.add(o.notTop),t.remove(o.top),this.onNotTop&&this.onNotTop.call(this))},bottom:function(){var t=this.elem.classList,o=this.classes;t.contains(o.bottom)||(t.add(o.bottom),t.remove(o.notBottom),this.onBottom&&this.onBottom.call(this))},notBottom:function(){var t=this.elem.classList,o=this.classes;t.contains(o.notBottom)||(t.add(o.notBottom),t.remove(o.bottom),this.onNotBottom&&this.onNotBottom.call(this))},getScrollY:function(){return void 0!==this.scroller.pageYOffset?this.scroller.pageYOffset:void 0!==this.scroller.scrollTop?this.scroller.scrollTop:(document.documentElement||document.body.parentNode||document.body).scrollTop},getViewportHeight:function(){return window.innerHeight||document.documentElement.clientHeight||document.body.clientHeight},getElementPhysicalHeight:function(t){return Math.max(t.offsetHeight,t.clientHeight)},getScrollerPhysicalHeight:function(){return this.scroller===window||this.scroller===document.body?this.getViewportHeight():this.getElementPhysicalHeight(this.scroller)},getDocumentHeight:function(){var t=document.body,o=document.documentElement;return Math.max(t.scrollHeight,o.scrollHeight,t.offsetHeight,o.offsetHeight,t.clientHeight,o.clientHeight)},getElementHeight:function(t){return Math.max(t.scrollHeight,t.offsetHeight,t.clientHeight)},getScrollerHeight:function(){return this.scroller===window||this.scroller===document.body?this.getDocumentHeight():this.getElementHeight(this.scroller)},isOutOfBounds:function(t){var o=t<0,n=t+this.getScrollerPhysicalHeight()>this.getScrollerHeight();return o||n},toleranceExceeded:function(t,o){return Math.abs(t-this.lastKnownScrollY)>=this.tolerance[o]},shouldUnpin:function(t,o){var n=t>this.lastKnownScrollY,i=t>=this.offset;return n&&i&&o},shouldPin:function(t,o){var n=t<this.lastKnownScrollY,i=t<=this.offset;return n&&o||i},update:function(){var t=this.getScrollY(),o=t>this.lastKnownScrollY?"down":"up",n=this.toleranceExceeded(t,o);this.isOutOfBounds(t)||(t<=this.offset?this.top():this.notTop(),t+this.getViewportHeight()>=this.getScrollerHeight()?this.bottom():this.notBottom(),this.shouldUnpin(t,n)?this.unpin():this.shouldPin(t,n)&&this.pin(),this.lastKnownScrollY=t)}},i.options={tolerance:{up:0,down:0},offset:0,scroller:window,classes:{pinned:"headroom--pinned",unpinned:"headroom--unpinned",top:"headroom--top",notTop:"headroom--not-top",bottom:"headroom--bottom",notBottom:"headroom--not-bottom",initial:"headroom"}},i.cutsTheMustard=void 0!==t&&t.rAF&&t.bind&&t.classList,i})?i.apply(o,e):i)||(t.exports=s)}()}}]);