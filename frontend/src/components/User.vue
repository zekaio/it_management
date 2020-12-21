<template>
  <div class="user">
    <van-cell center :border="false" size="large">
      <template #title>
        <!-- 头像 -->
        <van-image
          round
          width="2.5rem"
          height="2.5rem"
          :src="avatarDir + avatar"
          class="user_avatar"
          @click="$goTo(`/user?username=${username}`)"
        >
          <template v-slot:loading>
            <van-loading type="spinner" size="20" /> </template
        ></van-image>
        <span class="user_text">
          <!-- 用户名 -->
          {{ username }}
          <br />
          <!-- 自我介绍 -->
          <div class="user_description">
            {{ description ? `简介:${description}` : '' }}
          </div>
        </span>
      </template>
      <template #right-icon v-if="!isMe">
        <div @click="onFollow">
          <!-- 未关注 -->
          <svg
            t="1608439563093"
            class="icon"
            viewBox="0 0 1024 1024"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            p-id="2979"
            width="1.5rem"
            height="1.5rem"
            v-show="!followed"
          >
            <path
              d="M746.04088889 660.70755555c8.53333333-12.40177778 5.34755555-29.46844445-7.168-38.00177777-40.50488889-27.76177778-86.35733333-46.64888889-136.98844444-56.77511111 109.90933333-41.64266667 187.96088889-147.91111111 187.96088888-272.384 0-160.768-130.38933333-291.15733333-291.15733333-291.15733334s-291.15733333 130.50311111-291.15733333 291.27111112c0 126.976 81.23733333 234.95111111 194.56 274.77333333-51.65511111 10.69511111-99.328 29.24088889-142.67733334 55.52355555-58.02666667 35.27111111-107.97511111 84.30933333-148.36622222 145.74933334-68.15288889 103.65155555-85.44711111 206.16533333-86.12977778 210.48888888l-1.47911111 9.44355556c-2.27555555 14.90488889 7.96444445 28.89955555 22.86933333 31.17511111 1.36533333 0.22755555 2.84444445 0.34133333 4.20977778 0.34133333 13.19822222 0 24.91733333-9.67111111 26.96533334-23.21066666l1.36533333-9.10222222c0.56888889-3.29955555 16.83911111-96.36977778 77.824-189.21244445C238.47822222 675.27111111 358.17244445 612.12444445 512.34133333 612.12444445c75.88977778 0 141.76711111 18.77333333 195.81155556 55.63733333 12.40177778 8.64711111 29.35466667 5.46133333 37.888-7.05422223zM262.144 293.66044445c0-63.14666667 24.576-122.53866667 69.29066667-167.25333334s104.10666667-69.29066667 167.25333333-69.29066666 122.53866667 24.576 167.25333333 69.29066666 69.29066667 104.10666667 69.29066667 167.25333334-24.576 122.53866667-69.29066667 167.25333333-104.10666667 69.29066667-167.25333333 69.29066667-122.53866667-24.576-167.25333333-69.29066667-69.29066667-103.99288889-69.29066667-167.25333333zM994.98666667 821.58933333H877.11288889V703.71555555c0-15.13244445-12.17422222-27.30666667-27.30666667-27.30666666s-27.30666667 12.17422222-27.30666667 27.30666666v117.87377778H704.62577778c-15.13244445 0-27.30666667 12.17422222-27.30666667 27.30666667s12.17422222 27.30666667 27.30666667 27.30666667h117.87377777v117.87377778c0 15.13244445 12.17422222 27.30666667 27.30666667 27.30666666s27.30666667-12.17422222 27.30666667-27.30666666V876.20266667h117.87377778c15.13244445 0 27.30666667-12.17422222 27.30666666-27.30666667s-12.288-27.30666667-27.30666666-27.30666667z"
              fill="#409EFF"
              p-id="2980"
            ></path>
          </svg>
          <!-- 已关注 -->
          <svg
            t="1608439706518"
            class="icon"
            viewBox="0 0 1024 1024"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            p-id="4494"
            width="1.5rem"
            height="1.5rem"
            v-show="followed"
          >
            <path
              d="M355.84 744.8064L158.5664 536.064A64 64 0 1 0 65.536 624.128l242.0736 256a64 64 0 0 0 91.2896 1.7408l513.8432-503.296a64 64 0 1 0-89.6-91.4432l-467.3024 457.728z"
              p-id="4495"
              fill="#409EFF"
            ></path>
          </svg>
        </div>
      </template>
    </van-cell>
  </div>
</template>

<script>
import { Dialog } from 'vant';

import { avatarDir } from '../config';

export default {
  name: 'User',

  props: {
    avatar: String,
    username: String,
    description: String,
    followed: Boolean,
    index: Number,
  },

  data() {
    return { avatarDir };
  },

  methods: {
    onFollow() {
      if (this.followed) {
        Dialog.confirm({
          message: `不再关注<b>${this.username}</b>`,
          confirmButtonText: '取消关注',
          cancelButtonText: '返回',
          closeOnClickOverlay: true,
        })
          .then(() => {
            this.$emit('followEvent', this.index);
          })
          .catch(() => {
            return;
          });
      } else {
        this.$emit('followEvent', this.index);
      }
    },
  },

  computed: {
    isMe() {
      return this.username === localStorage.getItem('username');
    },
  },
};
</script>

<style scoped>
.user {
  background-color: white;
}
.user_avatar {
  vertical-align: middle;
}
.user_text {
  display: inline-block;
  vertical-align: middle;
  margin-left: 2vw;
  width: 60vw;
  font-size: 1.1rem;
}
.user_description {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 0.8rem;
  color: #708090;
}
</style>
