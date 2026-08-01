"""FastAPI ToDo Workbook — Week 1: API Gateway + Lambda (Mangum) + DynamoDB.

Lambda 上では Mangum が API Gateway イベントを ASGI に変換して FastAPI へ渡す。
ログは CloudWatch Logs に自動転送される（Week 1 のテーマ：監視）。
"""

import logging
import os
import uuid

import boto3
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel

# --- ログ設定：Lambda では stdout/stderr が CloudWatch Logs へ流れる ---
logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = os.environ.get("TABLE_NAME", "Todos")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

app = FastAPI(title="FastAPI ToDo Workbook")


class TodoIn(BaseModel):
    title: str
    completed: bool = False


class Todo(TodoIn):
    id: str


@app.get("/health")
def health():
    logger.info("health check called")
    return {"status": "ok", "table": TABLE_NAME}


@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: TodoIn):
    item = {"id": f"t-{uuid.uuid4().hex[:8]}", "title": todo.title, "completed": todo.completed}
    table.put_item(Item=item)
    logger.info("created todo id=%s", item["id"])
    return item


@app.get("/todos", response_model=list[Todo])
def list_todos():
    # 学習用の小規模テーブルなので Scan で全件取得（本来は Query + キー設計で絞る）
    items = table.scan()["Items"]
    logger.info("listed %d todos", len(items))
    return items


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: str):
    resp = table.get_item(Key={"id": todo_id})
    if "Item" not in resp:
        logger.warning("todo not found id=%s", todo_id)
        raise HTTPException(status_code=404, detail="todo not found")
    return resp["Item"]


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: str, todo: TodoIn):
    resp = table.get_item(Key={"id": todo_id})
    if "Item" not in resp:
        raise HTTPException(status_code=404, detail="todo not found")
    item = {"id": todo_id, "title": todo.title, "completed": todo.completed}
    table.put_item(Item=item)
    logger.info("updated todo id=%s", todo_id)
    return item


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: str):
    table.delete_item(Key={"id": todo_id})
    logger.info("deleted todo id=%s", todo_id)


# Lambda エントリポイント（--handler main.handler で指定する）
handler = Mangum(app)
