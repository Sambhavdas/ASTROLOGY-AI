
import streamlit as st
from openai import OpenAI

# =====================================================
# NVIDIA API CONNECTION
# =====================================================

NVIDIA_API_KEY = st.secrets["NVIDIA_API_KEY"]

client = OpenAI(
    api_key=NVIDIA_API_KEY,
    base_url="https://integrate.api.nvidia.com/v1"
)


# =====================================================
# PAGE SETUP
# =====================================================

st.set_page_config(
    page_title="Astrology AI",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 Astrology AI")
st.write(
    "Get a personalized astrology reading based on your birth details."
)

st.divider()


# =====================================================
# BIRTH INFORMATION
# =====================================================

st.header("🌟 Birth Information")

name = st.text_input(
    "Name / Identifier",
    placeholder="Enter your name"
)

dob = st.date_input(
    "Date of Birth"
)

birth_time = st.text_input(
    "Exact Time of Birth",
    placeholder="Example: 07:35 AM"
)

birth_place = st.text_input(
    "Place of Birth",
    placeholder="Example: Kolkata, West Bengal, India"
)


# =====================================================
# ASTROLOGY SYSTEM
# =====================================================

astrology_system = st.selectbox(
    "Preferred Astrology System",
    [
        "Vedic (Sidereal / Lahiri)",
        "Western (Tropical)",
        "Both Vedic and Western"
    ]
)


# =====================================================
# FOCUS AREAS
# =====================================================

focus_areas = st.multiselect(
    "Core Focus Areas",
    [
        "Career & Purpose",
        "Wealth & Money",
        "Relationships & Marriage",
        "Education",
        "General Life"
    ],
    default=["Career & Purpose"]
)

st.divider()


# =====================================================
# GENERATE ASTROLOGY READING
# =====================================================

if st.button("🔮 Generate Astrology Reading"):

    # -----------------------------
    # Input validation
    # -----------------------------

    if not name:
        st.warning("Please enter your name.")
        st.stop()

    if not birth_time:
        st.warning("Please enter your birth time.")
        st.stop()

    if not birth_place:
        st.warning("Please enter your birth place.")
        st.stop()

    selected_focus = ", ".join(focus_areas)


    # =================================================
    # AI PROMPT
    # =================================================

    prompt = f"""
You are an expert astrology interpretation assistant
proficient in both Vedic (Jyotish) and Western astrology.

Create a personalized astrology reading using the
following information.

Name:
{name}

Date of Birth:
{dob}

Exact Time of Birth:
{birth_time}

Place of Birth:
{birth_place}

Preferred Astrology System:
{astrology_system}

Focus Areas:
{selected_focus}


IMPORTANT RULES:

1. Do not present astrology as scientifically proven fact.

2. Do not make guaranteed or fatalistic predictions.

3. Treat astrology as an interpretive framework describing
tendencies, possibilities and patterns.

4. If the birth time is unknown or approximate, clearly
explain that Ascendant/Lagna and house placements may
not be reliable.

5. Do not invent planetary degrees, coordinates,
house cusps or astronomical calculations.

6. If exact astronomical calculations are unavailable,
say so clearly rather than pretending they are exact.

7. Give practical and constructive advice.

8. Clearly distinguish interpretation from factual
astronomical calculation.


STRUCTURE THE READING AS:


1. CORE CHART ARCHITECTURE

- Ascendant / Rising Sign
- Sun Sign
- Moon Sign
- Nakshatra if Vedic and reliably available
- Elemental balance
- Dominant modality


2. KEY PLANETARY INFLUENCES

Discuss:

- Mercury
- Venus
- Mars
- Jupiter
- Saturn
- Rahu / North Node
- Ketu / South Node

Include outer planets if Western astrology
is selected.


3. MAJOR ASPECTS / YOGAS

Discuss:

- Conjunctions
- Oppositions
- Trines
- Squares
- Important Vedic Yogas where reliably calculable


4. CAREER & PURPOSE

Discuss:

- Professional strengths
- Leadership style
- Suitable career environments
- Long-term development
- Potential areas for growth


5. WEALTH & ASSETS

Discuss:

- Financial tendencies
- Income-building strengths
- Saving and spending patterns
- Value creation


6. RELATIONSHIPS & MARRIAGE

Discuss:

- Relationship tendencies
- Communication style
- Attachment patterns
- Partner qualities
- Relationship growth areas


7. CURRENT CYCLES

Discuss relevant planetary transits or Vedic
Dasha periods only when they can be calculated
reliably from the available information.

Focus on the upcoming 6–12 months.

Do not make guaranteed predictions.


8. PRACTICAL RECOMMENDATIONS

Give 3–4 concrete recommendations for:

- Personal development
- Career
- Finance
- Relationships


Use clear headings, simple language,
and a supportive tone.

Do not claim certainty about the future.
"""


    # =================================================
    # CALL NVIDIA AI
    # =================================================

    with st.spinner("🔮 Generating your astrology reading..."):

        try:

            response = client.chat.completions.create(
                model="deepseek-ai/deepseek-v4.1-flash",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a careful astrology "
                            "interpretation assistant. "
                            "Never present astrology as "
                            "scientifically proven fact."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=4000
            )

            result = response.choices[0].message.content

            st.success("✨ Astrology Reading Generated!")

            st.markdown(result)

        except Exception as e:

            st.error(f"Error: {e}")