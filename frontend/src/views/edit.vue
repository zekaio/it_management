<template>
  <div class="edit">
    <van-nav-bar
      :title="$route.params.postId ? '编辑帖子' : '发表帖子'"
      left-arrow
      @click-left="onClickLeft"
      placeholder
      fixed
      z-index="100"
      style="margin-bottom: 10px;"
    >
      <template #right>
        <van-button style="height: 80%" type="info" @click="submit()">
          {{ $route.params.postId ? '修改' : '发表' }}
        </van-button>
      </template>
    </van-nav-bar>

    <van-field
      v-model="message"
      rows="10"
      autosize
      type="textarea"
      placeholder="请输入内容"
      maxlength="120"
      show-word-limit
    />
  </div>
</template>

<script>
import { Toast } from 'vant';
import { apis } from '../api/apis';
export default {
  data() {
    return {
      message: '',
    };
  },
  methods: {
    onClickLeft() {
      this.$router.back();
    },

    submit() {
      (() => {
        return this.$route.params.postId
          ? apis.updatePost(this.$route.params.postId, this.message)
          : apis.savePost(this.message);
      })()
        .then(() => {
          Toast({
            message: `${this.$route.params.postId ? '修改' : '发表'}成功`,
          });
          this.message = '';
          this.$router.push({
            path: '/index',
          });
        })
        .catch((err) => {
          Toast.fail({
            message:
              err.response.data.message || `未知错误${err.response.data}`,
          });
        });
    },
  },

  async mounted() {
    if (this.$route.params.postId) {
      apis.getPost(this.$route.params.postId).then((res) => {
        this.message = res.data.data.content;
      });
    }
  },
};
</script>

<style scoped>
.edit {
  min-height: 100vh;
}
</style>
