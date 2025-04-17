import streamlit as st
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile


def fetch_friend_posts(user_id):
    """
    Fetch the first 10 posts from a user's friends ordered by timestamp (descending).
    This function uses get_user_profile to get the friend list and get_user_posts for each friend.
    """
    # Get the current user's profile to retrieve the friends list.
    profile = get_user_profile(user_id)
    friend_ids = profile.get("friends", [])
    all_posts = []

    # For each friend, get their posts and attach the friend's full name to each post.
    for fid in friend_ids:
        posts = get_user_posts(fid)
        friend_profile = get_user_profile(fid)
        friend_name = friend_profile.get("full_name", fid)
        for post in posts:
            post["friend_name"] = friend_name
        all_posts.extend(posts)

    # Sort posts by timestamp descending
    # (Assumes timestamp is in a sortable string format like ISO 8601)
    all_posts.sort(key=lambda p: p["timestamp"], reverse=True)

    return all_posts[:10]


def community_page(user_id):
    """
    Renders the Community Page:
    - Shows the first 10 posts from the user's friends ordered by timestamp.
    - Displays one piece of GenAI advice and encouragement.
    """
    st.title("Community Hub")

    # Display Friends' Posts Section
    st.header("Friends' Posts")
    friend_posts = fetch_friend_posts(user_id)
    if friend_posts:
        for post in friend_posts:
            st.subheader(f"{post.get('friend_name', 'Unknown')}")
            st.write(f"**Timestamp:** {post.get('timestamp')}")
            st.write(post.get("content"))
            if post.get("image") and post.get("image").startswith("http"):
                st.image(post.get("image"), use_container_width=True)
            st.markdown("---")
    else:
        st.write("Your friends haven't posted anything yet.")

    # Display GenAI Advice Section
    st.header("Today's Encouragement")
    advice = get_genai_advice(user_id)
    st.write(f"**Timestamp:** {advice.get('timestamp')}")
    st.write(advice.get("content"))
    if advice.get("image"):
        st.image(advice.get("image"), use_container_width=True)


if __name__ == "__main__":
    # For testing purposes, we use a hard-coded user id.
    community_page("user1")
