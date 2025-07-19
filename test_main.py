import io
import json
import pytest
from fastapi.testclient import TestClient
from main import app, BasicInfo, PossibleTasks, CareerHistoryEntry, SkillSheetData

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

def test_upload_valid_json_file():
    """有効なJSONファイルのアップロードをテスト"""
    test_data = {
        "basic_info": {
            "name": "テスト太郎",
            "kana": "テストタロウ",
            "gender": "男性",
            "age": 30,
            "nearest_station": "東京",
            "experience_years": 5,
            "self_pr": "自己PR",
            "main_technologies": "Python, FastAPI",
            "qualifications": ""
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
                "start_date": "2018-04-01",
                "end_date": "2023-03-31",
                "duration": "5年",
                "overview": "プロジェクトA",
                "position": "SE",
                "scale_members": 5,
                "responsibilities": "要件定義、設計、開発",
                "tech_environment": "Python, Django"
            }
        ]
    }
    response = client.post(
        "/api/upload",
        files={
            "file": ("test.json", json.dumps(test_data), "application/json")
        }
    )
    assert response.status_code == 200
    assert response.json() == test_data

def test_upload_invalid_file_type():
    """無効なファイルタイプのアップロードをテスト"""
    response = client.post(
        "/api/upload",
        files={
            "file": ("test.txt", "これはテストです", "text/plain")
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "JSONファイルのみ対応しています"}

def test_upload_invalid_json_content():
    """無効なJSONコンテンツのアップロードをテスト"""
    response = client.post(
        "/api/upload",
        files={
            "file": ("test.json", "{invalid json}", "application/json")
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "無効なJSONファイルです。"}

def test_upload_empty_json_file():
    """空のJSONファイルのアップロードをテスト"""
    response = client.post(
        "/api/upload",
        files={
            "file": ("empty.json", "{}", "application/json")
        }
    )
    assert response.status_code == 200
    assert response.json() == {}


# Pydantic モデルのテスト

def test_basic_info_model_valid_data():
    """BasicInfoモデルが有効なデータで正しくインスタンス化されることをテスト"""
    data = {
        "name": "テスト太郎",
        "kana": "テストタロウ",
        "gender": "男性",
        "age": 30,
        "nearest_station": "東京",
        "experience_years": 5,
        "self_pr": "自己PR",
        "main_technologies": "Python, FastAPI",
        "qualifications": ""
    }
    info = BasicInfo(**data)
    assert info.name == "テスト太郎"
    assert info.age == 30

def test_basic_info_model_missing_required_field():
    """BasicInfoモデルで必須フィールドが欠けている場合にValidationErrorが発生することをテスト"""
    data = {
        "kana": "テストタロウ",
        "gender": "男性"
    }
    with pytest.raises(Exception):  # Pydantic ValidationErrorをキャッチ
        BasicInfo(**data)

def test_possible_tasks_model_valid_data():
    """PossibleTasksモデルが有効なデータで正しくインスタンス化されることをテスト"""
    data = {
        "customer_negotiation": "o",
        "research_analysis": "-"
    }
    tasks = PossibleTasks(**data)
    assert tasks.customer_negotiation == "o"
    assert tasks.research_analysis == "-"

def test_career_history_entry_model_valid_data():
    """CareerHistoryEntryモデルが有効なデータで正しくインスタンス化されることをテスト"""
    data = {
        "start_date": "2020-01-01",
        "end_date": "2021-12-31",
        "overview": "プロジェクトX",
        "position": "開発者",
        "responsibilities": "開発"
    }
    entry = CareerHistoryEntry(**data)
    assert entry.overview == "プロジェクトX"

def test_career_history_entry_model_missing_required_field():
    """CareerHistoryEntryモデルで必須フィールドが欠けている場合にValidationErrorが発生することをテスト"""
    data = {
        "start_date": "2020-01-01",
        "end_date": "2021-12-31",
        "overview": "プロジェクトX",
        "responsibilities": "開発"
    }
    with pytest.raises(Exception):  # Pydantic ValidationErrorをキャッチ
        CareerHistoryEntry(**data)

def test_skill_sheet_data_model_valid_data():
    """SkillSheetDataモデルが有効なデータで正しくインスタンス化されることをテスト"""
    data = {
        "basic_info": {
            "name": "テスト太郎",
            "kana": "テストタロウ",
            "gender": "男性"
        },
        "possible_tasks": {},
        "career_history": []
    }
    skill_sheet = SkillSheetData(**data)
    assert skill_sheet.basic_info.name == "テスト太郎"

def test_skill_sheet_data_model_invalid_data():
    """SkillSheetDataモデルで無効なデータが渡された場合にValidationErrorが発生することをテスト"""
    data = {
        "basic_info": {
            "kana": "テストタロウ",
            "gender": "男性"
        }, # nameが欠けている
        "possible_tasks": {},
        "career_history": []
    }
    with pytest.raises(Exception):  # Pydantic ValidationErrorをキャッチ
        SkillSheetData(**data)

def test_upload_valid_json_file():
    """有効なJSONファイルのアップロードをテスト"""
    test_data = {
        "basic_info": {
            "name": "テスト太郎",
            "kana": "テストタロウ",
            "gender": "男性",
            "age": 30,
            "nearest_station": "東京",
            "experience_years": 5,
            "self_pr": "自己PR",
            "main_technologies": "Python, FastAPI",
            "qualifications": ""
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
                "start_date": "2018-04-01",
                "end_date": "2023-03-31",
                "duration": "5年",
                "overview": "プロジェクトA",
                "position": "SE",
                "scale_members": 5,
                "responsibilities": "要件定義、設計、開発",
                "tech_environment": "Python, Django"
            }
        ]
    }
    response = client.post(
        "/api/upload",
        files={
            "file": ("test.json", json.dumps(test_data), "application/json")
        }
    )
    assert response.status_code == 200
    assert response.json() == test_data

def test_upload_invalid_file_type():
    """無効なファイルタイプのアップロードをテスト"""
    response = client.post(
        "/api/upload",
        files={
            "file": ("test.txt", "これはテストです", "text/plain")
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "JSONファイルのみ対応しています"}

def test_upload_invalid_json_content():
    """無効なJSONコンテンツのアップロードをテスト"""
    response = client.post(
        "/api/upload",
        files={
            "file": ("test.json", "{invalid json}", "application/json")
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "無効なJSONファイルです。"}

def test_upload_empty_json_file():
    """空のJSONファイルのアップロードをテスト"""
    response = client.post(
        "/api/upload",
        files={
            "file": ("empty.json", "{}", "application/json")
        }
    )
    assert response.status_code == 200
    assert response.json() == {}




