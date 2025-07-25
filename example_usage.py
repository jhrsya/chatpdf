#!/usr/bin/env python3
"""
Example usage of Claude Code Analyzer
This script demonstrates how to use the analyzer to analyze code repositories.
"""

import os
import asyncio
from claude_code_analyzer import ClaudeAnalyzer, AnalysisConfig, GitHubRepository

async def analyze_local_directory():
    """Example: Analyze a local directory"""
    
    # Set up configuration
    config = AnalysisConfig(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        temperature=0.1
    )
    
    # Initialize analyzer
    analyzer = ClaudeAnalyzer(config)
    
    # Analyze current directory
    print("🔍 Analyzing current directory...")
    code_files = analyzer.processor.extract_code_files(".")
    print(f"📁 Found {len(code_files)} code files")
    
    # Run analysis
    print("🏗️ Analyzing code structure...")
    structure_analysis = await analyzer.analyze_code_structure(code_files)
    
    print("⚙️ Analyzing functions and classes...")
    component_analysis = await analyzer.analyze_functions_and_classes(code_files)
    
    # Generate summary
    results = {
        'structure': structure_analysis,
        'components': component_analysis,
        'files_analyzed': len(code_files)
    }
    
    print("📋 Generating summary report...")
    summary_report = await analyzer.generate_summary_report(results)
    
    # Display results
    print("\n" + "="*50)
    print("ANALYSIS RESULTS")
    print("="*50)
    print(summary_report)

async def analyze_github_repository():
    """Example: Analyze a GitHub repository"""
    
    repo_url = "https://github.com/python/cpython"  # Example repository
    
    # Set up configuration
    config = AnalysisConfig(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-3-5-sonnet-20241022"
    )
    
    # Clone repository to temporary directory
    import tempfile
    temp_dir = tempfile.mkdtemp()
    
    print(f"📥 Cloning repository: {repo_url}")
    if GitHubRepository.clone_repository(repo_url, temp_dir):
        print("✅ Repository cloned successfully!")
        
        # Initialize analyzer
        analyzer = ClaudeAnalyzer(config)
        
        # Extract code files
        print("📁 Extracting code files...")
        code_files = analyzer.processor.extract_code_files(temp_dir)
        print(f"Found {len(code_files)} code files")
        
        # Limit analysis to first 50 files for demo
        code_files = code_files[:50]
        
        # Run analysis
        print("🔍 Running analysis...")
        structure_analysis = await analyzer.analyze_code_structure(code_files)
        
        # Display results
        print("\n" + "="*50)
        print("GITHUB REPOSITORY ANALYSIS")
        print("="*50)
        print(f"Repository: {repo_url}")
        print(f"Files analyzed: {len(code_files)}")
        print(f"Languages found: {structure_analysis.get('languages', [])}")
        print("\nArchitecture Analysis:")
        print(structure_analysis.get('architecture_analysis', 'No analysis available'))
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    else:
        print("❌ Failed to clone repository")

def simple_code_analysis_example():
    """Example: Simple synchronous code analysis for a single file"""
    
    # Example Python code to analyze
    sample_code = '''
import os
import sys
from typing import List, Dict

class DataProcessor:
    """A class for processing data"""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.data = []
    
    def load_data(self, file_path: str) -> List[Dict]:
        """Load data from file"""
        # Implementation here
        return []
    
    def process_data(self, data: List[Dict]) -> List[Dict]:
        """Process the loaded data"""
        processed = []
        for item in data:
            # Process each item
            processed.append(item)
        return processed
    
    def save_results(self, results: List[Dict], output_path: str):
        """Save results to file"""
        # Implementation here
        pass

def main():
    """Main function"""
    processor = DataProcessor("config.json")
    data = processor.load_data("input.csv")
    results = processor.process_data(data)
    processor.save_results(results, "output.json")

if __name__ == "__main__":
    main()
'''
    
    print("📝 Analyzing sample Python code...")
    print("\nCode to analyze:")
    print("-" * 40)
    print(sample_code)
    print("-" * 40)
    
    # Basic analysis without AI (simple pattern detection)
    lines = sample_code.split('\n')
    
    # Count different elements
    imports = [line for line in lines if line.strip().startswith('import') or line.strip().startswith('from')]
    classes = [line for line in lines if line.strip().startswith('class ')]
    functions = [line for line in lines if line.strip().startswith('def ')]
    
    print(f"\n📊 Basic Analysis Results:")
    print(f"📦 Imports: {len(imports)}")
    print(f"🏛️ Classes: {len(classes)}")
    print(f"⚙️ Functions: {len(functions)}")
    print(f"📏 Total Lines: {len(lines)}")
    
    print(f"\n📦 Imports found:")
    for imp in imports:
        print(f"  - {imp.strip()}")
    
    print(f"\n🏛️ Classes found:")
    for cls in classes:
        print(f"  - {cls.strip()}")
    
    print(f"\n⚙️ Functions found:")
    for func in functions:
        print(f"  - {func.strip()}")

if __name__ == "__main__":
    print("🤖 Claude Code Analyzer - Example Usage")
    print("=" * 50)
    
    # Check if API key is available
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️ ANTHROPIC_API_KEY not found in environment variables")
        print("Running simple analysis example instead...\n")
        simple_code_analysis_example()
    else:
        print("🔑 API key found, running full analysis...")
        
        # Run the async analysis
        try:
            asyncio.run(analyze_local_directory())
        except Exception as e:
            print(f"❌ Error during analysis: {e}")
            print("Running simple analysis example instead...\n")
            simple_code_analysis_example()