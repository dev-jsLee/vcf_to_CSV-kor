// DOM 요소 선택
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const customSeparator = document.getElementById('customSeparator');
const previewResult = document.getElementById('previewResult');
const addQuoteCheckbox = document.getElementById('addQuote');

// 파일 선택 이벤트
uploadArea.onclick = () => fileInput.click();

fileInput.onchange = (e) => {
    if (e.target.files.length > 0) {
        fileName.textContent = e.target.files[0].name;
        fileInfo.classList.add('show');
    }
};

// 드래그 앤 드롭
uploadArea.ondragover = (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
};

uploadArea.ondragleave = () => {
    uploadArea.classList.remove('dragover');
};

uploadArea.ondrop = (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    fileInput.files = e.dataTransfer.files;
    if (fileInput.files.length > 0) {
        fileName.textContent = fileInput.files[0].name;
        fileInfo.classList.add('show');
    }
};

// 전화번호 포맷 미리보기 함수
function formatPhonePreview() {
    const formatType = document.querySelector('input[name="format_type"]:checked').value;
    const separator = customSeparator.value || '-';
    const addQuote = addQuoteCheckbox.checked;
    const warningBox = document.getElementById('warningBox');
    
    // 경고 박스 표시 여부 결정
    if (formatType === 'number_only' && !addQuote) {
        warningBox.style.display = 'flex';
    } else {
        warningBox.style.display = 'none';
    }
    
    // 예시 전화번호들
    const examples = {
        '010': '01012345678',  // 11자리
        '02': '0212345678',     // 02 + 8자리
        '031': '03112345678'    // 031 + 8자리
    };
    
    let phone = examples['010'];
    let result = '';
    
    if (formatType === 'number_only') {
        result = phone;
        if (addQuote) {
            result = "'" + result;
        }
    } else {
        let sep = separator;
        if (formatType === 'space') {
            sep = ' ';
        } else if (formatType === 'dash') {
            sep = '-';
        }
        
        // 11자리 포맷팅
        result = phone.slice(0, 3) + sep + phone.slice(3, 7) + sep + phone.slice(7);
        
        if (addQuote) {
            result = "'" + result;
        }
    }
    
    previewResult.textContent = result;
    
    // 커스텀 구분자 입력란 활성화/비활성화
    customSeparator.disabled = (formatType !== 'custom');
}

// 이벤트 리스너 등록
document.querySelectorAll('input[name="format_type"]').forEach(radio => {
    radio.addEventListener('change', formatPhonePreview);
});

customSeparator.addEventListener('input', formatPhonePreview);
addQuoteCheckbox.addEventListener('change', formatPhonePreview);

// 초기 미리보기 업데이트
formatPhonePreview();

