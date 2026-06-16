# Resume Analyzer

An NLP-powered Streamlit application that analyzes resumes against job descriptions, extracting candidate details, identifying skills, calculating ATS match scores, and providing personalized improvement suggestions.

## Features

- **PDF Resume Parsing**: Extract text from PDF resumes automatically
- **Candidate Information Extraction**: 
  - Name extraction using spaCy NER
  - Email detection with regex
  - Phone number identification
  - Skill extraction from predefined database
- **ATS Match Score**: Keyword-based matching between resume skills and job description requirements
- **Semantic Similarity**: BERT-powered semantic comparison for contextual relevance
- **Missing Skills Analysis**: Identifies skills required by the job but absent from the resume
- **Smart Recommendations**: AI-generated suggestions to improve resume alignment with the job description

## Installation

### Requirements
- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/GulsherKhan-04/resumme-analyzer.git
cd resumme-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download spaCy language model:
```bash
python -m spacy download en_core_web_sm
```

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser to `http://localhost:8501`

3. Upload a resume PDF and paste the job description

4. View results including:
   - Candidate details (name, email, phone)
   - Extracted skills
   - ATS Match Score
   - Missing skills
   - Improvement suggestions

## How It Works

### Components

- **PDF Extraction**: Uses `pdfplumber` to extract text from PDF files
- **Text Cleaning**: Normalizes text (lowercase, removes special characters)
- **NER (Named Entity Recognition)**: spaCy extracts person names
- **Skill Matching**: Compares resume against predefined skill database
- **ATS Scoring**: Calculates percentage of required JD skills found in resume
- **Semantic Analysis**: BERT embeddings measure overall document similarity
- **Recommendations**: Generated based on missing skills and best practices

### Scoring Breakdown

- **ATS Match Score**: `(Matched Skills / Required JD Skills) × 100`
- **Semantic Similarity**: Cosine similarity between resume and JD embeddings (0-100)

## Project Structure

```
resumme-analyzer/
├── app.py                 # Main Streamlit application
├── skills_db.py          # Predefined skills database
├── requirements.txt      # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Dependencies

- **streamlit**: Web application framework
- **pdfplumber**: PDF text extraction
- **spacy**: NLP and named entity recognition
- **sentence-transformers**: BERT embeddings for semantic similarity
- **scikit-learn**: Cosine similarity calculations

## Example Usage

**Input Resume Skills**: Python, Docker, Git, GitHub, MySQL

**Job Description**: Python Developer, Docker, GitHub, Git

**Output**:
- ATS Match Score: 100%
- Missing Skills: []
- Recommendations: Suggestions to add GitHub links, quantify achievements, etc.

## Future Improvements

- Support for multiple file formats (DOCX, TXT)
- Resume template recommendations
- Integration with job boards API
- Batch resume analysis
- Interactive skill visualization
- Resume scoring history tracking
- Custom skill database management

## Troubleshooting

**Issue**: White screen on first load
- **Solution**: Models are loading in background. Wait 30-60 seconds, then refresh.

**Issue**: "No module named 'torchvision'"
- **Solution**: Optional dependency warning. Can be ignored or install: `pip install torchvision`

**Issue**: spaCy model not found
- **Solution**: Run `python -m spacy download en_core_web_sm`

## License

MIT License

## Author

**Gulsher Khan**
- GitHub: [@GulsherKhan-04](https://github.com/GulsherKhan-04)

## Support

For issues or suggestions, open an issue on the GitHub repository.
