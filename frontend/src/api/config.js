import axios from 'axios';
import { Toast } from 'vant';
import router from '../router';
import { baseURL, g } from '../config';

// axios配置
const instance = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
  showLoading: false,
});

instance.interceptors.response.use(
  (res) => {
    if (res.config.showLoading) {
      g.showLoading = false;
    }
    return Promise.resolve(res);
  },
  (err) => {
    if (err.config.showLoading) {
      g.showLoading = false;
    }
    if (!err.response) {
      Toast.fail({
        message: '服务器无法响应',
      });
    } else {
      console.log(err.response);
      switch (err.response.status) {
        // 未登录
        case 401:
          if (
            router.currentRoute.name != 'login' &&
            router.currentRoute.name != 'register'
          ) {
            Toast({
              message: '请先登录',
            });
            router.push({
              path: '/login',
            });
          }
          break;
        // 服务器错误
        case 500:
          Toast.fail({
            message: '服务器错误',
          });
          break;
        default:
          return Promise.reject(err);
      }
    }
    return new Promise(() => {});
  }
);

instance.interceptors.request.use(
  (config) => {
    if (config.showLoading) {
      g.showLoading = true;
    }
    if (/get/i.test(config.method)) {
      config.params = config.params || {};
      config.params.timestamp = new Date().getTime();
    }
    return config;
  },
  (err) => {
    return Promise.reject(err);
  }
);

export default instance;
