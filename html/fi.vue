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

<div>代理
<input v-model="proxy_ip" placeholder="代理ip"><input v-model="proxy_port" placeholder="代理端口"></div>
  <div>数据库
<input v-model="DB_ip" placeholder="数据库ip"><input v-model="DB_port" placeholder="数据库端口"><input v-model="DB_name" placeholder="数据库名字">
  <input v-model="DB_pass" placeholder="密码"><input v-model="DB_uase" placeholder="用户名"><input v-model="dbtf" type="radio" name="sex" value=true>验证
<input v-model="dbtf" type="radio" name="sex" value=false>无验证</div>

  <div>cookie
<input v-model="cookie" placeholder="cookie"><input v-model="uid" placeholder="uid"></div>

    <div>线程设置
<input v-model="T_num" placeholder="线程数量"><input v-model="T_time" placeholder="线程间隔"><input v-model="sctime" placeholder="收藏检查时间"></div>





 <n-button text v-on:click="postt" size="big">
              <!--              {{ topc }}-->
              提交数据

            </n-button>









</div>


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
            proxy_ip:'',proxy_port:'',DB_ip:'',DB_port:'',DB_name:'',DB_pass:'',DB_uase:'',T_num:'',dbtf:false,cookie:'',T_time:'',sctime:'',uid:''


            // fonts:"url('/font/coldnightforalligators.ttf')"

          }
          /////////////////////////////////////////////////////////////////////////////
        },
        methods: {
          postt: function () {c2es=this;
            axios.get('/first_api',data={params: {


    p_ip: c2es.proxy_ip,
              P_p: c2es.proxy_port,
              db_ip: c2es.DB_ip,
              db_port: c2es.DB_port,
              db_name: c2es.DB_name,
              cookie: c2es.cookie,
              T_num: c2es.T_num,
              T_time: c2es.T_time,
              sc_timr: c2es.sctime,
              verify: c2es.dbtf,
              DB_u: c2es.DB_uase,    DB_p: c2es.DB_pass,uid:c2es.uid}
              // 参数 firstName
       // 参数 lastName
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