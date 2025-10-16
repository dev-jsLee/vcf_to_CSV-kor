import csv
import re
import quopri
import base64

def format_phone_number(phone, format_type='dash', custom_separator='-', add_quote=True):
    """전화번호 포맷팅
    
    Args:
        phone: 전화번호
        format_type: 'number_only', 'quote_number', 'dash', 'space', 'custom'
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
    # 값 추출
    if ':' not in line:
        return ''
    
    parts = line.split(':', 1)
    value = parts[1] if len(parts) > 1 else ''
    
    # Base64 인코딩 체크
    if 'ENCODING=BASE64' in line.upper() or 'ENCODING=B' in line.upper():
        return decode_base64_value(value)
    
    # Quoted-Printable 인코딩 체크
    if 'ENCODING=QUOTED-PRINTABLE' in line.upper():
        return decode_quoted_printable(value)
    
    # CHARSET이 명시되어 있고 = 문자가 포함된 경우
    if 'CHARSET=' in line.upper() and '=' in value:
        # =XX 패턴이 있으면 Quoted-Printable로 간주
        if re.search(r'=[0-9A-F]{2}', value):
            return decode_quoted_printable(value)
    
    # 일반 텍스트이지만 = 패턴이 있으면 시도
    if re.search(r'=[0-9A-F]{2}', value):
        decoded = decode_quoted_printable(value)
        # 디코딩이 의미있게 되었는지 확인 (한글이나 알파벳이 있는지)
        if re.search(r'[가-힣a-zA-Z]', decoded):
            return decoded
    
    return value

def parse_vcf_to_csv(vcf_file, csv_file, format_type='dash', custom_separator='-', add_quote=True):
    """VCF 파일을 CSV로 변환"""
    contacts = []
    current_contact = {}
    
    with open(vcf_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            if line == 'BEGIN:VCARD':
                current_contact = {'name': '', 'phones': [], 'emails': [], 'organization': '', 'note': ''}
            
            elif line == 'END:VCARD':
                if current_contact:
                    contacts.append(current_contact)
                current_contact = {}
            
            elif ':' in line:
                # 속성과 값 분리
                key = line.split(';')[0].split(':')[0]
                value = decode_value(line)
                
                if key == 'FN':  # Full Name
                    current_contact['name'] = value
                elif key == 'N' and not current_contact['name']:  # Name (fallback)
                    # N:Last;First;Middle;Prefix;Suffix 형식
                    value = decode_value(line)
                    name_parts = value.split(';')
                    current_contact['name'] = ' '.join([p for p in name_parts if p])
                elif key == 'TEL':  # Telephone
                    formatted_phone = format_phone_number(value, format_type, custom_separator, add_quote)
                    current_contact['phones'].append(formatted_phone)
                elif key == 'EMAIL':  # Email
                    current_contact['emails'].append(value)
                elif key == 'ORG':  # Organization
                    current_contact['organization'] = value
                elif key == 'NOTE':  # Note
                    current_contact['note'] = value
    
    # CSV로 저장
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
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
    
    print(f"[완료] 변환 완료: {len(contacts)}개 연락처를 {csv_file}에 저장했습니다.")
    return contacts

def print_contacts(vcf_file, format_type='dash', custom_separator='-', add_quote=True):
    """VCF 파일 내용을 화면에 출력"""
    contacts = []
    current_contact = {}
    
    with open(vcf_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            if line == 'BEGIN:VCARD':
                current_contact = {}
            elif line == 'END:VCARD':
                if current_contact:
                    contacts.append(current_contact)
            elif ':' in line:
                key = line.split(';')[0].split(':')[0]
                value = decode_value(line)
                
                if key == 'FN':
                    current_contact['name'] = value
                elif key == 'TEL':
                    if 'phones' not in current_contact:
                        current_contact['phones'] = []
                    formatted_phone = format_phone_number(value, format_type, custom_separator, add_quote)
                    current_contact['phones'].append(formatted_phone)
                elif key == 'EMAIL':
                    if 'emails' not in current_contact:
                        current_contact['emails'] = []
                    current_contact['emails'].append(value)
    
    # 출력
    print(f"\n총 {len(contacts)}개의 연락처를 찾았습니다.\n")
    for i, contact in enumerate(contacts, 1):
        print(f"{i}. {contact.get('name', '이름 없음')}")
        if 'phones' in contact:
            for phone in contact['phones']:
                print(f"   전화: {phone}")
        if 'emails' in contact:
            for email in contact['emails']:
                print(f"   이메일: {email}")
        print()

# 사용 예시
if __name__ == "__main__":
    print("=== VCF 파일 변환 프로그램 ===\n")
    
    # 파일 경로 입력
    vcf_file = input("VCF 파일 경로를 입력하세요 (예: contacts.vcf): ").strip()
    
    try:
        # 1. 내용 미리보기
        print("\n[연락처 미리보기]")
        print_contacts(vcf_file)
        
        # 2. CSV로 변환
        csv_file = vcf_file.replace('.vcf', '.csv')
        parse_vcf_to_csv(vcf_file, csv_file)
        
        print(f"\n[완료] {csv_file} 파일을 Excel에서 열어보세요!")
        
    except FileNotFoundError:
        print(f"[오류] '{vcf_file}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"[오류] 오류 발생: {e}")