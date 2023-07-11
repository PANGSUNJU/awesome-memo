from fastapi import FastAPI, UploadFile, Form, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing_extensions import Annotated, List
import sqlite3


# class Memo(BaseModel):
#     id: str
#     title: str
#     createAt: str


con = sqlite3.connect('memo.db', check_same_thread=False)
cur = con.cursor()

app = FastAPI()


@app.post("/memos")
def create_memo(id: Annotated[int, Form()],
                title: Annotated[str, Form()],
                createAt: Annotated[int, Form()]
                ):
    cur.execute(f"""
                INSERT INTO memos(id,title,createAt)
                VALUES('{id}','{title}','{createAt}')
                """)
    con.commit()
    return '200'


@app.get("/memos")
def read_memo():
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    rows = cur.execute(f"""
                    SELECT * from memos;
                    """).fetchall()
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))


# @app.get("/memos/")
# def read_memo(sort_by: str, sort_order: str):
#     global memos
#     if sort_by == "title":
#         memos = sorted(
#             memos, key=lambda x: x.title, reverse=True if sort_order == "desc" else False)
#     elif sort_by == "createAt":
#         memos = sorted(
#             memos, key=lambda x: x.createAt, reverse=True if sort_order == "desc" else False)
#     return memos


@ app.put("/memos/{memo_id}")
def put_memo(id: Annotated[int, Form()],
             title: Annotated[str, Form()]):
    cur.execute(f"""
                UPDATE memos
                SET title='{title}'
                WHERE id='{id}'
                """)
    con.commit()
    return '200'


@ app.delete("/memos/{memo_id}")
def delete_memo(id: Annotated[int, Form()]):
    cur.execute(f"""
                DELETE FROM memos
                WHERE id='{id}'
                """)
    con.commit()
    return '성공했습니다.'


app.mount("/", StaticFiles(directory='static', html=True), name='static')
