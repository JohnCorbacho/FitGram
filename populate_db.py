import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect("local_database.db")
cursor = conn.cursor()

# SQL script as a multi-line string
sql_script = """
-- Insert data into SensorTypes table
INSERT INTO SensorTypes (SensorId, Name, Units)
VALUES 
  ('sensor3', 'Temperature', 'Celsius'),
  ('sensor1', 'Heart Rate', 'bpm'),
  ('sensor2', 'Step Count', 'steps');

-- Insert data into Users table
INSERT INTO Users (UserId, Name, Username, ImageUrl, DateOfBirth)
VALUES 
  ('user3', 'Charlie Brown', 'charlieb', 'http://example.com/images/charlie.jpg', '1992-11-05'),
  ('user1', 'Alice Johnson', 'alicej', 'http://example.com/images/alice.jpg', '1990-01-15'),
  ('user2', 'Bob Smith', 'bobsmith', 'http://example.com/images/bob.jpg', '1985-06-20');

-- Insert data into Workouts table
INSERT INTO Workouts (WorkoutId, UserId, StartTimestamp, EndTimestamp, StartLocationLat, StartLocationLong, EndLocationLat, EndLocationLong, TotalDistance, TotalSteps, CaloriesBurned)
VALUES 
  ('workout1', 'user1', '2024-07-29T07:00:00', '2024-07-29T08:00:00', 37.7749, -122.4194, 37.8049, -122.421, 5.0, 8000, 400.0),
  ('workout3', 'user3', '2024-07-29T18:00:00', '2024-07-29T19:00:00', 34.0522, -118.2437, 34.0622, -118.243, 4.0, 7000, 350.0),
  ('workout2', 'user2', '2024-07-29T09:00:00', '2024-07-29T10:00:00', 40.7128, -74.006, 40.7308, -73.9976, 6.5, 10000, 500.0);

-- Insert data into SensorData table
INSERT INTO SensorData (SensorId, WorkoutId, Timestamp, SensorValue)
VALUES 
  ('sensor1', 'workout3', '2024-07-29T18:20:00', 130.0),
  ('sensor1', 'workout1', '2024-07-29T07:15:00', 120.0),
  ('sensor1', 'workout2', '2024-07-29T09:20:00', 115.0),
  ('sensor2', 'workout2', '2024-07-29T09:40:00', 5000.0),
  ('sensor2', 'workout1', '2024-07-29T07:30:00', 3000.0),
  ('sensor2', 'workout3', '2024-07-29T18:40:00', 6000.0),
  ('sensor3', 'workout3', '2024-07-29T18:50:00', 36.8),
  ('sensor3', 'workout2', '2024-07-29T09:55:00', 37.0),
  ('sensor3', 'workout1', '2024-07-29T07:45:00', 36.5);

-- Insert data into Posts table
INSERT INTO Posts (PostId, AuthorId, Timestamp, ImageUrl, Content)
VALUES 
  ('post3', 'user3', '2024-07-29T15:00:00', 'http://example.com/posts/post3.jpg', NULL),
  ('post1', 'user1', '2024-07-29T12:00:00', 'http://example.com/posts/post1.jpg', NULL),
  ('post2', 'user2', '2024-07-29T13:30:00', 'http://example.com/posts/post2.jpg', NULL);

-- Insert data into Friends table
INSERT INTO Friends (UserId1, UserId2)
VALUES 
  ('user2', 'user3'),
  ('user1', 'user3'),
  ('user1', 'user2');
"""

cursor.executescript(sql_script)
conn.commit()
conn.close()

print("Database populated successfully!")
