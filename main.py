import streamlit as st
import os
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.serpapi_tools import SerpApiTools

# Initialize page config
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with modern design principles
st.markdown("""
    <style>
    /* Main theme colors and variables */
    :root {
        --primary-color: #4A90E2;
        --secondary-color: #F67280;
        --background-dark: #1E1E1E;
        --background-light: #F5F7FA;
        --text-primary: #2C3E50;
        --text-secondary: #7F8C8D;
        --success-color: #2ECC71;
        --warning-color: #F1C40F;
        --error-color: #E74C3C;
        --radius: 12px;
        --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Global styles */
    .main {
        background-color: var(--background-light);
    }

    /* Header styles */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        padding: 2rem;
        border-radius: var(--radius);
        color: white;
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
    }

    /* Card styles */
    .stCard {
        background: white;
        padding: 1.5rem;
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        margin: 1rem 0;
        border: none;
    }

    /* Button styles */
    .stButton > button {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color)) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: var(--radius) !important;
        font-weight: 600 !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

    /* Input field styles */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: var(--radius);
        border: 2px solid #E0E0E0;
        padding: 0.75rem;
        transition: border-color 0.2s ease;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.1);
    }

    /* Sidebar styles */
    .sidebar .sidebar-content {
        background-color: white;
        padding: 2rem;
    }

    .sidebar .element-container {
        margin-bottom: 1.5rem;
    }

    /* Travel summary card */
    .travel-summary {
        background: white;
        padding: 2rem;
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        margin-bottom: 2rem;
    }

    .travel-summary h4 {
        color: var(--primary-color);
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }

    /* Expander styles */
    .streamlit-expanderHeader {
        background-color: white;
        border-radius: var(--radius);
        border: none;
        box-shadow: var(--shadow);
        padding: 1rem;
    }

    /* Progress spinner */
    .stSpinner > div {
        border-color: var(--primary-color) !important;
    }

    /* Select box styles */
    .stSelectbox > div > div {
        border-radius: var(--radius);
    }

    /* Multiselect styles */
    .stMultiSelect > div > div {
        border-radius: var(--radius);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/airplane-take-off.png", width=96)
    st.title("✈️ Trip Settings")
    
    with st.container():
        st.subheader("🔑 API Configuration")
        groq_api_key = st.text_input("Groq API Key", type="password", help="Enter your Groq API key")
        serpapi_key = st.text_input("SerpAPI Key", type="password", help="Enter your SerpAPI key")
    
    st.divider()
    
    with st.container():
        st.subheader("🌍 Trip Details")
        destination = st.text_input(
            "Destination",
            placeholder="Where would you like to go?",
            help="Enter your dream destination"
        )
        
        duration = st.number_input(
            "Duration (Days)",
            min_value=1,
            max_value=30,
            value=5,
            help="How long would you like to stay?"
        )
        
        budget = st.select_slider(
            "Budget Level",
            options=["Budget", "Moderate", "Luxury"],
            value="Moderate",
            help="Select your preferred budget level"
        )
        
        travel_style = st.multiselect(
            "Travel Interests",
            ["Culture", "Nature", "Adventure", "Relaxation", "Food", "Shopping"],
            ["Culture", "Nature"],
            help="Select your travel interests"
        )

# Initialize session state
if 'travel_plan' not in st.session_state:
    st.session_state.travel_plan = None

# Main content area
st.markdown("""
    <div class='main-header'>
        <h1 style='font-size: 2.5rem; margin-bottom: 1rem;'>✈️ AI Travel Planner</h1>
        <p style='font-size: 1.2rem; opacity: 0.9;'>Your personal AI-powered travel companion</p>
    </div>
""", unsafe_allow_html=True)

# Travel Summary Card
if destination:
    st.markdown(f"""
        <div class='travel-summary'>
            <h4>🌟 Your Travel Preferences</h4>
            <p><strong>Destination:</strong> {destination}</p>
            <p><strong>Duration:</strong> {duration} days</p>
            <p><strong>Budget Level:</strong> {budget}</p>
            <p><strong>Travel Interests:</strong> {', '.join(travel_style)}</p>
        </div>
    """, unsafe_allow_html=True)

try:
    # Set API keys
    os.environ["GROQ_API_KEY"] = groq_api_key
    os.environ["SERPAPI_KEY"] = serpapi_key

    # Initialize travel agent
    travel_agent = Agent(
        name="Travel Planner",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[SerpApiTools()],
        instructions=[
            "You are a knowledgeable travel planning assistant.",
            "Create detailed, personalized travel plans based on user preferences.",
            "Provide current and accurate information about destinations.",
            "Include practical tips and local insights."
        ],
        show_tool_calls=True,
        markdown=True
    )

    # Generate travel plan
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ Generate My Perfect Travel Plan", use_container_width=True):
            if destination and groq_api_key and serpapi_key:
                try:
                    with st.spinner("🔍 Crafting your perfect travel itinerary..."):
                        prompt = f"""Create a detailed travel plan for {destination} for {duration} days.

Travel Preferences:
- Budget Level: {budget}
- Travel Interests: {', '.join(travel_style)}

Please provide:

1. 🌞 Best Time to Visit & Weather
2. 🏨 {budget}-level Accommodation Options
3. 🗺️ Day-by-Day Itinerary
4. 🍽️ Local Cuisine & Restaurants
5. 💡 Travel Tips & Transportation
6. 💰 Budget Breakdown

Format the response in clear markdown with emojis for better readability."""

                        response = travel_agent.run(prompt)
                        if hasattr(response, 'content'):
                            clean_response = response.content.replace('∣', '|').replace('\n\n\n', '\n\n')
                            st.session_state.travel_plan = clean_response
                            st.markdown(clean_response)
                        else:
                            st.session_state.travel_plan = str(response)
                            st.markdown(str(response))
                except Exception as e:
                    st.error(f"😟 Error generating travel plan: {str(e)}")
                    st.info("Please try again in a moment.")
            else:
                if not destination:
                    st.warning("🌍 Please enter a destination")
                if not groq_api_key or not serpapi_key:
                    st.warning("🔑 Please enter both API keys")

    # Q&A Section
    st.divider()
    
    with st.expander("🤔 Have a specific question about your trip?"):
        question = st.text_input(
            "",
            placeholder="Ask anything about your destination or travel plan...",
            key="qa_input"
        )
        
        if st.button("🔍 Get Answer", key="qa_button"):
            if question and st.session_state.travel_plan:
                with st.spinner("Searching for your answer..."):
                    try:
                        context_question = f"""
                        Based on this travel plan for {destination}:
                        {st.session_state.travel_plan}

                        Please answer: {question}
                        
                        Provide a clear, focused answer based on the travel plan.
                        """
                        response = travel_agent.run(context_question)
                        st.markdown("---")
                        st.markdown("### 💡 Answer")
                        if hasattr(response, 'content'):
                            st.markdown(response.content)
                        else:
                            st.markdown(str(response))
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            elif not st.session_state.travel_plan:
                st.warning("Please generate a travel plan first.")
            else:
                st.warning("Please enter your question.")

except Exception as e:
    st.error(f"Application Error: {str(e)}")
