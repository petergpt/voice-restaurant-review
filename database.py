import os
import psycopg2
from psycopg2.extras import DictCursor

DB_URL = os.getenv("REPLIT_DB_URL")

def get_connection():
    return psycopg2.connect(DB_URL, cursor_factory=DictCursor)

def insert_survey_record(user_id, recording_time, recording_length, mp3_file, transcribed_mp3, summarized_output, additional_metadata=None):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO surveys (
        user_id,
        recording_time,
        recording_length,
        mp3_file,
        transcribed_mp3,
        summarized_output,
        additional_metadata
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (user_id, recording_time, recording_length, mp3_file, transcribed_mp3, summarized_output, additional_metadata))
    connection.commit()
    cursor.close()
    connection.close()

def get_survey_records(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM surveys WHERE user_id = %s"
    cursor.execute(query, (user_id,))

    records = cursor.fetchall()
    cursor.close()
    connection.close()

    return records