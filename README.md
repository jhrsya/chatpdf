# 🤖 Claude Code Analyzer

A comprehensive Python implementation for analyzing codebases using Claude AI, inspired by various Claude analysis projects. This tool combines features for code search, agent interactions, and comprehensive code analysis using Anthropic's Claude API.

## ✨ Features

- **🔍 Multi-language Code Analysis**: Support for Python, JavaScript, TypeScript, Java, C++, Go, Rust, and more
- **🏗️ Architecture Analysis**: Comprehensive codebase structure and design pattern analysis
- **⚙️ Component Analysis**: Function and class extraction with detailed metadata
- **📊 Vector Database Integration**: ChromaDB for semantic code search and similarity analysis
- **🌐 Web Interface**: Beautiful Streamlit web UI for interactive analysis
- **💻 CLI Interface**: Command-line tool for batch processing and automation
- **📥 GitHub Integration**: Direct repository cloning and analysis
- **📋 Comprehensive Reporting**: AI-generated summary reports for stakeholders
- **🔧 Configurable**: Flexible configuration for different Claude models and parameters

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Anthropic API key
- Git (for repository cloning)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd claude-code-analyzer
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up your API key:**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Basic Usage

#### Command Line Interface

**Analyze a local directory:**
```bash
python claude_code_analyzer.py --directory ./my-project --output results.json
```

**Analyze a GitHub repository:**
```bash
python claude_code_analyzer.py --repo https://github.com/user/repo --output analysis.json
```

**Web Interface:**
```bash
python claude_code_analyzer.py --mode web
# or
streamlit run claude_code_analyzer.py
```

#### Python API

```python
import asyncio
from claude_code_analyzer import ClaudeAnalyzer, AnalysisConfig

# Configure the analyzer
config = AnalysisConfig(
    api_key="your-api-key",
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096
)

# Initialize analyzer
analyzer = ClaudeAnalyzer(config)

# Extract code files
code_files = analyzer.processor.extract_code_files("./my-project")

# Run analysis
async def run_analysis():
    structure = await analyzer.analyze_code_structure(code_files)
    components = await analyzer.analyze_functions_and_classes(code_files)
    
    results = {
        'structure': structure,
        'components': components,
        'files_analyzed': len(code_files)
    }
    
    summary = await analyzer.generate_summary_report(results)
    print(summary)

asyncio.run(run_analysis())
```

## 📖 Detailed Usage

### Configuration Options

The `AnalysisConfig` class provides comprehensive configuration:

```python
config = AnalysisConfig(
    api_key="your-api-key",                    # Anthropic API key
    model="claude-3-5-sonnet-20241022",        # Claude model to use
    max_tokens=4096,                           # Maximum tokens per request
    temperature=0.1,                           # Response creativity (0.0-1.0)
    chunk_size=8000,                           # Token chunk size for large files
    overlap_size=200,                          # Overlap between chunks
    vector_db_path="./chroma_db"               # ChromaDB storage path
)
```

### Supported Models

- `claude-3-5-sonnet-20241022` (recommended)
- `claude-3-opus-20240229`
- `claude-3-haiku-20240307`

### Command Line Options

```bash
python claude_code_analyzer.py [OPTIONS]

Options:
  --mode [cli|web]              Run mode (default: cli)
  --repo TEXT                   GitHub repository URL
  --directory TEXT              Local directory to analyze
  --api-key TEXT                Anthropic API key
  --model TEXT                  Claude model (default: claude-3-5-sonnet-20241022)
  --output TEXT                 Output file for results
  --help                        Show help message
```

### Web Interface Features

The Streamlit web interface provides:

- **Repository Analysis Tab**: Enter GitHub URLs for automatic cloning and analysis
- **File Upload Tab**: Upload individual code files for analysis
- **Analysis Results Tab**: View comprehensive analysis results with interactive visualizations
- **Configuration Sidebar**: Adjust API settings, model selection, and parameters

## 🔧 Architecture

### Core Components

1. **CodeProcessor**: Handles file extraction, language detection, and text chunking
2. **ClaudeAnalyzer**: Main analysis engine with Claude API integration
3. **GitHubRepository**: Repository cloning and management utilities
4. **StreamlitUI**: Web interface implementation

### Data Models

- **AnalysisConfig**: Configuration settings
- **CodeFile**: Individual file representation with metadata
- **AnalysisResult**: Structured analysis results

### Analysis Pipeline

```
Input (Repository/Files) 
    ↓
File Extraction & Processing
    ↓
Language Detection & Chunking
    ↓
Claude API Analysis
    ↓
Results Aggregation
    ↓
Report Generation
    ↓
Output (JSON/Web Interface)
```

## 📊 Analysis Types

### 1. Structure Analysis
- Overall architecture patterns
- Component relationships
- Technology stack identification
- Design pattern recognition
- System boundaries

### 2. Component Analysis
- Function extraction and documentation
- Class hierarchy analysis
- Dependency mapping
- Import/export analysis
- API surface analysis

