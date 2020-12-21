<template>
  <div class="index">
    <!-- 顶部导航栏 -->
    <van-nav-bar
      title="主页"
      @click-right="$goTo('search')"
      fixed
      placeholder
      z-index="100"
    >
      <template #right>
        <van-icon name="search" size="18" color="black" />
      </template>
    </van-nav-bar>

    <!-- 帖子 -->
    <van-pull-refresh v-model="refreshing" @refresh="refresh">
      <van-list
        v-model="loading"
        :finished="finished"
        finished-text="没有更多了"
        @load="getPosts"
      >
        <div v-for="(post, index) in posts" :key="index">
          <Post
            :post="post"
            :index="index"
            @deletePostEvent="deletePostEventHandler"
          />
        </div>
      </van-list>
    </van-pull-refresh>

    <!-- 底部导航栏 -->
    <van-tabbar v-model="active" placeholder>
      <van-tabbar-item icon="home-o" @click="refresh"></van-tabbar-item>
      <van-tabbar-item to="user" icon="user-o"> </van-tabbar-item>
    </van-tabbar>

    <!-- 发表帖子 -->
    <div class="submitIcon" @click="$goTo('/post/edit')">
      <svg
        t="1608362557923"
        class="icon"
        viewBox="0 0 1024 1024"
        version="1.1"
        xmlns="http://www.w3.org/2000/svg"
        p-id="29103"
        width="1.2rem"
        height="1.2rem"
      >
        <path
          d="M902.947 571.027h-332.293v332.346c0 32.387-26.267 58.628-58.655 58.628-32.387 0-58.654-26.241-58.654-58.628v-332.346h-332.295c-32.414 0-58.654-26.241-58.654-58.628 0-32.375 26.243-58.628 58.654-58.628h332.293v-332.346c0-32.375 26.267-58.628 58.654-58.628 32.388 0 58.655 26.254 58.655 58.628v332.347h332.293c32.414 0 58.655 26.252 58.655 58.626-0.001 32.387-26.241 58.626-58.655 58.626z"
          p-id="29104"
          fill="#ffffff"
        ></path>
      </svg>
    </div>
  </div>
</template>

<script>
import { Toast } from 'vant';

import { apis } from '../api/apis';

import Post from '../components/Post';

export default {
  name: 'index',

  components: { Post },

  data() {
    return {
      active: 0, // 底部导航栏活动位置

      loading: false, // list是否在加载
      finished: false, // list是否完全加载
      refreshing: false, // 上拉刷新

      posts: [], // 帖子
    };
  },

  methods: {
    // 刷新
    refresh() {
      let timeout = setTimeout(() => {
        Toast.fail({
          message: '请求超时，请重试',
        });
        return;
      }, 10000);
      apis
        .getPosts()
        .then((res) => {
          this.posts = res.data.data;
          if (res.data.data.length == 0) {
            this.finished = true;
          } else {
            this.finished = false;
          }
        })
        .catch((err) => this.$error(err))
        .finally(() => {
          clearTimeout(timeout);
        });
      this.refreshing = false;
    },

    // 获取更多帖子
    getPosts() {
      if (this.posts.length === 0) {
        apis
          .getPosts()
          .then((res) => {
            this.posts = res.data.data;
            if (res.data.data.length === 0) {
              this.finished = true;
            }
          })
          .catch((err) => this.$error(err))
          .finally(() => {
            this.loading = false;
          });
      } else {
        apis
          .getPosts({}, this.posts[this.posts.length - 1].post_id)
          .then((res) => {
            if (res.data.data.length === 0) {
              this.finished = true;
            } else {
              this.posts = [...this.posts, ...res.data.data];
            }
          })
          .catch((err) => this.$error(err))
          .finally(() => {
            this.loading = false;
          });
      }
    },

    // 删除帖子
    deletePostEventHandler(index) {
      this.posts.splice(index, 1);
    },
  },
};
</script>

<style scoped>
.index {
  background-color: rgb(230, 230, 230);
  min-height: 100vh;
}
.van-nav-bar {
  box-shadow: 0 2px 3px -1px rgb(221, 218, 218);
}
.submitIcon {
  position: fixed;
  bottom: 70px;
  right: 14px;
  background-color: red;
  padding: 1rem;
  border-radius: 50%;
}
</style>
