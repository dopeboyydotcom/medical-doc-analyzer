import streamlit as st
from analyzer import analyze_document, extract_pdf_text, ask_question

st.set_page_config(
    page_title="Medical Document Analyzer",
    page_icon=":hospital:",
    layout="wide"
)

st.title("Medical Document Analyzer")
st.markdown("Upload a clinical document to extract key medical information.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    pdf_bytes = uploaded_file.read()

    if "analysis_result" not in st.session_state:
        with st.spinner("Analyzing document..."):
            st.session_state.analysis_result = analyze_document(pdf_bytes)
            st.session_state.pdf_text = extract_pdf_text(pdf_bytes)
            st.session_state.messages = []

    result = st.session_state.analysis_result

    if "error" in result:
        st.error(f"Analysis failed: {result['error']}")
    else:
        if result.get("red_flags"):
            st.error("Red Flags Detected")
            for flag in result["red_flags"]:
                st.warning(flag)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Diagnoses")
            for d in result.get("diagnoses", []):
                st.write(f"• {d}")

            st.subheader("Allergies")
            for a in result.get("allergies", []):
                st.write(f"• {a}")

            st.subheader("Key Dates")
            dates = result.get("key_dates", {})
            if dates:
                if dates.get("admission"):
                    st.write(f"**Admission:** {dates['admission']}")
                if dates.get("discharge"):
                    st.write(f"**Discharge:** {dates['discharge']}")

        with col2:
            st.subheader("Medications")
            for med in result.get("medications", []):
                name = med.get("name", "Unknown")
                dose = med.get("dose", "Dose not specified")
                st.write(f"• **{name}** — {dose}")

        st.divider()
        with st.expander("View raw JSON output"):
            st.json(result)

        st.divider()
        st.subheader("Ask a question about this document")

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if question := st.chat_input("e.g. Are there any drug interactions I should know about?"):
            st.session_state.messages.append({
                "role": "user",
                "content": question
            })
            st.chat_message("user").write(question)

            with st.spinner("Thinking..."):
                answer = ask_question(
                    st.session_state.pdf_text,
                    st.session_state.messages
                )

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })
            st.chat_message("assistant").write(answer)