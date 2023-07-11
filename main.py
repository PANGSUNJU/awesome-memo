from fastapi import FastAPI, UploadFile, Form, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing_extensions import Annotated


class Memo(BaseModel):
    id: str
    title: str
    createAt: str


memos = []

app = FastAPI()


@app.post("/memos")
def create_memo(memo: Memo):
    memos.append(memo)
    return '200'

@app.get("/memos")
def read_memo():
    return memos


@app.get("/memos/")
def read_memo(sort_by: str, sort_order: str):
    global memos
    if sort_by == "title":
        memos = sorted(
            memos, key=lambda x: x.title, reverse=True if sort_order == "desc" else False)
    elif sort_by == "createAt":
        memos = sorted(
            memos, key=lambda x: x.createAt, reverse=True if sort_order == "desc" else False)
    return memos


@ app.put("/memos/{memo_id}")
def put_memo(req_memo: Memo):
    for memo in memos:
        if memo.id == req_memo.id:
            print(memo.id)
            print(req_memo.id)
            
            memo.title = req_memo.title
            return '성공했습니다.'
    return '해당id는 없습니다.'


@ app.delete("/memos/{memo_id}")
def delete_memo(memo_id):
    for index, memo in enumerate(memos):
        if memo.id == memo_id:
            memos.pop(index)
            return '성공했습니다.'
    return '해당id는 없습니다.'


app.mount("/", StaticFiles(directory='static', html=True), name='static')
