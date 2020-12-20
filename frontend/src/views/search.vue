<template>
  <div class="search">
    <!-- 搜索框 -->
    <form action="/">
      <van-search
        v-model="keyword"
        :placeholder="placeholderText"
        show-action
        @search="search"
        @input="searched = false"
        autofocus
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
          <div @click="search">搜索</div>
        </template>
      </van-search>
    </form>

    <!-- tabs -->
    <van-sticky>
      <van-tabs v-model="tabActivate">
        <van-tab title="帖子"></van-tab>
        <van-tab
          :title="this.$route.query.username === undefined ? '用户' : ''"
          :disabled="this.$route.query.username !== undefined"
        ></van-tab>
        <van-tab title="" disabled></van-tab>
        <van-tab title="" disabled></van-tab>
      </van-tabs>
    </van-sticky>

    <div v-show="searched">
      <!-- 帖子 -->
      <div v-show="tabActivate === 0">
        <van-pull-refresh v-model="postRefreshing" @refresh="refreshPosts">
          <van-list
            v-model="postLoading"
            :finished="postFinished"
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

      <!-- 用户 -->
      <div v-show="tabActivate === 1">
        <van-pull-refresh v-model="userRefreshing" @refresh="refreshUsers">
          <van-list
            v-model="userLoading"
            :finished="userFinished"
            finished-text="没有更多了"
            @load="getUsers"
            :immediate-check="false"
          >
            <div v-for="(user, index) in users" :key="index">
              <User
                :avatar="user.avatar"
                :username="user.username"
                :description="user.description"
                :followed="user.followed"
                :index="index"
                @followEvent="followEventHandler"
              />
            </div>
          </van-list>
        </van-pull-refresh>
      </div>
    </div>
  </div>
</template>

<script>
import { Toast } from 'vant';
import { apis } from '../api/apis';
import Post from '../components/Post';
import User from '../components/User';

export default {
  name: 'Search',
  data() {
    return {
      keyword: '',
      tabActivate: 0,
      searched: false,

      posts: [],
      postLoading: false, // list是否在加载
      postFinished: false, // list是否完全加载
      postRefreshing: false, // 上拉刷新

      users: [],
      userLoading: false,
      userFinished: false,
      userRefreshing: false,
    };
  },
  components: { Post, User },
  methods: {
    // 搜索
    async search() {
      if (this.keyword === '') {
        Toast.fail({ message: '关键词不能为空' });
        return;
      }
      this.refreshPosts();
      this.refreshUsers();
      this.searched = true;
    },

    // 刷新帖子
    refreshPosts() {
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
          if (res.data.data.length == 0) {
            this.postFinished = true;
          } else {
            this.postFinished = false;
          }
        })
        .catch((err) => this.$error(err))
        .finally(() => {
          clearTimeout(timeout);
        });
      this.postRefreshing = false;
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
              this.postFinished = true;
            }
          })
          .catch((err) => this.$error(err))
          .finally(() => {
            this.postLoading = false;
          });
      } else {
        apis
          .getPosts(
            { username: this.$route.query.username, keyword: this.keyword },
            this.posts[this.posts.length - 1].post_id
          )
          .then((res) => {
            if (res.data.data.length == 0) {
              this.postFinished = true;
            } else {
              this.posts = [...this.posts, ...res.data.data];
            }
          })
          .catch((err) => this.$error(err))
          .finally(() => {
            this.postLoading = false;
          });
      }
    },

    // 删除帖子
    deletePostEventHandler(index) {
      this.posts.splice(index, 1);
    },

    // 刷新用户信息
    refreshUsers() {
      let timeout = setTimeout(() => {
        Toast.fail({
          message: '请求超时，请重试',
        });
        return;
      }, 10000);

      apis
        .searchUsers(this.keyword)
        .then((res) => {
          this.users = res.data.data;
          if (res.data.data.length === 0) {
            this.userFinished = true;
          } else {
            this.userFinished = false;
          }
        })
        .catch((err) => this.$error(err))
        .finally(() => {
          clearTimeout(timeout);
        });
      this.userRefreshing = false;
    },

    // 加载用户信息
    getUsers() {
      if (this.keyword === '') {
        Toast.fail({ message: '关键词不能为空' });
        return;
      }

      if (this.users.length == 0) {
        apis
          .searchUsers(this.keyword)
          .then((res) => {
            this.users = res.data.data;
            if (res.data.data.length === 0) {
              this.userFinished = true;
            }
          })
          .catch((err) => this.$error(err))
          .finally(() => {
            this.userLoading = false;
          });
      } else {
        apis
          .searchUsers(this.keyword, this.users[this.users.length - 1].uuid)
          .then((res) => {
            if (res.data.data.length === 0) {
              this.userFinished = true;
            } else {
              this.users = [...this.users, ...res.data.data];
            }
          })
          .catch((err) => this.$error(err))
          .finally(() => {
            this.userLoading = false;
          });
      }
    },

    // 处理关注和取关事件
    followEventHandler(index) {
      apis
        .followUser(this.users[index].username, !this.users[index].followed)
        .then(() => {
          this.users[index].followed = !this.users[index].followed;
          Toast.success({
            message: `${this.users[index].followed ? '' : '取消'}关注成功`,
          });
        })
        .catch((err) => this.$error(err));
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
