import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request


CREATE_BOOKMARKS_TABLE = (
    "CREATE TABLE IF NOT EXISTS bookmarks ( id SERIAL PRIMARY KEY, name TEXT, url VARCHAR, folder_id INTEGER NULL, created_at TIMESTAMP, updated_at TIMESTAMP, FOREIGN KEY (folder_id) REFERENCES folders(id) ON DELETE CASCADE);"
)

CREATE_FOLDERS_TABLE = """"CREATE TABLE IF NOT EXISTS folders (id SERIAL PRIMARY KEY, name TEXT, description TEXT, created_at TIMESTAMP, updated_at TIMESTAMP);"""

INSERT_BOOKMARK_RETURN_ID = "INSERT INTO bookmarks (name, url) VALUES (%s, %s) RETURNING id;"

INSERT_FOLDER_RETURN_ID = (
    "INSERT INTO folders (name, description) VALUES (%s, %s) RETURNING id;")

load_dotenv()  # loads variables from .env file into environment

app = Flask(__name__)
url = os.environ.get("DATABASE_URL")  # gets variables from environment
connection = psycopg2.connect(url)


@app.route("/", methods=['GET'])
def index():
    return "Hello World!"


@app.route("/api/v1/bookmarks", methods=['POST'])
def create_bookmark():
    data = request.get_json()
    name = data["name"]
    url = data["url"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_BOOKMARKS_TABLE)
            cursor.execute(INSERT_BOOKMARK_RETURN_ID, (name, url))
            bookmark_id = cursor.fetchone()[0]

    return {"id": bookmark_id, "message": f"Bookmark {name} has been created."}, 201


if __name__ == "__main__":
    app.run(debug=True)
