import os
import random
import datetime
import requests
import pandas
#from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel

# Only do this in CI (like GitHub Actions)
if "BQ_SERVICE_ACCOUNT" in os.environ:
    credentials_path = "/tmp/bq_key.json"
    with open(credentials_path, "w") as f:
        f.write(os.environ["BQ_SERVICE_ACCOUNT"])
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path


from google.cloud import bigquery

#load_dotenv()

# Get project and dataset IDs from environment variables.
PROJECT_ID = "alien-span-454620-m0"
DATASET_ID = "CIS4993"

# Initialize BigQuery client once
bq_client = bigquery.Client(project="alien-span-454620-m0")

def get_user_sensor_data(user_id, workout_id):
    """
    Returns a list of timestamped sensor data for a given workout from BigQuery.
    Combines sensor readings with their sensor type and units.
    """
    query = f"""
        SELECT sd.SensorId, sd.Timestamp, sd.SensorValue, st.Name AS SensorType, st.Units
        FROM `{PROJECT_ID}.{DATASET_ID}.SensorData` sd
        JOIN `{PROJECT_ID}.{DATASET_ID}.SensorTypes` st
          ON sd.SensorId = st.SensorId
        WHERE sd.WorkoutId = @workout_id
        ORDER BY sd.Timestamp
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("workout_id", "STRING", workout_id)]
    )
    results = bq_client.query(query, job_config=job_config).result()

    sensor_data_list = []
    for row in results:
        sensor_data_list.append({
            "sensor_type": row["SensorType"],
            "timestamp": row["Timestamp"],
            "data": row["SensorValue"],
            "units": row["Units"]
        })
    return sensor_data_list

def get_user_workouts(user_id):
    """
    Returns a list of the user's workouts from BigQuery.
    """
    query = f"""
        SELECT WorkoutId, StartTimestamp, EndTimestamp, StartLocationLat, StartLocationLong,
               EndLocationLat, EndLocationLong, TotalDistance, TotalSteps, CaloriesBurned
        FROM `{PROJECT_ID}.{DATASET_ID}.Workouts`
        WHERE UserId = @user_id
        ORDER BY StartTimestamp DESC
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("user_id", "STRING", user_id)]
    )
    results = bq_client.query(query, job_config=job_config).result()

    workouts = []
    for row in results:
        workouts.append({
            'workout_id': row["WorkoutId"],
            'start_timestamp': row["StartTimestamp"],
            'end_timestamp': row["EndTimestamp"],
            'start_lat_lng': (row["StartLocationLat"], row["StartLocationLong"]),
            'end_lat_lng': (row["EndLocationLat"], row["EndLocationLong"]),
            'distance': row["TotalDistance"],
            'steps': row["TotalSteps"],
            'calories_burned': row["CaloriesBurned"],
        })
    return workouts

def get_user_profile(user_id):
    """
    Returns user profile data along with their friends' user IDs from BigQuery.
    Assumes that the Users table contains columns: UserId, Name, Username, ImageUrl, DateOfBirth,
    and that the Friends table has columns: UserId1 and UserId2.
    """
    # Fetch user details
    query = f"""
        SELECT Name, Username, DateOfBirth, ImageUrl
        FROM `{PROJECT_ID}.{DATASET_ID}.Users`
        WHERE UserId = @user_id
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("user_id", "STRING", user_id)]
    )
    result = bq_client.query(query, job_config=job_config).result().to_dataframe()
    if result.empty:
        return {}
    
    user_data = result.iloc[0].to_dict()

    # Fetch friends' user IDs using the modified query
    friends_query = f"""
        SELECT 
            CASE 
                WHEN UserId1 = @user_id THEN UserId2 
                ELSE UserId1 
            END AS friend_id
        FROM `{PROJECT_ID}.{DATASET_ID}.Friends`
        WHERE UserId1 = @user_id OR UserId2 = @user_id
    """
    friends_job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("user_id", "STRING", user_id)]
    )
    friends_df = bq_client.query(friends_query, job_config=friends_job_config).result().to_dataframe()
    friend_ids = friends_df["friend_id"].tolist() if not friends_df.empty else []
    
    return {
        "full_name": user_data["Name"],
        "username": user_data["Username"],
        "date_of_birth": user_data["DateOfBirth"],
        "profile_image": user_data["ImageUrl"],
        "friends": friend_ids
    }

def get_user_posts(user_id):
    """
    Returns a list of posts for the given user from BigQuery.
    Assumes Posts table has columns: PostId, AuthorId, Timestamp, Content, ImageUrl.
    """
    query = f"""
        SELECT PostId, AuthorId, Timestamp, Content, ImageUrl
        FROM `{PROJECT_ID}.{DATASET_ID}.Posts`
        WHERE AuthorId = @user_id
        ORDER BY Timestamp DESC
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("user_id", "STRING", user_id)]
    )
    results = bq_client.query(query, job_config=job_config).result()
    
    posts = []
    for row in results:
        posts.append({
            "user_id": row["AuthorId"],
            "post_id": row["PostId"],
            "timestamp": row["Timestamp"],
            "content": row["Content"],
            "image": row["ImageUrl"],
        })
    return posts

def get_genai_advice(user_id):
    """
    Returns the most recent advice from the Vertex AI model based on the user's information.
    Images should not be populated 100% of the time.
    Output: A dictionary with the keys: advice_id, timestamp, content, and image.
    """
    # Fetch user details from BigQuery
    query = f"""
        SELECT Name
        FROM `{PROJECT_ID}.{DATASET_ID}.Users`
        WHERE UserId = @user_id
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("user_id", "STRING", user_id)]
    )
    result_df = bq_client.query(query, job_config=job_config).result().to_dataframe()
    if result_df.empty:
        raise ValueError(f"User {user_id} not found.")
    
    user_name = result_df.iloc[0]["Name"]

    # Craft a personalized prompt
    prompt_text = f"Provide a single-sentence motivational fitness advice for {user_name}."

    # Initialize Vertex AI (using production credentials)
    vertexai.init(project=PROJECT_ID, location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-002")  # Your chosen Vertex AI model

    try:
        response = model.generate_content(prompt_text)
        advice_text = response.text.strip()
        if not advice_text:
            advice_text = "Stay motivated and keep up the good work!"
    except Exception as e:
        print(f"Error calling Vertex AI: {e}")
        advice_text = "Stay strong and keep pushing forward!"

    # Randomize image inclusion (50% chance)
    image_url_candidates = [
        "https://strongviking.com/wp-content/uploads/2024/09/1.jpg",
        "https://strongviking.com/wp-content/uploads/2024/09/5.jpg"
    ]
    image = random.choice(image_url_candidates) if random.random() < 0.5 else None

    return {
        "advice_id": f"advice_{user_id}_{int(datetime.datetime.now().timestamp())}",
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "content": advice_text,
        "image": image
    }
