from models.comment_models import Comment
from models.user_models import User

class CommentService:
    @staticmethod
    def add_comment(data, user_id):
        try:
            comment_id = Comment.create_comment(
                data["post_id"],
                user_id,
                data["content"],
                data.get("parent_id")
            )
            return {"message": "Comment added successfully", "comment_id": comment_id, "status": 201}
        except Exception as e:
            return {"message": f"Error adding comment: {str(e)}", "status": 500}

    @staticmethod
    def get_post_comments(post_id):
        try:
            comments = Comment.get_comments_by_post(post_id)
            comment_dict = {}
            root_comments = []

            # First pass: Create dictionary of all comments
            for comment in comments:
                comment["replies"] = []
                comment["depth"] = 0
                comment_dict[comment["_id"]] = comment

            # Second pass: Build the tree structure
            for comment in comments:
                if comment["parent_id"]:
                    parent = comment_dict.get(comment["parent_id"])
                    if parent:
                        comment["depth"] = parent["depth"] + 1
                        parent["replies"].append(comment)
                else:
                    root_comments.append(comment)

            # Sort replies by created_at
            for comment in comments:
                comment["replies"].sort(key=lambda x: x["created_at"], reverse=True)

            return {
                "comments": root_comments, 
                "total_comments": len(comments),
                "status": 200
            }
        except Exception as e:
            return {"message": str(e), "status": 500}
