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

      <!-- 帖子存在 -->
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

        <!-- tabs -->
        <van-sticky :offset-top="46">
          <van-tabs v-model="tabActivate">
            <van-tab :title="'评论 ' + post.comments_num"></van-tab>
            <van-tab title="" disabled></van-tab>
            <van-tab title="" disabled></van-tab>
            <van-tab title="" disabled></van-tab>
          </van-tabs>
        </van-sticky>

        <!-- 评论 -->
        <div v-show="tabActivate === 0">
          <van-pull-refresh
            v-model="refreshing"
            @refresh="refresh"
            :disabled="tabActivate !== 0"
          >
            <van-list
              v-model="loading"
              :finished="finished"
              finished-text="没有更多了"
              @load="getComments"
            >
              <div v-for="(comment, index) in comments" :key="index">
                <Comment
                  :comment="comment"
                  :index="index"
                  @deleteCommentEvent="deleteCommentEventHandler"
                  @editCommentEvent="editCommentEventHandler"
                  @hideInputEvent="hideInputEventHandler"
                ></Comment>
              </div>
            </van-list>
          </van-pull-refresh>
        </div>

        <!-- 输入框 -->
        <div class="detail_placeholder" v-show="!hideInput">
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
      <van-nav-bar
        :title="commentMode.edit ? '编辑评论' : '发表评论'"
        left-arrow
        @click-left="showComment = false"
        placeholder
        fixed
        z-index="100"
        style="margin-bottom: 10px; height: 46px"
      >
        <template #right>
          <van-button
            style="height: 80%"
            type="info"
            @click="submitComment()"
            >{{ commentMode.edit ? '修改' : '发表' }}</van-button
          >
        </template>
      </van-nav-bar>
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
      commentMode: { edit: false, comment_id: 0 },

      comments: [],

      loading: false, // list是否在加载
      finished: false, // list是否完全加载
      refreshing: false, // 上拉刷新

      locked: false,

      hideInput: false,
    };
  },
  methods: {
    onClickLeft() {
      this.$router.back();
    },

    refresh() {
      if (this.post !== {}) {
        this.finished = false;
        apis.getComments(this.post.post_id, 0, 0).then((res) => {
          if (res.data.data.comments.length == 0) {
            this.finished = true;
          }
          this.comments = res.data.data.comments;
          this.post.comments_num = res.data.data.comments_num;
          this.loading = false;
        });
      }
      this.refreshing = false;
    },

    getComments() {
      if (!this.locked && !this.finished) {
        this.locked = true;
        setTimeout(() => {
          this.locked = false;
        }, 1000);
        if (this.post.post_id !== undefined) {
          apis
            .getComments(
              this.post.post_id || this.$route.params.postId,
              0,
              this.comments.length
                ? this.comments[this.comments.length - 1].comment_id
                : 0,
            )
            .then((res) => {
              if (res.data.data.comments.length == 0) {
                this.finished = true;
                this.loading = false;
              }

              this.comments = [...this.comments, ...res.data.data.comments];
            });
        }
      } else if (!this.finished) {
        setTimeout(() => {
          this.getComments();
        }, 1000);
      }
      this.loading = false;
    },

    submitComment() {
      let promise;
      if (this.commentMode.edit == false) {
        promise = apis.saveComment(this.post.post_id, 0, this.commentText);
      } else {
        promise = apis.updateComment(
          this.commentMode.comment_id,
          this.commentText,
        );
      }
      promise
        .then(() => {
          Toast.success({ message: '发表成功' });
          this.commentText = '';
          this.showComment = false;
          this.commentMode = { edit: false, comment_id: 0 };
          this.refresh();
        })
        .catch((err) => {
          Toast.fail({
            message:
              err.response.data.message || `未知错误${err.response.data}`,
          });
        });
    },

    deleteCommentEventHandler(index) {
      this.comments.splice(index, 1);
    },

    editCommentEventHandler(index) {
      let comment = this.comments[index];
      this.commentText = comment.content;
      this.commentMode = { edit: true, comment_id: comment.comment_id };
      this.showComment = true;
    },

    hideInputEventHandler(hide) {
      this.hideInput = hide;
    },
  },
  async mounted() {
    apis
      .getPost(this.$route.params.postId, 0, 10)
      .then((res) => {
        this.post = res.data.data;
        this.comments = this.post.comments;

        if (this.comments.length == 0) {
          this.finished = true;
          this.loading = false;
        }
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
  z-index: 2017;
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
</style>
