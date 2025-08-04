# Intelligent Procurement Agent

This repository contains a multi-agent AI system designed to streamline the e-procurement process. The assistant supports the following key functionalities:

- Supplier search based on natural language requirements  
- Auto-generation of RFQs and RFPs from conversational input  
- Comparison of supplier proposals with intelligent recommendations  

Built using:

- LangGraph for agent orchestration  
- OpenAI and Vertex AI for LLM integration  
- Streamlit for a responsive user interface  
- Modular architecture with separate components for agents, tools, and supervision  

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Intelligent-Procurement-Agent.git
cd Intelligent-Procurement-Agent

## 2. Set up the environment

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## 3. Configure environment variables

Create a `.env` file in the root directory and add the following:

OPENAI_API_KEY=your-key
GOOGLE_PROJECT_ID=your-project-id
VERTEX_LOCATION=your-region

## 4. Launch the Streamlit app

streamlit run streamlit_app.py

