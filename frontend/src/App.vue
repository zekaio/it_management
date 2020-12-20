<template>
  <div id="app">
    <!-- loading -->
    <van-overlay class="up" :show="g.showLoading">
      <div class="loading_wrapper up" @click.stop>
        <van-loading size="50px" text-size="16px" vertical>
          加载中...
        </van-loading>
      </div>
    </van-overlay>
    <router-view :key="$route.fullPath"></router-view>
  </div>
</template>

<script>
import { Toast } from 'vant';
import { apis } from './api/apis';
import { g } from './config';

export default {
  name: 'App',
  data: () => {
    return { g };
  },
  async mounted() {
    apis
      .getUserInfo()
      .then((res) => {
        localStorage.setItem('username', res.data.data.username);
        localStorage.setItem('uuid', res.data.data.uuid);
      })
      .catch((err) => {
        this.$error(err, (err) => {
          if (err.response.status == 404) {
            Toast.fail({
              message: '用户不存在，请重新登录',
            });
            apis
              .logout()
              .then(() => {
                localStorage.setItem('username', undefined);
                localStorage.setItem('uuid', undefined);
                this.$router.push({
                  path: '/login',
                });
              })
              .catch((err) => this.$error(err));
            return true;
          }
        });
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
  background-color: rgb(230, 230, 230);
}
.loading_wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
.up {
  z-index: 10000;
}
</style>
