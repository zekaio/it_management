# 接口文档

## 错误处理

错误以 HTTP 状态码形式表示

### Response Body

```json
{
    "data":null,
    "message":"错误信息，直接显示给用户",
    "status":401
}
```

## 统一错误

`401`：用户未登录

`500`：服务器错误



## U. 用户部分

### U1.注册

```http
POST /users
```

#### Request Body

```json
{
    "username": "用户名",
    "password": "密码",
    "check_pwd": "二次验证密码"
}
```

#### Response Body

```json
{
    "data": null,
    "msg": "OK",
    "status": 200
}
```

#### 错误

`400`：两次输入密码不一致

`409`：用户已存在



### U2.修改密码

```http
PUT /users/me/password
```

#### Request Body

```json
{
    "password": "新密码",
    "check_pwd": "二次验证密码",
    "old_pwd": "旧密码"
}
```

#### Response Body

```json
{
    "data": null,
    "msg": "OK",
    "status": 200
}
```

#### 错误

`400`：两次输入密码不一致/旧密码错误

`404`：用户不存在



### U3.修改用户信息

```http
PUT /users/me/info
```

#### Request Body

```json
{
    "username": "用户名",
    "sex": "性别 男、女、不明",
    "grade": "年级 数字",
    "major": "专业",
    "description": "个人介绍"
}
```

#### Response Body

```json
{
    "data": null,
    "msg": "OK",
    "status": 200
}
```

#### 错误

`400`：性别、年龄、个人介绍不符合要求

`409`：用户名已存在



### U4.获取用户信息

```http
GET /users?uuid={uuid}&username={username}
```

不传uuid和username则是获取自己的

#### Response Body

```json
{
    "data": {
        "username": "用户名",
        "uuid": "uuid",
        "sex": "性别 男、女、不明",
    	"grade": "年级 数字",
    	"major": "专业",
    	"description": "个人介绍",
        "posts_num": "帖子数量",
        "avatar": "头像文件名"
    },
    "msg": "OK",
    "status": 200
}
```

#### 错误

`404`：用户不存在



### U5.查找用户

```http
GET /users/search?query={query}&last_user_uuid={last_user_uuid}&limit={limit}
```

#### Response Body

```json
{
	"data": [
	    {
	        "username": "用户名",
	        "uuid": "uuid",
	        "sex": "性别 男、女、不明",
	        "grade": "年级 数字",
	        "major": "专业",
	        "description": "个人介绍",
	        "posts_num": "帖子数量",
	        "avatar": "头像文件名"
	    },
	    ...
	],
	"msg": "OK",
	"status": 200
}
```



### U6.上传头像

```http
PUT /users/me/avatar
```

#### Request Body

图片文件

#### Response Body

```json
{
    "data": "头像地址",
    "msg": "OK",
    "status": 200
}
```

#### 错误

`400`：上传失败/不支持的文件类型



### U7.修改背景图

#### Request Body

#### Response Body

#### 错误



## S.用户会话部分

### S1.登录

```http
POST /session
```

#### Request Body

```json
{
    "username": "用户名",
    "password": "密码"
}
```

#### Response Body

```json
{
    "data": {
        "uuid": "uuid",
        "username":"用户名"
    },
    "msg": "OK",
    "status": 200
}
```

#### 错误

`400`：用户名或密码错误



### S2.登出

```http
DELETE /session
```

#### Response Body

```json
{
    "data": null,
    "msg": "OK",
    "status": 200
}
```



## P.帖子部分

### P1.获取多个帖子

```http
GET /posts?uuid={uuid}&username={username}&query={query}&last_id={last_id}&limit={limit}
```

#### 请求参数

| 参数名   | 说明                         | 默认值 |
| -------- | ---------------------------- | ------ |
| user_id  | uuid                         | 可选   |
| username | 用户名                       | 可选   |
| query    | 搜索关键词                   | 可选   |
| last_id  | 已获取帖子中最后一个帖子的id | 0      |
| limit    | 要获取的数目                 | 5      |

#### Response Body

```json
{
	"data":[
	        {
	            "post_id": "帖子id",
	            "username": "发帖人用户名",
	            "uuid": "发帖人uuid",
	            "content": "内容",
	            "comments_num": "评论数目",
	            "comments": [
	                {
	                    "comment_id": "评论id",
	                    "parent_id": "被评论的帖子或评论的id",
	                    "type": "是什么的评论，0是帖子，1是评论",
	                    "content": "评论内容",
	                    "comments_num": "评论数目",
	                    "username": "发帖人用户名",
	                    "uuid": "发帖人uuid"
	                }
	            ]
	        },
	    ]
	,
	"msg": "OK",
	"status": 200
}
```



### P2.通过id获取帖子

```http
GET /posts/{post_id}?last_comment_id={last_comment_id}&limit={limit}
```

#### 请求参数

| 参数名          | 说明             | 默认值 |
| --------------- | ---------------- | ------ |
| post_id         | 帖子id           |        |
| last_comment_id | 最后一个评论的id | 0      |
| limit           | 要获取的数目     | 5      |

#### Response Body

