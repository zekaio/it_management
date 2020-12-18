<template>
  <form action="/">
    <van-search
      v-model="value"
      placeholder="请输入搜索关键词"
      show-action
      @search="onSearch"
    >
      <template #left>
        <van-icon name="arrow-left" @click="back" />
      </template>
      <template #action>
        <div @click="onSearch">搜索</div>
      </template>
    </van-search>
  </form>
</template>

<script>
import { Toast } from 'vant';
import { apis } from '../api/apis';
export default {
  data() {
    return {
      value: '',
    };
  },

  methods: {
    onSearch() {
      // Toast(this.value);
      apis.searchPost(this.value).then((res) => {
        console.log(res);
      });
    },

    onCancel() {
      Toast('取消');
    },

    back() {
      this.$router.back();
    },
  },
};
</script>

<style scoped></style>
