import axios from 'axios';
import { Toast } from 'vant';
import router from '../router';

const baseURL = 'http://127.0.0.1:5000';

// axios配置
const instance = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

instance.interceptors.response.use(
  res => {
    return Promise.resolve(res);
  },
  err => {
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
  },
);

export default instance;
