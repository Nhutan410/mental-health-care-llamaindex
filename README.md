# AI Mental Health Care System

An intelligent mental health care system using LlamaIndex and OpenAI, capable of conversational therapy, psychological counseling, mental health analysis and diagnosis based on DSM-5 standards.

## 🎯 Features

- 🗣️ **Natural Conversation**: AI agent acts as a psychology expert
- 🔍 **Analysis & Diagnosis**: Assess mental health conditions according to DSM-5
- 📊 **Progress Tracking**: Store and analyze user health history
- 🔐 **Security**: Login/registration system to protect personal information

## 🛠️ Technologies Used

- **LlamaIndex**: RAG (Retrieval-Augmented Generation) framework
- **OpenAI GPT-4o-mini**: Large language model
- **Streamlit**: Web interface framework
- **ChromaDB**: Vector database for storing embeddings
- **Python 3.11**: Programming language

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Nhutan410/mental-health-care-llamaindex.git
cd mental-health-care
```

### 2. Create virtual environment

```bash
conda create -n mental_health python=3.11
conda activate mental_health
```

Or using venv:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure OpenAI API Key

Create `.streamlit/secrets.toml` file:

```toml
[openai]
OPENAI_API_KEY = "sk-your-api-key-here"
```

⚠️ **Important**: Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)

### 5. Build data

```bash
python build_data.py
```

This command will:

- Read DSM-5 documents
- Create nodes and embeddings
- Save to cache and index storage

## 🎮 Running the Application

```bash
streamlit run Home.py
```

Access: `http://localhost:8501`

## 📁 Project Structure

```
mental-health-care/
├── .streamlit/          # Streamlit configuration
├── data/                # Data and cache
│   ├── cache/          # Pipeline and chat cache
│   ├── index_storage/  # Vector indexes
│   ├── ingestion_storage/  # Source documents
│   └── user_storage/   # User information
├── src/                 # Main source code
│   ├── authenticate.py
│   ├── conversation_engine.py
│   ├── index_builder.py
│   ├── ingest_pipeline.py
│   └── prompts.py
├── pages/              # Streamlit pages
│   ├── 1_User_Health.py
│   └── 2_Chat.py
├── build_data.py       # Data building script
├── evaluate.py         # System evaluation script
└── Home.py            # Home page
```

## 📊 System Evaluation

The system has been evaluated using three key metrics:

### Evaluation Metrics

- **Correctness** (Scale: 1-5): Measures how accurate the answer is compared to the reference answer
- **Faithfulness** (Scale: 0-1): Evaluates whether the response is based on retrieved context without hallucination
- **Relevancy** (Scale: 0-1): Assesses if the response actually answers the query

### Performance Results

| Metric           | Score | Max Score |
| ---------------- | ----- | --------- |
| **Correctness**  | 4.57  | 5.0       |
| **Faithfulness** | 0.93  | 1.0       |
| **Relevancy**    | 0.71  | 1.0       |

To run evaluation:

```bash
python evaluate.py
```

Results will be saved in `eval_results/` directory

## 🔧 Customization

### Change LLM Model

Edit in `src/global_settings.py` or `src/ingest_pipeline.py`:

```python
Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0.2)
```

Available models: `gpt-4`, `gpt-4-turbo`, `gpt-4o-mini`, `gpt-3.5-turbo`

## 📝 Important Notes

- ⚠️ **Never share your OpenAI API Key**: Ensure `secrets.toml` is in `.gitignore`
- 💰 **API Costs**: OpenAI API usage is paid, monitor usage at [platform.openai.com](https://platform.openai.com)
- 🔒 **Security**: This system is for research and educational purposes only
- 🏥 **Medical Disclaimer**: Does not replace professional medical advice

## 🏗️ System Architecture

The system follows a RAG (Retrieval-Augmented Generation) architecture:

1. **Data Ingestion**: Process DSM-5 documents into nodes
2. **Indexing**: Create vector embeddings and store in ChromaDB
3. **Retrieval**: Find relevant information based on user queries
4. **Generation**: Use LLM to generate responses with retrieved context
5. **Memory**: Maintain conversation history for contextual responses
