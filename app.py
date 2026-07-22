import streamlit as st
from datetime import datetime

from ai.verifier import VeriSightVerifier
from ai.media_detector import analyze_media
from ai.report import generate_report


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="VeriSight",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ VeriSight")
st.subheader("AI for Ultra-Accurate Truth Detection")

st.markdown("""
Powered by **VeriSight Neural Intelligence**.

Verify claims and inspect media using semantic AI,
trusted evidence ranking, and transparent confidence scoring.
""")

st.divider()

verifier = VeriSightVerifier()

tab1, tab2 = st.tabs(
    [
        "📰 Fact Verification",
        "🎥 Media Verification"
    ]
)

# ==========================================================
# FACT VERIFICATION
# ==========================================================

with tab1:

    claim = st.text_area(
        "Enter a claim",
        placeholder="Example: NASA confirms water on Mars",
        height=140,
    )

    if st.button("Verify Claim", use_container_width=True):

        if not claim.strip():
            st.warning("Please enter a claim.")
            st.stop()

        with st.spinner("Searching trusted sources..."):

            verdict, confidence, reasoning, evidence = verifier.verify(claim)

        st.success("Verification Complete")

        left, right = st.columns([1, 2])

        with left:

            st.metric(
                "Confidence",
                f"{confidence}%"
            )

            st.progress(confidence / 100)

        with right:

            colors = {
                "Likely True": "green",
                "Mostly Supported": "orange",
                "Mixed Evidence": "gold",
                "Unverified": "red"
            }

            color = colors.get(verdict, "gray")

            st.markdown(
                f"<h2 style='color:{color}'>{verdict}</h2>",
                unsafe_allow_html=True
            )

            st.write(reasoning)

        st.divider()

        st.subheader("Evidence")

        if evidence:

            for article in evidence:

                with st.expander(article["title"]):

                    st.write(f"**Source:** {article['source']}")

                    st.write(
                        f"Similarity Score: **{article['similarity']:.2f}**"
                    )

                    if article.get("summary"):
                        st.write(article["summary"])

                    if article.get("link"):
                        st.link_button(
                            "Open Article",
                            article["link"]
                        )

        else:

            st.info("No relevant supporting evidence found.")

        report = generate_report(
            claim,
            verdict,
            confidence,
            reasoning,
            evidence
        )

        st.download_button(
            "⬇ Download Verification Report",
            report,
            file_name="verisight_report.txt",
            mime="text/plain",
            use_container_width=True,
        )

# ==========================================================
# MEDIA VERIFICATION
# ==========================================================

with tab2:

    uploaded = st.file_uploader(
        "Upload Image, Video or Audio",
        type=[
            "jpg",
            "jpeg",
            "png",
            "mp4",
            "mov",
            "avi",
            "mp3",
            "wav",
        ],
    )

    if uploaded is not None:

        if uploaded.type.startswith("image"):
            st.image(uploaded, use_container_width=True)

        elif uploaded.type.startswith("video"):
            st.video(uploaded)

        elif uploaded.type.startswith("audio"):
            st.audio(uploaded)

        if st.button("Analyze Media", use_container_width=True):

            with st.spinner("Analyzing media..."):

                result = analyze_media(uploaded)

            st.success("Analysis Complete")

            left, right = st.columns([1, 2])

            with left:

                st.metric(
                    "Confidence",
                    f"{result['confidence']}%"
                )

                st.progress(result["confidence"] / 100)

            with right:

                if result["confidence"] >= 80:
                    st.success(result["verdict"])

                elif result["confidence"] >= 60:
                    st.warning(result["verdict"])

                else:
                    st.error(result["verdict"])

                st.subheader("Reasoning")

                for item in result["reasoning"]:
                    st.write(f"• {item}")

            media_report = f"""
VERISIGHT MEDIA REPORT

Generated:
{datetime.now()}

File:
{uploaded.name}

Type:
{result['type']}

Verdict:
{result['verdict']}

Confidence:
{result['confidence']}%

Reasoning:
"""

            for item in result["reasoning"]:
                media_report += f"\n- {item}"

            st.download_button(
                "⬇ Download Media Report",
                media_report,
                file_name="media_report.txt",
                mime="text/plain",
                use_container_width=True,
            )

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "Powered by VeriSight Neural Intelligence • MVP v1.0"
)

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    max-width:1200px;
}

div[data-testid="stMetric"]{
    border-radius:16px;
    padding:20px;
    background:#1E293B;
}

.stButton>button{
    width:100%;
    height:50px;
    border-radius:12px;
    font-weight:bold;
    font-size:16px;
}

textarea{
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)