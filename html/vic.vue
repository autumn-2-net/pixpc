<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
  <script src="/js_css/vue3.2.34.js"></script>
  <script src="/js_css/naive.js"></script>
  <script src="/js_css/axios.js"></script>
  <script src="/js_css/boxicons.js"></script>
</head>
<body>
<div id="main">
<input v-model="ids" placeholder="id">





 <n-button text v-on:click="postt" size="big">
              <!--              {{ topc }}-->
              提交数据

            </n-button>
<template v-for="imgi in imgg">
  <img v-bind:src="imgi" >
</template></div>

          <script type="text/javascript">




  // import {dateZhCN, zhCN} from "../js_css";
  // import { defineComponent, ref } from "/js_css/vue3.2.34.js";
  // import { darkTheme } from "/js_css/naive.js";
  //   import type { NLocale, NDateLocale } from "/js_css/naive.js";
  const {dateZhCN, zhCN, darkTheme} = naive;
  // const type { NLocale, NDateLocale }=import("/js_css/naive.js");
  const {defineComponent, ref} = Vue;
  const vum = Vue.createApp({
        setup() {
          return {
            zhCN,
            dateZhCN,
            // locale: ref<NLocale | null>(null),
            // dateLocale: ref<NDateLocale | null>(null),
            locale: ref(null),
            dateLocale: ref(null),
            darkTheme,
            // theme: ref(null)
          }
        },
        //////////////////////////////////////////////////////////////////
        data() {
          return {
            ids:'',imgg:[]


            // fonts:"url('/font/coldnightforalligators.ttf')"

          }
          /////////////////////////////////////////////////////////////////////////////
        },
        methods: {
          postt: function () {c2es=this;
            axios.get('/apic',data={params: {


    ids: c2es.ids,
              }
              // 参数 firstName
       // 参数 lastName

  }) .then(function (response) {
    // console.log(response)c2es
              c2es.imgg=response.data

    ;
  })


          }

        },
      }
  );
  vum.use(naive);



  vum.mount(`#main`)
</script>



</body>
</html>
