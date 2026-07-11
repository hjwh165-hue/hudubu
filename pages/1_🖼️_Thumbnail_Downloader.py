import streamlit as st

st.set_page_config(page_title="썸네일 다운로더", page_icon="🖼️")
st.title("🖼️ 유튜브 썸네일 추출 및 저장")
st.write("---")

url = st.text_input("유튜브 동영상 링크를 입력하세요:")

if url:
    extract_video_id = st.session_state.get('extract_video_id')
    video_id = extract_video_id(url) if extract_video_id else None
    
    if video_id:
        # 유튜브 고화질 썸네일 주소 구조
        img_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
        st.markdown("### 📷 추출된 썸네일 (Max Resolution)")
        st.image(img_url, use_container_width=True)
        
        # 다운로드 링크 제공
        st.markdown(f"[🔗 여기를 우클릭해서 다른 이름으로 링크 저장]({img_url})")
    else:
        st.error("올바른 유튜브 URL 형식이 아닙니다.")
