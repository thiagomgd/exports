(window.webpackJsonp=window.webpackJsonp||[]).push([[11],{qI3T:function(e,t,c){"use strict";t.a=function(){if("querySelector"in document&&"addEventListener"in window){const e=document.querySelectorAll('[data-component="read-more"]');[].forEach.call(e,(function(e){const t=e.querySelector(".js-read-more-toggle"),c=e.querySelector(".js-read-more-wrapper");t&&t.addEventListener("click",(function(){const e=this.querySelector(".js-read-more-more"),a=this.querySelector(".js-read-more-less");c.classList.toggle("d-none"),e.classList.toggle("d-none"),a.classList.toggle("d-none"),e.classList.contains("d-none")?t.setAttribute("aria-expanded",!0):t.setAttribute("aria-expanded",!1)}))}));const t=document.querySelectorAll('[data-component="read-more-calc"]'),c=(e=>e*Math.max(document.documentElement.clientHeight,window.innerHeight||0)/100)(50);[].forEach.call(t,(function(e){const t=e.querySelector(".js-read-more-calc"),a=e.querySelector(".js-read-more-calc-wrapper");t&&a&&e.offsetHeight>c&&(a.classList.add("read-more-calc-initialized"),t.classList.remove("d-none"),t.addEventListener("click",(function(){t.classList.toggle("read-more-calc-active"),a.classList.toggle("read-more-calc-active"),a.classList.contains("read-more-calc-active")?a.setAttribute("aria-expanded",!0):a.setAttribute("aria-expanded",!1)})))}))}}}}]);