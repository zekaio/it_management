<template>
  <div class="login">
    <!-- 标题 -->
    <div class="title">注册</div>

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

      <!-- 确认密码 -->
      <van-field
        v-model="checkPwd"
        type="password"
        name="checkPwd"
        label="确认密码"
        placeholder="确认密码"
        :rules="[{ required: true, message: '请确认密码' }]"
      />

      <!-- 按钮 -->
      <div style="margin: 24px 64px;">
        <!-- 注册 -->
        <van-button round block type="info" native-type="submit">
          注册
        </van-button>

        <!-- 前往登录 -->
        <van-button
          style="margin-top: 24px"
          round
          block
          plain
          type="info"
          native-type="button"
          to="login"
        >
          前往登录
        </van-button>
      </div>
    </van-form>
  </div>
</template>

<script>
import { Toast } from 'vant';
import { apis } from '../api/apis';
export default {
  data() {
    return {
      username: '',
      password: '',
      checkPwd: '',
    };
  },
  methods: {
    onSubmit(values) {
      apis
        .register(values.username, values.password, values.checkPwd)
        .then(() => {
          Toast.success({
            message: '注册成功',
          });
          this.$router.push({
            path: '/login',
          });
        })
        .catch((err) => {
          Toast.fail({
            message:
              err.response.data.message || `未知错误${err.response.data}`,
          });
        });
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
