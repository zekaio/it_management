<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import { Toast } from 'vant';
import { apis } from './api/apis';
export default {
  name: 'App',
  async mounted() {
    apis
      .getUserInfo()
      .then((res) => {
        if (this.$route.path == '/') {
          this.$router.push({
            path: '/index',
          });
        }
        localStorage.setItem('username', res.data.data.username);
        localStorage.setItem('uuid', res.data.data.uuid);
        console.log('username: ' + localStorage.getItem('username'));
        console.log('uuid: ' + localStorage.getItem('uuid'));
      })
      .catch((err) => {
        if (err.response.status == 404) {
          Toast.fail({
            message: '用户不存在，请重新登陆',
          });
          localStorage.setItem('username', undefined);
          localStorage.setItem('uuid', undefined);
          this.$router.push({
            path: '/login',
          });
        } else {
          Toast.fail({
            message:
              err.response.data.message || `未知错误${err.response.data}`,
          });
        }
      });
  },
};
</script>

<style>
body {
  margin: 0;
  padding: 0;
  min-height: 100vh;
  min-width: 100vw;
}
.van-nav-bar {
  box-shadow: 0 2px 3px -1px rgb(221, 218, 218);
}
</style>
