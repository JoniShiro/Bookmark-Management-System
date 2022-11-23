# Bookmark-Management-System

This project created using Python-flask , REST Api and postgreSQL.

## API

|  HTTP  |            Endpoint            |             Description              |
| :----: | :----------------------------: | :----------------------------------: |
|  GET   |       /api/v1/bookmarks:       |       Get a list of bookmarks        |
|  GET   | /api/v1/bookmarks/folders/:id: | Get a list of bookmarks for a folder |
|  POST  |       /api/v1/bookmarks:       |        Create a new bookmark         |
|  PUT   |     /api/v1/bookmarks/:id:     |          Update a bookmark           |
| DELETE |     /api/v1/bookmarks/:id:     |          Delete a bookmark           |
|  GET   |        /api/v1/folders:        |        Get a list of folders         |
|  POST  |        /api/v1/folders:        |         Create a new folder          |
|  PUT   |      /api/v1/folders/:id:      |          Update a bookmark           |
| DELETE |      /api/v1/folders/:id:      |          Delete a bookmark           |

## Getting Started

```
python -m venv .venv
source .venv/bin/activate   # different in windows
pip install flask
pip3 install -r requirements.txt
```

Create .flaskenv file in the project and put :

```
FLASK_APP=app
FLASK_DEBUG=1
```

create .env file and put the url, you can get it from Elephantsql, create instance then on details you'll find URL just copy and paste it in the file :

```
DATABASE_URL = postgresql
```
