<template>
  <div>
    <!-- 顶部导航栏 -->
    <van-nav-bar
      title="我的"
      fixed
      placeholder
      z-index="100"
      left-arrow
      @click-left="back"
    />

    <div>用户页面</div>
    <van-button @click="logout" type="danger">退出登录</van-button>
  </div>
</template>

<script>
import { Toast } from 'vant';
import { apis } from '../api/apis';
export default {
  methods: {
    logout() {
      apis.logout().then(() => {
        Toast.success({ message: '退出成功' });
        localStorage.setItem('username', undefined);
        localStorage.setItem('uuid', undefined);
        this.$router.push({
          path: '/login',
        });
      });
    },

    back() {
      this.$router.back();
    },
  },
};
</script>

<style scoped></style>
