from urllib.parse import urlparse
import re

def extract_url_features(url) :
    feature = {}
    parsed = urlparse(url)

    # 기본 URL 기반 Feature
    feature['url_length'] = len(url)            # URL 전체 문자열 길이
    feature['num_dots'] = url.count('.')        # URL 내 점(.)의 개수
    feature['has_ip'] = int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', url)))    # IP 주소 포함 여부
    feature['has_https'] = int((parsed.scheme or '').lower() == 'https')            # HTTPS 사용 여부  
    feature['num_special_chars'] = len(re.findall(r'[^\w]', url))   # 특수문자 수 (@, ?, =, % 등)
    feature['has_at_symbol'] = int('@' in url)                      # @ 기호 포함 여부
    feature['path_length'] = len(parsed.path)                       # URL 경로 길이
    feature['num_digits'] = len(re.findall(r'\d', url))             # 숫자 개수

    return feature