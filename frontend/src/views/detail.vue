<template>
  <div class="detail">
    <div v-show="!commentShow">
      <!-- 顶部导航栏 -->
      <van-nav-bar
        :title="`${isPost ? '帖子' : '评论'}详情`"
        placeholder
        fixed
        z-index="100"
        style="margin-bottom: 10px"
      >
        <template #left>
          <van-icon
            name="arrow-left"
            size="18"
            color="black"
            @click="$back()"
          />
        </template>
      </van-nav-bar>

      <!-- 帖子不存在占位符 -->
      <van-empty
        :description="`${isPost ? '帖子' : '评论'}不存在`"
        v-if="showEmpty"
      ></van-empty>

      <!-- 帖子存在 -->
      <div v-else>
        <!-- 用户信息 -->
        <van-cell center size="large">
          <template #title>
            <!-- 头像 -->
            <van-image
              round
              width="2.5rem"
              height="2.5rem"
              :src="avatarDir + parent.avatar"
              class="detail_post_cell_title_image"
              @click="$goTo(`/user?username=${parent.username}`)"
            >
              <template v-slot:loading>
                <van-loading type="spinner" size="20" />
              </template>
            </van-image>
            <span class="detail_post_cell_title_text">
              <!-- 用户名 -->
              {{ parent.username }}
              <br />
              <!-- 发表时间 -->
              <span style="color: #708090;">
                {{ parent.created_at }}
              </span>
            </span>
          </template>
        </van-cell>

        <!-- 帖子内容 -->
        <div class="detail_content">
          {{ parent.content }}
        </div>

        <!-- tabs -->
        <van-sticky :offset-top="46">
          <van-tabs v-model="tabActivate">
            <van-tab :title="'评论 ' + parent.comments_num"></van-tab>
            <van-tab title="" disabled></van-tab>
            <van-tab title="" disabled></van-tab>
            <van-tab title="" disabled></van-tab>
          </van-tabs>
        </van-sticky>

        <!-- 评论 -->
        <div v-show="tabActivate === 0" class="detail_comments">
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
              :immediate-check="false"
            >
              <div
                v-for="(comment, index) in comments"
                :key="index"
                class="van-hairline--bottom"
              >
                <Comment
                  :comment="comment"
                  :index="index"
                  @deleteCommentEvent="deleteCommentEventHandler"
                  @editCommentEvent="editCommentEventHandler"
                  @hideInputEvent="hideInputEventHandler"
                  @replyCommentEvent="replyCommentEventHandler"
                ></Comment>
                <div
                  style="margin-left:2rem; font-size:0.8rem; color: #1E90FF; padding-bottom:0.5rem"
                  @click="
                    $goTo(
                      `/post/${$route.params.postId}/comment/${comment.comment_id}`
                    )
                  "
                  v-if="isPost && comment.comments_num"
                >
                  共{{ comment.comments_num }}条回复
                </div>
              </div>
            </van-list>
          </van-pull-refresh>
        </div>

        <!-- 输入框 -->
        <div class="detail_placeholder" v-show="!hideInput">
          <div class="detail_bar" @click="replyParent">
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
    <div v-show="commentShow" class="detail_comment">
      <van-nav-bar
        :title="commentMode.edit ? '编辑评论' : '发表评论'"
        placeholder
        fixed
        z-index="100"
        style="margin-bottom: 10px; height: 46px"
      >
        <template #left>
          <van-icon
            name="arrow-left"
            size="18"
            @click="hideComment"
            color="black"
          />
        </template>
        <template #right>
          <svg
            t="1608363092807"
            class="icon"
            viewBox="0 0 1024 1024"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            p-id="29879"
            height="60%"
            @click="submitComment()"
          >
            <path
              d="M886.054743 152.46239c-1.845021 20.7373-3.671623 41.475624-5.539156 62.209854-2.509147 27.867698-5.054109 55.732325-7.575536 83.597977-2.895957 32.013111-5.794983 64.026222-8.670473 96.04138-2.801812 31.18628-5.562692 62.376653-8.364505 93.562932-2.844791 31.682583-5.728468 63.36312-8.579399 95.045703-2.478448 27.536146-4.926196 55.075363-7.404644 82.611509-2.867304 31.847336-5.750981 63.694671-8.630564 95.542007-1.066285 11.778254-2.095731 23.558555-3.222391 35.329646-1.699712 17.729803-16.054651 25.987884-32.29145 18.415418-25.63996-11.954263-51.201126-24.076348-76.788897-36.141128-56.142671-26.472931-112.302739-52.910047-168.374802-79.531358-3.825119-1.814322-5.638417-1.137916-8.147564 2.009773-44.242643 55.501058-88.609107 110.905926-132.956128 166.323073-9.82374 12.275581-23.985274 14.042831-33.486672 3.539616-3.02694-3.345188-5.319146-8.332782-5.832845-12.81077-3.357468-29.281907-6.14086-58.630329-9.097192-87.958284-3.223415-31.978319-6.444782-63.957661-9.638521-95.940073-2.498914-25.02086-5.079692-50.03558-7.320733-75.080999-0.434905-4.853541-1.947352-7.474228-6.695492-9.497305-80.055291-34.108842-160.004157-68.468394-240.004189-102.706173-8.015557-3.431146-13.956873-8.516977-15.233959-17.550725-1.531889-10.828626 3.604084-18.926048 14.94641-23.656793 30.249955-12.618389 60.532655-25.159006 90.808192-37.71395 221.6164-91.901083 443.233823-183.798073 664.850224-275.699156 11.831466-4.90573 20.134573-3.948939 27.185152 3.198855C884.606765 140.288117 886.416993 145.975653 886.054743 152.46239zM839.570036 196.137099c-0.382717-0.186242-0.765433-0.37146-1.14815-0.555655C713.69314 334.177012 588.965417 472.773603 463.955262 611.68128c2.165316 1.146103 3.730974 2.068102 5.372358 2.830465 27.976168 12.983709 55.401798 27.04189 83.601046 39.676651 76.962859 34.483372 152.834874 71.403237 229.142817 107.351983 1.877767 0.88516 3.791349 1.697665 6.363941 2.844791C805.527708 574.450331 822.54836 385.293203 839.570036 196.137099zM158.005129 466.417849c1.616824 0.87288 2.574638 1.49198 3.608178 1.935072 68.333318 29.305443 136.684032 58.572 204.977441 87.970564 3.091408 1.330298 4.834098 0.431835 7.021927-1.469468C502.166539 443.227684 630.755196 331.636143 759.331573 220.033345c1.224898-1.063215 2.358721-2.233877 3.533476-3.354398-0.201591-0.26299-0.404206-0.525979-0.606821-0.788969C561.042461 299.31604 359.824647 382.742101 158.005129 466.417849zM402.997935 762.605641c0.240477 0.00614 0.479931 0.01228 0.719384 0.01842 0.391926-1.408069 0.854461-2.799766 1.165546-4.225231 10.367115-47.625694 20.662599-95.268784 31.198559-142.857639 0.777713-3.511987 2.682086-7.186679 5.087878-9.866718 108.571764-120.839159 217.258139-241.577011 325.923024-362.333282 0.935302-1.039679 1.749854-2.187829 2.620687-3.284813-1.721201 0.506537-2.987031 1.464351-4.182252 2.501984-90.098018 78.18571-180.190919 156.376537-270.282796 234.56941-35.985586 31.234375-71.985498 62.452377-107.888196 93.78192-1.5104 1.316995-3.119037 3.777023-2.963495 5.554506 1.763157 20.068058 3.860934 40.10644 5.869684 60.153008 3.236718 32.3068 6.464225 64.614623 9.714246 96.921423C400.955416 743.229339 401.991002 752.916978 402.997935 762.605641zM420.887374 783.756357c0.306992 0.152473 0.611937 0.303922 0.917906 0.456395 32.251541-40.325427 64.50206-80.651878 97.083106-121.388674-21.970384-10.965749-43.12724-21.525246-64.709791-32.298614C442.960089 682.164564 431.923732 732.960461 420.887374 783.756357z"
              p-id="29880"
            ></path>
          </svg>
        </template>
      </van-nav-bar>
      <div class="detail_comment_container">
        <van-field
          id="comment_textarea"
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
import Comment from '../components/Comment';
import { avatarDir } from '../config';

