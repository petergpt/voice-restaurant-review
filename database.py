import os
import psycopg2
from psycopg2.extras import DictCursor

DB_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DB_URL, cursor_factory=DictCursor)

def create_surveys_table():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS surveys (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(255) NOT NULL,
        recording_time TIMESTAMP NOT NULL,
        recording_length INTEGER NOT NULL,
        wav_file BYTEA NOT NULL,
        transcribed_wav TEXT NOT NULL,
        summarized_output TEXT NOT NULL,
        additional_metadata TEXT
    );
    """

    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

def insert_survey_record(user_id, recording_time, recording_length, wav_file, transcribed_wav, summarized_output, additional_metadata=None):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO surveys (
        user_id,
        recording_time,
        recording_length,
        wav_file,
        transcribed_wav,
        summarized_output,
        additional_metadata
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (user_id, recording_time, recording_length, psycopg2.Binary(wav_file), transcribed_wav, summarized_output, additional_metadata))
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