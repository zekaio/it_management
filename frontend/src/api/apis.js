import instance from './config';

export let apis = {};

/* 用户部分 */

/**
 * 注册
 * POST /users
 * @param {string} username - 用户名
 * @param {string} password - 密码
 * @param {string} check_pwd - 再次输入密码
 */
apis.register = (username, password, check_pwd) => {
  return instance({
    url: '/users',
    method: 'post',
    data: JSON.stringify({ username, password, check_pwd }),
  });
};

/**
 * 修改密码
 * PUT /users/me/password
 * @param {string} password - 新密码
 * @param {string} check_pwd - 二次验证密码
 * @param {string} old_pwd - 旧密码
 */
apis.updatePassword = (password, check_pwd, old_pwd) => {
  return instance({
    url: '/users/me/password',
    method: 'put',
    data: JSON.stringify({ password, check_pwd, old_pwd }),
  });
};

/**
 * 修改用户信息
 * PUT /users/me/info
 * @param {string} username - 用户名
 * @param {string} sex - 性别
 * @param {string} grade - 年级
 * @param {string} major - 专业
 * @param {string} description - 个人介绍
 */
apis.updateUserInfo = (data) => {
  return instance({
    url: '/users/me/info',
    method: 'put',
    data: JSON.stringify(data),
  });
};

/**
 * 获取用户信息
 * GET /users
 * @param {string} uuid - uuid，可选
 * @param {string} username - username，可选
 */
apis.getUserInfo = (params) => {
  return instance({
    url: '/users',
    method: 'get',
    params,
  });
};

/**
 * 查找用户
 * GET /users/search?query={query}&last_user_uuid={last_user_uuid}&limit={limit}
 * @param {string} query - 查询关键字
 * @param {string} last_user_uuid - 最后一个用户的uuid
 * @param {number} limit - 返回数量
 */
apis.searchUsers = (query, last_user_uuid, limit = 10) => {
  return instance({
    url: '/users/search',
    method: 'get',
    params: { query, last_user_uuid, limit },
  });
};

/**
 * 上传头像
 * PUT /users/me/avatar
 * @param {File} file
 */
apis.uploadAvatar = (file) => {
  let data = new FormData();
  data.append('avatar', file);
  return instance({
    url: '/users/me/avatar',
    method: 'put',
    headers: { 'Content-Type': 'multipart/form-data' },
    data,
    showLoading: true,
  });
};

/**
 * 上传背景
 * PUT /users/me/bg
 * @param {File} file
 */
apis.uploadBg = (file) => {
  let data = new FormData();
  data.append('bg', file);
  return instance({
    url: '/users/me/bg',
    method: 'put',
    headers: { 'Content-Type': 'multipart/form-data' },
    data,
    showLoading: true,
  });
};

/* 用户会话部分 */

/**
 * 登录
 * POST /session
 * @param {string} username - 用户名
 * @param {string} password - 密码
 */
apis.login = (username, password) => {
  return instance({
    url: '/session',
    method: 'post',
    data: JSON.stringify({ username, password }),
  });
};

/**
 * 登出
 * DELETE /session
 */
apis.logout = () => {
  return instance({
    url: '/session',
    method: 'delete',
  });
};

/* 帖子部分 */

/**
 * 获取多个帖子
 * GET /posts?last_id={last_id}&limit={limit}&uuid={uuid}&keyword={keyword}&username={username}
 * @param {string} uuid - uuid，可选
 * @param {string} keyword - 搜索关键字，可选
 * @param {string} username - 用户名，可选
 * @param {number} last_id - 已获取帖子中最后一个帖子的id
 * @param {number} limit - 要获取的数目
 */
apis.getPosts = (queryParams, last_id = 0, limit = 10) => {
  return instance({
    url: '/posts',
    method: 'get',
    params: { ...queryParams, last_id, limit },
  });
};

/**
 * 通过id获取帖子
 * GET /posts/{post_id}?last_comment_id={last_comment_id}&limit={limit}
 * @param {number} post_id - 帖子id
 * @param {number} last_comment_id - 最后一个评论的id
 * @param {number} limit - 要获取的数目
 */
apis.getPost = (post_id, last_comment_id = 0, limit = 10) => {
  return instance({
    url: `/posts/${post_id}`,
    method: 'get',
    params: { last_comment_id, limit },
  });
};

/**
 * 发表帖子
 * POST /posts
 * @param {string} content - 内容
 */
apis.savePost = (content) => {
  return instance({
    url: '/posts',
    method: 'post',
    data: JSON.stringify({ content }),
  });
};

/**
 * 修改帖子
 * PUT /posts/{post_id}
 * @param {number} post_id - 帖子id
 * @param {string} content - 新内容
 */
apis.updatePost = (post_id, content) => {
  return instance({
    url: `/posts/${post_id}`,
    method: 'put',
    data: JSON.stringify({ content }),
  });
};

/**
 * 删除帖子
 * DELETE /posts/{post_id}
 * @param {number} post_id - 帖子id
 */
apis.deletePost = (post_id) => {
  return instance({
    url: `/posts/${post_id}`,
    method: 'delete',
  });
};

/* 评论部分 */

/**
 * 通过id获取某个帖子或评论的多条评论
 * GET /comments?parent_id={parent_id}&type={type}&last_id={last_id}&limit={limit}
 * @param {number} parent_id - 被评论的帖子或评论的id
 * @param {number} type - 是什么的评论，0是帖子，1是评论
 * @param {number} last_id - 已获取评论中最后一个评论的id
 * @param {number} limit - 要获取的数量
 */
apis.getComments = (parent_id, type, last_id = 0, limit = 10) => {
  return instance({
    url: '/comments',
    method: 'get',
    params: { parent_id, type, last_id, limit },
  });
};

/**
 * 通过id获取一条评论的详细信息和它的评论
 * GET /comments/{comment_id}?last_comment_id={last_comment_id}&limit={limit}
 * @param {number} comment_id - 评论id
 * @param {number} last_comment_id - 最后一个评论的id
 * @param {number} limit - 要获取的数目
 */
apis.getComment = (comment_id, last_comment_id = 0, limit = 10) => {
  return instance({
    url: `/comments/${comment_id}`,
    method: 'get',
    params: { last_comment_id, limit },
  });
};

/**
 * 发表评论
 * POST /comments
 * @param {number} parent_id - 被评论的帖子或评论的id
 * @param {number} type - 是什么的评论，0是帖子，1是评论
 * @param {string} content - 内容
 */
apis.saveComment = (parent_id, type, content) => {
  return instance({
    url: '/comments',
    method: 'post',
    data: JSON.stringify({ parent_id, type, content }),
  });
};

/**
 * 修改评论
 * PUT /comments/{commend_id}
 * @param {number} comment_id - 评论id
 * @param {string} content - 新内容
 */
apis.updateComment = (comment_id, content) => {
  return instance({
    url: `/comments/${comment_id}`,
    method: 'put',
    data: JSON.stringify({ content }),
  });
};

/**
 * 删除评论
 * DELETE /comments/{comment_id}
 * @param {number} commend_id - 评论id
 */
apis.deleteComment = (commend_id) => {
  return instance({
    url: `/comments/${commend_id}`,
    method: 'delete',
  });
};
