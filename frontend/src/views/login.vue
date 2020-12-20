<template>
  <div class="login">
    <!-- 标题 -->
    <div class="title">登录</div>

    <!-- 表单 -->
    <van-form @submit="onSubmit">
      <!-- 用户名 -->
      <van-field
        v-model="username"
        type="text"
        name="username"
        label="用户名"
        placeholder="用户名"
        :rules="[{ required: true, message: '请填写用户名' }]"
      />

      <!-- 密码 -->
      <van-field
        v-model="password"
        type="password"
        name="password"
        label="密码"
        placeholder="密码"
        :rules="[{ required: true, message: '请填写密码' }]"
      />

      <!-- 按钮 -->
      <div style="margin: 24px 64px;">
        <!-- 登录 -->
        <van-button round block type="info" native-type="submit">
          登录
        </van-button>

        <!-- 前往注册 -->
        <van-button
          style="margin-top: 24px"
          round
          block
          plain
          type="info"
          native-type="button"
          to="register"
        >
          前往注册
        </van-button>
      </div>
    </van-form>
  </div>
</template>

<script>
import { apis } from '../api/apis';

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    onSubmit(values) {
      apis
        .login(values.username, values.password)
        .then(() => {
          this.$router.push({
            path: '/',
          });
        })
        .catch((err) => this.$error(err));
    },
  },
};
</script>

<style scoped>
.login {
  min-height: 100vh;
  min-width: 100vw;
  display: flex;
  display: -webkit-flex;
  align-items: center;
  flex-direction: column;
}
.title {
  text-align: center;
  margin: 20px 0;
  font-size: 32px;
}
</style>
