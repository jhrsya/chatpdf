#!/usr/bin/env python3
"""
Claude Code Analyzer - A Python implementation inspired by various Claude analysis projects
Combines features for code analysis, agent interactions, and comprehensive Claude API usage.
"""

import os
import sys
import json
import asyncio
import argparse
import logging
from typing import List, Dict, Any, Optional, AsyncGenerator
from dataclasses import dataclass, asdict
from pathlib import Path
import subprocess
import tempfile
import zipfile
import requests
from urllib.parse import urlparse

# Third-party imports
import anthropic
import streamlit as st
import chromadb
from chromadb.config import Settings
import git
from git import Repo
import tiktoken

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AnalysisConfig:
    """Configuration for Claude code analysis"""
    api_key: str
    model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 4096
    temperature: float = 0.1
    chunk_size: int = 8000
    overlap_size: int = 200
    vector_db_path: str = "./chroma_db"
    
@dataclass
class CodeFile:
    """Represents a code file with metadata"""
    path: str
    content: str
    language: str
    size: int
    lines: int
    
@dataclass
class AnalysisResult:
    """Results from code analysis"""
    summary: str
    architecture: Dict[str, Any]
    dependencies: List[str]
    functions: List[Dict[str, Any]]
    classes: List[Dict[str, Any]]
    complexity_score: float
    suggestions: List[str]

