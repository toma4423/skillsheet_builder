/**
 * SkillSheet Builder - Index Page JavaScript
 * Handles file upload functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    const loadFileBtn = document.getElementById('loadFileBtn');
    const fileInput = document.getElementById('fileInput');
    
    if (loadFileBtn && fileInput) {
        // ファイル選択ボタンのクリックイベント
        loadFileBtn.addEventListener('click', function() {
            fileInput.click();
        });
        
        // ファイル選択時の処理
        fileInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (!file) return;
            
            // ファイル形式チェック
            if (!file.name.endsWith('.json')) {
                alert('JSONファイルを選択してください。');
                fileInput.value = '';
                return;
            }
            
            // ファイルサイズチェック (5MB上限)
            if (file.size > 5 * 1024 * 1024) {
                alert('ファイルサイズは5MB以下にしてください。');
                fileInput.value = '';
                return;
            }
            
            // FormDataの作成
            const formData = new FormData();
            formData.append('file', file);
            
            // ローディング表示
            loadFileBtn.disabled = true;
            loadFileBtn.textContent = 'ファイル読み込み中...';
            
            // ファイルアップロード
            fetch('/api/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('ファイルのアップロードに失敗しました。');
                }
                return response.json();
            })
            .then(data => {
                // セッションストレージにデータを保存
                sessionStorage.setItem('skillsheetData', JSON.stringify(data));
                
                // スキルシート編集ページへリダイレクト
                window.location.href = '/skillsheet';
            })
            .catch(error => {
                console.error('Error:', error);
                alert(error.message || 'ファイルの読み込みに失敗しました。');
            })
            .finally(() => {
                // ボタンを元に戻す
                loadFileBtn.disabled = false;
                loadFileBtn.textContent = 'ファイルから読み込み';
                fileInput.value = '';
            });
        });
    }
});