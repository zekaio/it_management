<template>
  <div class="index">
    <!-- 顶部导航栏 -->
    <van-nav-bar
      title="主页"
      @click-right="goTo('search')"
      fixed
      placeholder
      z-index="100"
    >
      <template #right>
        <van-icon name="search" size="18" />
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
          <Post :post="post" :index="index" @deletePostEvent="deletePost" />
        </div>
      </van-list>
    </van-pull-refresh>

    <!-- 底部导航栏 -->
    <van-tabbar v-model="active" placeholder>
      <van-tabbar-item icon="home-o" @click="refresh"></van-tabbar-item>
      <van-tabbar-item to="user" icon="user-o"> </van-tabbar-item>
    </van-tabbar>

    <!-- 发表帖子 -->
    <van-icon
      name="add"
      color="red"
      style="position: fixed; bottom: 80px; right: 10px; background-color: white; border-radius: 50%"
      size="60px"
      @click="goTo('/post/edit')"
    />
  </div>
</template>

<script>
import Post from '../components/post';
import { apis } from '../api/apis';
import { Toast } from 'vant';
export default {
  name: 'index',
  components: { Post },
  data() {
    return {
      active: 0, // 底部导航栏活动位置

      loading: false, // list是否在加载
      finished: false, // list是否完全加载
      refreshing: false, // 上拉刷新

      count: 0, // post数量

      posts: [], // 帖子

      post: {
        post_id: '12',
        username: 'username',
        uuid: '33a1a7e2-c88f-41c4-90b6-7ab245bf5b03',
        content: '这是帖子内容',
        comments_num: '100',
        created_at: '2019-10-20',
        // "comments": [
        //     {
        //         "comment_id": "评论id",
        //         "parent_id": "被评论的帖子或评论的id",
        //         "type": "是什么的评论，0是帖子，1是评论",
        //         "content": "评论内容",
        //         "comments_num": "评论数目",
        //         "username": "发帖人用户名",
        //         "uuid": "发帖人uuid"
        //     }
        // ]
      },
    };
  },

  methods: {
    // 刷新
    refresh() {
      console.log('刷新');
      let timeout = setTimeout(() => {
        Toast.fail({
          message: '请求超时，请重试',
        });
        return;
      }, 10000);
      apis.getPosts().then(res => {
        console.log(res);
        this.posts = res.data.data;
        console.log(this.posts);
        this.refreshing = false;
        console.log('刷新完成');
        this.finished = false;
        clearTimeout(timeout);
      });
    },

    // 跳转页面
    goTo(path) {
      this.$router.push({
        path,
      });
    },
    // 获取更多帖子
    getPosts() {
      if (this.posts.length == 0) {
        apis.getPosts().then(res => {
          console.log(res);
          this.posts = res.data.data;
          console.log(this.posts);
          this.loading = false;
          console.log('刷新完成');
        });
      } else {
        console.log('加载新帖子');
        apis.getPosts(this.posts[this.posts.length - 1].post_id).then(res => {
          console.log(res);
          if (res.data.data.length == 0) {
            this.finished = true;
          } else {
            this.posts = [...this.posts, ...res.data.data];
          }
          this.loading = false;
          console.log('获取完成');
        });
      }

      // setTimeout(() => {
      //   this.count = this.count + 5;
      //   console.log(this.count);
      // }, 1000);
    },
    deletePost(index) {
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
</style>
