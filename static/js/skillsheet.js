/**
 * SkillSheet Builder - Skillsheet Page JavaScript
 * Handles form functionality, validation, and submission
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM要素の取得
    const skillsheetForm = document.getElementById('skillsheetForm');
    const careerEntries = document.getElementById('careerEntries');
    const addCareerBtn = document.getElementById('addCareerBtn');
    const previewBtn = document.getElementById('previewBtn');

    // 文字数カウンター設定
    setupCharCounter('self_pr', 500);
    setupCharCounter('main_technologies', 200);
    setupCharCounter('qualifications', 200);

    // セッションストレージからデータを読み込む
    loadDataFromSessionStorage();

    // 経歴追加ボタンのイベントリスナー
    if (addCareerBtn) {
        addCareerBtn.addEventListener('click', addCareerEntry);
    }

    // プレビューボタンのイベントリスナー
    if (previewBtn) {
        previewBtn.addEventListener('click', submitForm);
    }

    // 初期経歴エントリの削除ボタンを非表示に
    updateRemoveButtons();

    // 業務期間の自動計算を設定
    setupDurationCalculation(0);
});

/**
 * 文字数カウンターの設定
 */
function setupCharCounter(elementId, maxLength) {
    const element = document.getElementById(elementId);
    const counter = document.getElementById(`${elementId}_count`);

    if (element && counter) {
        // 初期カウント
        counter.textContent = element.value.length;

        // 入力イベント
        element.addEventListener('input', function() {
            counter.textContent = element.value.length;

            // 文字数制限を超えた場合
            if (element.value.length > maxLength) {
                counter.style.color = 'red';
            } else {
                counter.style.color = '';
            }
        });
    }
}

/**
 * 業務期間の自動計算
 */
function setupDurationCalculation(index) {
    const startDateInput = document.getElementById(`start_date_${index}`);
    const endDateInput = document.getElementById(`end_date_${index}`);
    const durationInput = document.getElementById(`duration_${index}`);
    const currentJobCheckbox = document.getElementById(`current_job_${index}`);

    if (startDateInput && endDateInput && durationInput) {
        const calculateDuration = function() {
            if (!startDateInput.value) return;

            let endDate;
            if (currentJobCheckbox && currentJobCheckbox.checked) {
                // 「現在」が選択されている場合は今日の日付を使用
                endDate = new Date();
            } else if (endDateInput.value) {
                // 終了日が入力されている場合
                endDate = new Date(endDateInput.value);
                // 月末に設定
                endDate.setMonth(endDate.getMonth() + 1, 0);
            } else {
                return;
            }

            const startDate = new Date(startDateInput.value);
            // 月初に設定
            startDate.setDate(1);

            // 月数の差を計算
            const months = (endDate.getFullYear() - startDate.getFullYear()) * 12 + 
                          (endDate.getMonth() - startDate.getMonth());

            // 年と月に変換
            const years = Math.floor(months / 12);
            const remainingMonths = months % 12;

            // 表示形式
            let durationText = '';
            if (years > 0) {
                durationText += `${years}年`;
            }
            durationText += `${remainingMonths}ヶ月`;

            durationInput.value = durationText;
        };

        // イベントリスナーの設定
        startDateInput.addEventListener('change', calculateDuration);
        endDateInput.addEventListener('change', calculateDuration);

        if (currentJobCheckbox) {
            currentJobCheckbox.addEventListener('change', function() {
                endDateInput.disabled = this.checked;
                if (this.checked) {
                    endDateInput.value = '';
                }
                calculateDuration();
            });
        }

        // 初期計算
        calculateDuration();
    }
}

/**
 * 新しい職務経歴エントリを追加
 */
