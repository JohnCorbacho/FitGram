#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
import os
from modules import display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts
from community_page import community_page
from activity_page import activity_page
from weather_advice import get_weather_data, get_ai_advice, get_ai_advice_workout

userId = 'user1'
st.set_page_config(layout="wide")

def display_app_page():
    """Displays the home page of the app."""

    #Fetch user Posts
    user_profile = get_user_profile(userId)
    user_posts = get_user_posts(userId)
    # Fetch Recent Workouts
    workouts_list = get_user_workouts(userId)
    # Fetch GenAI advice using the current user id
    advice_data = get_genai_advice(userId)

    # Create two columns: main, weather
    main_col, weather_col = st.columns([2, 1])

    # --- Center Column: Main Content ---
    with main_col:
        st.title('Welcome to CIS 4993!')
        for post in user_posts:
            full_name = user_profile.get("full_name", userId)
            display_post(
                username=full_name,  
                user_image=user_profile["profile_image"],
                timestamp=post["timestamp"],  
                content=post["content"],  
                post_image=post["image"] 
            )
        # Display Activity Summary
        workouts = get_user_workouts(userId)
        display_activity_summary(workouts)
        
        # Display Recent Workouts
        display_recent_workouts(workouts_list)
        
        # Pass the advice data (timestamp, content, image) to the display function
        display_genai_advice(advice_data['timestamp'], advice_data['content'], advice_data['image'])


    # --- Right Column: Weather ---
    with weather_col:
        api_key = os.getenv("WEATHER_API_KEY")
        st.header("⛅ Weather")
        city = st.text_input(label="What is your city?",value="Miami")
        if st.button("Submit") and city:
            weather = get_weather_data(city, api_key)
            
            if weather:
                st.write(f"Weather in {weather['city']}: {weather['description']} and {weather['temp']}°F")
                advice = get_ai_advice(weather)
                st.success(advice)
            else:
                st.error("Could not fetch weather data for that city.")
        st.header("🏋️‍♂️ Workout Split")
        workout = st.text_input(label="What muscle do you wish to hit?",value="Chest")
        if st.button("Lets do it!") and workout:
            workout = get_ai_advice_workout(workout)
            st.success(workout)

# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    user_profile = get_user_profile(userId)  # Already exists

    with st.sidebar:
        st.markdown("""
    <style>
    /* Sidebar radio labels – font styling */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
        padding: 15px 4px;
    }
    </style>
    """, unsafe_allow_html=True)

    #display_app_page()
        st.image(user_profile.get("profile_image", ""), width=100)
        st.markdown(f"### {user_profile.get('full_name', 'User')}")
        st.markdown("---")  # Optional separator

    page = st.sidebar.radio("Select a Page", ["🏠 Home", "👥 Community", "🏃 Activity"])

    
    if page == "🏠 Home":
        display_app_page()
    elif page == "👥 Community":
        community_page(userId)
    elif page == "🏃 Activity":
        activity_page(userId)
