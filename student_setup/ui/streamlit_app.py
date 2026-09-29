import os

import httpx
import streamlit as st

BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")
st.set_page_config(page_title="College Student Copilot", page_icon="🎓", layout="wide")
st.title("🎓 College Student Copilot")

msg = st.chat_input("Ask about academic support, e.g. 'Analyze CSE 3rd year'")
if msg:
    with st.spinner("Agents working..."):
        r = httpx.post(f"{BACKEND}/chat", json={"message": msg}, timeout=300)
        st.session_state["last"] = r.json()

data = st.session_state.get("last")
if data:
    left, right = st.columns([3, 1])
    with left:
        if data.get("summary"):
            st.subheader(data["summary"])
        for s in data.get("flagged", []):
            with st.expander(f"{s['student_id']} - {s['name']}"):
                st.json(s["evidence"])
                for i in s["indicators"]:
                    st.write("•", i)
        if data.get("analysis"):
            st.json(data["analysis"])
        if data.get("answer"):
            st.write(data["answer"])
            st.caption("Sources: " + ", ".join(data.get("sources", [])))
        if data.get("recommendations"):
            st.markdown("**Recommendations (for faculty review)**")
            st.write(data["recommendations"])
        if data.get("draft"):
            d = data["draft"]
            st.markdown("**Draft message**")
            st.text_area("Review", d["content"], key=f"d{d['id']}")
            c1, c2 = st.columns(2)
            if c1.button("Approve", key=f"a{d['id']}"):
                st.success(httpx.post(f"{BACKEND}/drafts/{d['id']}/approve").json()["status"])
            if c2.button("Cancel", key=f"c{d['id']}"):
                st.warning(httpx.post(f"{BACKEND}/drafts/{d['id']}/cancel").json()["status"])
    with right:
        st.markdown("**Agent Activity**")
        for step in dict.fromkeys(data.get("trace", [])):
            st.write("✓", step)
