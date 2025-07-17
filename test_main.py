import io
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    """トップページが正常に表示されることをテスト"""
    response = client.get("/")
    assert response.status_code == 200
    assert "SkillSheet Builder" in response.text

def test_read_skillsheet():
    """スキルシート編集ページが正常に表示されることをテスト"""
    response = client.get("/skillsheet")
    assert response.status_code == 200
    assert "スキルシート編集" in response.text

def test_read_preview():
    """プレビューページが正常に表示されることをテスト"""
    response = client.get("/preview")
    assert response.status_code == 200
    assert "スキルシートプレビュー" in response.text

def test_preview_api():
    """プレビューAPIが正常に動作することをテスト"""
    test_data = {
        "basic_info": {
            "name": "テスト 太郎",
            "kana": "てすと たろう",
            "gender": "男性",
            "age": 30,
            "nearest_station": "東京",
            "experience_years": 5,
            "self_pr": "テスト用の自己PRです。",
            "main_technologies": "Python, FastAPI, JavaScript",
            "qualifications": "基本情報技術者"
        },
        "possible_tasks": {
            "customer_negotiation": "o",
            "research_analysis": "o",
            "requirement_definition": "o",
            "basic_design": "o",
            "detailed_design": "o",
            "pg_development": "o",
            "unit_test": "o",
            "integration_test": "o",
            "system_maintenance": "o",
            "nw_design": "-",
            "nw_construction": "-",
            "nw_operation": "-",
            "sv_design": "-",
            "sv_construction": "-",
            "sv_operation": "-"
        },
        "career_history": [
            {
                "start_date": "2020-01-01",
                "end_date": "2022-01-01",
                "duration": "2年0ヶ月",
                "overview": "テスト用プロジェクト1",
                "position": "SE",
                "scale_members": 5,
                "responsibilities": "要件定義、設計、開発",
                "tech_environment": "OS: Windows\n言語: Python\nDB: PostgreSQL"
            }
        ]
    }
    
    response = client.post("/api/preview", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert data["basic_info"]["name"] == "テスト 太郎"
    assert data["career_history"][0]["position"] == "SE"

def test_generate_xlsx_api():
    """XLSX生成APIが正常に動作することをテスト"""
    test_data = {
        "basic_info": {
            "name": "テスト 太郎",
            "kana": "てすと たろう",
            "gender": "男性",
            "age": 30,
            "nearest_station": "東京",
            "experience_years": 5,
            "self_pr": "テスト用の自己PRです。",
            "main_technologies": "Python, FastAPI, JavaScript",
            "qualifications": "基本情報技術者"
        },
        "possible_tasks": {
            "customer_negotiation": "o",
            "research_analysis": "o",
            "requirement_definition": "o",
            "basic_design": "o",
            "detailed_design": "o",
            "pg_development": "o",
            "unit_test": "o",
            "integration_test": "o",
            "system_maintenance": "o",
            "nw_design": "-",
            "nw_construction": "-",
            "nw_operation": "-",
            "sv_design": "-",
            "sv_construction": "-",
            "sv_operation": "-"
        },
        "career_history": [
            {
                "start_date": "2020-01-01",
                "end_date": "2022-01-01",
                "duration": "2年0ヶ月",
                "overview": "テスト用プロジェクト1",
                "position": "SE",
                "scale_members": 5,
                "responsibilities": "要件定義、設計、開発",
                "tech_environment": "OS: Windows\n言語: Python\nDB: PostgreSQL"
            }
        ]
    }
    
    response = client.post("/api/generate-xlsx", json=test_data)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert len(response.content) > 0

def test_upload_invalid_file():
    """無効なファイルのアップロードをテスト"""
    # テキストファイルを作成
    text_file = io.BytesIO(b"This is not an XLSX file")
    
    response = client.post(
        "/api/upload",
        files={"file": ("test.txt", text_file, "text/plain")}
    )
    assert response.status_code == 400
    assert "XLSXファイルのみ対応しています" in response.json()["detail"]