function addCareerEntry() {
    const entries = document.querySelectorAll('.career-entry');
    const newIndex = entries.length;

    // 新しいエントリのHTML
    const newEntryHTML = `
        <div class="career-entry" data-index="${newIndex}">
            <div class="career-header">
                <h3>職務経歴 #${newIndex + 1}</h3>
                <button type="button" class="btn btn-danger remove-career">削除</button>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="start_date_${newIndex}">業務開始年月 <span class="required">*</span></label>
                    <input type="month" id="start_date_${newIndex}" name="career_history[${newIndex}].start_date" required>
                </div>

                <div class="form-group">
                    <label for="end_date_${newIndex}">業務終了年月 <span class="required">*</span></label>
                    <div class="end-date-container">
                        <input type="month" id="end_date_${newIndex}" name="career_history[${newIndex}].end_date" required>
                        <label class="checkbox-label">
                            <input type="checkbox" id="current_job_${newIndex}" class="current-job-checkbox"> 現在
                        </label>
                    </div>
                </div>

                <div class="form-group">
                    <label for="duration_${newIndex}">業務期間</label>
                    <input type="text" id="duration_${newIndex}" name="career_history[${newIndex}].duration" readonly>
                </div>
            </div>

            <div class="form-group">
                <label for="overview_${newIndex}">業務概要（及び業務内容） <span class="required">*</span></label>
                <textarea id="overview_${newIndex}" name="career_history[${newIndex}].overview" rows="4" required></textarea>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="position_${newIndex}">ポジション <span class="required">*</span></label>
                    <input type="text" id="position_${newIndex}" name="career_history[${newIndex}].position" required placeholder="例: SE, PG, PM, PL">
                </div>

                <div class="form-group">
                    <label for="scale_members_${newIndex}">規模（人数）</label>
                    <input type="number" id="scale_members_${newIndex}" name="career_history[${newIndex}].scale_members" min="1" placeholder="例: 5">
                </div>
            </div>

            <div class="form-group">
                <label for="responsibilities_${newIndex}">担当業務 <span class="required">*</span></label>
                <textarea id="responsibilities_${newIndex}" name="career_history[${newIndex}].responsibilities" rows="4" required placeholder="箇条書きで入力することをお勧めします"></textarea>
            </div>

            <div class="form-group">
                <label for="tech_environment_${newIndex}">技術環境</label>
                <textarea id="tech_environment_${newIndex}" name="career_history[${newIndex}].tech_environment" rows="4" placeholder="例: OS: Linux&#10;言語: Python&#10;FW: FastAPI&#10;DB: PostgreSQL&#10;Cloud: AWS&#10;Tool: Git"></textarea>
            </div>
        </div>
    `;

    // DOMに追加
    careerEntries.insertAdjacentHTML('beforeend', newEntryHTML);

    // 削除ボタンのイベントリスナーを設定
    const newEntry = careerEntries.lastElementChild;
    const removeBtn = newEntry.querySelector('.remove-career');
    if (removeBtn) {
        removeBtn.addEventListener('click', function() {
            removeCareerEntry(newEntry);
        });
    }

    // 業務期間の自動計算を設定
    setupDurationCalculation(newIndex);

    // 削除ボタンの表示状態を更新
    updateRemoveButtons();
}

/**
 * 職務経歴エントリを削除
 */
function removeCareerEntry(entry) {
    if (confirm('この職務経歴を削除してもよろしいですか？')) {
        entry.remove();

        // インデックスを振り直す
        const entries = document.querySelectorAll('.career-entry');
        entries.forEach((entry, index) => {
            entry.setAttribute('data-index', index);
            entry.querySelector('h3').textContent = `職務経歴 #${index + 1}`;

            // 入力要素のIDと名前を更新
            const inputs = entry.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                const oldId = input.id;
                const baseName = oldId.substring(0, oldId.lastIndexOf('_'));
                input.id = `${baseName}_${index}`;

                if (input.name && input.name.includes('career_history')) {
                    input.name = input.name.replace(/career_history\[\d+\]/, `career_history[${index}]`);
                }
            });

            // ラベルのfor属性を更新
            const labels = entry.querySelectorAll('label[for]');
            labels.forEach(label => {
                const oldFor = label.getAttribute('for');
                if (oldFor && oldFor.includes('_')) {
                    const baseName = oldFor.substring(0, oldFor.lastIndexOf('_'));
                    label.setAttribute('for', `${baseName}_${index}`);
                }
            });
        });

        // 削除ボタンの表示状態を更新
        updateRemoveButtons();
    }
}

/**
 * 削除ボタンの表示状態を更新
 */
function updateRemoveButtons() {
    const entries = document.querySelectorAll('.career-entry');
    const removeButtons = document.querySelectorAll('.remove-career');

    // 経歴が1つしかない場合は削除ボタンを非表示
    if (entries.length === 1) {
        removeButtons[0].style.display = 'none';
    } else {
        removeButtons.forEach(btn => {
            btn.style.display = 'block';
        });
    }
}

