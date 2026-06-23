import json
import streamlit as st

from utils.ollama_client import analyze_vacancy
from utils.postprocess import postprocess

st.set_page_config(
    page_title="Sourcing Assistant",
    page_icon="🔎",
    layout="wide"
)

with open("styles.css", encoding="utf-8") as css:
    st.markdown(
        f"<style>{css.read()}</style>",
        unsafe_allow_html=True
    )

st.markdown("""
<div class="hero">
    <h1>🔎 Sourcing Assistant</h1>
    <p>AI-помощник для генерации Boolean-запросов для hh.ru</p>
</div>
""", unsafe_allow_html=True)

vacancy = st.text_area(
    "Текст вакансии",
    height=350,
    placeholder="Вставьте сюда текст вакансии..."
)

if st.button("✨ Сгенерировать", use_container_width=True):

    if not vacancy.strip():
        st.warning("Введите текст вакансии.")
        st.stop()

    with st.spinner("Анализируем вакансию..."):
        result = analyze_vacancy(vacancy)
        try:
            data = json.loads(result)
            data = postprocess(data)

            role = data.get("role", "")
            boolean = data.get("boolean", "")

            must_have = " ".join(data.get("must_have", []))
            any_words = " ".join(data.get("any_words", []))

            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.subheader("👤 Целевая должность")
            st.code(role, language=None)
            st.markdown("</div>", unsafe_allow_html=True)

            st.subheader("🔎 Булевый запрос для hh.ru")
            st.code(boolean, language=None)

            st.subheader("✅ Обязательный стек (Точно есть)")
            st.code(must_have, language=None)

            st.subheader("🧰 Поисковые технологии")
            st.code(any_words, language=None)

            st.info(
                """
💡 После генерации Boolean не забудьте настроить фильтры hh.ru:

• регион поиска
• опыт работы
• возраст кандидатов
• образование
"""
            )
        except Exception:
            st.error("Не удалось обработать ответ модели.")
            with st.expander("Ответ модели"):
                st.code(result)
