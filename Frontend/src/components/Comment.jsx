import React, { useState } from "react";
import axios from "axios";

// Recursive comment component for displaying nested replies
const Comment = ({ comment, postId, onReplySuccess }) => {
  const [isReplying, setIsReplying] = useState(false);
  const [replyContent, setReplyContent] = useState("");

  const handleReply = async () => {
    try {
      const token = localStorage.getItem("token");
      const mongoLikeId = postId.toString().padStart(24, "0");

      await axios.post(
        "http://localhost:5000/comments",
        {
          post_id: mongoLikeId,
          content: replyContent,
          parent_id: comment._id,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      setReplyContent("");
      setIsReplying(false);
      onReplySuccess();
    } catch (error) {
      console.error("Reply failed:", error);
    }
  };

  return (
    <div className="ml-4 mt-4">
      <div className="bg-gray-50 p-4 rounded-lg border-l-4 border-blue-500">
        <div className="flex items-center gap-2 mb-2">
          <span className="font-semibold text-blue-600">
            {comment.username || "Anonymous"}
          </span>
          <span className="text-xs text-gray-500">•</span>
          <span className="text-xs text-gray-500">
            {new Date(comment.created_at).toLocaleDateString()}
          </span>
        </div>
        <p className="text-gray-700 mb-2">{comment.content}</p>
        <div className="mt-2 text-sm text-gray-500">
          <button
            onClick={() => setIsReplying(!isReplying)}
            className="text-blue-500 hover:underline flex items-center gap-1"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6"
              />
            </svg>
            Reply
          </button>
        </div>

        {isReplying && (
          <div className="mt-2 flex gap-2">
            <input
              type="text"
              value={replyContent}
              onChange={(e) => setReplyContent(e.target.value)}
              className="flex-1 p-2 border rounded"
              placeholder="Write a reply..."
            />
            <button
              onClick={handleReply}
              className="bg-blue-500 text-white px-4 py-2 rounded"
            >
              Send
            </button>
          </div>
        )}

        {comment.replies && comment.replies.length > 0 && (
          <div className="mt-4 space-y-4">
            {comment.replies.map((reply) => (
              <Comment
                key={reply._id}
                comment={reply}
                postId={postId}
                onReplySuccess={onReplySuccess}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Comment;
