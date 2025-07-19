import json
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="SkillSheet Builder", description="ITエンジニア向けスキルシート作成Webアプリケーション")

# 静的ファイルとテンプレートの設定
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# データモデル
class BasicInfo(BaseModel):
    name: str
    kana: str
    gender: str
    age: Optional[int] = None
    nearest_station: Optional[str] = None
    experience_years: Optional[int] = None
    self_pr: Optional[str] = None
    main_technologies: Optional[str] = None
    qualifications: Optional[str] = None


class PossibleTasks(BaseModel):
    customer_negotiation: str = "-"
    research_analysis: str = "-"
    requirement_definition: str = "-"
    basic_design: str = "-"
    detailed_design: str = "-"
    pg_development: str = "-"
    unit_test: str = "-"
    integration_test: str = "-"
    system_maintenance: str = "-"
    nw_design: str = "-"
    nw_construction: str = "-"
    nw_operation: str = "-"
    sv_design: str = "-"
    sv_construction: str = "-"
    sv_operation: str = "-"


class CareerHistoryEntry(BaseModel):
    start_date: str
    end_date: str
    duration: Optional[str] = None
    overview: str
    position: str
    scale_members: Optional[int] = None
    responsibilities: str
    tech_environment: Optional[str] = None


class SkillSheetData(BaseModel):
    basic_info: BasicInfo
    possible_tasks: PossibleTasks
    career_history: List[CareerHistoryEntry]


# ルート
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/skillsheet", response_class=HTMLResponse)
async def skillsheet(request: Request):
    return templates.TemplateResponse(request, "skillsheet.html")


@app.get("/preview", response_class=HTMLResponse)
async def preview(request: Request):
    return templates.TemplateResponse(request, "preview.html")


# API エンドポイント
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="JSONファイルのみ対応しています")

    try:
        contents = await file.read()
        data = json.loads(contents)
        return data
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="無効なJSONファイルです。")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ファイルの解析に失敗しました: {str(e)}")
