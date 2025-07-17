from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import date, datetime
import os
import io
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

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
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/skillsheet", response_class=HTMLResponse)
async def skillsheet(request: Request):
    return templates.TemplateResponse("skillsheet.html", {"request": request})

@app.get("/preview", response_class=HTMLResponse)
async def preview(request: Request):
    return templates.TemplateResponse("preview.html", {"request": request})

# API エンドポイント
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="XLSXファイルのみ対応しています")

    try:
        # ファイルの内容を読み込む
        contents = await file.read()

        # openpyxlでExcelファイルを解析
        wb = openpyxl.load_workbook(io.BytesIO(contents))
        ws = wb.active

        # データを抽出
        data = extract_data_from_excel(ws)

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ファイルの解析に失敗しました: {str(e)}")

@app.post("/api/preview")
async def generate_preview(data: SkillSheetData):
    # プレビュー生成のためのデータ処理
    # 実際のプレビューはフロントエンドで行うため、データをそのまま返す
    return data

@app.post("/api/generate-xlsx")
async def generate_xlsx(data: SkillSheetData):
    try:
        # XLSXファイルを生成
        xlsx_data = generate_xlsx_file(data)

        # 一時ファイルとして保存せずにメモリ上で処理
        return FileResponse(
            xlsx_data,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="職務経歴書.xlsx"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"XLSXファイルの生成に失敗しました: {str(e)}")

# Excelファイルからデータを抽出する関数
def extract_data_from_excel(worksheet):
    # 基本的なデータ構造
    data = {
        "basic_info": {},
        "possible_tasks": {},
        "career_history": []
    }

    # 基本情報の抽出（例）
    data["basic_info"]["name"] = worksheet.cell(row=2, column=4).value or ""
    data["basic_info"]["kana"] = worksheet.cell(row=3, column=4).value or ""

    # 性別の抽出（例）
    gender_cell = worksheet.cell(row=2, column=6).value
    if gender_cell:
        if "男性" in str(gender_cell):
            data["basic_info"]["gender"] = "男性"
        elif "女性" in str(gender_cell):
            data["basic_info"]["gender"] = "女性"
        else:
            data["basic_info"]["gender"] = "その他"
    else:
        data["basic_info"]["gender"] = "回答しない"

    # 年齢の抽出（例）
    age_cell = worksheet.cell(row=3, column=6).value
    if age_cell and isinstance(age_cell, str) and "歳" in age_cell:
        try:
            data["basic_info"]["age"] = int(age_cell.replace("歳", "").strip())
        except:
            data["basic_info"]["age"] = None
    else:
        data["basic_info"]["age"] = None

    # 最寄駅の抽出
    data["basic_info"]["nearest_station"] = worksheet.cell(row=4, column=4).value or ""

    # 実務経験の抽出
    exp_cell = worksheet.cell(row=5, column=4).value
    if exp_cell and isinstance(exp_cell, str) and "年" in exp_cell:
        try:
            data["basic_info"]["experience_years"] = int(exp_cell.replace("年", "").strip())
        except:
            data["basic_info"]["experience_years"] = None
    else:
        data["basic_info"]["experience_years"] = None

    # 自己PR、主要技術、保有資格の抽出は複雑なため省略
    # 実際の実装では、セルの位置を特定して抽出する必要がある

    # 対応可能業務の抽出も省略
    # 実際の実装では、表の位置を特定して各業務項目の値を抽出する

    # 職務経歴の抽出も省略
    # 実際の実装では、各職務経歴ブロックを特定して情報を抽出する

    return data

