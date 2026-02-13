import streamlit as st
import g4f
import time

# 1. إعدادات الصفحة والهوية
st.set_page_config(page_title="X Assistant V2", page_icon="🤖", layout="wide")

# تعريف المستخدم في الذاكرة
if 'user_name' not in st.session_state:
    st.session_state.user_name = "أحمد الحريف"
    st.session_state.nickname = "Harreef"

st.title("🤖 X Assistant V2")
st.markdown(f"مبرمج التطبيق: **{st.session_state.user_name} (أحمد الحريف)**")

# 2. القائمة الجانبية للميزات الجديدة
st.sidebar.title(f"أهلاً يا {st.session_state.nickname}")
language = st.sidebar.selectbox("لغة الحوار:", ["العامية المصرية 🇪🇬", "العربية الفصحى"])

# خاصية البحث (X-Search)
st.sidebar.markdown("---")
search_query = st.sidebar.text_input("🔍 محرك بحث سريع:")
if search_query:
    st.sidebar.info(f"جاري البحث عن معلومات حديثة حول: {search_query}")

# خاصية إرسال الصور
uploaded_file = st.sidebar.file_uploader("📸 ارفع صورة للمساعد:", type=["jpg", "png", "jpeg"])
if uploaded_file:
    st.sidebar.image(uploaded_file, caption="تم استلام الصورة", use_column_width=True)

# 3. نظام الذاكرة والرسائل
if "messages" not in st.session_state:
    # تعليمات النظام لضبط الشخصية
    system_instruction = (
        f"أنت X Assistant V2. مبرمجك هو أحمد الحريف (Harreef). "
        f"تحدث بطلاقة بالعامية المصرية. تذكر دائماً أن تنادي المستخدم بلقبه '{st.session_state.nickname}'. "
        f"لديك قدرة على البحث وتحليل الصور."
    )
    st.session_state.messages = [
        {"role": "system", "content": system_instruction}
    ]

# عرض الرسائل القديمة (ما عدا تعليمات النظام)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 4. معالجة إدخال المستخدم والرد
if prompt := st.chat_input("اسأل X Assistant V2..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # استدعاء الذكاء الاصطناعي (GPT-4)
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                messages=st.session_state.messages,
            )
            
            # محاكاة الكتابة التدريجية لشكل احترافي
            full_response = ""
            for chunk in response:
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.01)
            message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error("السيرفر مشغول شوية يا حريف، جرب تدوس تاني!")
