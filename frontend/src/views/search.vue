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
export default {
  data() {
    return {
      value: '',
    };
  },

  methods: {
    onSearch() {
      Toast(this.value);
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
