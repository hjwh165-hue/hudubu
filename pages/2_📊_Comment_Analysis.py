import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="댓글 분석기", page_icon="📊", layout="wide")
st.title("📊 댓글 기초 통계 및 분석")
st.write("---")

url = st.text_input("분석할 유튜브 동영상 링크를 입력하세요:")

if url:
    get_youtube = st.session_state.get('get_youtube_client')
    extract_id = st.session_state.get('extract_video_id')
    
    youtube = get_youtube()
    video_id = extract_id(url)
    
    if youtube and video_id:
        with st.spinner("댓글 데이터를 수집하는 중... (최대 100개)"):
            try:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=100,
                    textFormat="plainText"
                )
                response = request.execute()
                
                comments_data = []
                for item in response.get('items', []):
                    snippet = item['snippet']['topLevelComment']['snippet']
                    comments_data.append({
                        "작성자": snippet['authorDisplayName'],
                        "댓글": snippet['textDisplay'],
                        "좋아요": snippet['likeCount'],
                        "작성일": snippet['publishedAt'][:10] # 날짜만 추출
                    })
                
                df = pd.DataFrame(comments_data)
                
                if not df.empty:
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.metric("수집된 총 댓글 수", f"{len(df)}개")
                        st.metric("평균 좋아요 수", f"{df['좋아요'].mean():.1f}개")
                    
                    with col2:
                        st.subheader("📅 일자별 댓글 작성 추이")
                        date_counts = df['작성일'].value_counts().sort_index().reset_index()
                        date_counts.columns = ['작성일', '댓글수']
                        fig = px.bar(date_counts, x='작성일', y='댓글수', color_discrete_sequence=['#FF4B4B'])
                        st.plotly_chart(fig, use_container_width=True)
                        
                    st.write("---")
                    st.subheader("📋 수집된 댓글 데이터 원본")
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("이 영상에는 댓글이 없거나 비활성화되어 있습니다.")
            except Exception as e:
                st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")
