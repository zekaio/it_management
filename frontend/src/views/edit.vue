<template>
  <div class="edit">
    <div>编辑页面</div>
    <div>
      帖子id：{{ $route.params.post_id ? $route.params.post_id : '新帖子' }}
    </div>
    <van-field
      v-model="message"
      rows="1"
      autosize
      type="textarea"
      placeholder="请输入内容"
      maxlength="120"
      show-word-limit
    />
    <van-button type="info" @click="submit">发表</van-button>
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
    submit() {
      apis.savePost(this.message).then(res => {
        Toast({
          message: `发表成功，id为${res.data.data.post_id}`,
        });
        this.message = '';
        this.$router.push({
          path: '/index',
        });
      });
    },
  },
};
</script>

<style scoped>
.edit {
  min-height: 100vh;
}
</style>
