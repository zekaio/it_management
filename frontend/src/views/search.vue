<template>
  <div class="search">
    <!-- 搜索框 -->
    <form action="/">
      <van-search
        v-model="keyword"
        :placeholder="placeholderText"
        show-action
        @search="getPosts"
      >
        <template #left>
          <van-icon
            name="arrow-left"
            size="18"
            @click="$back()"
            color="black"
          />
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
  name: 'Search',
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
      if (this.keyword === '') {
        Toast.fail({ message: '关键词不能为空' });
        return;
      }
      let timeout = setTimeout(() => {
        Toast.fail({
          message: '请求超时，请重试',
        });
        return;
      }, 10000);

      apis
        .getPosts({
          username: this.$route.query.username,
          keyword: this.keyword,
        })
        .then((res) => {
          this.posts = res.data.data;
          this.refreshing = false;
          if (res.data.data.length == 0) {
            this.finished = true;
          } else {
            this.finished = false;
          }
          clearTimeout(timeout);
        })
        .catch((err) => this.$error(err));
    },

    // 加载帖子
    getPosts() {
      if (this.keyword === '') {
        Toast.fail({ message: '关键词不能为空' });
        return;
      }

      if (this.posts.length == 0) {
        apis
          .getPosts({
            username: this.$route.query.username,
            keyword: this.keyword,
          })
          .then((res) => {
            this.posts = res.data.data;
            if (res.data.data.length == 0) {
              this.finished = true;
            }
            this.loading = false;
          })
          .catch((err) => this.$error(err));
      } else {
        apis
          .getPosts(
            { username: this.$route.query.username, keyword: this.keyword },
            this.posts[this.posts.length - 1].post_id
          )
          .then((res) => {
            if (res.data.data.length == 0) {
              this.finished = true;
            } else {
              this.posts = [...this.posts, ...res.data.data];
            }
            this.loading = false;
          })
          .catch((err) => this.$error(err));
      }
    },

    // 删除帖子
    deletePostEventHandler(index) {
      this.posts.splice(index, 1);
    },
  },

  computed: {
    placeholderText: function() {
      return this.$route.query.username === undefined
        ? '请输入搜索关键词'
        : '搜索Ta的帖子';
    },
  },
};
</script>
