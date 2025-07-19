/**
 * SkillSheet Builder - Preview Page JavaScript
 * Handles preview display and JSON generation
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM要素の取得
    const previewContent = document.getElementById('previewContent');
    const downloadJsonBtn = document.getElementById('downloadJsonBtn');
    const backToEditBtn = document.getElementById('backToEditBtn');
    
    // セッションストレージからプレビューデータを読み込む
    loadPreviewData();
    
    // JSONダウンロードボタンのイベントリスナー
    if (downloadJsonBtn) {
        downloadJsonBtn.addEventListener('click', downloadJson);
    }
    
    // 編集に戻るボタンのイベントリスナー
    if (backToEditBtn) {
        backToEditBtn.addEventListener('click', function() {
            // フォームデータをセッションストレージに保存して編集ページに戻る
            const previewData = sessionStorage.getItem('previewData');
            if (previewData) {
                sessionStorage.setItem('skillsheetData', previewData);
            }
            window.location.href = '/skillsheet';
        });
    }
});

/**
 * セッションストレージからプレビューデータを読み込み、表示する
 */
function loadPreviewData() {
    const previewData = sessionStorage.getItem('previewData');
    if (!previewData) {
        showError('プレビューデータが見つかりません。');
        return;
    }
    
    try {
        const data = JSON.parse(previewData);
        
        // プレビューHTMLを生成
        const previewHTML = generatePreviewHTML(data);
        
        // プレビュー表示
        previewContent.innerHTML = previewHTML;
    } catch (error) {
        console.error('Error loading preview data:', error);
        showError('プレビューデータの読み込みに失敗しました。');
    }
}

/**
 * プレビューHTMLを生成
 */
function generatePreviewHTML(data) {
    if (!data || !data.basic_info) {
        return '<div class="error">データが不正です。</div>';
    }
    
    const basicInfo = data.basic_info;
    const possibleTasks = data.possible_tasks || {};
    const careerHistory = data.career_history || [];
    
    let html = `
        <div class="excel-section">
            <h2 class="excel-section-title">職務経歴書</h2>
            
            <table class="excel-table">
                <tr>
                    <th style="width: 15%;">氏名</th>
                    <td style="width: 35%;">${escapeHTML(basicInfo.name || '')}</td>
                    <th style="width: 15%;">ふりがな</th>
                    <td style="width: 35%;">${escapeHTML(basicInfo.kana || '')}</td>
                </tr>
                <tr>
                    <th>性別</th>
                    <td>${escapeHTML(basicInfo.gender || '')}</td>
                    <th>年齢</th>
                    <td>${basicInfo.age ? `${basicInfo.age}歳` : ''}</td>
                </tr>
                <tr>
                    <th>最寄駅</th>
                    <td>${escapeHTML(basicInfo.nearest_station || '')}</td>
                    <th>実務経験</th>
                    <td>${basicInfo.experience_years ? `${basicInfo.experience_years}年` : ''}</td>
                </tr>
            </table>
        </div>
    `;
    
    // 自己PR
    if (basicInfo.self_pr) {
        html += `
            <div class="excel-section">
                <h3 class="excel-section-title">自己PR</h3>
                <div class="excel-merged-cell" style="padding: 10px; white-space: pre-wrap;">${escapeHTML(basicInfo.self_pr)}</div>
            </div>
        `;
    }
    
    // 主要技術
    if (basicInfo.main_technologies) {
        html += `
            <div class="excel-section">
                <h3 class="excel-section-title">主要技術</h3>
                <div class="excel-merged-cell" style="padding: 10px; white-space: pre-wrap;">${escapeHTML(basicInfo.main_technologies)}</div>
            </div>
        `;
    }
    
    // 保有資格
    if (basicInfo.qualifications) {
        html += `
            <div class="excel-section">
                <h3 class="excel-section-title">保有資格</h3>
                <div class="excel-merged-cell" style="padding: 10px; white-space: pre-wrap;">${escapeHTML(basicInfo.qualifications)}</div>
            </div>
        `;
    }
    
    // 対応可能業務
    html += `
        <div class="excel-section">
            <h3 class="excel-section-title">対応可能業務</h3>
            <table class="task-matrix">
                <tr>
                    <th>顧客折衝</th>
                    <th>調査分析</th>
                    <th>要件定義</th>
                    <th>基本設計</th>
                    <th>詳細設計</th>
                </tr>
                <tr>
                    <td>${possibleTasks.customer_negotiation || '-'}</td>
                    <td>${possibleTasks.research_analysis || '-'}</td>
                    <td>${possibleTasks.requirement_definition || '-'}</td>
                    <td>${possibleTasks.basic_design || '-'}</td>
                    <td>${possibleTasks.detailed_design || '-'}</td>
                </tr>
                <tr>
                    <th>PG開発</th>
                    <th>単体テスト</th>
                    <th>結合テスト</th>
                    <th>システム保守</th>
                    <th>NW設計</th>
                </tr>
                <tr>
                    <td>${possibleTasks.pg_development || '-'}</td>
                    <td>${possibleTasks.unit_test || '-'}</td>
                    <td>${possibleTasks.integration_test || '-'}</td>
                    <td>${possibleTasks.system_maintenance || '-'}</td>
                    <td>${possibleTasks.nw_design || '-'}</td>
                </tr>
                <tr>
                    <th>NW構築</th>
                    <th>NW運用</th>
                    <th>SV設計</th>
                    <th>SV構築</th>
                    <th>SV運用</th>
                </tr>
                <tr>
                    <td>${possibleTasks.nw_construction || '-'}</td>
                    <td>${possibleTasks.nw_operation || '-'}</td>
                    <td>${possibleTasks.sv_design || '-'}</td>
                    <td>${possibleTasks.sv_construction || '-'}</td>
                    <td>${possibleTasks.sv_operation || '-'}</td>
                </tr>
            </table>
        </div>
    `;
    
    // 職務経歴
    if (careerHistory.length > 0) {
        html += `
            <div class="excel-section">
                <h3 class="excel-section-title">職務経歴</h3>
        `;
        
        careerHistory.forEach((career, index) => {
            const startDate = formatDate(career.start_date);
            const endDate = career.end_date === 'current' ? '現在' : formatDate(career.end_date);
            
            html += `
                <div class="career-entry-preview">
                    <table class="career-history-table">
                        <tr>
                            <th class="career-period" style="width: 20%;">期間</th>
                            <th class="career-overview" style="width: 50%;">業務概要</th>
                            <th class="career-position" style="width: 20%;">ポジション</th>
                            <th class="career-scale" style="width: 10%;">規模</th>
                        </tr>
                        <tr>
                            <td class="career-period">${startDate} 〜 ${endDate}<br>${career.duration || ''}</td>
                            <td class="career-overview">${escapeHTML(career.overview || '')}</td>
                            <td class="career-position">${escapeHTML(career.position || '')}</td>
                            <td class="career-scale">${career.scale_members ? `${career.scale_members}名` : ''}</td>
                        </tr>
                    </table>
                    
                    <table class="career-history-table">
                        <tr>
                            <th style="width: 20%;">担当業務</th>
                            <td class="career-responsibilities" style="width: 80%;">${formatMultiline(career.responsibilities)}</td>
                        </tr>
                        <tr>
                            <th style="width: 20%;">技術環境</th>
                            <td class="career-tech-environment" style="width: 80%;">${formatMultiline(career.tech_environment)}</td>
                        </tr>
                    </table>
                </div>
            `;
        });
        
        html += `</div>`;
    }
    
    return html;
}

