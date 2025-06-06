import streamlit as st
from utils.ai_service import get_ai_response
from utils.tts_service import text_to_speech

def render():
    """Hiển thị trang trò chuyện"""
    # Đầu trang có biểu tượng hấp dẫn
    col1, col2 = st.columns([1, 9])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2665/2665038.png", width=60)
    with col2:
        st.header("Trò chuyện với AI")
    
    # Hiển thị thông báo nếu chưa cung cấp API key
    if not st.session_state.api_key:
        st.info("🔑 Vui lòng nhập Google AI API Key trong phần cài đặt để bắt đầu trò chuyện", icon="ℹ️")
        st.divider()
    
    # Hiển thị lịch sử trò chuyện với kiểu dáng tốt hơn
    for i, message in enumerate(st.session_state.chat_history):
        role_icon = "🧑‍💻" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=role_icon):
            st.markdown(message["content"])
            if message["role"] == "assistant" and "audio_path" in message:
                st.audio(message["audio_path"], format="audio/mp3")
    
    # Nhập tin nhắn với placeholder hữu ích
    user_input = st.chat_input("Nhập câu hỏi của bạn...", key="chat_input")
    
    if user_input:
        if not st.session_state.api_key:
            st.error("⚠️ Bạn cần nhập API Key trước khi gửi tin nhắn", icon="🔒")
            return
            
        # Hiển thị tin nhắn người dùng
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(user_input)
        
        # Lưu tin nhắn người dùng vào lịch sử
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Hiển thị phản hồi của AI với spinner
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("AI đang suy nghĩ..."):
                response = get_ai_response(
                    user_input, 
                    st.session_state.selected_model, 
                    st.session_state.api_key
                )
                st.markdown(response)
                
                # Chuyển văn bản thành giọng nói với thông báo
                with st.spinner("Đang chuyển đổi thành giọng nói..."):
                    audio_path = text_to_speech(
                        response, 
                        st.session_state.tts_language, 
                        st.session_state.tts_speed
                    )
                    if audio_path:
                        st.audio(audio_path, format="audio/mp3")
        
        # Lưu phản hồi của AI vào lịch sử
        st.session_state.chat_history.append({
            "role": "assistant", 
            "content": response, 
            "audio_path": audio_path if 'audio_path' in locals() else None
        })
    
    # Thêm nút xóa lịch sử trò chuyện nếu có tin nhắn
    if st.session_state.chat_history:
        if st.button("🗑️ Xóa lịch sử trò chuyện", use_container_width=True, key="clear_chat_btn"):
            st.session_state.chat_history = []
            st.rerun()