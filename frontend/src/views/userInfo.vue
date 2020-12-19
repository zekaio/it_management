<template>
  <div class="user_info">
    <!-- 顶部导航栏 -->
    <van-nav-bar
      title="个人资料"
      placeholder
      fixed
      z-index="100"
      style="margin-bottom: 10px"
    >
      <template #left>
        <van-icon name="arrow-left" size="18" color="black" @click="$back()" />
      </template>
    </van-nav-bar>

    <!-- 头像 -->
    <van-image
      :src="avatar"
      round
      width="23vw"
      height="23vw"
      @click="imageActionSheetShow = true"
      style="margin-top:2rem"
    />
    <!-- 弹出层 -->
    <van-action-sheet
      v-model="imageActionSheetShow"
      :actions="imageActions"
      @select="onSelectImageAction"
      cancel-text="取消"
      close-on-popstate
      round
    />
    <!-- 上传头像 -->
    <van-uploader
      v-show="false"
      ref="uploader"
      :after-read="afterRead"
      :max-size="2048 * 1024"
      result-type="file"
      @oversize="onOversize"
    />

    <!-- 表单 -->
    <van-form @submit="onSubmit" style="margin-top:2rem">
      <!-- 昵称 -->
      <van-field
        v-model="info.username"
        type="text"
        name="username"
        label="用户名"
        placeholder="请输入用户名"
        :rules="[{ required: true, message: '请填写用户名' }]"
      />
      <!-- 性别 -->
      <van-field
        readonly
        clickable
        name="sex"
        :value="info.sex"
        label="性别"
        placeholder="点击选择性别"
        @click="sexPickerShow = true"
      />
      <van-popup v-model="sexPickerShow" position="bottom">
        <van-picker
          show-toolbar
          :columns="sexColumns"
          @confirm="onSexConfirm"
          @cancel="sexPickerShow = false"
        />
      </van-popup>
      <!-- 年级 -->
      <van-field
        readonly
        clickable
        name="grade"
        :value="info.grade"
        label="年级"
        placeholder="点击选择年级"
        @click="gradePickerShow = true"
      />
      <van-popup v-model="gradePickerShow" position="bottom">
        <van-picker
          show-toolbar
          :columns="gradeColumns"
          @confirm="onGradeConfirm"
          @cancel="gradePickerShow = false"
        />
      </van-popup>
      <!-- 专业 -->
      <van-field
        v-model="info.major"
        type="text"
        name="major"
        label="专业"
        placeholder="请输入专业"
      />

      <!-- 个人介绍 -->
      <van-field
        v-model="info.description"
        type="textarea"
        name="description"
        label="个人简介"
        autosize
        placeholder="请输入个人简介"
        show-word-limit
        maxlength="50"
      />

      <div style="margin: 24px 64px;">
        <van-button round plain block type="info" native-type="submit">
          保存信息
        </van-button>
        <van-button
          style="margin-top: 24px"
          round
          block
          type="danger"
          native-type="button"
          @click="logout"
        >
          退出登录
        </van-button>
      </div>
    </van-form>
  </div>
</template>

<script>
import { Toast, ImagePreview } from 'vant';
import { apis } from '../api/apis';
import { avatarDir } from '../config';
export default {
  name: 'userInfo',
  data() {
    return {
      info: {},

      sexColumns: ['男', '女', '不明'],
      imageActions: [{ name: '查看头像' }, { name: '修改头像' }],

      imageActionSheetShow: false,
      sexPickerShow: false,
      gradePickerShow: false,

      lock: false,
    };
  },
  methods: {
    // 退出登录
    logout() {
      apis
        .logout()
        .then(() => {
          Toast.success({ message: '退出成功' });
          localStorage.setItem('username', undefined);
          localStorage.setItem('uuid', undefined);
          this.$router.push({
            path: '/login',
          });
        })
        .catch((err) => this.$error(err));
    },

    // 限制图片大小
    onOversize() {
      Toast.fail({
        message: '文件大小不能超过2m',
      });
    },

    // 选择头像操作
    onSelectImageAction(item) {
      this.imageActionSheetShow = false;
      if (item.name == '查看头像') {
        ImagePreview({
          images: [this.avatar],
          showIndex: false,
        });
      } else if (item.name == '修改头像') {
        this.$refs.uploader.chooseFile();
      }
    },

    // 上传图片
    afterRead(file) {
      apis
        .uploadAvatar(file.file)
        .then((res) => {
          this.info.avatar = res.data.data;
          Toast.success({ message: '上传成功' });
        })
        .catch((err) => this.$error(err));
    },

    // 确认性别
    onSexConfirm(sex) {
      this.info.sex = sex;
      this.sexPickerShow = false;
    },

    // 确认年级
    onGradeConfirm(grade) {
      this.info.grade = grade;
      this.gradePickerShow = false;
    },

    // 保存信息
    onSubmit(values) {
      if (!this.lock) {
        this.lock = true;
        apis
          .updateUserInfo(values)
          .then(() => {
            Toast.success({
              message: '修改成功',
            });
            localStorage.setItem('username', values.username);
          })
          .catch((err) => this.$error(err))
          .finally(() => {
            this.lock = false;
          });
      }
    },
  },
  async mounted() {
    // 获取个人信息
    apis
      .getUserInfo()
      .then((res) => {
        this.info = res.data.data;
      })
      .catch((err) => this.$error(err));
  },
  computed: {
    gradeColumns: function() {
      let date = new Date();
      let year = date.getFullYear();
      return Array.from(new Array(year + 1).keys())
        .slice(year - 10)
        .reverse();
    },
    avatar: function() {
      return avatarDir + this.info.avatar;
    },
  },
};
</script>

<style scoped>
.user_info {
  display: flex;
  display: -webkit-flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}
</style>
