import requests
import json
import time

KAKAO_REST_API_KEY = ""

def collect_real_full_data():
    # 전국을 커버하는 상세 지역 리스트 (일부 발췌, 실제로는 더 추가 가능)
    # 서울 25개구, 경기 31개 시군 등을 모두 포함해야 합니다.
    comprehensive_regions = [
        # 서울 (25개구 전체)
        "강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", 
        "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", 
        "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구",
        # 경기 주요 도시
        "수원시", "성남시", "의정부시", "안양시", "부천시", "광명시", "평택시", "동두천시", 
        "안산시", "고양시", "과천시", "구리시", "남양주시", "오산시", "시흥시", "군포시", 
        "의왕시", "하남시", "용인시", "파주시", "이천시", "안성시", "김포시", "화성시", 
        "광주시", "양주시", "포천시", "여주시",
        # 기타 광역시 및 지방 주요 도시
        "인천", "부산", "대구", "대전", "광주", "울산", "세종", "제주",
        "천안시", "청주시", "전주시", "창원시", "포항시", "구미시", "원주시", "강릉시",
        "춘천시", "목포시", "여수시", "순천시", "익산시", "군산시", "경주시"
    ]
    
    total_cafes = {}
    
    headers = {"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    for area in comprehensive_regions:
        print(f"📡 {area} 지역 수집 중...")
        for page in range(1, 4):
            params = {"query": f"{area} 고양이 카페", "page": page}
            res = requests.get(url, headers=headers, params=params)
            
            if res.status_code == 200:
                docs = res.json().get("documents", [])
                if not docs: break
                
                for item in docs:
                    # 중복 제거 및 데이터 저장
                    total_cafes[item['id']] = {
                        "name": item['place_name'],
                        "address": item['address_name'],
                        "phone": item['phone'] if item['phone'] else "번호 없음",
                        "url": item['place_url']
                    }
                if res.json().get("meta", {}).get("is_end"): break
            time.sleep(0.1)

    # 저장
    with open("cat_cafes.json", "w", encoding="utf-8") as f:
        json.dump(list(total_cafes.values()), f, ensure_ascii=False, indent=4)
    
    print(f"\n✅ 최종 완료! 총 {len(total_cafes)}개의 데이터를 수집했습니다.")

if __name__ == "__main__":
    collect_real_full_data()