class CodeProcessor:
    """Processes and analyzes code files"""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.encoding = tiktoken.get_encoding("cl100k_base")
        
    def detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        ext_to_lang = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript', 
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.cs': 'csharp',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.clj': 'clojure',
            '.ml': 'ocaml',
            '.hs': 'haskell',
            '.r': 'r',
            '.m': 'matlab',
            '.sh': 'bash',
            '.sql': 'sql',
            '.html': 'html',
            '.css': 'css',
            '.xml': 'xml',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.toml': 'toml',
            '.ini': 'ini',
            '.cfg': 'config'
        }
        
        suffix = Path(file_path).suffix.lower()
        return ext_to_lang.get(suffix, 'text')
    
    def read_file_safely(self, file_path: str) -> Optional[str]:
        """Safely read file content with proper encoding handling"""
        try:
            # Try UTF-8 first
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                # Fall back to latin-1
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                logger.warning(f"Could not read file {file_path}: {e}")
                return None
        except Exception as e:
            logger.warning(f"Error reading file {file_path}: {e}")
            return None
    
    def extract_code_files(self, directory: str) -> List[CodeFile]:
        """Extract all relevant code files from directory"""
        code_files = []
        
        # Common code file extensions
        code_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.hpp',
            '.go', '.rs', '.rb', '.php', '.cs', '.swift', '.kt', '.scala', '.clj',
            '.ml', '.hs', '.r', '.m', '.sh', '.sql', '.html', '.css', '.xml', 
            '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.md', '.txt'
        }
        
        # Directories to skip
        skip_dirs = {
            '.git', '__pycache__', 'node_modules', '.next', 'dist', 'build',
            '.vscode', '.idea', 'venv', 'env', '.env', 'target', 'bin', 'obj'
        }
        
        for root, dirs, files in os.walk(directory):
            # Skip unwanted directories
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            for file in files:
                file_path = os.path.join(root, file)
                if any(file.endswith(ext) for ext in code_extensions):
                    content = self.read_file_safely(file_path)
                    if content is not None:
                        relative_path = os.path.relpath(file_path, directory)
                        code_file = CodeFile(
                            path=relative_path,
                            content=content,
                            language=self.detect_language(file_path),
                            size=len(content),
                            lines=len(content.splitlines())
                        )
                        code_files.append(code_file)
        
        return code_files
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks that fit within token limits"""
        tokens = self.encoding.encode(text)
        chunks = []
        
        for i in range(0, len(tokens), self.config.chunk_size - self.config.overlap_size):
            chunk_tokens = tokens[i:i + self.config.chunk_size]
            chunk_text = self.encoding.decode(chunk_tokens)
            chunks.append(chunk_text)
            
        return chunks

class ClaudeAnalyzer:
    """Main analyzer using Claude API"""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.client = anthropic.Anthropic(api_key=config.api_key)
        self.processor = CodeProcessor(config)
        
        # Initialize vector database
        self.chroma_client = chromadb.PersistentClient(
            path=config.vector_db_path,
            settings=Settings(allow_reset=True)
        )
        
    async def analyze_code_structure(self, code_files: List[CodeFile]) -> Dict[str, Any]:
        """Analyze overall code structure and architecture"""
        
        # Prepare context for Claude
        context = self._prepare_code_context(code_files)
        
        prompt = f"""
        Analyze the following codebase and provide a comprehensive architectural overview:

        {context}

        Please provide:
        1. Overall architecture pattern and design
        2. Main components and their relationships
        3. Key technologies and frameworks used
        4. Data flow and system boundaries
        5. Potential architectural improvements
        
        Format your response as a structured analysis.
        """
        
        try:
            response = self.client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                "architecture_analysis": response.content[0].text,
                "total_files": len(code_files),
                "total_lines": sum(f.lines for f in code_files),
                "languages": list(set(f.language for f in code_files))
            }
            
        except Exception as e:
            logger.error(f"Error analyzing code structure: {e}")
            return {"error": str(e)}
    
    async def analyze_functions_and_classes(self, code_files: List[CodeFile]) -> Dict[str, Any]:
        """Analyze functions and classes in the codebase"""
        
        functions = []
        classes = []
        
        for file in code_files:
            if file.language in ['python', 'javascript', 'typescript', 'java']:
                analysis = await self._analyze_file_components(file)
                functions.extend(analysis.get('functions', []))
                classes.extend(analysis.get('classes', []))
        
        return {
            "functions": functions,
            "classes": classes,
            "function_count": len(functions),
            "class_count": len(classes)
        }
    
    async def _analyze_file_components(self, file: CodeFile) -> Dict[str, Any]:
        """Analyze individual file for functions and classes"""
        
        prompt = f"""
        Analyze this {file.language} file and extract information about functions and classes:

        File: {file.path}
        ```{file.language}
        {file.content[:2000]}  # Truncate for context
        ```

        Please provide:
        1. List of functions with their names, parameters, and purposes
        2. List of classes with their methods and attributes
        3. Dependencies and imports
        
        Format as JSON.
        """
        
        try:
            response = self.client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Try to extract JSON from response
            content = response.content[0].text
            # Simple extraction - in production, use proper JSON parsing
            return {"functions": [], "classes": [], "raw_analysis": content}
            
        except Exception as e:
            logger.error(f"Error analyzing file {file.path}: {e}")
            return {"functions": [], "classes": []}
    
    def _prepare_code_context(self, code_files: List[CodeFile]) -> str:
        """Prepare code context for Claude analysis"""
        
        # Prioritize important files
        important_files = []
        other_files = []
        
        for file in code_files:
            if any(keyword in file.path.lower() for keyword in 
                   ['main', 'app', 'index', 'server', 'client', 'config']):
                important_files.append(file)
            else:
                other_files.append(file)
        
        context = "=== PROJECT STRUCTURE ===\n"
        
        # Add file tree
        context += "Files:\n"
        for file in code_files[:20]:  # Limit to first 20 files
            context += f"- {file.path} ({file.language}, {file.lines} lines)\n"
        
        if len(code_files) > 20:
            context += f"... and {len(code_files) - 20} more files\n"
        
        context += "\n=== KEY FILES CONTENT ===\n"
        
        # Add content of important files
        for file in important_files[:5]:  # Limit to 5 important files
            context += f"\n--- {file.path} ---\n"
            # Truncate content to fit in context
            content = file.content[:1500] if len(file.content) > 1500 else file.content
            context += f"```{file.language}\n{content}\n```\n"
        
        return context
    
    async def generate_summary_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate a comprehensive summary report"""
        
        prompt = f"""
        Based on the following code analysis results, generate a comprehensive summary report:

        {json.dumps(analysis_results, indent=2)}

        Please provide:
        1. Executive Summary
        2. Technical Overview
        3. Key Findings
        4. Recommendations for improvement
        5. Potential risks and concerns
        6. Suggested next steps

        Make it suitable for both technical and non-technical stakeholders.
        """
        
        try:
            response = self.client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"Error generating summary report: {e}")
            return f"Error generating report: {e}"