export default {
  name: 'Detail',
  components: { Comment },
  data() {
    return {
      parent: {},

      showEmpty: false,
      tabActivate: 0,
      commentShow: false,

      commentText: '',
      commentMode: { edit: false, comment_id: 0, parent: true }, // type true：回复主贴,false：回复评论

      comments: [],

      loading: false, // list是否在加载
      finished: false, // list是否完全加载
      refreshing: false, // 上拉刷新

      locked: false,

      hideInput: false,

      avatarDir,
    };
  },
  methods: {
    // 判断object是否为空
    checkObjectEmpty(obj) {
      return Boolean(obj && Object.keys(obj).length);
    },

    // 刷新
    refresh() {
      if (this.checkObjectEmpty(this.parent)) {
        let timeout = setTimeout(() => {
          Toast.fail({
            message: '请求超时，请重试',
          });
          return;
        }, 10000);
        apis
          .getComments(
            this.isPost ? this.parent.post_id : this.parent.comment_id,
            this.isPost ? 0 : 1
          )
          .then((res) => {
            if (res.data.data.comments.length == 0) {
              this.finished = true;
            } else {
              this.finished = false;
            }
            this.comments = res.data.data.comments;
            this.parent.comments_num = res.data.data.comments_num;
          })
          .catch((err) => this.$error(err))
          .finally(() => {
            clearTimeout(timeout);
          });
      }
      this.refreshing = false;
    },

    // 获取评论
    getComments() {
      if (this.checkObjectEmpty(this.parent)) {
        apis
          .getComments(
            this.isPost ? this.parent.post_id : this.parent.comment_id,
            this.isPost ? 0 : 1,
            this.comments.length
              ? this.comments[this.comments.length - 1].comment_id
              : 0
          )
          .then((res) => {
            if (res.data.data.comments.length == 0) {
              this.finished = true;
            } else {
              this.comments = [...this.comments, ...res.data.data.comments];
            }
          })
          .catch((err) => this.$error(err))
          .finally(() => {
            this.loading = false;
          });
      }
    },

    // 提交评论
    submitComment() {
      if (!this.lock) {
        this.lock = true;
        (() => {
          if (this.commentMode.edit) {
            // 编辑
            return apis.updateComment(
              this.commentMode.comment_id,
              this.commentText
            );
          } else if (this.commentMode.parent) {
            // 回复主贴
            return apis.saveComment(
              this.isPost ? this.parent.post_id : this.parent.comment_id,
              this.isPost ? 0 : 1,
              this.commentText
            );
          } else {
            // 回复评论
            return apis.saveComment(
              this.commentMode.comment_id,
              1,
              this.commentText
            );
          }
        })()
          .then(() => {
            Toast.success({ message: '发表成功' });
            this.hideComment();
            this.refresh();
          })
          .catch((err) => this.$error(err))
          .finally(() => {
            this.lock = false;
          });
      }
    },

    // 回复主贴
    replyParent() {
      this.commentMode = { edit: false, comment_id: 0, parent: true };
      this.showComment();
    },

    // 回复评论
    replyCommentEventHandler(index) {
      this.commentMode = {
        edit: false,
        comment_id: this.comments[index].comment_id,
        parent: false,
      };
      this.showComment();
    },

    // 显示评论页
    showComment() {
      this.commentShow = true;
      setTimeout(() => {
        document.querySelector('#comment_textarea').focus();
      }, 50);
    },

    // 退出评论页
    hideComment() {
      this.commentText = '';
      this.commentShow = false;
      this.commentMode = { edit: false, comment_id: 0, parent: true };
    },

    // 删除评论
    deleteCommentEventHandler(index) {
      this.comments.splice(index, 1);
      this.parent.comments_num = this.parent.comments_num - 1;
    },

    // 修改评论
    editCommentEventHandler(index) {
      let comment = this.comments[index];
      this.commentText = comment.content;
      this.commentMode = { edit: true, comment_id: comment.comment_id };
      this.commentShow = true;
    },

    // 隐藏输入框
    hideInputEventHandler(hide) {
      this.hideInput = hide;
    },
  },
  async mounted() {
    if (this.isPost) {
      apis
        .getPost(this.$route.params.postId)
        .then((res) => {
          this.parent = res.data.data;
          this.comments = this.parent.comments;
          if (this.comments.length == 0) {
            this.finished = true;
            this.loading = false;
          }
        })
        .catch((err) =>
          this.$error(err, (err) => {
            if (err.response.status === 404) {
              this.showEmpty = true;
              return true;
            }
          })
        );
    } else {
      apis
        .getComment(this.$route.params.commentId)
        .then((res) => {
          this.parent = res.data.data;
          this.comments = this.parent.comments;
          if (this.comments.length == 0) {
            this.finished = true;
            this.loading = false;
          }
        })
        .catch((err) =>
          this.$error(err, (err) => {
            if (err.response.status === 404) {
              this.showEmpty = true;
              return true;
            }
          })
        );
    }
  },
  computed: {
    isPost: function() {
      return this.$route.name === 'PostDetail';
    },
  },
};
</script>

<style scoped>
.detail {
  min-height: 100vh;
}
.detail_post_cell_title_image {
  vertical-align: middle;
}
.detail_post_cell_title_text {
  margin-left: 2vw;
  display: inline-block;
  vertical-align: middle;
}
.detail_content {
  padding: 1rem 2rem;
  background-color: white;
  margin-bottom: 12px;
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
  background-color: #fff;
}
.detail_input_placeholder {
  height: 54px;
  border-radius: 4px;
  flex: 1;
  height: 36px;
  margin: 0 13px;
  background-color: rgba(133, 133, 133, 0.25);
}
.detail_input_text {
  line-height: 36px;
  margin-left: 10px;
  font-size: 14px;
  color: rgb(120, 120, 120);
  letter-spacing: 0;
}
.detail_comments {
  background-color: white;
}
</style>
