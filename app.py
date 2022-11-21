import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, session, jsonify
from flask_session.__init__ import Session
from datetime import datetime, timezone


load_dotenv()  # loads variables from .env file into environment

app = Flask(__name__)
url = os.environ.get("DATABASE_URL")  # gets variables from environment
app.secret_key = os.environ.get("secret_key")
connection = psycopg2.connect(url)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config.from_object(__name__)
Session(app)

CREATE_BOOKMARKS_TABLE = (
    "CREATE TABLE IF NOT EXISTS bookmarks ( id SERIAL PRIMARY KEY, name TEXT, url VARCHAR, folder_id INTEGER NULL, created_at timestamp, updated_at timestamp, FOREIGN KEY (folder_id) REFERENCES folders(id) ON DELETE CASCADE);"
)

CREATE_FOLDERS_TABLE = """CREATE TABLE IF NOT EXISTS folders (id SERIAL PRIMARY KEY, name TEXT, description TEXT, created_at timestamp, updated_at timestamp);"""

INSERT_BOOKMARK_RETURN_ID = "INSERT INTO bookmarks (name, url,created_at) VALUES (%s, %s, %s) RETURNING id;"

INSERT_FOLDER_RETURN_ID = (
    "INSERT INTO folders (name, description, created_at) VALUES (%s, %s, %s) RETURNING id;")

GET_ALL_BOOKMARKS_LIST = (""" SELECT * FROM bookmarks;""")
GET_ALL_FOLDERS_LIST = (""" SELECT * FROM folders; """)

UPDATE_BOOKMARKS = ("""UPDATE bookmarks
                    SET name = %s,
                        url = %s,
                        folder_id = %s,
                        updated_at = %s
                        WHERE id = %s ;""")

UPDATE_FOLDERS = ("""UPDATE folders
                    SET name = %s,
                        description = %s,
                        updated_at = %s
                        WHERE id = %s ;""")

DELETE_A_BOOKMARK_ROW = ("""DELETE FROM bookmarks WHERE id = %s;""")

DELETE_A_FOLDER = ("""DELETE FROM folders WHERE id = %s; """)


@app.route("/")
def index():
    return "Hello World!"


@app.route("/api/v1/bookmarks", methods=['POST'])
def create_bookmark():
    data = request.get_json()
    name = data["name"]
    url = data["url"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_FOLDERS_TABLE)
            cursor.execute(CREATE_BOOKMARKS_TABLE)
            cursor.execute(INSERT_BOOKMARK_RETURN_ID, (name, url))
            bookmark_id = cursor.fetchone()[0]

    return {"id": bookmark_id, "message": f"Bookmark {name} has been created."}, 201


@app.route("/api/v1/bookmarks", methods=['GET'])
def get_all_bookmarks():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_ALL_BOOKMARKS_LIST)
            bookmarks_list = cursor.fetchall()

    return {"bookmark_list": bookmarks_list}, 200


@app.route("/api/v1/folders", methods=['POST'])
def create_folder():
    folder_data = request.get_json()
    folder_name = folder_data["name"]
    description = folder_data["description"]
    created_at = datetime.now(timezone.utc)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_FOLDERS_TABLE)
            cursor.execute(INSERT_FOLDER_RETURN_ID,
                           (folder_name, description, created_at))
            folder_id = cursor.fetchone()[0]

    return {"id": folder_id, "message": f"Folder {folder_name} has been created."}, 201


@app.route("/api/v1/folders", methods=['GET'])
def get_all_folders():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_ALL_FOLDERS_LIST)
            folders_list = cursor.fetchall()

    return {"folder_list": folders_list}, 200


@app.route("/api/v1/folders/<int:folders_id>", methods=['PUT'])
def update_folder(folder_id):
    folder_update_data = request.get_json()
    folder_name = folder_update_data["name"]
    folder_url = folder_update_data["description"]
    updated_at = datetime.now(timezone.utc)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_FOLDERS, (folder_name,
                           folder_url, updated_at, folder_id))

    return "successfuly updated", 204


@app.route("/api/v1/bookmarks/<int:bookmark_id>", methods=['PUT'])
def update_bookmark(bookmark_id):
    bookmark_update_data = request.get_json()
    bookmark_name = bookmark_update_data["name"]
    bookmark_url = bookmark_update_data["url"]
    bookmark_folder = bookmark_update_data["folder_id"]
    updated_at = datetime.now(timezone.utc)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_BOOKMARKS, (bookmark_name,
                           bookmark_url, bookmark_folder, updated_at, bookmark_id))

    return "successfuly updated", 204


@app.route("/api/v1/bookmarks/<int:bookmark_id>", methods=['DELETE'])
def delete_bookmark(bookmark_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_A_BOOKMARK_ROW, (bookmark_id,))

    return "successfuly deleted", 204


@app.route("/api/v1/folders/<int:folder_id>", methods=['DELETE'])
def delete_folder(folder_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_A_FOLDER, (folder_id,))

    return "successfuly deleted", 204


if __name__ == "__main__":
    app.run(debug=True)
