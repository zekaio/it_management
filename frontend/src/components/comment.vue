<template>
  <div
    class="comment van-hairline--bottom"
    style="margin:2px 16px; max-height=40vh; padding-bottom: 8px"
  >
    <!-- 用户信息 -->
    <van-cell
      :title="comment.username"
      :label="comment.created_at"
      size="small"
      :border="false"
    >
      <template #right-icon>
        <van-icon
          name="arrow-down"
          @click="showActionSheet"
          v-show="isOwner"
          style="font-size: 16px; line-height: inherit; margin:auto 0;"
        />
      </template>
    </van-cell>

    <!-- 评论内容 -->
    <div class="comment_content">
      {{ comment.content }}
    </div>

    <!-- 弹出层 -->
    <van-action-sheet
      v-model="actionSheetShow"
      :actions="actions"
      @select="onSelect"
      cancel-text="取消"
      close-on-popstate
      round
      style="z-index:20000"
    />
  </div>
</template>

<script>
import { Dialog, Toast } from 'vant';
import { apis } from '../api/apis';
export default {
  name: 'Comment',

  props: {
    comment: Object,
    index: Number,
  },

  data() {
    return {
      actionSheetShow: false,
      actions: [{ name: '编辑' }, { name: '删除', color: '#ee0a24' }],
    };
  },

  methods: {
    showActionSheet() {
      this.actionSheetShow = true;
    },

    onSelect(item) {
      this.actionSheetShow = false;
      if (item.name == '编辑') {
        this.$emit('editCommentEvent', this.index);
      } else if (item.name == '删除') {
        Dialog.confirm({
          message: '确认要删除吗？',
        }).then(() => {
          apis.deleteComment(this.comment.comment_id).then(() => {
            Toast.success({ message: '删除成功' });
            this.$emit('deleteCommentEvent', this.index);
          });
        });
      }
    },
  },

  computed: {
    isOwner: function() {
      return localStorage.getItem('uuid') == this.comment.uuid;
    },
  },
};
</script>

<style scoped>
.comment_content {
  margin: 0 16px;
}
</style>
