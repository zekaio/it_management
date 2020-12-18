<template>
  <div class="user">
    <!-- 顶部导航栏 -->
    <van-nav-bar
      fixed
      placeholder
      z-index="100"
      left-arrow
      @click-left="back"
      v-if="this.$route.params.uuid !== undefined"
    />

    <div>用户页面</div>
    <van-button @click="logout" type="danger">退出登录</van-button>

    <!-- 底部导航栏 -->
    <van-tabbar
      v-model="active"
      placeholder
      v-if="this.$route.params.uuid === undefined"
    >
      <van-tabbar-item to="/" icon="home-o"></van-tabbar-item>
      <van-tabbar-item icon="user-o"> </van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script>
import { Toast } from 'vant';
import { apis } from '../api/apis';
export default {
  data() {
    return {
      active: 1,
    };
  },
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
