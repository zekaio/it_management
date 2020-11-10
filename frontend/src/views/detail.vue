<template>
  <div class="detail">
    <div v-show="!showComment">
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
        <!-- 用户信息 -->
        <van-cell
          :title="post.username"
          :label="post.created_at"
          size="large"
        />
        <!-- 帖子内容 -->
        <div class="detail_content">
          {{ post.content }}
        </div>
        <van-sticky :offset-top="46">
          <van-tabs v-model="tabActivate">
            <van-tab :title="'评论  ' + post.comments_num"></van-tab>
            <van-tab title="" disabled></van-tab>
            <van-tab title="" disabled></van-tab>
            <van-tab title="" disabled></van-tab> </van-tabs
        ></van-sticky>
        <div v-for="(comment, index) in comments" :key="index">
          <Comment :comment="comment" :index="index"></Comment>
        </div>
        <!-- <Comment :comment="comments[0]"></Comment> -->
        <!-- 输入框 -->
        <div class="detail_placeholder">
          <div class="detail_bar" @click="showComment = true">
            <div class="detail_input">
              <div class="detail_input_placeholder">
                <span class="detail_input_text">点击发表评论</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 评论页 -->
    <div v-show="showComment" class="detail_comment">
      <!-- <div> -->
      <van-nav-bar
        title="发表评论"
        left-arrow
        @click-left="showComment = false"
        placeholder
        fixed
        z-index="100"
        style="margin-bottom: 10px; height: 46px"
      >
        <template #right>
          <van-button style="height: 80%" type="info" @click="submitComment()"
            >发表</van-button
          >

          <!-- <van-icon name="search" size="18" /> -->
        </template></van-nav-bar
      >
      <!-- </div> -->
      <div class="detail_comment_container">
        <van-field
          v-model="commentText"
          rows="10"
          autosize
          type="textarea"
          placeholder="请输入内容"
          maxlength="120"
          show-word-limit
        />
      </div>
    </div>
    <!-- <van-goods-action style="position: relative;">
        <van-goods-action-icon
          style="margin: auto;"
          icon="chat-o"
          :text="commentsNum"
          @click="toDetail"
        />
      </van-goods-action> -->
  </div>
</template>

<script>
import { apis } from '../api/apis';
import { Toast } from 'vant';
import Comment from '../components/comment';

export default {
  name: 'detail',
  components: { Comment },
  data() {
    return {
      post: {},
      showEmpty: false,
      tabActivate: 0,
      showComment: false,
      commentText: '',
      comments: [],
    };
  },
  methods: {
    onClickLeft() {
      this.$router.back();
    },
    getComment() {
      apis
        .getComments(
          this.post.post_id,
          0,
          this.comments.length
            ? this.comment[this.comments.length - 1].comment_id
            : 0,
        )
        .then((res) => {
          // console.log(res.data.data);
          // this.comments = res.data.data;
          this.comments = [...this.comments, ...res.data.data.comments];
          // console.log(this.comments);
        });
    },
    submitComment() {
      apis
        .saveComment(this.post.post_id, 0, this.commentText)
        .then(() => {
          Toast.success({ message: '发表成功' });
          this.commentText = '';
          this.showComment = false;
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
    apis
      .getPost(this.$route.params.postId)
      .then((res) => {
        this.post = res.data.data;
        this.getComment();
        console.log(this.comments);
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

<style scoped>
.detail_content {
  padding: 5px 40px;
}
.detail_placeholder {
  height: 54px;
}
.detail_bar {
  position: fixed;
  z-index: 11000;
  bottom: 0;
  left: 0;
  right: 0;
  width: 100%;
  height: auto;
}
.detail_input {
  display: flex;
  box-sizing: content-box;
  align-items: center;
  height: 54px;
  width: 100%;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: env(safe-area-inset-bottom);
  background-color: #fff;
  border-bottom: none !important;
}
.detail_input_placeholder {
  height: 54px;
  border-radius: 4px;
  flex: 1;
  height: 36px;
  margin: 0 13px;
  background-color: #f6f6f6;
}
.detail_input_text {
  line-height: 36px;
  margin-left: 10px;
  font-size: 14px;
  color: #999;
  letter-spacing: 0;
}
/* .detail_comment {
  min-height: 100vh;
  position: fixed;
  width: 100vw;
  top: 0;
  left: 0;
  z-index: 100000;
} */
/* .detail_comment_container {
  position: relative;
} */
</style>
