// Post list component with commenting functionality
import React, { useState, useEffect } from "react";
import axios from "axios";
import Comment from "./Comment";

// Helper function to convert numeric ID to MongoDB-like ObjectId
const generateMongoLikeId = (numericId) => {
  return numericId.toString().padStart(24, "0");
};

const Posts = () => {
  const [posts, setPosts] = useState([]);
  const [comments, setComments] = useState({});
  const [newComments, setNewComments] = useState({}); // Change to object for per-post comments
  const [commentError, setCommentError] = useState("");

  useEffect(() => {
    const fetchPosts = async () => {
      const response = await axios.get("https://dummyjson.com/posts?limit=10");
      setPosts(response.data.posts);
    };
    fetchPosts();
  }, []);

  useEffect(() => {
    const fetchComments = async (postId) => {
      try {
        const token = localStorage.getItem("token");
        const mongoLikeId = generateMongoLikeId(postId);
        const response = await axios.get(
          `http://localhost:5000/comments/${mongoLikeId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        setComments((prev) => ({
          ...prev,
          [postId]: response.data.comments,
        }));
      } catch (error) {
        console.error("Failed to fetch comments:", error);
      }
    };

    posts.forEach((post) => fetchComments(post.id));
  }, [posts]);

  const handleComment = async (postId) => {
    try {
      setCommentError("");
      const token = localStorage.getItem("token");
      const comment = newComments[postId] || "";

      if (!comment.trim()) {
        setCommentError("Comment cannot be empty");
        return;
      }

      const mongoLikeId = generateMongoLikeId(postId);

      const response = await axios.post(
        `http://localhost:5000/comments`,
        {
          post_id: mongoLikeId,
          content: comment,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      // Clear only this post's comment
      setNewComments((prev) => ({
        ...prev,
        [postId]: "",
      }));
      await fetchPostComments(postId);
    } catch (error) {
      console.error("Comment failed:", error.response?.data || error);
      setCommentError(error.response?.data?.message || "Failed to add comment");
    }
  };

  const fetchPostComments = async (postId) => {
    try {
      const token = localStorage.getItem("token");
      const mongoLikeId = generateMongoLikeId(postId);
      const response = await axios.get(
        `http://localhost:5000/comments/${mongoLikeId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setComments((prev) => ({
        ...prev,
        [postId]: response.data.comments,
      }));
    } catch (error) {
      console.error("Failed to fetch comments:", error);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      {posts.map((post) => (
        <div key={post.id} className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-2xl font-bold mb-2">{post.title}</h2>
          <p className="text-gray-600 mb-4">{post.body}</p>

          <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
            <div className="flex space-x-4">
              <span>👁️ {post.views} views</span>
              <span>👍 {post.reactions?.likes || 0}</span>
              <span>👎 {post.reactions?.dislikes || 0}</span>
            </div>
            <div className="flex space-x-2">
              {post.tags.map((tag) => (
                <span key={tag} className="bg-gray-200 px-2 py-1 rounded">
                  {tag}
                </span>
              ))}
            </div>
          </div>

          <div className="border-t pt-4">
            <div className="flex flex-col gap-2 mb-4">
              {commentError && (
                <div className="text-red-500 text-sm">{commentError}</div>
              )}
              <div className="flex gap-2">
                <input
                  type="text"
                  value={newComments[post.id] || ""}
                  onChange={(e) =>
                    setNewComments((prev) => ({
                      ...prev,
                      [post.id]: e.target.value,
                    }))
                  }
                  placeholder="Add a comment..."
                  className="flex-1 p-2 border rounded"
                />
                <button
                  onClick={() => handleComment(post.id)}
                  className="bg-blue-500 text-white px-4 py-2 rounded"
                >
                  Comment
                </button>
              </div>
            </div>

            <div className="mt-4">
              {comments[post.id]?.map((comment) => (
                <Comment
                  key={comment._id}
                  comment={comment}
                  postId={post.id} // Add this line
                  onReplySuccess={() => {
                    // Refresh comments for this post
                    const token = localStorage.getItem("token");
                    const mongoLikeId = generateMongoLikeId(post.id);
                    axios
                      .get(`http://localhost:5000/comments/${mongoLikeId}`, {
                        headers: {
                          Authorization: `Bearer ${token}`,
                        },
                      })
                      .then((response) => {
                        setComments((prev) => ({
                          ...prev,
                          [post.id]: response.data.comments,
                        }));
                      });
                  }}
                />
              ))}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Posts;