/**
 * JSONファイルをダウンロード
 */
function downloadJson() {
    const previewData = sessionStorage.getItem('previewData');
    if (!previewData) {
        alert('データが見つかりません。');
        return;
    }
    
    // ボタンを無効化
    const downloadBtn = document.getElementById('downloadJsonBtn');
    if (downloadBtn) {
        downloadBtn.disabled = true;
        downloadBtn.textContent = 'ファイル生成中...';
    }
    
    // APIにリクエスト
    fetch('/api/export-json', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: previewData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('JSONファイルの生成に失敗しました。');
        }
        return response.blob();
    })
    .then(blob => {
        // ファイル名の生成（現在の日時を含む）
        const now = new Date();
        const dateStr = `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}`;
        const timeStr = `${String(now.getHours()).padStart(2, '0')}${String(now.getMinutes()).padStart(2, '0')}`;
        const fileName = `skillsheet_${dateStr}_${timeStr}.json`;
        
        // ダウンロードリンクの作成
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = fileName;
        
        // リンクをクリックしてダウンロード
        document.body.appendChild(a);
        a.click();
        
        // クリーンアップ
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error.message || 'JSONファイルの生成に失敗しました。');
    })
    .finally(() => {
        // ボタンを元に戻す
        if (downloadBtn) {
            downloadBtn.disabled = false;
            downloadBtn.textContent = 'JSON出力';
        }
    });
}

/**
 * エラーメッセージを表示
 */
function showError(message) {
    const previewContent = document.getElementById('previewContent');
    if (previewContent) {
        previewContent.innerHTML = `<div class="error" style="color: red; text-align: center; padding: 2rem;">${message}</div>`;
    }
}

/**
 * 日付をフォーマット (YYYY-MM-DD -> YYYY年MM月)
 */
function formatDate(dateStr) {
    if (!dateStr) return '';
    
    try {
        const date = new Date(dateStr);
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        return `${year}年${month}月`;
    } catch (e) {
        return dateStr;
    }
}

/**
 * 複数行テキストをHTMLで表示
 */
function formatMultiline(text) {
    if (!text) return '';
    return escapeHTML(text).replace(/\n/g, '<br>');
}

/**
 * HTMLエスケープ
 */
function escapeHTML(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}