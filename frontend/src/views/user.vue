<template>
  <div class="user">
    <!-- 顶部导航栏 -->
    <van-nav-bar fixed placeholder z-index="100">
      <!-- 返回箭头 -->
      <template #left>
        <van-icon
          name="arrow-left"
          size="18"
          color="black"
          @click="$back()"
          v-if="$route.query.username !== undefined"
        />
      </template>
      <template #right>
        <!-- 搜索 -->
        <van-icon
          name="search"
          size="1.5rem"
          color="black"
          @click="$goTo(`/search?username=${info.username}`)"
        />

        <!-- 发帖 -->
        <svg
          t="1608349113391"
          class="icon"
          viewBox="0 0 1024 1024"
          version="1.1"
          xmlns="http://www.w3.org/2000/svg"
          p-id="11499"
          width="1.5rem"
          height="1.5rem"
          style="margin-left:3vw"
          v-if="isMe"
          @click="$goTo('/post/edit')"
        >
          <path
            d="M128 736v160h160l471.467-471.467-160-160L128 736z m755.2-435.2c17.067-17.067 17.067-42.667 0-59.733L782.933 140.8c-17.066-17.067-42.666-17.067-59.733 0l-78.933 78.933 160 160L883.2 300.8z"
            p-id="11500"
          ></path>
        </svg>
      </template>
    </van-nav-bar>
    <!-- <div class="user_nav_bar">
      <div class="user_nav_bar_content">
        <div class="user_nav_bar_right_icon">
          <van-icon name="search" size="1.5rem" />
          <svg
            t="1608349113391"
            class="icon"
            viewBox="0 0 1024 1024"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            p-id="11499"
            width="1.5rem"
            height="1.5rem"
            style="margin-left:3vw"
            v-if="isMe"
          >
            <path
              d="M128 736v160h160l471.467-471.467-160-160L128 736z m755.2-435.2c17.067-17.067 17.067-42.667 0-59.733L782.933 140.8c-17.066-17.067-42.666-17.067-59.733 0l-78.933 78.933 160 160L883.2 300.8z"
              p-id="11500"
            ></path>
          </svg>
        </div>
      </div>
    </div> -->

    <!-- 用户信息 -->
    <div class="user_info">
      <!-- 背景 -->
      <van-image
        class="user_info_bg"
        :src="bgDir + info.bg"
        fit="cover"
        @click="imageActionSheetShow = true"
      >
        <template v-slot:loading>
          <van-loading type="spinner" size="20" />
        </template>
        <!-- <template v-slot:error>
          <van-image
            class="user_info_bg"
            src="https://zekaio.cn/zimg/be4195b3a62a88637312bb2d84ebbc21"
            fit="cover"
          />
        </template> -->
      </van-image>
      <!-- 弹出层 -->
      <van-action-sheet
        v-model="imageActionSheetShow"
        :actions="imageActions"
        @select="onSelectImageAction"
        cancel-text="取消"
        close-on-popstate
        round
      />
      <!-- 上传背景 -->
      <van-uploader
        v-show="false"
        ref="uploader"
        :after-read="afterRead"
        :max-size="2048 * 1024"
        result-type="file"
        @oversize="onOversize"
      />

      <!-- 右侧icon -->
      <div class="user_info_float_right">
        <!-- 主页 -->
        <div class="user_info_self" v-if="isMe">
          <!-- 修改个人信息 -->
          <svg
            t="1608346182635"
            class="icon"
            viewBox="0 0 1024 1024"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            p-id="4571"
            width="1.5rem"
            height="1.5rem"
            @click="$goTo('/user/info')"
          >
            <path
              d="M814.08 634.88c11.264-13.312 9.216-32.768-3.072-43.008-45.056-37.888-96.256-66.56-151.552-84.992 72.704-45.056 121.856-125.952 121.856-218.112-1.024-141.312-115.712-256-257.024-256S267.264 147.456 267.264 289.792c0 92.16 49.152 173.056 121.856 218.112-65.536 21.504-125.952 58.368-177.152 108.544-82.944 82.944-129.024 194.56-129.024 312.32 0 17.408 13.312 30.72 30.72 30.72s30.72-13.312 30.72-30.72c0-101.376 38.912-196.608 110.592-268.288 71.68-71.68 166.912-111.616 268.288-111.616 91.136 0 178.176 31.744 246.784 91.136 13.312 9.216 32.768 8.192 44.032-5.12zM328.704 288.768c0-107.52 88.064-195.584 195.584-195.584 107.52 0 195.584 88.064 195.584 195.584 0 107.52-88.064 195.584-195.584 195.584-108.544 0-195.584-87.04-195.584-195.584zM677.7856 890.112l170.88512-170.88512 44.89216 44.89216L722.67776 935.0144zM654.336 958.464l60.416-16.384-45.056-45.056zM854.85568 712.21248l8.68352-8.69376 44.9024 44.89216-8.69376 8.69376zM913.408 710.656L901.12 698.368c-9.216-9.216-23.552-9.216-32.768 0l-2.048 2.048 45.056 45.056 2.048-2.048c9.216-9.216 9.216-23.552 0-32.768z"
              p-id="4572"
            ></path>
          </svg>
        </div>

        <!-- 他人 -->
        <div class="user_info_other" v-if="!isMe">
          <!-- 关注按钮 -->
          <div
            class="user_info_other_like"
            :class="{
              user_info_other_like_followed: info.follow_status,
              user_info_other_like_not_followed: !info.follow_status,
            }"
            @click="followUser"
          >
            {{ info.follow_status ? '已' : '' }}关注
          </div>
        </div>
      </div>

      <!-- 信息 -->
      <div class="user_info_main">
        <!-- 头像 -->
        <van-image
          round
          width="20vw"
          height="20vw"
          class="user_info_avatar"
          :src="avatarDir + info.avatar"
          @click="showAvatar"
        >
          <template v-slot:loading>
            <van-loading type="spinner" size="20" />
          </template>
        </van-image>
        <div class="user_info_detail">
          <!-- 用户名 -->
          {{ info.username }}
          <!-- 年级 -->
          {{ info.grade ? `${info.grade}级` : '' }}
          <!-- 专业 -->
          {{ info.major }}
          <!-- 男 -->
          <svg
            t="1608317756246"
            viewBox="0 0 1024 1024"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            p-id="1977"
            data-spm-anchor-id="a313x.7781069.0.i0"
            height="0.8rem"
            width="0.8rem"
            style="fill:#00BFFF"
            v-if="info.sex === '男'"
          >
            <path
              d="M954.418 135.399c0.093-9.733-3.424-19.304-9.797-26.662-6.823-7.866-16.619-12.837-26.993-13.695-0.143-0.016-0.289-0.029-0.432-0.044L684.744 78.163c-22.091-1.596-41.315 15.019-42.918 37.12-1.602 22.105 15.019 41.32 37.124 42.922l144.701 10.482L651.691 339.99c-61.707-55.677-143.442-89.573-233.098-89.573-192.249 0-348.093 155.845-348.093 348.09s155.845 348.091 348.093 348.091c192.243 0 348.087-155.846 348.087-348.091 0-73.632-22.859-141.916-61.868-198.156l161.967-161.355-9.13 130.178c-1.553 22.105 15.116 41.282 37.222 42.834 0.955 0.063 1.905 0.099 2.851 0.099 20.881 0 38.499-16.169 39.983-37.32l16.624-236.958C954.384 137.021 954.408 136.206 954.418 135.399 954.423 135.104 954.418 135.536 954.418 135.399L954.418 135.399zM665.416 702.739c-13.489 31.883-32.813 60.534-57.436 85.16-24.623 24.623-53.272 43.946-85.159 57.436-32.969 13.94-68.036 21.011-104.233 21.011-36.194 0-71.258-7.07-104.228-21.011-31.888-13.489-60.537-32.813-85.161-57.436-24.627-24.626-43.95-53.277-57.435-85.16-13.945-32.969-21.013-68.042-21.013-104.232 0-36.192 7.068-71.259 21.013-104.229 13.485-31.887 32.808-60.537 57.435-85.164 24.624-24.624 53.273-43.947 85.161-57.431 32.97-13.945 68.034-21.014 104.228-21.014 36.197 0 71.264 7.068 104.233 21.014 31.887 13.484 60.536 32.808 85.159 57.431 24.623 24.627 43.946 53.277 57.436 85.164 13.945 32.971 21.014 68.037 21.014 104.229C686.43 634.697 679.361 669.771 665.416 702.739L665.416 702.739zM665.416 702.739"
              p-id="1978"
              data-spm-anchor-id="a313x.7781069.0.i1"
              class=""
            ></path>
          </svg>
          <!-- 女 -->
          <svg
            t="1608317789860"
            viewBox="0 0 1024 1024"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            p-id="1921"
            height="0.8rem"
            width="0.8rem"
            style="fill:#FF1493"
            v-if="info.sex === '女'"
          >
            <path
              d="M796.479 354.576c0-156.872-127.204-284.076-284.081-284.076-156.873 0-284.077 127.204-284.077 284.076 0 146.08 110.665 265.014 252.515 280.859l0 66.35-126.26 0c-17.42 0-31.561 14.142-31.561 31.566 0 17.42 14.141 31.562 31.561 31.562l126.26 0 0 157.821c0 17.426 14.142 31.566 31.562 31.566 17.425 0 31.565-14.141 31.565-31.566L543.963 764.913 670.22 764.913c17.425 0 31.565-14.142 31.565-31.562 0-17.425-14.141-31.566-31.565-31.566L543.964 701.785l0-66.35C685.814 619.527 796.479 500.656 796.479 354.576L796.479 354.576zM291.449 354.576c0-121.833 99.115-220.949 220.95-220.949 121.838 0 220.953 99.116 220.953 220.949 0 121.839-99.115 220.954-220.953 220.954C390.564 575.53 291.449 476.415 291.449 354.576L291.449 354.576zM291.449 354.576"
              p-id="1922"
            ></path>
          </svg>
        </div>

        <!-- 简介 -->
        <div class="user_info_description">简介：{{ info.description }}</div>

        <!-- 关注和粉丝 -->
        <div class="user_info_follow">
          <span @click="$goTo(`follow?type=follow&username=${info.username}`)">
            {{ info.follow_num }} 关注
          </span>
          <span
            style="margin-left:4vw;"
            @click="$goTo(`follow?type=fans&username=${info.username}`)"
          >
            {{ info.fans_num }} 粉丝
          </span>
        </div>
      </div>
    </div>

    <!-- 帖子数量 -->
    <div class="user_info_posts_num">全部帖子 · {{ info.posts_num }}</div>

    <!-- 帖子 -->
    <van-pull-refresh v-model="refreshing" @refresh="refresh">
      <van-list
        v-model="loading"
        :finished="finished"
        finished-text="没有更多了"
        @load="getPosts"
      >
        <div v-for="(post, index) in posts" :key="index">
          <Post
            :post="post"
            :index="index"
            @deletePostEvent="deletePostEventHandler"
          />
        </div>
      </van-list>
    </van-pull-refresh>

    <!-- 底部导航栏 -->
    <van-tabbar v-model="active" placeholder v-if="isMe">
      <van-tabbar-item to="/" icon="home-o"></van-tabbar-item>
      <van-tabbar-item icon="user-o"> </van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script>
