import streamlit as st
from data_fetcher import get_user_workouts, get_user_posts, get_user_profile
from google.cloud import bigquery

# Initialize BigQuery client
client = bigquery.Client(project="alien-span-454620-m0")

# Function to insert a post into BigQuery
def insert_post(user_id, content):
    # Inserts a new post into the 'posts' table in BigQuery.
    
    query = """
    INSERT INTO `alien-span-454620-m0.CIS4993.Posts` (user_id, post_id, timestamp, content, image)
    VALUES (@user_id, GENERATE_UUID(), CURRENT_TIMESTAMP(), @content, NULL)
    """
    
    query_params = [
        bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
        bigquery.ScalarQueryParameter("content", "STRING", content),
    ]

    job_config = bigquery.QueryJobConfig(query_parameters=query_params)

    # Execute the query
    client.query(query, job_config=job_config).result()  # Wait for the job to complete

    print(f"Post created for user {user_id} with content: {content}")

# Function to display the activity page
def activity_page(user_id):
    """
    Renders the Activity Page:
    - Shows the 3 most recent workouts.
    - Displays an activity summary.
    - Allows the user to share a workout statistic as a post.
    """
    st.title(f"Activity Page for {user_id}")

    # Get the user's workouts
    workouts = get_user_workouts(user_id)
    recent_workouts = workouts[:3]  # Get the most recent 3 workouts

    # Activity summary (total distance, steps, calories burned)
    activity_summary = {
        "total_distance": sum(w.get("distance", 0) for w in recent_workouts),
        "total_steps": sum(w.get("steps", 0) for w in recent_workouts),
        "calories_burned": sum(w.get("calories_burned", 0) for w in recent_workouts),
    }

    # Display recent workouts
    st.header("Recent Workouts")
    for i, workout in enumerate(recent_workouts):
        st.subheader(f"Workout {i + 1}")
        st.write(f"**Date:** {workout.get('date')}")
        st.write(f"**Distance:** {workout.get('distance', 'N/A')} meters")
        st.write(f"**Steps:** {workout.get('steps', 'N/A')}")
        st.write(f"**Calories Burned:** {workout.get('calories_burned', 'N/A')}")
        st.markdown("---")

    # Display activity summary
    st.header("Activity Summary")
    st.write(f"**Total Distance:** {activity_summary['total_distance']} meters")
    st.write(f"**Total Steps:** {activity_summary['total_steps']} steps")
    st.write(f"**Total Calories Burned:** {activity_summary['calories_burned']} kcal")
    
    # Button to share a workout stat
    st.header("Share Your Progress!")
    share_choice = st.selectbox(
        "What would you like to share?",
        ["Total Steps", "Total Distance", "Calories Burned"]
    )
    
    # Form for sharing
    if st.button("Share"):
        content = ""
        if share_choice == "Total Steps":
            content = f"Look at this, I walked {activity_summary['total_steps']} steps today!"
        elif share_choice == "Total Distance":
            content = f"Check it out, I ran {activity_summary['total_distance']} meters today!"
        elif share_choice == "Calories Burned":
            content = f"Wow, I burned {activity_summary['calories_burned']} calories today!"

        # Insert post into BigQuery
        if content:
            insert_post(user_id, content)
        else:
            st.error("No statistic selected to share!")

        # Show a confirmation message
        st.success("Your progress has been shared!")

# This function can be called to render the activity page with a user ID
if __name__ == "__main__":
    if "user_id" in st.session_state:  # Check if user_id is already in session
        activity_page(st.session_state.user_id)
    else:
        st.write("You must be logged in to view the activity page.")