/**
 * セッションストレージからデータを読み込む
 */
function loadDataFromSessionStorage() {
    const storedData = sessionStorage.getItem('skillsheetData');
    if (!storedData) return;

    try {
        const data = JSON.parse(storedData);

        // 基本情報の設定
        if (data.basic_info) {
            Object.keys(data.basic_info).forEach(key => {
                const element = document.getElementById(key);
                if (element) {
                    if (element.type === 'radio') {
                        const radio = document.querySelector(`input[name="basic_info.${key}"][value="${data.basic_info[key]}"]`);
                        if (radio) radio.checked = true;
                    } else {
                        element.value = data.basic_info[key];
                    }
                }
            });
        }

        // 対応可能業務の設定
        if (data.possible_tasks) {
            Object.keys(data.possible_tasks).forEach(key => {
                const element = document.getElementById(key);
                if (element) {
                    element.value = data.possible_tasks[key];
                }
            });
        }

        // 職務経歴の設定
        if (data.career_history && data.career_history.length > 0) {
            // 最初のエントリを設定
            const firstEntry = data.career_history[0];
            Object.keys(firstEntry).forEach(key => {
                const element = document.getElementById(`${key}_0`);
                if (element) {
                    if (key === 'start_date' || key === 'end_date') {
                        // 日付形式の変換 (YYYY-MM-DD -> YYYY-MM)
                        const date = new Date(firstEntry[key]);
                        const year = date.getFullYear();
                        const month = String(date.getMonth() + 1).padStart(2, '0');
                        element.value = `${year}-${month}`;
                    } else {
                        element.value = firstEntry[key];
                    }
                }
            });

            // 「現在」チェックボックスの処理
            if (firstEntry.end_date === 'current') {
                const currentCheckbox = document.getElementById('current_job_0');
                if (currentCheckbox) {
                    currentCheckbox.checked = true;
                    const endDateInput = document.getElementById('end_date_0');
                    if (endDateInput) endDateInput.disabled = true;
                }
            }

            // 2つ目以降のエントリを追加
            for (let i = 1; i < data.career_history.length; i++) {
                addCareerEntry();

                const entry = data.career_history[i];
                Object.keys(entry).forEach(key => {
                    const element = document.getElementById(`${key}_${i}`);
                    if (element) {
                        if (key === 'start_date' || key === 'end_date') {
                            if (entry[key] === 'current') {
                                const currentCheckbox = document.getElementById(`current_job_${i}`);
                                if (currentCheckbox) {
                                    currentCheckbox.checked = true;
                                    const endDateInput = document.getElementById(`end_date_${i}`);
                                    if (endDateInput) endDateInput.disabled = true;
                                }
                            } else {
                                // 日付形式の変換 (YYYY-MM-DD -> YYYY-MM)
                                const date = new Date(entry[key]);
                                const year = date.getFullYear();
                                const month = String(date.getMonth() + 1).padStart(2, '0');
                                element.value = `${year}-${month}`;
                            }
                        } else {
                            element.value = entry[key];
                        }
                    }
                });
            }
        }

        // 文字数カウンターの更新
        updateAllCharCounters();

        // セッションストレージをクリア
        sessionStorage.removeItem('skillsheetData');
    } catch (error) {
        console.error('Error loading data from session storage:', error);
    }
}

/**
 * すべての文字数カウンターを更新
 */
function updateAllCharCounters() {
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(textarea => {
        const counterId = `${textarea.id}_count`;
        const counter = document.getElementById(counterId);
        if (counter) {
            counter.textContent = textarea.value.length;
        }
    });
}

/**
 * フォームをサブミット
 */
function submitForm() {
    // フォームのバリデーション
    if (!validateForm()) {
        return;
    }

    // フォームデータの収集
    const formData = collectFormData();

    // ローディング表示
    previewBtn.disabled = true;
    previewBtn.textContent = 'プレビュー生成中...';

    // APIにデータを送信
    fetch('/api/preview', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('プレビューの生成に失敗しました。');
        }
        return response.json();
    })
    .then(data => {
        // プレビューデータをセッションストレージに保存
        sessionStorage.setItem('previewData', JSON.stringify(data));

        // プレビューページへリダイレクト
        window.location.href = '/preview';
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error.message || 'プレビューの生成に失敗しました。');
    })
    .finally(() => {
        // ボタンを元に戻す
        previewBtn.disabled = false;
        previewBtn.textContent = 'プレビュー表示';
    });
}

