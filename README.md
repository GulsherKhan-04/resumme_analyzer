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
