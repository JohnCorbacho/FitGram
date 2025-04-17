#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################
import streamlit as st
from internals import create_component
from dotenv import load_dotenv


# This one has been written for you as an example. You may change it as wanted.
def display_my_custom_component(value):
    """Displays a 'my custom component' which showcases an example of how custom
    components work.

    value: the name you'd like to be called by within the app
    """
    # Define any templated data from your HTML file. The contents of
    # 'value' will be inserted to the templated HTML file wherever '{{NAME}}'
    # occurs. You can add as many variables as you want.
    data = {
        'NAME': value,
    }
    # Register and display the component by providing the data and name
    # of the HTML file. HTML must be placed inside the "custom_components" folder.
    html_file_name = "my_custom_component"
    create_component(data, html_file_name)


def display_post(username, user_image, timestamp, content, post_image=None):
    """
    Displays a user post on the Steamlit app

    Parameters:

    String username -> The user's name
    String user_image -> The URL of the user's profile image
    String timestamp -> The timestamp of the post
    String content -> The post content text
    String post_image -> URL to a post image (This field is optional)

    
    """
     # Default profile fallback
    default_profile_image = "https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png"
    profile_image = user_image if user_image and user_image.startswith("http") else default_profile_image

    # Post image HTML (optional)
    post_image_html = ""
    if post_image and isinstance(post_image, str) and post_image.startswith("http"):
        post_image_html = f"<img src='{post_image}' style='width:100%; margin-top:15px; border-radius:8px;'>"

    # HTML block with everything inside
    post_html = f"""
    <div style='
        background-color: #2f2f2f;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    '>
        <div style='display: flex; align-items: center; gap: 15px;'>
            <img src="{profile_image}" width="80" height="80" style="border-radius: 50%;">
            <div>
                <h4 style='margin: 0; color: white;'>{username}</h4>
                <p style='margin: 2px 0; color: #ccc;'>{timestamp}</p>
            </div>
        </div>
        <p style='margin-top: 15px; color: white;'>{content}</p>
        {post_image_html}
    </div>
    """

    st.markdown(post_html, unsafe_allow_html=True)
    


def display_activity_summary(workouts):
    """Displays a user’s activity summary.""" # Line written by ChatGPT
    if not workouts:
        st.warning("No workouts available.")
        return

    total_distance = sum(w['distance'] for w in workouts)
    total_steps = sum(w['steps'] for w in workouts)
    total_calories = sum(w['calories_burned'] for w in workouts)

    st.subheader("Activity Summary") # Line written by ChatGPT
    st.metric(label="Total Distance (miles)", value=total_distance) # Line written by ChatGPT
    st.metric(label="Total Steps", value=total_steps) # Line written by ChatGPT
    st.metric(label="Total Calories Burned", value=total_calories)# Line written by ChatGPT


def display_recent_workouts(workouts_list):
    """Displays recent workouts in rectangles."""
    st.title("Recent Workouts")

    for workout in workouts_list:
        start_timestamp = str(workout["start_timestamp"]).replace("T", " ")
        end_timestamp = str(workout["end_timestamp"]).replace("T", " ")

        date = start_timestamp.split()[0]
        start_time = start_timestamp.split()[1]
        end_time = end_timestamp.split()[1]

        # Extract hours and minutes
        #start_h, start_m, _ = map(int, start_time.split(":"))
        #end_h, end_m, _ = map(int, end_time.split(":"))

        #Added for testing
        start_parts = start_time.split(":")
        start_h = int(start_parts[0])
        start_m = int(start_parts[1])
        start_s = int(start_parts[2].split("+")[0])

        #Added for testing
        end_parts = end_time.split(":")
        end_h = int(end_parts[0])
        end_m = int(end_parts[1])
        end_s = int(end_parts[2].split("+")[0])


        # Calculate duration directly
        duration = (end_h * 60 + end_m) - (start_h * 60 + start_m)

        with st.container():
            st.markdown(
                f"""
                <div style="padding: 15px; border-radius: 10px; background-color: #333333; margin-bottom: 10px;">
                    <strong>Workout ID:</strong> {workout["workout_id"]} <br>
                    <strong>Date:</strong> {date} <br>
                    <strong>Duration:</strong> {duration} minutes ({start_time} - {end_time}) <br>
                    <strong>Distance:</strong> {workout["distance"]} km <br>
                    <strong>Calories:</strong> {workout["calories_burned"]} kcal
                </div>
                """,
                unsafe_allow_html=True
            )


def display_genai_advice(timestamp, content, image):
    """
    Displays GenAI-created advice on the Streamlit app.
    
    Parameters:
        timestamp (str): The timestamp of when the advice was generated.
        content (str): The advice content text.
        image (str): URL to an image. If None, no image is displayed.
    """
    st.header("GenAI Advice")
    st.write(f"**Timestamp:** {timestamp}")
    st.write(content)
    
    # Provide a default image if none is returned
    default_image_url = 'https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    image_to_display = image if image else default_image_url
    st.image(image_to_display, caption="Motivational Image", use_container_width=True)
