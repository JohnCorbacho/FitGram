import sqlite3

def create_database():
    # Connect to (or create) the SQLite database file
    conn = sqlite3.connect("local_database.db")
    cursor = conn.cursor()

    # Create SensorTypes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SensorTypes (
            SensorId STRING PRIMARY KEY,
            Name STRING NOT NULL,
            Units STRING NOT NULL
        )
    """)

    # Create SensorData table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SensorData (
            SensorId STRING,
            WorkoutId STRING,
            Timestamp DATETIME NOT NULL,
            SensorValue FLOAT NOT NULL,
            PRIMARY KEY (SensorId, WorkoutId),
            FOREIGN KEY (SensorId) REFERENCES SensorTypes(SensorId),
            FOREIGN KEY (WorkoutId) REFERENCES Workouts(WorkoutId)
        )
    """)

    # Create Workouts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Workouts (
            WorkoutId STRING PRIMARY KEY,
            UserId STRING NOT NULL,
            StartTimestamp DATETIME NOT NULL,
            EndTimestamp DATETIME NOT NULL,
            StartLocationLat FLOAT NOT NULL,
            StartLocationLong FLOAT NOT NULL,
            EndLocationLat FLOAT NOT NULL,
            EndLocationLong FLOAT NOT NULL,
            TotalDistance FLOAT NOT NULL,
            TotalSteps INTEGER NOT NULL,
            CaloriesBurned FLOAT NOT NULL,
            FOREIGN KEY (UserId) REFERENCES Users(UserId)
        )
    """)

    # Create Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            UserId STRING PRIMARY KEY,
            Name STRING NOT NULL,
            Username STRING UNIQUE NOT NULL,
            ImageUrl STRING,
            DateOfBirth DATE NOT NULL
        )
    """)

    # Create Posts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Posts (
            PostId STRING PRIMARY KEY,
            AuthorId STRING NOT NULL,
            Timestamp DATETIME NOT NULL,
            ImageUrl STRING,
            Content STRING,
            FOREIGN KEY (AuthorId) REFERENCES Users(UserId)
        )
    """)

    # Create Friends table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Friends (
            UserId1 STRING NOT NULL,
            UserId2 STRING NOT NULL,
            PRIMARY KEY (UserId1, UserId2),
            FOREIGN KEY (UserId1) REFERENCES Users(UserId),
            FOREIGN KEY (UserId2) REFERENCES Users(UserId)
        )
    """)

    conn.commit()
    conn.close()
    print("Database schema created successfully.")

if __name__ == "__main__":
    create_database()
