<template>
  <div class="comment">
    <!-- 用户信息 -->
    <van-cell
      :title="comment.username"
      :label="comment.created_at"
      size="small"
    />
    <div class="comment_content">{{ comment.content }}</div>
  </div>
</template>

<script>
export default {
  name: 'Comment',
  props: {
    comment: Object,
    index: Number,
  },
  data() {
    return {};
  },
  methods: {},
  async mounted() {},
};
</script>

<style scoped>
.comment_content {
  margin: 0 16px;
}
</style>
