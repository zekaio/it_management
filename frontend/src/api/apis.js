import instance from './config';

export let apis = {};

/* 用户部分 */

/**
 * 注册
 * POST /user
 * @param {string} username - 用户名
 * @param {string} password - 密码
 * @param {string} check_pwd - 再次输入密码
 */
apis.register = (username, password, check_pwd) => {
  return instance({
    url: '/user',
    method: 'post',
    data: JSON.stringify({
      username,
      password,
      check_pwd,
    }),
  });
};

/**
 * 修改密码
 * PUT /user/password
 * @param {string} password - 新密码
 * @param {string} check_pwd - 二次验证密码
 * @param {string} old_pwd - 旧密码
 */
apis.updatePassword = (password, check_pwd, old_pwd) => {
  return instance({
    url: '/user/password',
    method: 'put',
    data: JSON.stringify({
      password,
      check_pwd,
      old_pwd,
    }),
  });
};

/**
 * 修改用户信息
 */

/**
 * 获取用户信息
 * GET /user
 */
apis.getUserInfo = () => {
  return instance({
    url: '/user',
    method: 'get',
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
    data: JSON.stringify({
      username,
      password,
    }),
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
 * GET /posts?last_id={lastId}&limit={limit}
 * @param {number} lastId - 已获取帖子中最后一个帖子的id
 * @param {number} limit - 要获取的数目
 */
apis.getPosts = (lastId = 0, limit = 5) => {
  return instance({
    url: `/posts?last_id=${lastId}&limit=${limit}`,
    method: 'get',
  });
};

/**
 * 获取特定用户的帖子
 * GET /posts?uuid={uuid}&last_id={lastId}&limit={limit}
 * @param {string} uuid - uuid
 * @param {number} lastId - 已获取帖子中最后一个帖子的id
 * @param {number} limit - 要获取的数目
 */
apis.getUserPosts = (uuid, lastId = 0, limit = 5) => {
  return instance({
    url: `/posts?uuid=${uuid}&last_id=${lastId}&limit=${limit}`,
    method: 'get',
  });
};

/**
 * 通过id获取帖子
 * GET /posts/{postId}?last_comment_id={lastCommentId}&limit={limit}
 * @param {number} postId - 帖子id
 * @param {number} lastCommentId - 最后一个评论的id
 * @param {number} limit - 要获取的数目
 */
apis.getPost = (postId, lastCommentId = 0, limit = 5) => {
  return instance({
    url: `/posts/${postId}?last_comment_id=${lastCommentId}&limit${limit}`,
    method: 'get',
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
    data: JSON.stringify({
      content,
    }),
  });
};

/**
 * 修改帖子
 * PUT /posts/{postId}
 * @param {number} postId - 帖子id
 * @param {string} content - 新内容
 */
apis.updatePost = (postId, content) => {
  return instance({
    url: `/posts/${postId}`,
    method: 'put',
    data: JSON.stringify({
      content,
    }),
  });
};

/**
 * 删除帖子
 * DELETE /posts/{postId}
 * @param {number} postId - 帖子id
 */
apis.deletePost = (postId) => {
  return instance({
    url: `/posts/${postId}`,
    method: 'delete',
  });
};

/* 评论部分 */

/**
 * 通过id获取某个帖子或评论的多条评论
 * GET /comments?parent_id={parentId}&type={type}&last_id={lastId}&limit={limit}
 * @param {number} parentId - 被评论的帖子或评论的id
 * @param {number} type - 是什么的评论，0是帖子，1是评论
 * @param {number} lastId - 已获取评论中最后一个评论的id
 * @param {number} limit - 要获取的数量
 */
apis.getComments = (parentId, type, lastId = 0, limit = 5) => {
  return instance({
    url: `/comments?parent_id=${parentId}&type=${type}&last_id=${lastId}&limit=${limit}`,
    method: 'get',
  });
};

/**
 * 通过id获取一条评论的详细信息和它的评论
 * GET /comments/{commentId}?last_comment_id={lastCommentId}&limit={limit}
 * @param {number} commentId - 评论id
 * @param {number} lastCommentId - 最后一个评论的id
 * @param {number} limit - 要获取的数目
 */
apis.getComment = (commentId, lastCommentId = 0, limit = 5) => {
  return instance({
    url: `/comments/${commentId}?last_comment_id=${lastCommentId}&limit=${limit}`,
    method: 'get',
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
    data: JSON.stringify({
      parent_id,
      type,
      content,
    }),
  });
};

/**
 * 修改评论
 * PUT /comments/{commendId}
 * @param {number} commentId - 评论id
 * @param {string} content - 新内容
 */
apis.updateComment = (commentId, content) => {
  return instance({
    url: `/comments/${commentId}`,
    method: 'put',
    data: JSON.stringify({ content }),
  });
};

/**
 * 删除评论
 * DELETE /comments/{commentId}
 * @param {number} commendId - 评论id
 */
apis.deleteComment = (commendId) => {
  return instance({
    url: `/comments/${commendId}`,
    method: 'delete',
  });
};
