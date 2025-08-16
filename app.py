import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
import re
from collections import Counter
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="AI Dream Journal Analyzer",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 2rem;
    }
    .dream-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

class DreamAnalyzer:
    def __init__(self):
        self.emotions = ['joy', 'fear', 'anger', 'sadness', 'surprise', 'love', 'anxiety']
        self.dream_themes = ['flying', 'falling', 'chase', 'water', 'animals', 'death', 'school', 'work', 'family']
    
    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        return {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity,
            'emotion': self.get_dominant_emotion(text)
        }
    
    def get_dominant_emotion(self, text):
        emotion_keywords = {
            'joy': ['happy', 'joy', 'excited', 'wonderful', 'amazing', 'great', 'love'],
            'fear': ['scared', 'afraid', 'terrified', 'nightmare', 'horror', 'panic'],
            'anger': ['angry', 'mad', 'furious', 'rage', 'annoyed', 'frustrated'],
            'sadness': ['sad', 'depressed', 'crying', 'tears', 'lonely', 'grief'],
            'anxiety': ['worried', 'anxious', 'nervous', 'stress', 'tension', 'uneasy']
        }
        
        text_lower = text.lower()
        emotion_scores = {}
        
        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            emotion_scores[emotion] = score
        
        return max(emotion_scores, key=emotion_scores.get) if max(emotion_scores.values()) > 0 else 'neutral'
    
    def extract_themes(self, text):
        theme_keywords = {
            'flying': ['fly', 'flying', 'soar', 'wings', 'air', 'sky'],
            'falling': ['fall', 'falling', 'drop', 'cliff', 'height'],
            'chase': ['chase', 'run', 'escape', 'pursue', 'follow'],
            'water': ['water', 'ocean', 'river', 'swim', 'drown', 'flood'],
            'animals': ['dog', 'cat', 'bird', 'snake', 'lion', 'animal'],
            'death': ['death', 'die', 'dead', 'funeral', 'grave'],
            'school': ['school', 'teacher', 'exam', 'classroom', 'student'],
            'work': ['work', 'office', 'boss', 'meeting', 'job'],
            'family': ['mother', 'father', 'family', 'parent', 'sibling']
        }
        
        text_lower = text.lower()
        found_themes = []
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                found_themes.append(theme)
        
        return found_themes
    
    def predict_next_dream(self, dreams_df):
        if len(dreams_df) < 3:
            return "Need more dreams for prediction"
        
        recent_emotions = dreams_df.tail(5)['emotion'].tolist()
        recent_themes = []
        for themes in dreams_df.tail(5)['themes']:
            recent_themes.extend(themes)
        
        emotion_counter = Counter(recent_emotions)
        theme_counter = Counter(recent_themes)
        
        predicted_emotion = emotion_counter.most_common(1)[0][0] if emotion_counter else 'neutral'
        predicted_theme = theme_counter.most_common(1)[0][0] if theme_counter else 'unknown'
        
        return f"Likely emotion: {predicted_emotion}, Likely theme: {predicted_theme}"