# XLSXファイルを生成する関数
def generate_xlsx_file(data: SkillSheetData):
    # 新しいワークブックを作成
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "職務経歴書"

    # スタイル定義
    title_font = Font(name='游ゴシック', size=14, bold=True)
    header_font = Font(name='游ゴシック', size=11, bold=True)
    normal_font = Font(name='游ゴシック', size=11)

    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    header_fill = PatternFill(start_color="E0E0E0", end_color="E0E0E0", fill_type="solid")

    # タイトル
    ws['A1'] = "職務経歴書"
    ws['A1'].font = title_font
    ws.merge_cells('A1:I1')
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')

    # 基本情報
    ws['B2'] = "氏名"
    ws['B2'].font = header_font
    ws['B2'].border = thin_border
    ws['B2'].fill = header_fill

    ws['D2'] = data.basic_info.name
    ws['D2'].font = normal_font
    ws['D2'].border = thin_border
    ws.merge_cells('D2:E2')

    ws['F2'] = "性別"
    ws['F2'].font = header_font
    ws['F2'].border = thin_border
    ws['F2'].fill = header_fill

    ws['H2'] = data.basic_info.gender
    ws['H2'].font = normal_font
    ws['H2'].border = thin_border
    ws.merge_cells('H2:I2')

    ws['B3'] = "ふりがな"
    ws['B3'].font = header_font
    ws['B3'].border = thin_border
    ws['B3'].fill = header_fill

    ws['D3'] = data.basic_info.kana
    ws['D3'].font = normal_font
    ws['D3'].border = thin_border
    ws.merge_cells('D3:E3')

    ws['F3'] = "年齢"
    ws['F3'].font = header_font
    ws['F3'].border = thin_border
    ws['F3'].fill = header_fill

    ws['H3'] = f"{data.basic_info.age}歳" if data.basic_info.age else ""
    ws['H3'].font = normal_font
    ws['H3'].border = thin_border
    ws.merge_cells('H3:I3')

    ws['B4'] = "最寄駅"
    ws['B4'].font = header_font
    ws['B4'].border = thin_border
    ws['B4'].fill = header_fill

    ws['D4'] = data.basic_info.nearest_station
    ws['D4'].font = normal_font
    ws['D4'].border = thin_border
    ws.merge_cells('D4:E4')

    ws['F4'] = "実務経験"
    ws['F4'].font = header_font
    ws['F4'].border = thin_border
    ws['F4'].fill = header_fill

    ws['H4'] = f"{data.basic_info.experience_years}年" if data.basic_info.experience_years else ""
    ws['H4'].font = normal_font
    ws['H4'].border = thin_border
    ws.merge_cells('H4:I4')

    # 自己PR
    current_row = 6
    if data.basic_info.self_pr:
        ws[f'A{current_row}'] = "自己PR"
        ws[f'A{current_row}'].font = header_font
        ws[f'A{current_row}'].fill = header_fill
        ws[f'A{current_row}'].border = thin_border
        ws.merge_cells(f'A{current_row}:I{current_row}')

        current_row += 1
        ws[f'A{current_row}'] = data.basic_info.self_pr
        ws[f'A{current_row}'].font = normal_font
        ws[f'A{current_row}'].alignment = Alignment(wrap_text=True, vertical='top')
        ws[f'A{current_row}'].border = thin_border

        # 複数行のテキストに対応するために行の高さを調整
        lines = data.basic_info.self_pr.count('\n') + 1
        ws.row_dimensions[current_row].height = max(15 * lines, 30)

        ws.merge_cells(f'A{current_row}:I{current_row}')
        current_row += 2

    # 主要技術
    if data.basic_info.main_technologies:
        ws[f'A{current_row}'] = "主要技術"
        ws[f'A{current_row}'].font = header_font
        ws[f'A{current_row}'].fill = header_fill
        ws[f'A{current_row}'].border = thin_border
        ws.merge_cells(f'A{current_row}:I{current_row}')

        current_row += 1
        ws[f'A{current_row}'] = data.basic_info.main_technologies
        ws[f'A{current_row}'].font = normal_font
        ws[f'A{current_row}'].alignment = Alignment(wrap_text=True, vertical='top')
        ws[f'A{current_row}'].border = thin_border

        lines = data.basic_info.main_technologies.count('\n') + 1
        ws.row_dimensions[current_row].height = max(15 * lines, 30)

        ws.merge_cells(f'A{current_row}:I{current_row}')
        current_row += 2

    # 保有資格
    if data.basic_info.qualifications:
        ws[f'A{current_row}'] = "保有資格"
        ws[f'A{current_row}'].font = header_font
        ws[f'A{current_row}'].fill = header_fill
        ws[f'A{current_row}'].border = thin_border
        ws.merge_cells(f'A{current_row}:I{current_row}')

        current_row += 1
        ws[f'A{current_row}'] = data.basic_info.qualifications
        ws[f'A{current_row}'].font = normal_font
        ws[f'A{current_row}'].alignment = Alignment(wrap_text=True, vertical='top')
        ws[f'A{current_row}'].border = thin_border

        lines = data.basic_info.qualifications.count('\n') + 1
        ws.row_dimensions[current_row].height = max(15 * lines, 30)

        ws.merge_cells(f'A{current_row}:I{current_row}')
        current_row += 2

    # 対応可能業務
    ws[f'A{current_row}'] = "対応可能業務"
    ws[f'A{current_row}'].font = header_font
    ws[f'A{current_row}'].fill = header_fill
    ws[f'A{current_row}'].border = thin_border
    ws.merge_cells(f'A{current_row}:I{current_row}')

    current_row += 1

    # 対応可能業務の表を作成
    tasks = [
        ("顧客折衝", data.possible_tasks.customer_negotiation),
        ("調査分析", data.possible_tasks.research_analysis),
        ("要件定義", data.possible_tasks.requirement_definition),
        ("基本設計", data.possible_tasks.basic_design),
        ("詳細設計", data.possible_tasks.detailed_design),
        ("PG開発", data.possible_tasks.pg_development),
        ("単体テスト", data.possible_tasks.unit_test),
        ("結合テスト", data.possible_tasks.integration_test),
        ("システム保守", data.possible_tasks.system_maintenance),
        ("NW設計", data.possible_tasks.nw_design),
        ("NW構築", data.possible_tasks.nw_construction),
        ("NW運用", data.possible_tasks.nw_operation),
        ("SV設計", data.possible_tasks.sv_design),
        ("SV構築", data.possible_tasks.sv_construction),
        ("SV運用", data.possible_tasks.sv_operation)
    ]

    # 3列×5行で表示
    for i in range(0, len(tasks), 3):
        row = current_row + (i // 3)
        for j in range(min(3, len(tasks) - i)):
            task_name, task_value = tasks[i + j]
            col = j * 3 + 1  # A, D, G

            ws.cell(row=row, column=col).value = task_name
            ws.cell(row=row, column=col).font = normal_font
            ws.cell(row=row, column=col).border = thin_border
            ws.cell(row=row, column=col).alignment = Alignment(horizontal='center')

            ws.cell(row=row, column=col + 1).value = task_value
            ws.cell(row=row, column=col + 1).font = normal_font
            ws.cell(row=row, column=col + 1).border = thin_border
            ws.cell(row=row, column=col + 1).alignment = Alignment(horizontal='center')

            # 空白セル
            ws.cell(row=row, column=col + 2).border = thin_border

    current_row += (len(tasks) + 2) // 3 + 2

    # 職務経歴
    if data.career_history:
        ws[f'A{current_row}'] = "職務経歴"
        ws[f'A{current_row}'].font = header_font
        ws[f'A{current_row}'].fill = header_fill
        ws[f'A{current_row}'].border = thin_border
        ws.merge_cells(f'A{current_row}:I{current_row}')

        current_row += 1

        for career in data.career_history:
            # 期間
            start_date = career.start_date
            if start_date.endswith("-01"):
                start_date = start_date[:-3]  # YYYY-MM-01 -> YYYY-MM

            end_date = "現在" if career.end_date == "current" else career.end_date
            if end_date != "現在" and end_date.endswith("-01"):
                end_date = end_date[:-3]  # YYYY-MM-01 -> YYYY-MM

            period = f"{start_date} 〜 {end_date}"
            if career.duration:
                period += f"\n({career.duration})"

            ws[f'A{current_row}'] = "期間"
            ws[f'A{current_row}'].font = header_font
            ws[f'A{current_row}'].fill = header_fill
            ws[f'A{current_row}'].border = thin_border

            ws[f'B{current_row}'] = "業務概要"
            ws[f'B{current_row}'].font = header_font
            ws[f'B{current_row}'].fill = header_fill
            ws[f'B{current_row}'].border = thin_border
            ws.merge_cells(f'B{current_row}:E{current_row}')

            ws[f'F{current_row}'] = "ポジション"
            ws[f'F{current_row}'].font = header_font
            ws[f'F{current_row}'].fill = header_fill
            ws[f'F{current_row}'].border = thin_border
            ws.merge_cells(f'F{current_row}:G{current_row}')

            ws[f'H{current_row}'] = "規模"
            ws[f'H{current_row}'].font = header_font
            ws[f'H{current_row}'].fill = header_fill
            ws[f'H{current_row}'].border = thin_border
            ws.merge_cells(f'H{current_row}:I{current_row}')

            current_row += 1

            ws[f'A{current_row}'] = period
            ws[f'A{current_row}'].font = normal_font
            ws[f'A{current_row}'].alignment = Alignment(wrap_text=True, vertical='top')
            ws[f'A{current_row}'].border = thin_border

            ws[f'B{current_row}'] = career.overview
            ws[f'B{current_row}'].font = normal_font
            ws[f'B{current_row}'].alignment = Alignment(wrap_text=True, vertical='top')
            ws[f'B{current_row}'].border = thin_border
            ws.merge_cells(f'B{current_row}:E{current_row}')

            ws[f'F{current_row}'] = career.position
            ws[f'F{current_row}'].font = normal_font
            ws[f'F{current_row}'].alignment = Alignment(wrap_text=True, vertical='top')
            ws[f'F{current_row}'].border = thin_border
            ws.merge_cells(f'F{current_row}:G{current_row}')

            ws[f'H{current_row}'] = f"{career.scale_members}名" if career.scale_members else ""
            ws[f'H{current_row}'].font = normal_font
            ws[f'H{current_row}'].alignment = Alignment(horizontal='center', vertical='top')
            ws[f'H{current_row}'].border = thin_border
            ws.merge_cells(f'H{current_row}:I{current_row}')

            # 行の高さを調整
            lines_overview = career.overview.count('\n') + 1
            ws.row_dimensions[current_row].height = max(15 * lines_overview, 30)

            current_row += 1

            # 担当業務
            ws[f'A{current_row}'] = "担当業務"
            ws[f'A{current_row}'].font = header_font
            ws[f'A{current_row}'].fill = header_fill
            ws[f'A{current_row}'].border = thin_border

            ws[f'B{current_row}'] = career.responsibilities
            ws[f'B{current_row}'].font = normal_font
            ws[f'B{current_row}'].alignment = Alignment(wrap_text=True, vertical='top')
            ws[f'B{current_row}'].border = thin_border
            ws.merge_cells(f'B{current_row}:I{current_row}')

            lines_resp = career.responsibilities.count('\n') + 1
            ws.row_dimensions[current_row].height = max(15 * lines_resp, 30)

            current_row += 1

            # 技術環境
            ws[f'A{current_row}'] = "技術環境"
            ws[f'A{current_row}'].font = header_font
            ws[f'A{current_row}'].fill = header_fill
            ws[f'A{current_row}'].border = thin_border

            ws[f'B{current_row}'] = career.tech_environment or ""
            ws[f'B{current_row}'].font = normal_font
            ws[f'B{current_row}'].alignment = Alignment(wrap_text=True, vertical='top')
            ws[f'B{current_row}'].border = thin_border
            ws.merge_cells(f'B{current_row}:I{current_row}')

            if career.tech_environment:
                lines_tech = career.tech_environment.count('\n') + 1
                ws.row_dimensions[current_row].height = max(15 * lines_tech, 30)

            current_row += 2

    # 列幅の調整
    for col in range(1, 10):
        column_letter = get_column_letter(col)
        ws.column_dimensions[column_letter].width = 12

    # メモリ上でファイルを保存
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return output