class GitHubRepository:
    """Handle GitHub repository operations"""
    
    @staticmethod
    def clone_repository(repo_url: str, target_dir: str) -> bool:
        """Clone a GitHub repository"""
        try:
            if os.path.exists(target_dir):
                import shutil
                shutil.rmtree(target_dir)
            
            Repo.clone_from(repo_url, target_dir)
            logger.info(f"Successfully cloned {repo_url} to {target_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Error cloning repository: {e}")
            return False
    
    @staticmethod
    def download_repository_zip(repo_url: str, target_dir: str) -> bool:
        """Download repository as ZIP file"""
        try:
            # Convert GitHub URL to ZIP download URL
            if "github.com" in repo_url:
                if repo_url.endswith('.git'):
                    repo_url = repo_url[:-4]
                zip_url = f"{repo_url}/archive/main.zip"
            else:
                logger.error("Only GitHub repositories are supported")
                return False
            
            response = requests.get(zip_url)
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(response.content)
                    tmp_path = tmp_file.name
                
                with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
                    zip_ref.extractall(target_dir)
                
                os.unlink(tmp_path)
                logger.info(f"Successfully downloaded {repo_url} to {target_dir}")
                return True
            else:
                logger.error(f"Failed to download repository: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error downloading repository: {e}")
            return False