def main():
    st.markdown('<h1 class="main-header">🌙 AI Dream Journal Analyzer</h1>', unsafe_allow_html=True)
    
    analyzer = DreamAnalyzer()
    
    # Initialize session state
    if 'dreams' not in st.session_state:
        st.session_state.dreams = []
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Add Dream", "Analytics", "Predictions", "Export Data"])
    
    if page == "Add Dream":
        st.header("📝 Record Your Dream")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            dream_text = st.text_area("Describe your dream:", height=200, placeholder="I dreamed that I was flying over a beautiful landscape...")
            
        with col2:
            dream_date = st.date_input("Dream Date", datetime.now())
            lucid = st.checkbox("Was this a lucid dream?")
            sleep_quality = st.slider("Sleep Quality (1-10)", 1, 10, 7)
            
        if st.button("Analyze & Save Dream", type="primary"):
            if dream_text:
                # Analyze the dream
                sentiment = analyzer.analyze_sentiment(dream_text)
                themes = analyzer.extract_themes(dream_text)
                
                dream_entry = {
                    'date': dream_date.strftime('%Y-%m-%d'),
                    'text': dream_text,
                    'polarity': sentiment['polarity'],
                    'subjectivity': sentiment['subjectivity'],
                    'emotion': sentiment['emotion'],
                    'themes': themes,
                    'lucid': lucid,
                    'sleep_quality': sleep_quality,
                    'word_count': len(dream_text.split())
                }
                
                st.session_state.dreams.append(dream_entry)
                
                # Display analysis
                st.success("Dream analyzed and saved!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Emotion", sentiment['emotion'].title())
                with col2:
                    st.metric("Sentiment", f"{sentiment['polarity']:.2f}")
                with col3:
                    st.metric("Themes Found", len(themes))
                
                if themes:
                    st.write("**Detected Themes:**", ", ".join(themes))
            else:
                st.error("Please enter a dream description!")
    
    elif page == "Analytics":
        st.header("📊 Dream Analytics")
        
        if not st.session_state.dreams:
            st.warning("No dreams recorded yet. Add some dreams to see analytics!")
            return
        
        df = pd.DataFrame(st.session_state.dreams)
        df['date'] = pd.to_datetime(df['date'])
        
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Dreams", len(df))
        with col2:
            avg_sentiment = df['polarity'].mean()
            st.metric("Avg Sentiment", f"{avg_sentiment:.2f}")
        with col3:
            lucid_pct = (df['lucid'].sum() / len(df)) * 100
            st.metric("Lucid Dreams", f"{lucid_pct:.1f}%")
        with col4:
            avg_sleep = df['sleep_quality'].mean()
            st.metric("Avg Sleep Quality", f"{avg_sleep:.1f}")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Emotion distribution
            emotion_counts = df['emotion'].value_counts()
            fig_emotions = px.pie(values=emotion_counts.values, names=emotion_counts.index, 
                                title="Dream Emotions Distribution")
            st.plotly_chart(fig_emotions, use_container_width=True)
        
        with col2:
            # Sentiment over time
            fig_sentiment = px.line(df, x='date', y='polarity', title="Sentiment Over Time")
            st.plotly_chart(fig_sentiment, use_container_width=True)
        
        # Theme analysis
        all_themes = []
        for themes in df['themes']:
            all_themes.extend(themes)
        
        if all_themes:
            theme_counts = Counter(all_themes)
            fig_themes = px.bar(x=list(theme_counts.keys()), y=list(theme_counts.values()),
                              title="Most Common Dream Themes")
            st.plotly_chart(fig_themes, use_container_width=True)
        
        # Sleep quality vs sentiment correlation
        fig_corr = px.scatter(df, x='sleep_quality', y='polarity', 
                            title="Sleep Quality vs Dream Sentiment",
                            trendline="ols")
        st.plotly_chart(fig_corr, use_container_width=True)
    
    elif page == "Predictions":
        st.header("🔮 Dream Predictions")
        
        if len(st.session_state.dreams) < 3:
            st.warning("Need at least 3 dreams for predictions!")
            return
        
        df = pd.DataFrame(st.session_state.dreams)
        prediction = analyzer.predict_next_dream(df)
        
        st.markdown(f"""
        <div class="dream-card">
            <h3>🌟 Next Dream Prediction</h3>
            <p>{prediction}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Pattern analysis
        st.subheader("📈 Pattern Analysis")
        
        # Weekly patterns
        df['date'] = pd.to_datetime(df['date'])
        df['weekday'] = df['date'].dt.day_name()
        
        weekday_sentiment = df.groupby('weekday')['polarity'].mean().reindex([
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
        ])
        
        fig_weekly = px.bar(x=weekday_sentiment.index, y=weekday_sentiment.values,
                           title="Average Sentiment by Day of Week")
        st.plotly_chart(fig_weekly, use_container_width=True)
        
        # Recommendations
        st.subheader("💡 Recommendations")
        
        avg_sentiment = df['polarity'].mean()
        if avg_sentiment < -0.1:
            st.info("💙 Your dreams tend to be negative. Consider relaxation techniques before bed.")
        elif avg_sentiment > 0.1:
            st.success("😊 Your dreams are generally positive! Keep up good sleep habits.")
        else:
            st.info("😐 Your dreams are emotionally balanced.")
    
    elif page == "Export Data":
        st.header("📤 Export Your Data")
        
        if not st.session_state.dreams:
            st.warning("No dreams to export!")
            return
        
        df = pd.DataFrame(st.session_state.dreams)
        
        # Display data
        st.subheader("Your Dream Data")
        st.dataframe(df)
        
        # Export options
        col1, col2 = st.columns(2)
        
        with col1:
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name=f"dreams_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col2:
            json_data = df.to_json(orient='records', indent=2)
            st.download_button(
                label="Download as JSON",
                data=json_data,
                file_name=f"dreams_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()