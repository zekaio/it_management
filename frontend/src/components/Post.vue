<template>
  <div class="post">
    <!-- 用户信息 -->
    <van-cell center :size="large">
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
      <template #right-icon v-if="!detail">
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
      style="margin:4px 16px; max-height=40vh"
    >
      <!-- 文字 -->
      <div>{{ post.content }}</div>

      <!-- 图片 -->
      <div v-if="post.imgs_name && post.imgs_name.length >= 2">
        <van-grid
          :border="false"
          square
          gutter="4"
          :column-num="post.imgs_name.length >= 3 ? 3 : post.imgs_name.length"
        >
          <van-grid-item
            v-for="(img_name, index) in post.imgs_name"
            :key="index"
          >
            <van-image
              :src="postImageDir + img_name"
              fit="cover"
              @click="previewImage($event, postImageDir + img_name)"
            >
              <template v-slot:loading>
                <van-loading type="spinner" size="20" />
              </template>
              <template v-slot:error>
                <van-image
                  style="display:inline-block"
                  :class="img_class"
                  @click="previewImage($event, errorImage)"
                  :src="errorImage"
                ></van-image>
              </template>
            </van-image>
          </van-grid-item>
        </van-grid>
      </div>

      <div v-if="post.imgs_name && post.imgs_name.length === 1">
        <van-image
          :src="postImageDir + post.imgs_name[0]"
          fit="cover"
          class="post_imgs_one"
          @click="previewImage($event, postImageDir + post.imgs_name[0])"
        >
          <template v-slot:loading>
            <van-loading type="spinner" size="20" />
          </template>
          <template v-slot:error>
            <van-image
              style="display:inline-block; justify-content: flex-start; flex-direction: row;"
              :class="img_class"
              @click="previewImage($event, errorImage)"
              :src="errorImage"
            ></van-image>
          </template>
        </van-image>
      </div>
    </div>

    <!-- 底部导航 -->
    <van-goods-action style="position: relative;" v-if="!detail">
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
import { Dialog, ImagePreview, Toast } from 'vant';

import { apis } from '../api/apis';
import { avatarDir, postImageDir, errorImage } from '../config';

export default {
  name: 'Post',

  props: {
    post: Object,
    index: { type: Number, default: 0 },
    large: { type: String, default: '' },
    detail: { type: Boolean, default: false },
  },

  data() {
    return {
      actionSheetShow: false,
      actions: [{ name: '编辑' }, { name: '删除', color: '#ee0a24' }],
      avatarDir,
      postImageDir,
      errorImage,
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

    // 预览图片
    previewImage(e, img_url) {
      e.stopPropagation();
      e.preventDefault();
      ImagePreview({ images: [img_url], showIndex: false });
    },
  },

  computed: {
    isOwner() {
      return localStorage.getItem('uuid') === this.post.uuid;
    },

    commentsNum() {
      return this.post.comments_num + '';
    },

    img_class() {
      if (!this.post.imgs_name) return '';
      switch (this.post.imgs_name.length) {
        case 0:
          return '';
        case 1:
          return 'post_imgs_one';
        case 2:
          return 'post_imgs_two';
        default:
          return 'post_imgs_multiple';
      }
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
.post_imgs {
  display: flex;
  display: -webkit-flex;
  flex-direction: row;
  justify-content: center;
  margin-right: -3px;
  margin-top: 8px;
}
.post_imgs_one {
  margin-right: 3px;
  justify-content: flex-start;
  width: 70%;
}
.post_imgs_two {
  width: 100%;
  margin-right: 3px;
}
.post_imgs_multiple {
  margin-right: 3px;
  width: 100%;
}
</style>

<style>
.post_imgs > div > div > .van-image__error {
  position: relative;
  flex-direction: row;
  justify-content: flex-start;
}
</style>
