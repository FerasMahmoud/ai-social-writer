import streamlit as st
import anthropic
import json

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Social Writer ✨",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── CSS Styling ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .main { background: #0f0f1a; }
    
    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 20px 60px rgba(102,126,234,0.4);
    }
    .hero h1 { color: white; font-size: 2.5rem; font-weight: 800; margin: 0; }
    .hero p  { color: rgba(255,255,255,0.85); font-size: 1.1rem; margin-top: 10px; }

    .card {
        background: #1a1a2e;
        border: 1px solid #2d2d4e;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .result-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #4a4a8a;
        border-radius: 16px;
        padding: 24px;
        margin: 12px 0;
        position: relative;
        transition: all 0.3s;
    }
    .result-card:hover { border-color: #667eea; box-shadow: 0 8px 30px rgba(102,126,234,0.2); }

    .result-label {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 4px 14px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .result-text {
        color: #e0e0ff;
        font-size: 1rem;
        line-height: 1.7;
        white-space: pre-wrap;
    }

    .hashtags {
        color: #667eea;
        font-weight: 600;
        font-size: 0.95rem;
        margin-top: 12px;
        line-height: 1.8;
    }

    .badge {
        display: inline-block;
        background: rgba(102,126,234,0.15);
        border: 1px solid rgba(102,126,234,0.3);
        color: #a0a8f0;
        padding: 3px 10px;
        border-radius: 8px;
        font-size: 0.78rem;
        margin: 3px;
    }

    .stat-row {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
    }
    .stat {
        flex: 1;
        background: #1a1a2e;
        border: 1px solid #2d2d4e;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    .stat-num { color: #667eea; font-size: 1.5rem; font-weight: 800; }
    .stat-lbl { color: #666; font-size: 0.75rem; margin-top: 4px; }

    .generate-btn button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        padding: 14px 40px !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        width: 100% !important;
        cursor: pointer !important;
        box-shadow: 0 8px 25px rgba(102,126,234,0.4) !important;
    }

    .footer {
        text-align: center;
        color: #444;
        font-size: 0.8rem;
        margin-top: 40px;
        padding: 20px;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextArea"] label,
    div[data-testid="stTextInput"] label,
    div[data-testid="stSlider"] label {
        color: #a0a8f0 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── Hero Section ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>✨ AI Social Writer</h1>
    <p>Generate viral social media content in seconds using AI</p>
</div>
""", unsafe_allow_html=True)

# ─── Stats ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stat-row">
    <div class="stat"><div class="stat-num">5</div><div class="stat-lbl">Platforms</div></div>
    <div class="stat"><div class="stat-num">3</div><div class="stat-lbl">Variations</div></div>
    <div class="stat"><div class="stat-num">∞</div><div class="stat-lbl">Ideas</div></div>
    <div class="stat"><div class="stat-num">⚡</div><div class="stat-lbl">Instant</div></div>
</div>
""", unsafe_allow_html=True)

# ─── API Key Input ────────────────────────────────────────────────────────────
with st.expander("🔑 Enter your Anthropic API Key", expanded=False):
    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="sk-ant-...",
        help="Get your key from console.anthropic.com"
    )
    st.markdown('<span class="badge">🔒 Never stored</span> <span class="badge">🔒 Session only</span>', unsafe_allow_html=True)

# Use session state for API key
if api_key:
    st.session_state["api_key"] = api_key
stored_key = st.session_state.get("api_key", "")

# ─── Input Form ──────────────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox(
        "📱 Platform",
        ["Instagram", "Twitter / X", "LinkedIn", "TikTok", "Facebook"],
        index=0
    )
with col2:
    tone = st.selectbox(
        "🎭 Tone",
        ["Professional", "Casual & Fun", "Inspirational", "Funny & Witty", "Educational", "Sales & Promotional"],
        index=0
    )

topic = st.text_area(
    "💡 What's your post about?",
    placeholder="e.g. Launching our new coffee blend that helps you focus better during work hours...",
    height=100
)

col3, col4 = st.columns(2)
with col3:
    language = st.selectbox(
        "🌍 Language",
        ["English", "Arabic", "Spanish", "French"],
        index=0
    )
with col4:
    num_variations = st.slider("📝 Variations", min_value=1, max_value=3, value=3)

include_hashtags = st.checkbox("# Include Hashtags", value=True)
include_cta = st.checkbox("📣 Include Call-to-Action", value=True)
include_emoji = st.checkbox("😊 Include Emojis", value=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─── Platform Limits ─────────────────────────────────────────────────────────
platform_limits = {
    "Instagram": "2,200 characters, story-friendly",
    "Twitter / X": "280 characters, punchy and direct",
    "LinkedIn": "3,000 characters, professional and insightful",
    "TikTok": "150 characters caption, hook-first",
    "Facebook": "63,206 characters, conversational"
}

# ─── Generate Button ─────────────────────────────────────────────────────────
st.markdown('<div class="generate-btn">', unsafe_allow_html=True)
generate = st.button("⚡ Generate Content")
st.markdown('</div>', unsafe_allow_html=True)

# ─── Generation Logic ────────────────────────────────────────────────────────
if generate:
    if not topic.strip():
        st.error("❌ Please enter a topic for your post!")
    elif not stored_key:
        st.error("❌ Please enter your Anthropic API key above!")
    else:
        with st.spinner("🤖 AI is crafting your content..."):
            try:
                client = anthropic.Anthropic(api_key=stored_key)

                extras = []
                if include_hashtags: extras.append("relevant hashtags (10-15)")
                if include_cta:      extras.append("a strong call-to-action")
                if include_emoji:    extras.append("appropriate emojis")

                prompt = f"""You are an expert social media content creator specializing in viral, engaging content.

Create {num_variations} different {platform} post variation(s) about: "{topic}"

Requirements:
- Platform: {platform} ({platform_limits[platform]})
- Tone: {tone}
- Language: {language}
- Include: {', '.join(extras) if extras else 'clean text only'}

For each variation, provide:
1. The main post caption (optimized for {platform})
2. Hashtags (if requested) - on a new line starting with HASHTAGS:
3. A brief note on why this variation works - on a new line starting with WHY:

Separate each variation with: ---VARIATION---

Make each variation genuinely different in angle, hook, and approach. Make them scroll-stopping and highly engaging."""

                response = client.messages.create(
                    model="claude-opus-4-5",
                    max_tokens=2000,
                    messages=[{"role": "user", "content": prompt}]
                )

                raw = response.content[0].text
                variations = raw.split("---VARIATION---")

                st.markdown("---")
                st.markdown(f"### 🎉 Your {platform} Content is Ready!")
                st.markdown(f'<span class="badge">✅ {len(variations)} variations</span> <span class="badge">📱 {platform}</span> <span class="badge">🎭 {tone}</span>', unsafe_allow_html=True)
                st.markdown("")

                for i, var in enumerate(variations, 1):
                    var = var.strip()
                    if not var:
                        continue

                    # Split caption, hashtags, why
                    caption = var
                    hashtags_text = ""
                    why_text = ""

                    if "HASHTAGS:" in var:
                        parts = var.split("HASHTAGS:")
                        caption = parts[0].strip()
                        rest = parts[1] if len(parts) > 1 else ""
                        if "WHY:" in rest:
                            h_parts = rest.split("WHY:")
                            hashtags_text = h_parts[0].strip()
                            why_text = h_parts[1].strip()
                        else:
                            hashtags_text = rest.strip()
                    elif "WHY:" in var:
                        parts = var.split("WHY:")
                        caption = parts[0].strip()
                        why_text = parts[1].strip()

                    st.markdown(f"""
<div class="result-card">
    <div class="result-label">Variation {i}</div>
    <div class="result-text">{caption}</div>
    {'<div class="hashtags">' + hashtags_text + '</div>' if hashtags_text else ''}
    {'<div style="margin-top:12px; color:#666; font-size:0.82rem; font-style:italic;">💡 ' + why_text + '</div>' if why_text else ''}
</div>
""", unsafe_allow_html=True)

                    # Copy button using st.code for easy copying
                    with st.expander(f"📋 Copy Variation {i}"):
                        full_text = caption
                        if hashtags_text:
                            full_text += "\n\n" + hashtags_text
                        st.code(full_text, language=None)

                st.success("✅ Done! Copy your favorite variation and post it!")

            except anthropic.AuthenticationError:
                st.error("❌ Invalid API key. Please check your Anthropic API key.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Made with ❤️ using Claude AI · <a href="https://console.anthropic.com" style="color:#667eea">Get API Key</a>
</div>
""", unsafe_allow_html=True)
