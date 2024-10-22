import streamlit as st
from PIL import Image
import os

# portfolio page title
st.set_page_config(page_title="Gentley's Portfolio", page_icon="🚀")
st.title("🚀 Gentley's Data Science Portfolio")

col1, col2 = st.columns([1, 2])
with col1:
    image_path = 'profile_picture.jpg'
    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image, caption='Gentley - Data Science Enthusiast', width=150, use_column_width='always')
    else:
        st.warning("Profile picture not found. Please upload 'profile_picture.jpg' to the project directory.")

with col2:
    st.subheader("📬 Contact Information")
    st.write("Feel free to connect with me:")
    st.markdown("**Email**: gentleyrakotomalala@gmail.com")
    st.markdown("[💼 LinkedIn](https://www.linkedin.com/in/gentley-tsen)")
    st.markdown("[🐱 Github](https://github.com/GentleyR?tab=repositories)")

#emphasis box
st.subheader("👋 Introduction")
st.info("""
    Hello, I'm Gentley, a 4th year engineering student specializing in Data Science at EFREI Paris.
    I have experience in data manipulation, machine learning, and data visualization, and I'm passionate
    about using data to drive innovation and solve complex challenges.
""")

# education with expanders section
st.subheader("🎓 Education")
with st.expander("EFREI Paris - Data and AI Specialization"):
    st.write("Pursuing a Master's Degree in Engineering with a focus on Data and AI, in a curriculum taught entirely in English. Relevant courses include Mathematics for Data Science, Data Visualization, Machine Learning, and Advanced Databases. Expected graduation: July 2026.")
with st.expander("University of California, Irvine - Exchange Program"):
    st.write("Semester abroad at one of the top 10 public universities in the United States. Achieved a 3.86 GPA, significantly enhancing adaptability, English language proficiency, and understanding of international professional practices. Aug 2023 - Dec 2023.")
with st.expander("Lycée Français de Tananarive"):
    st.write("Developed critical problem-solving and analytical thinking skills. Acquired intercultural skills essential for working in diverse environments. 2014 - 2021.")

#skills section in columns
st.subheader("🛠️ Technical Skills")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Programming Languages**")
    st.write("- Python\n- SQL")
with col2:
    st.markdown("**Data Science Tools**")
    st.write("- Pandas\n- NumPy\n- Matplotlib\n- Seaborn\n- Scikit-learn\n- TensorFlow\n- Tableau\n- Power BI")
st.markdown("**Machine Learning**: Decision Trees, Random Forest, Hyperparameter Tuning, Clustering, Reinforcement Learning, Neural Networks, Deep Learning")
st.markdown("**Techniques**: Data Cleaning, Statistical Analysis, Exploratory Data Analysis (EDA), Predictive Modeling")
st.markdown("**Deployment**: Flask-based web applications, deployment on Render")

#projects bullet points
st.subheader("📁 Selected Projects")
st.write("""
    - **5G Antenna Management and Prediction System (5GSPOT Project)**: Implemented clustering techniques using K-means to categorize antenna frequencies and applied LSTM models to predict future antenna demands with 97% accuracy. Managed a dataset of 1,000,000 communication records; performed data cleaning and exploratory data analysis (EDA).
    - **DVF Data Analysis (Real Estate Valuation Data)**: Integrated and cleaned over 9 million real estate transaction records, resulting in a 30% reduction in data inconsistencies and improved model accuracy. Developed machine learning models using K-means for clustering and KNN for price prediction, achieving a 10% improvement in predictive accuracy.
    - **Diabetes Classification Project**: A machine learning model to classify diabetic patients using Random Forest, with hyperparameter tuning.
""")

# sofr skills bullet points
st.subheader("🤝 Soft Skills")
st.write("""
    - **Adaptability**: Quickly adapt to new environments and learning conditions, demonstrated through international studies and projects.
    - **High Standards**: Rigorous attention to detail and quality, ensuring that all work meets or exceeds expectations.
    - **Problem-Solving**: Developed innovative solutions to complex challenges, reducing data processing times and improving model accuracy.
    - **Project Management**: Managed multiple data science projects from planning to execution, maintaining timelines and quality standards.
    - **Teamwork**: Collaborated effectively in diverse teams to deliver complex projects and achieve common goals.
""")