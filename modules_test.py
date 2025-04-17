#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.
#############################################################################

import unittest
from streamlit.testing.v1 import AppTest
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts

# Write your tests below

class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""

    def test_display_post(self):

        try:
            display_post(
                username="TestUser",
                user_image="https://en.wikipedia.org/wiki/File:Mr._Clean_logo.png",
                timestamp="2024-03-04 10:00:00",
                content="This is a test post",
                post_image=None
            )
        except Exception as e:
            self.fail(f"display_post raised an exception unexpectedly: {e}")

class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function."""

    def setUp(self):
        """Set up sample workout data for testing."""
        self.workouts = [
            {
                'workout_id': 'workout1',
                'start_timestamp': '2024-01-01 08:00:00',
                'end_timestamp': '2024-01-01 09:00:00',
                'distance': 5.0,
                'steps': 3000,
                'calories_burned': 250,
                'start_lat_lng': (1.0, 4.0),
                'end_lat_lng': (1.1, 4.1)
            },
            {
                'workout_id': 'workout2',
                'start_timestamp': '2024-01-02 08:30:00',
                'end_timestamp': '2024-01-02 10:00:00',
                'distance': 6.5,
                'steps': 4000,
                'calories_burned': 300,
                'start_lat_lng': (1.0, 4.0),
                'end_lat_lng': (1.1, 4.1)
            }
        ]

    def test_display_activity_summary_runs(self):
        """Test that display_activity_summary runs without errors and returns None."""
        try:
            result = display_activity_summary(self.workouts)
            self.assertIsNone(result)
        except Exception as e:
            self.fail(f"display_activity_summary raised an exception unexpectedly: {e}")


class TestDisplayGenAiAdvice(unittest.TestCase):
    """Tests the display_genai_advice function."""

    def test_display_genai_advice_no_image(self):
        """Test that display_genai_advice works without an image."""
        try:
            display_genai_advice("2024-01-01 00:00:00", "Keep pushing your limits!", None)
        except Exception as e:
            self.fail(f"display_genai_advice raised an exception unexpectedly: {e}")

    def test_display_genai_advice_with_image(self):
        """Test that display_genai_advice works with an image."""
        try:
            display_genai_advice("2024-01-01 00:00:00", "Keep pushing your limits!", "http://example.com/image.png")
        except Exception as e:
            self.fail(f"display_genai_advice raised an exception unexpectedly: {e}")


class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function."""

    def setUp(self):
        """Set up the mock data for testing."""
        self.workouts_list = [
            {
                'workout_id': 'workout1',
                'start_timestamp': '2024-01-01 08:00:00',
                'end_timestamp': '2024-01-01 09:00:00',
                'start_lat_lng': (1.0, 4.0),
                'end_lat_lng': (1.1, 4.1),
                'distance': 8.2,
                'steps': 1900,
                'calories_burned': 380
            },
            {
                'workout_id': 'workout2',
                'start_timestamp': '2024-01-01 10:00:00',
                'end_timestamp': '2024-01-01 11:15:00',
                'start_lat_lng': (1.0, 4.0),
                'end_lat_lng': (1.1, 4.1),
                'distance': 6.5,
                'steps': 1500,
                'calories_burned': 250
            }
        ]

    def test_display_recent_workouts(self):
        """Test that display_recent_workouts function processes the list of workouts."""
        try:
            display_recent_workouts(self.workouts_list)
        except Exception as e:
            self.fail(f"display_recent_workouts raised an exception unexpectedly: {e}")

if __name__ == "__main__":
    unittest.main()
