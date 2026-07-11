import streamlit as st
import pandas as pd
import plotly.express as px
from langdetect import detect

st.set_page_config(page_title="언어별 분류", page_icon="🌐")
st.title("🌐 언어별 댓글 자동 분류기")
st.write("---")

url = st.text_input("글로벌 반응을 확인할 유튜브 동영상 링크를 입력하세요:")

# 언어 코드를 알아보기 쉬운 한글 국가/언어명으로 매핑
lang_map = {
    'ko': '🇰🇷 한국어', 'en': '🇺🇸 영어', 'ja': '🇯🇵 일본어', 
    'zh-cn': '🇨🇳 중국어', 'zh-tw': '🇨🇳 중국어', 'es': '🇪🇸 스페인어',
    'fr': '🇫🇷 프랑스어', 'de': '🇩🇪 독일어', 'vi': '🇻🇳 베트남어', 
    'th': '🇹🇭 태국어', 'id': '🇮🇩 인도네시아어'
}

if url:
    youtube = st.session_state.get('get_youtube_client')()
    video_id = st.session_state.get('extract_video_id')(url)
    
    if youtube and video_id:
        with st.spinner("댓글 언어 분석기 작동 중..."):
            try:
                request = youtube.commentThreads().list(
                    part="snippet", gl="US", videoId=video_id, maxResults=50
                )
                response = request.execute()
                
                classified_data = []
                for item in response.get('items', []):
                    text = item['snippet']['topLevelComment']['snippet']['textDisplay']
                    
                    # 공백이나 특수문자만 있는 경우 에러 방지용 예외 처리
                    try:
                        lang_code = detect(text)
                        lang_name = lang_map.get(lang_code, f"🏳️ 기타 ({lang_code})")
                    except:
                        lang_name = "🏳️ 감지 불가/이모지"
                        
                    classified_data.append({
                        "내용": text,
                        "분류된 언어": lang_name
                    })
                
                df = pd.DataFrame(classified_data)
                
                # 시각화용 차트 출력
                st.subheader("📊 댓글 언어 분포도")
                lang_counts = df['분류된 언어'].value_counts().reset_index()
                lang_counts.columns = ['언어', '개수']
                
                fig = px.pie(lang_counts, values='개수', names='언어', hole=0.3)
                st.plotly_chart(fig, use_container_width=True)
                
                # 세부 데이터 확인
                st.write("---")
                st.subheader("🔍 언어별 댓글 모아보기")
                selected_lang = st.selectbox("확인할 언어를 선택하세요:", lang_counts['언어'].tolist())
                
                filtered_df = df[df['분류된 언어'] == selected_lang]
                for idx, row in filtered_df.iterrows():
                    st.info(row['내용'])
                    
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
