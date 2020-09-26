<template>
  <div class="post">
    <van-cell :title="post.username" :label="post.created_at">
      <template #right-icon>
        <van-icon
          name="arrow-down"
          @click="showActionSheet"
          v-show="isOwner"
          style="font-size: 16px; line-height: inherit; margin:auto 0;"
        />
      </template>
    </van-cell>
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
        :text="comments_num"
        @click="toDetail"
      />
    </van-goods-action>

    <!-- // 弹出层
    <van-popup
      v-model="popupShow"
      position="bottom"
      round
      :style="{ height: '30%' }"
    ></van-popup> -->
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
    };
  },
  methods: {
    toDetail() {
      this.$router.push({
        path: `/post/${this.post.post_id}/detail`,
      });
    },

    showActionSheet() {
      this.actionSheetShow = true;
      console.log('显示');
      //   this.$router.push({});
    },

    onSelect(item) {
      this.actionSheetShow = false;
      if (item.name == '编辑') {
        this.$router.push({
          path: `/post/${this.post.post_id}/edit`,
        });
        console.log('编辑');
      } else if (item.name == '删除') {
        Dialog.confirm({
          message: '确认要删除吗？',
        })
          .then(() => {
            apis.deletePost(this.post.post_id).then(() => {
              Toast.success({ message: '删除成功' });
              this.$emit('deletePostEvent', this.index);
            });
            console.log('删除');
          })
          .catch(() => {
            console.log('取消');
          });
      }
      console.log(item);
    },
  },
  computed: {
    isOwner: function() {
      return localStorage.getItem('uuid') == this.post.uuid;
    },
    comments_num: function() {
      return this.post.comments_num + '';
    },
  },
};
</script>

<style scoped>
.post {
  /* max-height: 50vh; */
  margin-top: 10px;
  background-color: white;
}
/* .icon {
} */
</style>
