<template>
  <div class="login">
    <div class="title">登录</div>
    <van-form @submit="onSubmit">
      <van-field
        v-model="username"
        type="text"
        name="username"
        label="用户名"
        placeholder="用户名"
        :rules="[{ required: true, message: '请填写用户名' }]"
      />
      <van-field
        v-model="password"
        type="password"
        name="password"
        label="密码"
        placeholder="密码"
        :rules="[{ required: true, message: '请填写密码' }]"
      />
      <div style="margin: 16px 64px;">
        <van-button round block type="info" native-type="submit">
          登录
        </van-button>
        <van-button
          style="margin-top: 16px"
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
import { Toast } from 'vant';
import { apis } from '../api/apis';
export default {
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
            path: '/index',
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
}

.title {
  text-align: center;
  margin: 20px 0;
  font-size: 32px;
}
</style>
