#############################################################################
# data_fetcher_test.py
#
# This file contains tests for data_fetcher.py.
#
# You will write these tests in Unit 3.
#############################################################################

import os

# Only do this in CI (like GitHub Actions)
if "BQ_SERVICE_ACCOUNT" in os.environ:
    credentials_path = "/tmp/bq_key.json"
    with open(credentials_path, "w") as f:
        f.write(os.environ["BQ_SERVICE_ACCOUNT"])
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

import unittest
import datetime
from data_fetcher import get_genai_advice
from data_fetcher import get_user_sensor_data
from data_fetcher import get_user_posts
from unittest.mock import MagicMock

    
from google.cloud import bigquery



# Mocked data for SensorData query result
mock_sensor_data = [
    {"SensorId": 1, "Timestamp": "2024-07-29T07:15:00", "SensorValue": 25.5},
    {"SensorId": 2, "Timestamp": "2024-07-29T07:16:00", "SensorValue": 30.0},
]

# Mocked data for SensorTypes query result
mock_sensor_types = [
    {"SensorId": 1, "sensor_type": "Accelerometer", "units": "m/s^2"},
    {"SensorId": 2, "sensor_type": "Gyroscope", "units": "rad/s"},
]
class TestDataFetcher(unittest.TestCase):

    def test_foo(self):
        """Tests foo."""
        pass

    def setUp(self):
            # Setup the mock BigQuery client
            self.mock_bigquery_client = MagicMock(spec=bigquery.Client)
            
            # Mock the query results for SensorData and SensorTypes
            self.mock_bigquery_client.query.return_value.result.return_value = mock_sensor_data  # For SensorData
            self.mock_bigquery_client.query.side_effect = [
                mock_sensor_data,  # First query result (SensorData)
                mock_sensor_types,  # Second query result (SensorTypes)
            ]
    
    def test_get_user_sensor_data(self):
        # Define test inputs
        workout_id = "workout123"
        user_id = "user456"
         
        # Call the function with the mock BigQuery client
        result = get_user_sensor_data(user_id, workout_id)
         
        # Expected result after combining SensorData and SensorTypes
        expected_result = [
            {"sensor_type": "Accelerometer", "timestamp": "2024-07-29T07:15:00", "data": 25.5, "units": "m/s^2"},
            {"sensor_type": "Gyroscope", "timestamp": "2024-07-29T07:16:00", "data": 30.0, "units": "rad/s"},
        ]
         
        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)
 
        # Verify the queries that were executed
        self.mock_bigquery_client.query.assert_any_call(
            f"SELECT SensorId, Timestamp, SensorValue FROM `alien-span-454620-m0.CIS4993.SensorData` WHERE WorkoutId = '{workout_id}' ORDER BY Timestamp"
        )
        self.mock_bigquery_client.query.assert_any_call(
            f"SELECT SensorId, Name AS sensor_type, Units AS units FROM `alien-span-454620-m0.CIS4993.SensorTypes` WHERE SensorId IN (1, 2)"
        )



class TestDataFetcher(unittest.TestCase):

    def test_foo(self):
        """Tests foo."""
        pass

class TestGetUserPosts(unittest.TestCase):
    """Tests for the get_user_posts function."""

    def test_returns_list(self):
        """Test that get_user_posts returns a list."""
        from data_fetcher import get_user_posts
        posts = get_user_posts("user1")
        self.assertIsInstance(posts, list)

    def test_posts_have_required_fields(self):
        """Test that each post has the required keys."""
        from data_fetcher import get_user_posts
        posts = get_user_posts("user1")
        if posts:
            post = posts[0]
            self.assertIn("user_id", post)
            self.assertIn("post_id", post)
            self.assertIn("timestamp", post)
            self.assertIn("content", post)
            self.assertIn("image", post)

    def test_unknown_user_returns_empty_list(self):
        """Test that an unknown user returns an empty list."""
        from data_fetcher import get_user_posts
        posts = get_user_posts("unknown_user_xyz")
        self.assertIsInstance(posts, list)
        self.assertEqual(len(posts), 0)
    



class TestGetGenAiAdvice(unittest.TestCase):
    """Tests for the get_genai_advice function."""

    def test_returns_dictionary_with_keys(self):
        """Test that get_genai_advice returns a dictionary with the required keys."""
        advice = get_genai_advice("user1")
        self.assertIsInstance(advice, dict)
        expected_keys = {"advice_id", "timestamp", "content", "image"}
        self.assertTrue(expected_keys.issubset(advice.keys()),
                        f"Returned dictionary keys: {advice.keys()} do not include all expected keys: {expected_keys}")

    def test_content_is_non_empty(self):
        """Test that the content field in the returned dictionary is a non-empty string."""
        advice = get_genai_advice("user1")
        content = advice.get("content", "").strip()
        self.assertIsInstance(content, str)
        self.assertNotEqual(content, "", "The advice content should not be empty.")

    def test_timestamp_format(self):
        """Test that the timestamp is formatted as 'YYYY-MM-DD HH:MM:SS'."""
        advice = get_genai_advice("user1")
        timestamp = advice.get("timestamp", "")
        try:
            datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            self.fail("Timestamp format is incorrect; expected 'YYYY-MM-DD HH:MM:SS'.")

    def test_invalid_user_raises_value_error(self):
        """Test that providing a non-existent user ID raises a ValueError."""
        with self.assertRaises(ValueError):
            get_genai_advice("nonexistent_user")

if __name__ == "__main__":
    unittest.main()
