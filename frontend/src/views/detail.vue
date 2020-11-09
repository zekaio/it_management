<template>
  <div class="detail">
    <!-- 顶部导航栏 -->
    <van-nav-bar
      :title="post.username"
      left-arrow
      @click-left="onClickLeft"
      placeholder
      fixed
      z-index="100"
      style="margin-bottom: 10px"
    ></van-nav-bar>
    <!-- 帖子不存在占位符 -->
    <van-empty description="帖子不存在" v-if="showEmpty"></van-empty>
    <div v-else>
      <!-- <div>{{ post.content }}</div> -->

      <div>
        {{ post.content }}
      </div>
    </div>
  </div>
</template>

<script>
import { apis } from '../api/apis';
import { Toast } from 'vant';
export default {
  name: 'detail',
  data() {
    return {
      post: {},

      showEmpty: false,
    };
  },
  methods: {
    onClickLeft() {
      this.$router.back();
    },
  },
  async mounted() {
    apis
      .getPost(this.$route.params.postId)
      .then((res) => {
        this.post = res.data.data;
      })
      .catch((err) => {
        if (err.response.status === 404) {
          this.showEmpty = true;
        }

        Toast.fail({
          message: err.response.data.message || `未知错误${err.response.data}`,
        });
      });
  },
};
</script>

<style scoped></style>