/**
 * フォームのバリデーション
 */
function validateForm() {
    // 必須項目のチェック
    const requiredInputs = document.querySelectorAll('input[required], textarea[required]');
    let isValid = true;

    requiredInputs.forEach(input => {
        // 無効化されている入力フィールドはスキップ（「現在」が選択されている場合など）
        if (input.disabled) {
            return;
        }

        if (!input.value.trim()) {
            input.classList.add('invalid');
            isValid = false;

            // エラーメッセージの表示
            let errorMsg = input.nextElementSibling;
            if (!errorMsg || !errorMsg.classList.contains('error-message')) {
                errorMsg = document.createElement('div');
                errorMsg.className = 'error-message';
                errorMsg.style.color = 'red';
                errorMsg.style.fontSize = '0.8rem';
                errorMsg.style.marginTop = '0.25rem';
                input.parentNode.insertBefore(errorMsg, input.nextSibling);
            }
            errorMsg.textContent = '必須項目です';
        } else {
            input.classList.remove('invalid');

            // エラーメッセージの削除
            const errorMsg = input.nextElementSibling;
            if (errorMsg && errorMsg.classList.contains('error-message')) {
                errorMsg.remove();
            }
        }
    });

    // 文字数制限のチェック
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(textarea => {
        const maxLength = parseInt(textarea.getAttribute('maxlength'));
        if (textarea.value.length > maxLength) {
            textarea.classList.add('invalid');
            isValid = false;

            // エラーメッセージの表示
            let errorMsg = textarea.nextElementSibling;
            if (!errorMsg || !errorMsg.classList.contains('error-message')) {
                errorMsg = document.createElement('div');
                errorMsg.className = 'error-message';
                errorMsg.style.color = 'red';
                errorMsg.style.fontSize = '0.8rem';
                errorMsg.style.marginTop = '0.25rem';
                textarea.parentNode.insertBefore(errorMsg, textarea.nextSibling);
            }
            errorMsg.textContent = `${maxLength}文字以内で入力してください`;
        }
    });

    if (!isValid) {
        // 最初のエラー要素までスクロール
        const firstInvalid = document.querySelector('.invalid');
        if (firstInvalid) {
            firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        alert('入力内容に不備があります。必須項目を入力してください。');
    }

    return isValid;
}

/**
 * フォームデータの収集
 */
function collectFormData() {
    const formData = {
        basic_info: {},
        possible_tasks: {},
        career_history: []
    };

    // 基本情報の収集
    const basicInfoInputs = document.querySelectorAll('[name^="basic_info."]');
    basicInfoInputs.forEach(input => {
        const key = input.name.replace('basic_info.', '');

        if (input.type === 'radio') {
            if (input.checked) {
                formData.basic_info[key] = input.value;
            }
        } else {
            formData.basic_info[key] = input.value;
        }
    });

    // 対応可能業務の収集
    const taskInputs = document.querySelectorAll('[name^="possible_tasks."]');
    taskInputs.forEach(input => {
        const key = input.name.replace('possible_tasks.', '');
        formData.possible_tasks[key] = input.value;
    });

    // 職務経歴の収集
    const careerEntries = document.querySelectorAll('.career-entry');
    careerEntries.forEach((entry, index) => {
        const careerData = {};

        // 各入力フィールドの値を取得
        const inputs = entry.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            if (input.name && input.name.includes('career_history')) {
                const key = input.name.match(/\.([^.]+)$/)[1];

                if (key === 'start_date' || key === 'end_date') {
                    if (key === 'end_date' && input.disabled) {
                        // 「現在」が選択されている場合
                        careerData[key] = 'current';
                    } else if (input.value) {
                        // 日付形式の変換 (YYYY-MM -> YYYY-MM-DD)
                        careerData[key] = `${input.value}-01`;
                    }
                } else if (key === 'scale_members') {
                    careerData[key] = input.value ? parseInt(input.value) : null;
                } else {
                    careerData[key] = input.value;
                }
            }
        });

        formData.career_history.push(careerData);
    });

    return formData;
}
