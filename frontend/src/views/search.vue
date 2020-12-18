<template>
  <div class="search">
    <!-- 搜索框 -->
    <form action="/">
      <van-search
        v-model="keyword"
        placeholder="请输入搜索关键词"
        show-action
        @search="getPosts"
      >
        <template #left>
          <van-icon name="arrow-left" @click="back" />
        </template>
        <template #action>
          <div @click="getPosts">搜索</div>
        </template>
      </van-search>
    </form>

    <!-- 帖子 -->
    <van-pull-refresh v-model="refreshing" @refresh="refresh">
      <van-list
        v-model="loading"
        :finished="finished"
        finished-text="没有更多了"
        @load="getPosts"
        :immediate-check="false"
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
  </div>
</template>

<script>
import { Toast } from 'vant';
import { apis } from '../api/apis';
import Post from '../components/Post';
export default {
  data() {
    return {
      keyword: '',
      posts: [],
      loading: false, // list是否在加载
      finished: false, // list是否完全加载
      refreshing: false, // 上拉刷新
    };
  },
  components: { Post },

  methods: {
    // 刷新
    refresh() {
      let timeout = setTimeout(() => {
        Toast.fail({
          message: '请求超时，请重试',
        });
        return;
      }, 10000);
      apis.searchPost(this.keyword).then((res) => {
        this.posts = res.data.data;
        this.refreshing = false;
        if (res.data.data.length == 0) {
          this.finished = true;
        } else {
          this.finished = false;
        }
        clearTimeout(timeout);
      });
    },

    getPosts() {
      if (this.keyword === '') {
        Toast.fail({ message: '关键词不能为空' });
        return;
      }
      if (this.posts.length == 0) {
        apis.searchPost(this.keyword).then((res) => {
          this.posts = res.data.data;
          if (res.data.data.length == 0) {
            this.finished = true;
          }
          this.loading = false;
        });
      } else {
        apis
          .searchPost(this.keyword, this.posts[this.posts.length - 1].post_id)
          .then((res) => {
            if (res.data.data.length == 0) {
              this.finished = true;
            } else {
              this.posts = [...this.posts, ...res.data.data];
            }
            this.loading = false;
          });
      }
    },

    // 删除帖子
    deletePostEventHandler(index) {
      this.posts.splice(index, 1);
    },

    back() {
      this.$router.back();
    },
  },
};
</script>

<style scoped></style>