import { Dialog, ImagePreview, Toast } from 'vant';

import { apis } from '../api/apis';
import { avatarDir, bgDir } from '../config';

import Post from '../components/Post';

export default {
  name: 'User',

  components: { Post },

  data() {
    return {
      info: {},
      posts: [],
      active: 1,
      loading: false,
      finished: false,
      refreshing: false,
      avatarDir,
      bgDir,
      imageActionSheetShow: false,
    };
  },

  methods: {
    // 刷新
    refresh() {
      let timeout = setTimeout(() => {
        Toast.fail({
          message: '请求超时，请重试',
        });
        return;
      }, 10000);
      apis
        .getPosts({ username: this.username })
        .then((res) => {
          this.posts = res.data.data;
          if (res.data.data.length == 0) {
            this.finished = true;
          } else {
            this.finished = false;
          }
        })
        .catch((err) => this.$error(err))
        .finally(() => {
          clearTimeout(timeout);
        });
      this.refreshing = false;
    },

    //获取帖子
    getPosts() {
      if (this.posts.length == 0) {
        apis
          .getPosts({ username: this.username })
          .then((res) => {
            this.posts = res.data.data;
            if (res.data.data.length == 0) {
              this.finished = true;
            }
          })
          .catch((err) => this.$error(err))
          .finally(() => {
            this.loading = false;
          });
      } else {
        apis
          .getPosts(
            { username: this.username },
            this.posts[this.posts.length - 1].post_id
          )
          .then((res) => {
            if (res.data.data.length == 0) {
              this.finished = true;
            } else {
              this.posts = [...this.posts, ...res.data.data];
            }
          })
          .catch((err) => this.$error(err))
          .finally(() => {
            this.loading = false;
          });
      }
    },

    // 处理删除帖子事件
    deletePostEventHandler(index) {
      this.posts.splice(index, 1);
    },

    // 查看头像大图
    showAvatar() {
      ImagePreview({
        images: [this.avatarDir + this.info.avatar],
        showIndex: false,
      });
    },

    // 选择背景操作
    onSelectImageAction(item) {
      this.imageActionSheetShow = false;
      if (item.name == '查看背景') {
        ImagePreview({
          images: [bgDir + this.info.bg],
          showIndex: false,
        });
      } else if (item.name == '修改背景') {
        this.$refs.uploader.chooseFile();
      }
    },

    // 限制图片大小
    onOversize() {
      Toast.fail({
        message: '文件大小不能超过2m',
      });
    },

    // 上传背景
    afterRead(file) {
      apis
        .uploadBg(file.file)
        .then((res) => {
          this.info.bg = res.data.data;
          Toast.success({ message: '上传成功' });
        })
        .catch((err) => this.$error(err));
    },

    // 关注用户
    followUser() {
      if (this.info.follow_status) {
        Dialog.confirm({
          message: `不再关注<b>${this.info.username}</b>`,
          confirmButtonText: '取消关注',
          cancelButtonText: '返回',
          closeOnClickOverlay: true,
        })
          .then(() => {
            apis
              .followUser(this.info.username, false)
              .then(() => {
                this.info.follow_status = false;
                this.info.fans_num--;
                Toast.success({ message: '取消关注成功' });
              })
              .catch((err) => this.$error(err));
          })
          .catch(() => {
            return;
          });
      } else {
        apis
          .followUser(this.info.username, true)
          .then(() => {
            this.info.follow_status = true;
            this.info.fans_num++;
            Toast.success({ message: '关注成功' });
          })
          .catch((err) => this.$error(err));
      }
    },
  },

  async mounted() {
    apis
      .getUserInfo({ username: this.username })
      .then((res) => {
        this.info = res.data.data;
      })
      .catch((err) =>
        this.$error(err, () => {
          this.finished = true;
        })
      );
  },

  computed: {
    username() {
      return this.$route.query.username || localStorage.getItem('username');
    },

    isMe() {
      return (
        this.username === undefined ||
        this.username === localStorage.getItem('username')
      );
    },

    imageActions() {
      return this.isMe
        ? [{ name: '查看背景' }, { name: '修改背景' }]
        : [{ name: '查看背景' }];
    },
  },
};
</script>

