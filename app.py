from flask import Flask, render_template, request, send_file
import csv
import re
import quopri
import base64
import io
import os

app = Flask(__name__)

# 버전 정보 읽기
def get_version():
    """VERSION 파일에서 버전 정보를 읽어옴"""
    try:
        with open('VERSION', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return '1.0.0'

APP_VERSION = get_version()

def decode_quoted_printable(text):
    """Quoted-Printable 인코딩된 텍스트를 디코딩"""
    try:
        # 문자열을 바이트로 변환 (ASCII 또는 latin-1)
        if isinstance(text, str):
            # ASCII로 먼저 시도 (더 안전함)
            try:
                text = text.encode('ascii')
            except UnicodeEncodeError:
                text = text.encode('latin-1')
        
        # Quoted-Printable 디코딩
        decoded = quopri.decodestring(text)
        
        # UTF-8을 최우선으로 시도 (한글은 거의 항상 UTF-8)
        try:
            result = decoded.decode('utf-8')
            # UTF-8 디코딩이 성공하면 바로 반환
            return result
        except UnicodeDecodeError:
            pass
        
        # UTF-8 실패 시 한국어 인코딩 시도
        for encoding in ['euc-kr', 'cp949']:
            try:
                return decoded.decode(encoding)
            except (UnicodeDecodeError, LookupError):
                continue
        
        # 마지막 수단: errors='replace'로 UTF-8 디코딩
        return decoded.decode('utf-8', errors='replace')
    except Exception as e:
        # 예외 발생 시 원본 반환
        return text if isinstance(text, str) else text.decode('utf-8', errors='replace')

def decode_base64_value(text):
    """Base64 인코딩된 텍스트를 디코딩"""
    try:
        decoded = base64.b64decode(text)
        for encoding in ['utf-8', 'euc-kr', 'cp949']:
            try:
                return decoded.decode(encoding)
            except:
                continue
        return decoded.decode('utf-8', errors='ignore')
    except:
        return text

def decode_value(line):
    """VCF 라인에서 값을 추출하고 인코딩 처리"""
    if ':' not in line:
        return ''
    
    parts = line.split(':', 1)
    value = parts[1] if len(parts) > 1 else ''
    
    if 'ENCODING=BASE64' in line.upper() or 'ENCODING=B' in line.upper():
        return decode_base64_value(value)
    
    if 'ENCODING=QUOTED-PRINTABLE' in line.upper():
        return decode_quoted_printable(value)
    
    if 'CHARSET=' in line.upper() and '=' in value:
        if re.search(r'=[0-9A-F]{2}', value):
            return decode_quoted_printable(value)
    
    if re.search(r'=[0-9A-F]{2}', value):
        decoded = decode_quoted_printable(value)
        if re.search(r'[가-힣a-zA-Z]', decoded):
            return decoded
    
    return value

def format_phone_number(phone, format_type='dash', custom_separator='-', add_quote=True):
    """전화번호 포맷팅
    
    Args:
        phone: 전화번호
        format_type: 'number_only', 'dash', 'space', 'custom'
        custom_separator: 커스텀 구분자 (format_type='custom'일 때 사용)
        add_quote: 맨 앞에 작은따옴표 추가 여부
    """
    if not phone:
        return ''
    
    # 숫자만 추출
    phone = re.sub(r'[^0-9]', '', phone)
    
    # 1로 시작하면 앞에 0 추가
    if phone.startswith('1') and len(phone) >= 10:
        phone = '0' + phone
    
    # 포맷 타입에 따라 처리
    if format_type == 'number_only':
        # 숫자만
        if add_quote:
            return f"'{phone}"
        else:
            return phone
    else:
        # 구분자 결정
        if format_type == 'space':
            sep = ' '
        elif format_type == 'custom':
            sep = custom_separator
        else:  # 'dash' (기본값)
            sep = '-'
        
        # 번호 길이에 따라 분리
        if len(phone) == 11:
            formatted = f"{phone[:3]}{sep}{phone[3:7]}{sep}{phone[7:]}"
        elif len(phone) == 10:
            if phone.startswith('02'):
                formatted = f"{phone[:2]}{sep}{phone[2:6]}{sep}{phone[6:]}"
            else:
                formatted = f"{phone[:3]}{sep}{phone[3:6]}{sep}{phone[6:]}"
        elif len(phone) == 9:
            formatted = f"{phone[:2]}{sep}{phone[2:5]}{sep}{phone[5:]}"
        elif len(phone) == 8:
            formatted = f"{phone[:4]}{sep}{phone[4:]}"
        else:
            formatted = phone
        
        # 작은따옴표 추가 여부
        if add_quote:
            return f"'{formatted}"
        else:
            return formatted

def parse_vcf_content(vcf_content, format_type='dash', custom_separator='-', add_quote=True):
    """VCF 내용을 파싱하여 연락처 리스트 반환"""
    contacts = []
    current_contact = {}
    
    lines = vcf_content.decode('utf-8', errors='ignore').split('\n')
    
    for line in lines:
        line = line.strip()
        
        if line == 'BEGIN:VCARD':
            current_contact = {'name': '', 'phones': [], 'emails': [], 'organization': '', 'note': ''}
        
        elif line == 'END:VCARD':
            if current_contact:
                contacts.append(current_contact)
            current_contact = {}
        
        elif ':' in line:
            key = line.split(';')[0].split(':')[0]
            value = decode_value(line)
            
            if key == 'FN':
                current_contact['name'] = value
            elif key == 'N' and not current_contact['name']:
                value = decode_value(line)
                name_parts = value.split(';')
                current_contact['name'] = ' '.join([p for p in name_parts if p])
            elif key == 'TEL':
                formatted_phone = format_phone_number(value, format_type, custom_separator, add_quote)
                current_contact['phones'].append(formatted_phone)
            elif key == 'EMAIL':
                current_contact['emails'].append(value)
            elif key == 'ORG':
                current_contact['organization'] = value
            elif key == 'NOTE':
                current_contact['note'] = value
    
    return contacts

def create_csv_from_contacts(contacts):
    """연락처 리스트를 CSV로 변환"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 헤더
    writer.writerow(['이름', '전화번호1', '전화번호2', '전화번호3', '이메일1', '이메일2', '회사', '메모'])
    
    # 데이터
    for contact in contacts:
        phones = contact['phones'] + [''] * (3 - len(contact['phones']))
        emails = contact['emails'] + [''] * (2 - len(contact['emails']))
        
        writer.writerow([
            contact['name'],
            phones[0] if len(phones) > 0 else '',
            phones[1] if len(phones) > 1 else '',
            phones[2] if len(phones) > 2 else '',
            emails[0] if len(emails) > 0 else '',
            emails[1] if len(emails) > 1 else '',
            contact['organization'],
            contact['note']
        ])
    
    output.seek(0)
    return output.getvalue()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', version=APP_VERSION)
        
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', version=APP_VERSION)
        
        if file and file.filename.endswith('.vcf'):
            try:
                # 폼 데이터 받기
                format_type = request.form.get('format_type', 'dash')
                custom_separator = request.form.get('custom_separator', '-')
                add_quote = request.form.get('add_quote') == 'true'
                
                # VCF 파싱
                vcf_content = file.read()
                contacts = parse_vcf_content(vcf_content, format_type, custom_separator, add_quote)
                
                # CSV 생성
                csv_content = create_csv_from_contacts(contacts)
                
                # CSV 파일로 반환
                output = io.BytesIO()
                output.write(csv_content.encode('utf-8-sig'))
                output.seek(0)
                
                original_filename = file.filename.replace('.vcf', '')
                
                return send_file(
                    output,
                    mimetype='text/csv',
                    as_attachment=True,
                    download_name=f'{original_filename}.csv'
                )
            except Exception as e:
                return f"<h1>오류 발생</h1><p>{str(e)}</p><a href='/'>돌아가기</a>"
    
    return render_template('index.html', version=APP_VERSION)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

