from app.extends.check import BaseModel, Parameter
from app.extends.helper import check_post_or_comment_content


class CommentModel(BaseModel):
    parent_id = Parameter(int)
    type = Parameter(int)
    content = Parameter(str, check_func=check_post_or_comment_content)