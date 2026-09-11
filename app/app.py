import streamlit as st


st.set_page_config(
    page_title="AI Decision Quality Lab",
    page_icon="🧠",
    layout="centered",
)


st.title("🧠 AI Decision Quality Lab")

st.write(
    """
    Does AI actually improve human decision-making,
    or does it simply make people more confident?
    """
)

st.divider()

st.subheader("Investment Decision")

st.write("A company is considering a new investment.")

col1, col2 = st.columns(2)

with col1:
    st.metric("Expected Return", "8%")
    st.metric("Success Probability", "70%")

with col2:
    st.metric("Potential Loss", "€200,000")
    st.metric("Investment", "€1,000,000")

st.divider()

st.subheader("What would you decide?")

decision = st.radio(
    "Choose one:",
    ["Invest", "Do not invest"],
)

confidence = st.slider(
    "How confident are you?",
    min_value=0,
    max_value=100,
    value=50,
)

if st.button("Submit Decision"):
    st.success("Decision recorded!")

    st.write(f"**Decision:** {decision}")
    st.write(f"**Confidence:** {confidence}%")