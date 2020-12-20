import Vue from 'vue';
import VueRouter from 'vue-router';

import Login from './views/Login.vue';
import Register from './views/Register.vue';
import Index from './views/Index.vue';
import Detail from './views/Detail.vue';
import Edit from './views/Edit.vue';
import Search from './views/Search.vue';
import User from './views/User.vue';
import UserInfo from './views/UserInfo.vue';
import Follow from './views/Follow.vue';

Vue.use(VueRouter);

const routerPush = VueRouter.prototype.push;

VueRouter.prototype.push = function push(location) {
  return routerPush.call(this, location).catch((error) => error);
};

const routes = [
  // 首页
  {
    path: '/',
    name: 'Index',
    component: Index,
  },
  // 登录
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  // 注册
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  // 帖子详情
  {
    path: '/post/:postId/detail',
    name: 'PostDetail',
    component: Detail,
  },
  // 评论详情
  {
    path: '/post/:postId/comment/:commentId',
    name: 'CommentDetail',
    component: Detail,
  },
  // 编辑
  {
    path: '/post/:postId?/edit',
    name: 'Edit',
    component: Edit,
  },
  // 搜索
  {
    path: '/search',
    name: 'Search',
    component: Search,
  },
  // 用户主页
  {
    path: '/user',
    name: 'User',
    component: User,
  },
  // 用户信息
  {
    path: '/user/info',
    name: 'UserInfo',
    component: UserInfo,
  },
  // 关注列表
  {
    path: '/follow',
    name: 'Follow',
    component: Follow,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: '/it/',
  routes,
});

export default router;
