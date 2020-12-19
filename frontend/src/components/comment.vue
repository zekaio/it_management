<template>
  <div
    class="comment van-hairline--bottom"
    style="margin:2px 16px; max-height=40vh; padding-bottom: 8px"
  >
    <!-- 用户信息 -->
    <van-cell size="small" :border="false">
      <template #title>
        <van-image
          round
          width="2.5rem"
          height="2.5rem"
          :src="avatarDir + comment.avatar"
          class="comment_cell_title_image"
          @click="$goTo(`/user?username=${comment.username}`)"
        />
        <span class="comment_cell_title_text">
          {{ comment.username }}
          <br />
          <span style="color: #708090;">
            {{ comment.created_at }}
          </span>
        </span>
      </template>
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
      @closed="onClosed"
    />
  </div>
</template>

<script>
import { Dialog, Toast } from 'vant';
import { apis } from '../api/apis';
import { avatarDir } from '../config';
export default {
  name: 'Comment',

  props: {
    comment: Object,
    index: Number,
  },

  data() {
    return {
      actionSheetShow: false,
      avatarDir,
      actions: [{ name: '编辑' }, { name: '删除', color: '#ee0a24' }],
    };
  },

  methods: {
    showActionSheet() {
      console.log(this.comment.avatar);
      this.actionSheetShow = true;
      this.$emit('hideInputEvent', true);
    },

    onSelect(item) {
      this.actionSheetShow = false;
      if (item.name == '编辑') {
        this.$emit('editCommentEvent', this.index);
      } else if (item.name == '删除') {
        Dialog.confirm({
          message: '确认要删除吗？',
        }).then(() => {
          apis
            .deleteComment(this.comment.comment_id)
            .then(() => {
              Toast.success({ message: '删除成功' });
              this.$emit('deleteCommentEvent', this.index);
            })
            .catch((err) => this.$error(err));
        });
      }
    },

    onClosed() {
      this.$emit('hideInputEvent', false);
    },
  },

  computed: {
    isOwner: function() {
      return localStorage.getItem('uuid') === this.comment.uuid;
    },
  },
};
</script>

<style scoped>
.comment_content {
  margin: 0 16px;
}
.comment_cell_title_image {
  vertical-align: middle;
}
.comment_cell_title_text {
  margin-left: 2vw;
  display: inline-block;
  vertical-align: middle;
}
</style>
