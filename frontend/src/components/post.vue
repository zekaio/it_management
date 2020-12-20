<template>
  <div class="post">
    <!-- 用户信息 -->
    <van-cell center>
      <template #title>
        <van-image
          round
          width="2.5rem"
          height="2.5rem"
          :src="avatarDir + post.avatar"
          class="post_cell_title_image"
          @click="$goTo(`/user?username=${post.username}`)"
        >
          <template v-slot:loading>
            <van-loading type="spinner" size="20" />
          </template>
        </van-image>
        <span class="post_cell_title_text">
          {{ post.username }}
          <br />
          <span style="color: #708090;">
            {{ post.created_at }}
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

    <!-- 帖子内容 -->
    <div
      class="content"
      @click="toDetail"
      style="margin:2px 16px; max-height=40vh"
    >
      {{ post.content }}
    </div>

    <!-- 底部导航 -->
    <van-goods-action style="position: relative;">
      <van-goods-action-icon
        style="margin: auto;"
        icon="chat-o"
        :text="commentsNum"
        @click="toDetail"
      />
    </van-goods-action>

    <!-- 弹出层 -->
    <van-action-sheet
      v-model="actionSheetShow"
      :actions="actions"
      @select="onSelect"
      cancel-text="取消"
      close-on-popstate
      round
    />
  </div>
</template>

<script>
import { Dialog, Toast } from 'vant';
import { apis } from '../api/apis';
import { avatarDir } from '../config';

export default {
  name: 'Post',
  props: {
    post: Object,
    index: Number,
  },
  data() {
    return {
      actionSheetShow: false,
      actions: [{ name: '编辑' }, { name: '删除', color: '#ee0a24' }],
      avatarDir,
    };
  },
  methods: {
    // 查看帖子详情
    toDetail() {
      this.$router.push({
        path: `/post/${this.post.post_id}/detail`,
      });
    },

    // 显示动作面板
    showActionSheet() {
      this.actionSheetShow = true;
    },

    // 处理动作面板选择
    onSelect(item) {
      this.actionSheetShow = false;
      if (item.name == '编辑') {
        this.$router.push({
          path: `/post/${this.post.post_id}/edit`,
        });
      } else if (item.name == '删除') {
        Dialog.confirm({
          message: '确认要删除吗？',
        }).then(() => {
          apis
            .deletePost(this.post.post_id)
            .then(() => {
              Toast.success({ message: '删除成功' });
              this.$emit('deletePostEvent', this.index);
            })
            .catch((err) => this.$error(err));
        });
      }
    },
  },

  computed: {
    isOwner: function() {
      return localStorage.getItem('uuid') === this.post.uuid;
    },

    commentsNum: function() {
      return this.post.comments_num + '';
    },
  },
};
</script>

<style scoped>
.post {
  margin-top: 10px;
  background-color: white;
}

.post_cell_title_image {
  vertical-align: middle;
}
.post_cell_title_text {
  margin-left: 2vw;
  display: inline-block;
  vertical-align: middle;
}
</style>