```json
{
	"data": {
	    "post_id": "帖子id",
	    "username": "发帖人用户名",
	    "uuid": "发帖人uuid",
	    "content": "内容",
	    "comments_num": "评论数目",
	    "comments": [
	        {
	            "id": "评论id",
	            "parent_id": "被评论的帖子或评论的id",
	            "type": "是什么的评论，0是帖子，1是评论",
	            "content": "评论内容",
	            "comments_num": "评论数目",
	            "username": "发帖人用户名",
	            "uuid": "发帖人uuid"
	        }
	    ]
	},
	"msg": "OK",
	"status": 200
}
```

#### 错误

`404`：帖子不存在



### P3.发表帖子

```http
POST /posts
```

#### Request Body

```json
{
    "content": "帖子内容"
}
```

#### Response Body

```json
{
	"data": {
	    "post_id": "帖子id"
	},
	"msg": "OK",
	"status": 200
}
```

#### 错误

`400`：帖子内容为空或长度超过120字

`404`：当前登录用户不存在



### P4.修改帖子

```http
PUT /posts/{post_id}
```

#### 请求参数

| 参数名  | 说明   | 默认值 |
| ------- | ------ | ------ |
| post_id | 帖子id |        |

#### Request Body

```json
{
    "content": "帖子内容"
}
```

#### Response Body

```json
{
	"data": {
	    "post_id": "帖子id"
	},
	"msg": "OK",
	"status": 200
}
```

#### 错误

`400`：帖子内容为空或长度超过120字

`403`：没有权限修改该帖子

`404`：帖子不存在



### P5.删除帖子

```http
DELETE /posts/{post_id}
```

#### 请求参数

| 参数名  | 说明   | 默认值 |
| ------- | ------ | ------ |
| post_id | 帖子id |        |

#### Response Body

```json
{
	"data": null,
	"msg": "OK",
	"status": 200
}
```

#### 错误

`403`：没有权限删除该帖子

`404`：帖子不存在



## C.评论部分

### C1.通过id获取某个帖子或评论的多条评论

```http
GET /comments?parent_id={parent_id}&type={type}&last_id={last_id}&limit={limit}
```

#### 请求参数

| 参数名    | 说明                           | 默认值 |
| --------- | ------------------------------ | ------ |
| parent_id | 被评论的帖子或评论的id         |        |
| type      | 是什么的评论，0是帖子，1是评论 |        |
| last_id   | 已获取评论中最后一个评论的id   | 0      |
| limit     | 要获取的数目                   | 5      |

#### Response Body

```json
{
	"data": {
	    "comments": [
	        {
	            "comment_id": "评论id",
	            "parent_id": "被评论的帖子或评论的id",
	            "type": "是什么的评论，0是帖子，1是评论",
	            "content": "评论内容",
	            "comments_num": "评论数目",
	            "username": "发帖人用户名",
	            "uuid": "发帖人uuid"
	        }
	    ]
	},
	"msg": "OK",
	"status": 200
}
```



### C2.通过id获取一条评论的详细信息和它的评论

```http
GET /comments/{comment_id}?last_comment_id={last_comment_id}&limit={limit}
```

#### 请求参数

| 参数名          | 说明             | 默认值 |
| --------------- | ---------------- | ------ |
| comment_id      | 评论id           |        |
| last_comment_id | 最后一个评论的id | 0      |
| limit           | 要获取的数目     | 5      |

#### Response Body

```json
{
	"data": {
		"comment_id": "评论id",
		"parent_id": "被评论的帖子或评论的id",
		"type": "是什么的评论，0是帖子，1是评论",
		"content": "评论内容",
		"comments_num": "评论数目",
		"username": "发帖人用户名",
		"uuid": "发帖人uuid",
		"comments": [
		    {
		        "id": "评论id",
		        "parent_id": "被评论的帖子或评论的id",
		        "type": "是什么的评论，0是帖子，1是评论",
		        "content": "评论内容",
		        "comments_num": "评论数目",
		        "username": "发帖人用户名",
		        "uuid": "发帖人uuid"
		    }
		]
	},
	"msg": "OK",
	"status": 200
}
```

#### 错误

`404`：评论不存在



### C3.发表评论

```http
POST /comments
```

#### Request Body

```json
{
    "parent_id": "被评论的帖子或评论的id",
    "type": "是什么的评论，0是帖子，1是评论",
    "content": "内容"
}
```

#### Response Body

```json
{
	"data": {
	    "comment_id": "评论id"
	},
	"msg": "OK",
	"status": 200
}
```

#### 错误

`404`：用户/评论/帖子不存在



### C4.修改评论

```http
PUT /comments/{comment_id}
```

#### 请求参数

| 参数名     | 说明   | 默认值 |
| ---------- | ------ | ------ |
| comment_id | 评论id |        |

#### Request Body

```json
{
	"content": "新内容"
}
```

#### Response Body

```json
{
	"data": {
		"comment_id": "评论id"
	},
	"msg": "OK",
	"status": 200
}
```

#### 错误

`400`：帖子内容为空或长度超过120字

`403`：没有权限修改评论

`404`：评论不存在



### C5.删除评论

```http
DELETE /comments/{comment_id}
```

#### Response Body

```json
{
	"data": null,
	"msg": "OK",
	"status": 200
}
```

#### 错误

`403`：没有权限删除评论

`404`：评论不存在
