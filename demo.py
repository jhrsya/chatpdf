#!/usr/bin/env python3
"""
Claude Code Analyzer - Standalone Demo
Demonstrates the core concepts without requiring external dependencies.
"""

import os
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from pathlib import Path

@dataclass
class AnalysisConfig:
    """Configuration for Claude code analysis"""
    api_key: str = "demo-key"
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

class MockCodeProcessor:
    """Mock processor for demonstration purposes"""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
        
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
            '.html': 'html',
            '.css': 'css',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown'
        }
        
        suffix = Path(file_path).suffix.lower()
        return ext_to_lang.get(suffix, 'text')
    
    def read_file_safely(self, file_path: str) -> Optional[str]:
        """Safely read file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception:
                return None
        except Exception:
            return None
    
    def extract_code_files(self, directory: str) -> List[CodeFile]:
        """Extract all relevant code files from directory"""
        code_files = []
        
        # Common code file extensions
        code_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.hpp',
            '.go', '.rs', '.rb', '.php', '.cs', '.swift', '.kt', '.scala',
            '.html', '.css', '.json', '.yaml', '.yml', '.md', '.txt'
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

class MockAnalyzer:
    """Mock analyzer for demonstration"""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.processor = MockCodeProcessor(config)
    
    def analyze_code_structure(self, code_files: List[CodeFile]) -> Dict[str, Any]:
        """Mock analysis of code structure"""
        
        # Calculate basic statistics
        total_files = len(code_files)
        total_lines = sum(f.lines for f in code_files)
        languages = list(set(f.language for f in code_files))
        
        # Calculate language distribution
        lang_stats = {}
        for file in code_files:
            lang = file.language
            if lang not in lang_stats:
                lang_stats[lang] = {'files': 0, 'lines': 0}
            lang_stats[lang]['files'] += 1
            lang_stats[lang]['lines'] += file.lines
        
        # Find important files
        important_files = []
        for file in code_files:
            if any(keyword in file.path.lower() for keyword in 
                   ['main', 'app', 'index', 'server', 'client', 'config']):
                important_files.append({
                    'path': file.path,
                    'language': file.language,
                    'lines': file.lines
                })
        
        # Mock architectural analysis
        architecture_analysis = f"""
CODEBASE ANALYSIS SUMMARY

Overall Structure:
- Total Files: {total_files}
- Total Lines of Code: {total_lines}
- Programming Languages: {', '.join(languages)}

Language Distribution:
{self._format_language_stats(lang_stats)}

Key Files Identified:
{self._format_important_files(important_files)}

Architectural Patterns:
- File organization suggests a {"modular" if len(languages) > 1 else "single-language"} architecture
- {"Multi-technology stack" if len(languages) > 2 else "Simple technology stack"} detected
- Code distribution indicates {"large-scale" if total_lines > 1000 else "small to medium-scale"} project

Recommendations:
1. Consider adding documentation if README files are missing
2. Ensure consistent code organization across modules
3. Review large files for potential refactoring opportunities
4. Implement automated testing if not present
"""
        
        return {
            "architecture_analysis": architecture_analysis,
            "total_files": total_files,
            "total_lines": total_lines,
            "languages": languages,
            "language_stats": lang_stats,
            "important_files": important_files
        }
    
    def _format_language_stats(self, lang_stats: Dict) -> str:
        """Format language statistics"""
        lines = []
        for lang, stats in sorted(lang_stats.items(), key=lambda x: x[1]['lines'], reverse=True):
            lines.append(f"  - {lang}: {stats['files']} files, {stats['lines']} lines")
        return '\n'.join(lines)
    
    def _format_important_files(self, files: List[Dict]) -> str:
        """Format important files list"""
        if not files:
            return "  - No key files identified"
        
        lines = []
        for file in files[:5]:  # Top 5 important files
            lines.append(f"  - {file['path']} ({file['language']}, {file['lines']} lines)")
        return '\n'.join(lines)
    
    def analyze_functions_and_classes(self, code_files: List[CodeFile]) -> Dict[str, Any]:
        """Mock analysis of functions and classes"""
        
        total_functions = 0
        total_classes = 0
        
        # Simple pattern matching for demo
        for file in code_files:
            if file.language == 'python':
                total_functions += file.content.count('def ')
                total_classes += file.content.count('class ')
            elif file.language in ['javascript', 'typescript']:
                total_functions += file.content.count('function ')
                total_functions += file.content.count('=> ')
                total_classes += file.content.count('class ')
            elif file.language == 'java':
                total_functions += file.content.count('public ') + file.content.count('private ')
                total_classes += file.content.count('class ')
        
        return {
            "function_count": total_functions,
            "class_count": total_classes,
            "functions": [],  # Would contain detailed function info
            "classes": []     # Would contain detailed class info
        }
    
    def generate_summary_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate a comprehensive summary report"""
        
        structure = analysis_results.get('structure', {})
        components = analysis_results.get('components', {})
        
        report = f"""
# CLAUDE CODE ANALYZER - ANALYSIS REPORT

## Executive Summary
This analysis was performed on a codebase containing {structure.get('total_files', 0)} files 
and approximately {structure.get('total_lines', 0)} lines of code across 
{len(structure.get('languages', []))} programming languages.

## Technical Overview

### Languages and Technologies
The codebase uses the following technologies:
{', '.join(structure.get('languages', []))}

### Scale and Complexity
- **Files**: {structure.get('total_files', 0)}
- **Lines of Code**: {structure.get('total_lines', 0)}
- **Functions**: {components.get('function_count', 0)} (estimated)
- **Classes**: {components.get('class_count', 0)} (estimated)

### Architecture Assessment
{structure.get('architecture_analysis', 'No detailed analysis available')}

## Key Findings

1. **Code Organization**: The project shows {"good" if structure.get('total_files', 0) > 5 else "basic"} file organization
2. **Technology Stack**: {"Diverse" if len(structure.get('languages', [])) > 2 else "Focused"} technology choices
3. **Scale**: {"Large-scale" if structure.get('total_lines', 0) > 1000 else "Small to medium-scale"} project

## Recommendations

1. **Documentation**: Ensure comprehensive README and code documentation
2. **Testing**: Implement automated testing if not already present
3. **Code Quality**: Consider static analysis tools for code quality
4. **Architecture**: Review for potential refactoring opportunities

## Next Steps

1. Detailed security analysis
2. Performance optimization review
3. Code quality metrics implementation
4. Automated CI/CD pipeline setup

---
*Report generated by Claude Code Analyzer*
"""
        return report