### 3. Quality Analysis
- Code complexity assessment
- Best practice compliance
- Security vulnerability identification
- Performance bottleneck detection
- Maintainability scoring

## 🌟 Advanced Features

### Vector Database Integration

The analyzer uses ChromaDB for semantic code search:

```python
# Access the vector database
chroma_client = analyzer.chroma_client

# Create collection for code embeddings
collection = chroma_client.create_collection("code_analysis")

# Query similar code patterns
results = collection.query(
    query_texts=["function that handles authentication"],
    n_results=5
)
```

### Custom Analysis Prompts

Extend the analyzer with custom prompts:

```python
class CustomAnalyzer(ClaudeAnalyzer):
    async def analyze_security_patterns(self, code_files):
        prompt = """
        Analyze the following code for security vulnerabilities:
        - SQL injection risks
        - XSS vulnerabilities
        - Authentication bypasses
        - Data exposure risks
        """
        # Implementation here
```

### Batch Processing

Process multiple repositories:

```python
repositories = [
    "https://github.com/user/repo1",
    "https://github.com/user/repo2",
    "https://github.com/user/repo3"
]

for repo_url in repositories:
    # Clone and analyze each repository
    temp_dir = tempfile.mkdtemp()
    GitHubRepository.clone_repository(repo_url, temp_dir)
    
    code_files = analyzer.processor.extract_code_files(temp_dir)
    results = await analyzer.analyze_code_structure(code_files)
    
    # Save results
    with open(f"analysis_{repo_url.split('/')[-1]}.json", 'w') as f:
        json.dump(results, f, indent=2)
```

## 🔒 Security & Privacy

- **API Key Security**: Store API keys in environment variables
- **Local Processing**: Code analysis happens locally before sending to Claude
- **Data Minimization**: Only relevant code snippets are sent to the API
- **Temporary Files**: Cloned repositories are automatically cleaned up
- **No Data Persistence**: Code content is not stored permanently

## 🛠️ Development

### Running Tests

```bash
python -m pytest tests/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Project Structure

```
claude-code-analyzer/
├── claude_code_analyzer.py    # Main analyzer implementation
├── example_usage.py           # Example scripts
├── requirements.txt           # Dependencies
├── README.md                  # Documentation
├── tests/                     # Test suite
│   ├── test_analyzer.py
│   ├── test_processor.py
│   └── test_github.py
└── docs/                      # Additional documentation
    ├── api_reference.md
    └── examples/
```

## 📚 Examples

### Analyze a Python Project

```python
# Example: Analyze a Flask application
import asyncio
from claude_code_analyzer import ClaudeAnalyzer, AnalysisConfig

async def analyze_flask_app():
    config = AnalysisConfig(api_key=os.getenv("ANTHROPIC_API_KEY"))
    analyzer = ClaudeAnalyzer(config)
    
    # Clone Flask repository
    GitHubRepository.clone_repository(
        "https://github.com/pallets/flask", 
        "./flask_repo"
    )
    
    # Extract and analyze
    code_files = analyzer.processor.extract_code_files("./flask_repo")
    analysis = await analyzer.analyze_code_structure(code_files)
    
    print(f"Architecture: {analysis['architecture_analysis']}")
    print(f"Languages: {analysis['languages']}")
    print(f"Total files: {analysis['total_files']}")

asyncio.run(analyze_flask_app())
```

### Custom Analysis Function

```python
async def analyze_api_endpoints(analyzer, code_files):
    """Custom analysis to find API endpoints"""
    
    api_prompt = """
    Analyze the following code and identify all API endpoints:
    - HTTP methods (GET, POST, PUT, DELETE)
    - Route patterns
    - Authentication requirements
    - Input/output schemas
    """
    
    api_files = [f for f in code_files if 'api' in f.path.lower()]
    
    for file in api_files[:5]:  # Limit for demo
        context = f"File: {file.path}\n```{file.language}\n{file.content[:2000]}\n```"
        
        response = await analyzer.client.messages.create(
            model=analyzer.config.model,
            max_tokens=analyzer.config.max_tokens,
            messages=[{"role": "user", "content": api_prompt + "\n\n" + context}]
        )
        
        print(f"API endpoints in {file.path}:")
        print(response.content[0].text)
        print("-" * 50)
```

## 🤝 Inspiration

This project is inspired by several excellent Claude-related projects:

- **Claude Coder**: Agent-based coding assistant functionality
- **Mental Health Image Analysis**: Multi-modal analysis concepts
- **Claude Code Reverse Engineering**: Understanding Claude's internal workings
- **Research Projects**: Academic approaches to AI-assisted code analysis

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Anthropic for the Claude API
- The open-source community for inspiration and tools
- Contributors to the various Claude analysis projects that inspired this work

## 📞 Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Discussions**: Join the community discussion
- **Documentation**: Check the docs/ directory for detailed guides

---

**Happy coding with Claude! 🤖✨**