class StreamlitUI:
    """Streamlit web interface for the analyzer"""
    
    @staticmethod
    def run_streamlit_app():
        """Run the Streamlit web application"""
        
        st.set_page_config(
            page_title="Claude Code Analyzer",
            page_icon="🤖",
            layout="wide"
        )
        
        st.title("🤖 Claude Code Analyzer")
        st.markdown("Analyze codebases using Claude AI for insights and recommendations")
        
        # Sidebar configuration
        with st.sidebar:
            st.header("Configuration")
            
            api_key = st.text_input(
                "Anthropic API Key",
                type="password",
                value=os.getenv("ANTHROPIC_API_KEY", "")
            )
            
            model = st.selectbox(
                "Claude Model",
                ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-haiku-20240307"]
            )
            
            max_tokens = st.slider("Max Tokens", 1000, 8000, 4096)
            temperature = st.slider("Temperature", 0.0, 1.0, 0.1)
        
        # Main interface
        tab1, tab2, tab3 = st.tabs(["Repository Analysis", "File Upload", "Analysis Results"])
        
        with tab1:
            st.header("GitHub Repository Analysis")
            
            repo_url = st.text_input("GitHub Repository URL")
            
            if st.button("Analyze Repository"):
                if not api_key:
                    st.error("Please provide an Anthropic API key")
                    return
                
                if not repo_url:
                    st.error("Please provide a repository URL")
                    return
                
                with st.spinner("Cloning repository..."):
                    temp_dir = tempfile.mkdtemp()
                    
                    if GitHubRepository.clone_repository(repo_url, temp_dir):
                        st.success("Repository cloned successfully!")
                        
                        # Run analysis
                        config = AnalysisConfig(
                            api_key=api_key,
                            model=model,
                            max_tokens=max_tokens,
                            temperature=temperature
                        )
                        
                        analyzer = ClaudeAnalyzer(config)
                        
                        with st.spinner("Extracting code files..."):
                            code_files = analyzer.processor.extract_code_files(temp_dir)
                            st.info(f"Found {len(code_files)} code files")
                        
                        with st.spinner("Analyzing code structure..."):
                            structure_analysis = asyncio.run(
                                analyzer.analyze_code_structure(code_files)
                            )
                        
                        with st.spinner("Analyzing functions and classes..."):
                            component_analysis = asyncio.run(
                                analyzer.analyze_functions_and_classes(code_files)
                            )
                        
                        # Store results in session state
                        st.session_state['analysis_results'] = {
                            'structure': structure_analysis,
                            'components': component_analysis,
                            'code_files': [asdict(f) for f in code_files]
                        }
                        
                        with st.spinner("Generating summary report..."):
                            summary_report = asyncio.run(
                                analyzer.generate_summary_report(st.session_state['analysis_results'])
                            )
                            st.session_state['summary_report'] = summary_report
                        
                        st.success("Analysis complete! Check the Analysis Results tab.")
                        
                        # Clean up
                        import shutil
                        shutil.rmtree(temp_dir)
                    else:
                        st.error("Failed to clone repository")
        
        with tab2:
            st.header("Upload Code Files")
            
            uploaded_files = st.file_uploader(
                "Choose files",
                type=['py', 'js', 'ts', 'java', 'cpp', 'c', 'go', 'rs'],
                accept_multiple_files=True
            )
            
            if uploaded_files and st.button("Analyze Uploaded Files"):
                if not api_key:
                    st.error("Please provide an Anthropic API key")
                    return
                
                # Process uploaded files
                code_files = []
                for uploaded_file in uploaded_files:
                    content = str(uploaded_file.read(), "utf-8")
                    code_file = CodeFile(
                        path=uploaded_file.name,
                        content=content,
                        language=CodeProcessor(None).detect_language(uploaded_file.name),
                        size=len(content),
                        lines=len(content.splitlines())
                    )
                    code_files.append(code_file)
                
                # Run analysis similar to repository analysis
                config = AnalysisConfig(
                    api_key=api_key,
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                analyzer = ClaudeAnalyzer(config)
                
                with st.spinner("Analyzing uploaded files..."):
                    structure_analysis = asyncio.run(
                        analyzer.analyze_code_structure(code_files)
                    )
                    component_analysis = asyncio.run(
                        analyzer.analyze_functions_and_classes(code_files)
                    )
                
                st.session_state['analysis_results'] = {
                    'structure': structure_analysis,
                    'components': component_analysis,
                    'code_files': [asdict(f) for f in code_files]
                }
                
                summary_report = asyncio.run(
                    analyzer.generate_summary_report(st.session_state['analysis_results'])
                )
                st.session_state['summary_report'] = summary_report
                
                st.success("Analysis complete! Check the Analysis Results tab.")
        
        with tab3:
            st.header("Analysis Results")
            
            if 'analysis_results' in st.session_state:
                results = st.session_state['analysis_results']
                
                # Summary Report
                if 'summary_report' in st.session_state:
                    st.subheader("📋 Summary Report")
                    st.markdown(st.session_state['summary_report'])
                
                # Structure Analysis
                st.subheader("🏗️ Architecture Analysis")
                if 'structure' in results:
                    st.json(results['structure'])
                
                # Component Analysis
                st.subheader("⚙️ Components Analysis")
                if 'components' in results:
                    st.json(results['components'])
                
                # Code Files Overview
                st.subheader("📁 Code Files")
                if 'code_files' in results:
                    files_df = st.dataframe(results['code_files'])
                    
            else:
                st.info("No analysis results available. Please run an analysis first.")

async def main():
    """Main CLI entry point"""
    
    parser = argparse.ArgumentParser(description="Claude Code Analyzer")
    parser.add_argument("--mode", choices=["cli", "web"], default="cli", help="Run mode")
    parser.add_argument("--repo", help="GitHub repository URL")
    parser.add_argument("--directory", help="Local directory to analyze")
    parser.add_argument("--api-key", help="Anthropic API key")
    parser.add_argument("--model", default="claude-3-5-sonnet-20241022", help="Claude model")
    parser.add_argument("--output", help="Output file for results")
    
    args = parser.parse_args()
    
    if args.mode == "web":
        # Run Streamlit app
        StreamlitUI.run_streamlit_app()
        return
    
    # CLI mode
    api_key = args.api_key or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("API key is required. Set ANTHROPIC_API_KEY or use --api-key")
        return
    
    config = AnalysisConfig(api_key=api_key, model=args.model)
    analyzer = ClaudeAnalyzer(config)
    
    # Determine source directory
    if args.repo:
        logger.info(f"Cloning repository: {args.repo}")
        temp_dir = tempfile.mkdtemp()
        if not GitHubRepository.clone_repository(args.repo, temp_dir):
            logger.error("Failed to clone repository")
            return
        source_dir = temp_dir
    elif args.directory:
        source_dir = args.directory
    else:
        logger.error("Either --repo or --directory is required")
        return
    
    # Extract and analyze code files
    logger.info("Extracting code files...")
    code_files = analyzer.processor.extract_code_files(source_dir)
    logger.info(f"Found {len(code_files)} code files")
    
    # Run analysis
    logger.info("Analyzing code structure...")
    structure_analysis = await analyzer.analyze_code_structure(code_files)
    
    logger.info("Analyzing functions and classes...")
    component_analysis = await analyzer.analyze_functions_and_classes(code_files)
    
    # Combine results
    results = {
        'structure': structure_analysis,
        'components': component_analysis,
        'files_analyzed': len(code_files),
        'total_lines': sum(f.lines for f in code_files)
    }
    
    # Generate summary
    logger.info("Generating summary report...")
    summary_report = await analyzer.generate_summary_report(results)
    
    # Output results
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
            f.write(f"\n\n=== SUMMARY REPORT ===\n{summary_report}")
        logger.info(f"Results saved to {args.output}")
    else:
        print("\n" + "="*50)
        print("CLAUDE CODE ANALYSIS RESULTS")
        print("="*50)
        print(json.dumps(results, indent=2))
        print("\n" + "="*50)
        print("SUMMARY REPORT")
        print("="*50)
        print(summary_report)
    
    # Clean up if we cloned a repo
    if args.repo:
        import shutil
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--web":
        # Remove the --web argument and run Streamlit
        sys.argv.remove("--web")
        StreamlitUI.run_streamlit_app()
    else:
        asyncio.run(main())