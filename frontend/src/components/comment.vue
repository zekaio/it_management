<template>
  <div
    class="comment"
    style="margin:2px 1rem; max-height=40vh; padding-bottom: 8px"
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
        >
          <template v-slot:loading>
            <van-loading type="spinner" size="20" />
          </template>
        </van-image>
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
    <div class="comment_content" @click="replyComment">
      <span v-if="comment.type && comment.parent_id !== comment.root_id">
        回复<span
          style=" color: #1E90FF;"
          @click="$goTo(`/user?username=${comment.parent_user_info.username}`)"
        >
          @{{ comment.parent_user_info.username }} </span
        >:
      </span>
      <span>{{ comment.content }}</span>
      <!-- 图片 -->
      <span
        style=" color: #1E90FF; margin-left:8px;"
        v-if="comment.img_name"
        @click="previewImage($event, commentImageDir + comment.img_name)"
        >查看图片</span
      >
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
import { Dialog, Toast, ImagePreview } from 'vant';

import { apis } from '../api/apis';
import { avatarDir, commentImageDir } from '../config';

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
      commentImageDir,
      actions: [{ name: '编辑' }, { name: '删除', color: '#ee0a24' }],
    };
  },

  methods: {
    // 显示动作面板
    showActionSheet() {
      this.actionSheetShow = true;
      this.$emit('hideInputEvent', true);
    },

    // 处理动作面板选择
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

    // 关闭动作面板
    onClosed() {
      this.$emit('hideInputEvent', false);
    },

    replyComment() {
      this.$emit('replyCommentEvent', this.index);
    },

    // 预览图片
    previewImage(e, img_url) {
      e.stopPropagation();
      e.preventDefault();
      ImagePreview({ images: [img_url], showIndex: false });
    },
  },

  computed: {
    isOwner() {
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
  margin-left: 1rem;
  display: inline-block;
  vertical-align: middle;
}
</style>
