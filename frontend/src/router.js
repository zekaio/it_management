import Vue from 'vue';
import VueRouter from 'vue-router';

import login from './views/login.vue';
import register from './views/register.vue';
import index from './views/index.vue';
import detail from './views/detail.vue';
import edit from './views/edit.vue';
import search from './views/search.vue';
import user from './views/user.vue';

Vue.use(VueRouter);

const routerPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return routerPush.call(this, location).catch((error) => error);
};

const routes = [
  // 首页
  {
    path: '/index',
    name: 'index',
    component: index,
  },
  // 登录
  {
    path: '/login',
    name: 'login',
    component: login,
  },
  // 注册
  {
    path: '/register',
    name: 'register',
    component: register,
  },
  // 帖子详情
  {
    path: '/post/:postId/detail',
    name: 'post',
    component: detail,
  },
  // 编辑
  {
    path: '/post/:postId?/edit',
    name: 'edit',
    component: edit,
  },
  // 搜索
  {
    path: '/search',
    name: 'search',
    component: search,
  },
  // 用户主页
  {
    path: '/user',
    name: 'user',
    component: user,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