def demonstrate_analysis():
    """Demonstrate the code analysis functionality"""
    
    print("🤖 Claude Code Analyzer - Demo")
    print("=" * 50)
    
    # Set up configuration
    config = AnalysisConfig(
        api_key="demo-key",
        model="claude-3-5-sonnet-20241022"
    )
    
    # Initialize analyzer
    analyzer = MockAnalyzer(config)
    
    # Analyze current directory
    print("🔍 Analyzing current directory...")
    code_files = analyzer.processor.extract_code_files(".")
    print(f"📁 Found {len(code_files)} code files")
    
    # Show file breakdown
    if code_files:
        print("\n📋 File breakdown:")
        for file in code_files[:10]:  # Show first 10 files
            print(f"  - {file.path} ({file.language}, {file.lines} lines)")
        if len(code_files) > 10:
            print(f"  ... and {len(code_files) - 10} more files")
    
    # Run structure analysis
    print("\n🏗️ Analyzing code structure...")
    structure_analysis = analyzer.analyze_code_structure(code_files)
    
    # Run component analysis
    print("⚙️ Analyzing functions and classes...")
    component_analysis = analyzer.analyze_functions_and_classes(code_files)
    
    # Combine results
    results = {
        'structure': structure_analysis,
        'components': component_analysis,
        'files_analyzed': len(code_files)
    }
    
    # Generate summary
    print("📋 Generating summary report...")
    summary_report = analyzer.generate_summary_report(results)
    
    # Display results
    print("\n" + "="*50)
    print("ANALYSIS RESULTS")
    print("="*50)
    print(summary_report)
    
    # Save results to file
    with open("demo_analysis_results.json", "w") as f:
        # Convert CodeFile objects to dictionaries for JSON serialization
        serializable_results = {
            'structure': structure_analysis,
            'components': component_analysis,
            'files_analyzed': len(code_files),
            'code_files': [asdict(f) for f in code_files[:5]]  # Save first 5 files
        }
        json.dump(serializable_results, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: demo_analysis_results.json")
    print("\n✅ Demo completed successfully!")

def show_sample_code_analysis():
    """Show analysis of sample code"""
    
    print("\n" + "="*50)
    print("SAMPLE CODE ANALYSIS")
    print("="*50)
    
    # Sample Python code
    sample_code = '''
import os
import sys
from typing import List, Dict, Optional

class DataProcessor:
    """A class for processing data files"""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.data = []
        self.processed_count = 0
    
    def load_data(self, file_path: str) -> List[Dict]:
        """Load data from a file"""
        # Mock implementation
        return []
    
    def process_data(self, data: List[Dict]) -> List[Dict]:
        """Process the loaded data"""
        processed = []
        for item in data:
            # Process each item
            processed.append(self._transform_item(item))
        return processed
    
    def _transform_item(self, item: Dict) -> Dict:
        """Transform a single data item"""
        # Transform logic here
        return item
    
    def save_results(self, results: List[Dict], output_path: str):
        """Save results to file"""
        # Save implementation
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
    
    # Analyze the sample code
    lines = sample_code.split('\n')
    
    # Count different elements
    imports = [line for line in lines if line.strip().startswith('import') or line.strip().startswith('from')]
    classes = [line for line in lines if line.strip().startswith('class ')]
    functions = [line for line in lines if line.strip().startswith('def ')]
    
    print("📝 Sample Code Analysis:")
    print(f"📏 Total Lines: {len(lines)}")
    print(f"📦 Imports: {len(imports)}")
    print(f"🏛️ Classes: {len(classes)}")
    print(f"⚙️ Functions: {len(functions)}")
    
    print(f"\n📦 Imports found:")
    for imp in imports:
        print(f"  - {imp.strip()}")
    
    print(f"\n🏛️ Classes found:")
    for cls in classes:
        print(f"  - {cls.strip()}")
    
    print(f"\n⚙️ Functions found:")
    for func in functions:
        print(f"  - {func.strip()}")
    
    # Mock complexity analysis
    complexity_score = len(functions) * 0.1 + len(classes) * 0.2
    print(f"\n📊 Complexity Score: {complexity_score:.1f}")
    
    print("\n💡 Insights:")
    print("  - Well-structured class-based design")
    print("  - Good use of type hints")
    print("  - Proper separation of concerns")
    print("  - Documentation strings present")

if __name__ == "__main__":
    print("🚀 Starting Claude Code Analyzer Demo...")
    
    try:
        # Run the main demonstration
        demonstrate_analysis()
        
        # Show sample code analysis
        show_sample_code_analysis()
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print("\nThis is a mock demonstration of the Claude Code Analyzer.")
        print("The real implementation requires external dependencies and API keys.")
        
    print("\n🎉 Demo finished!")
    print("\nTo use the full version:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Set API key: export ANTHROPIC_API_KEY='your-key'")
    print("3. Run: python claude_code_analyzer.py --help")