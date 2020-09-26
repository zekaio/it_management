<template>
  <div>
    <div>编辑页面</div>
    <div>
      帖子id：{{ $route.params.post_id ? $route.params.post_id : '新帖子' }}
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style></style>