<style scoped>
.user_info {
  width: 100vw;
  min-height: 30vh;
  background-color: white;
}
.user_info_bg {
  width: 100vw;
  height: 15vh;
}
.user_info_avatar {
  margin-top: -8vw;
}
.user_info_main {
  margin-left: 1rem;
}
.user_info_detail {
  margin-top: 1vw;
  vertical-align: middle;
  font-size: 1.2rem;
}
.user_info_description {
  margin-top: 2vw;
  font-size: 0.7rem;
}
.user_info_follow {
  color: #708090;
  margin-top: 2vw;
  font-size: 0.8rem;
  padding-bottom: 3vw;
}
.user_info_other_like {
  border: 1px solid;
  padding: 0.3rem 1rem;
  border-radius: 1rem;
}
.user_info_other_like_followed {
  background-color: #d3d3d3;
}
.user_info_other_like_not_followed {
  background-color: #409eff;
  color: white;
}
.user_info_float_right {
  position: absolute;
  right: 3vw;
  margin-top: 3vw;
}
.user_info_posts_num {
  color: gray;
  font-size: 0.7rem;
  padding: 0.5rem 0.5rem 0;
}
/* 顶部导航栏 */
/* .user_nav_bar {
  background-color: transparent;
  position: fixed;
  z-index: 100;
  top: 0;
}
.user_nav_bar_content {
  position: relative;
  width: 100vw;
}
.user_nav_bar_right_icon {
  position: absolute;
  margin-top: 3vw;
  right: 3vw;
} */
</style>
