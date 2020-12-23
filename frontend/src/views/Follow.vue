<template>
  <div class="follow">
    <!-- 顶部导航栏 -->
    <van-nav-bar
      :title="isFollow ? '关注' : '粉丝'"
      fixed
      placeholder
      style="margin-bottom: 10px;"
      z-index="100"
    >
      <!-- 返回箭头 -->
      <template #left>
        <van-icon name="arrow-left" size="18" color="black" @click="$back()" />
      </template>
    </van-nav-bar>

    <!-- 用户列表 -->
    <van-pull-refresh v-model="refreshing" @refresh="refresh">
      <van-list
        v-model="loading"
        :finished="finished"
        finished-text="没有更多了"
        @load="getUsers"
      >
        <div v-for="(user, index) in users" :key="index">
          <User
            :avatar="isFollow ? user.followed_user_avatar : user.user_avatar"
            :username="
              isFollow ? user.followed_user_username : user.user_username
            "
            :description="
              isFollow ? user.followed_user_description : user.user_description
            "
            :followed="user.followed"
            :index="index"
            @followEvent="followEventHandler"
          />
        </div>
      </van-list>
    </van-pull-refresh>
  </div>
</template>

<script>
import { Toast } from 'vant';

import { apis } from '../api/apis';

import User from '../components/User';

export default {
  name: 'Follow',

  components: { User },

  data() {
    return {
      loading: false, // list是否在加载
      finished: false, // list是否完全加载
      refreshing: false, // 上拉刷新
      users: [],
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

      let queryMethod = this.isFollow ? apis.getFollowList : apis.getFansList;
      queryMethod({ username: this.username })
        .then((res) => {
          this.users = res.data.data;
          if (res.data.data.length < 20) {
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

    // 获取用户信息
    getUsers() {
      let queryMethod = this.isFollow ? apis.getFollowList : apis.getFansList;
      if (this.users.length === 0) {
        queryMethod({ username: this.username })
          .then((res) => {
            this.users = res.data.data;
            if (res.data.data.length < 20) {
              this.finished = true;
            }
          })
          .catch((err) => this.$error(err))
          .finally(() => {
            this.loading = false;
          });
      } else {
        queryMethod(
          { username: this.username },
          this.users[this.users.length - 1].follow_id
        )
          .then((res) => {
            if (res.data.data.length < 20) {
              this.finished = true;
            } else {
              this.users = [...this.users, ...res.data.data];
            }
          })
          .catch((err) => this.$error(err))
          .finally(() => {
            this.loading = false;
          });
      }
    },

    // 处理关注或取关事件
    followEventHandler(index) {
      apis
        .followUser(
          this.isFollow
            ? this.users[index].followed_user_username
            : this.users[index].user_username,
          !this.users[index].followed
        )
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
    // 页面类型，关注还是粉丝
    type() {
      return this.$route.query.type;
    },

    // 对应用户的用户名
    username() {
      return this.$route.query.username;
    },

    // 当前页面是否是关注
    isFollow() {
      return this.type === 'follow';
    },
  },
};
</script>

<style scoped></style>
