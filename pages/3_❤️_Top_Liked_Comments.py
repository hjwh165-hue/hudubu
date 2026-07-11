import streamlit as st
import pandas as pd

st.set_page_config(page_title="인기 댓글", page_icon="❤️")
st.title("❤️ 좋아요가 가장 많은 베스트 댓글")
st.write("---")

url = st.text_input("유튜브 동영상 링크를 입력하세요:")

if url:
    youtube = st.session_state.get('get_youtube_client')()
    video_id = st.session_state.get('extract_video_id')(url)
    
    if youtube and video_id:
        with st.spinner("인기 댓글 필터링 중..."):
            try:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=50,
                    order="relevance" # 유관성/인기 순으로 정렬하여 호출
                )
                response = request.execute()
                
                comments = []
                for item in response.get('items', []):
                    snippet = item['snippet']['topLevelComment']['snippet']
                    comments.append({
                        "작성자": snippet['authorDisplayName'],
                        "좋아요 👍": snippet['likeCount'],
                        "내용": snippet['textDisplay']
                    })
                
                df = pd.DataFrame(comments)
                # 좋아요 순으로 완벽 재정렬 후 상위 10개만 표기
                df = df.sort_values(by="좋아요 👍", ascending=False).head(10)
                
                st.subheader("🏆 Top 10 베스트 댓글 리스트")
                for idx, row in df.iterrows():
                    with st.chat_message("user"):
                        st.markdown(f"**{row['작성자']}** (👍 좋아요 {row['좋아요 👍']}개)")
                        st.write(row['내용'])
                        
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
