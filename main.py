import streamlit as st
from googleapiclient.discovery import build
import re

st.set_page_config(page_title="YouTube Analytics Hub", page_icon="📺", layout="centered")

st.title("📺 YouTube Video Analytics Hub")
st.subheader("YouTube API를 활용한 영상 분석 및 데이터 추출 툴킷")
st.write("---")

st.markdown("""
왼쪽 사이드바 메뉴를 이용해 원하는 분석 도구 페이지로 이동하세요!

### ⚙️ 제공하는 기능
1. **🖼️ 썸네일 다운로더**: 영상의 최고 화질 썸네일을 확인하고 다운로드합니다.
2. **📊 댓글 감정 & 통계 분석**: 전체 댓글의 작성 추이 및 핵심 키워드를 확인합니다.
3. **❤️ 베스트 댓글 추출**: 좋아요를 가장 많이 받은 상위 댓글들을 모아봅니다.
4. **🌐 언어별 댓글 분류**: 글로벌 댓글들을 국가/언어별로 분류하여 통계를 냅니다.
""")

# 공통 함수 1: 유튜브 URL에서 Video ID 추출하기
def extract_video_id(url):
    regex = r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
    match = re.search(regex, url)
    if match:
        return match.group(4)
    return None

# 공통 함수 2: API 클라이언트 빌드 (Secrets 안전 불러오기)
def get_youtube_client():
    try:
        api_key = st.secrets["YOUTUBE_API_KEY"]
        return build('youtube', 'v3', developerKey=api_key)
    except Exception as e:
        st.error("❌ Streamlit Secrets에 'YOUTUBE_API_KEY'가 설정되지 않았거나 올바르지 않습니다.")
        return None

# 다른 페이지에서 가져다 쓸 수 있도록 세션 스토리지에 함수 등록
st.session_state['extract_video_id'] = extract_video_id
st.session_state['get_youtube_client'] = get_youtube_client

st.write("---")
st.info("💡 이 사이트는 사용자가 입력한 URL의 데이터를 실시간으로 YouTube API를 통해 가져옵니다.")
