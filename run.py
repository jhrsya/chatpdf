#!/usr/bin/env python3
"""
Claude Code Analyzer - Simple launcher script
Provides easy access to all functionality with user-friendly interface.
"""

import os
import sys
import subprocess
import argparse

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        "anthropic",
        "streamlit", 
        "chromadb",
        "gitpython",
        "tiktoken",
        "requests"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed!")
    return True

def check_api_key():
    """Check if API key is configured"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  ANTHROPIC_API_KEY not found in environment variables")
        print("   Set it with: export ANTHROPIC_API_KEY='your-api-key'")
        return False
    
    print("🔑 API key found!")
    return True

def run_tests():
    """Run the test suite"""
    print("🧪 Running tests...")
    try:
        result = subprocess.run([sys.executable, "test_basic.py"], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def run_example():
    """Run the example usage script"""
    print("📝 Running example...")
    try:
        result = subprocess.run([sys.executable, "example_usage.py"], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running example: {e}")
        return False

def run_web_interface():
    """Start the web interface"""
    print("🌐 Starting web interface...")
    print("   This will open a browser window with the Streamlit app")
    print("   Press Ctrl+C to stop")
    
    try:
        # Try different ways to run Streamlit
        commands_to_try = [
            [sys.executable, "claude_code_analyzer.py", "--web"],
            ["streamlit", "run", "claude_code_analyzer.py"],
            [sys.executable, "-m", "streamlit", "run", "claude_code_analyzer.py"]
        ]
        
        for cmd in commands_to_try:
            try:
                subprocess.run(cmd, check=True)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        print("❌ Could not start Streamlit. Try installing with: pip install streamlit")
        return False
        
    except KeyboardInterrupt:
        print("\n👋 Web interface stopped")
        return True
    except Exception as e:
        print(f"❌ Error starting web interface: {e}")
        return False

def run_cli_analysis(args):
    """Run CLI analysis"""
    print("💻 Running CLI analysis...")
    
    cmd = [sys.executable, "claude_code_analyzer.py"]
    
    if args.repo:
        cmd.extend(["--repo", args.repo])
    elif args.directory:
        cmd.extend(["--directory", args.directory])
    else:
        print("❌ Please specify either --repo or --directory")
        return False
    
    if args.output:
        cmd.extend(["--output", args.output])
    
    if args.model:
        cmd.extend(["--model", args.model])
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ Analysis completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Analysis failed with return code {e.returncode}")
        return False
    except Exception as e:
        print(f"❌ Error running analysis: {e}")
        return False

def show_interactive_menu():
    """Show interactive menu for users"""
    print("\n" + "="*50)
    print("🤖 Claude Code Analyzer")
    print("="*50)
    
    while True:
        print("\nChoose an option:")
        print("1. 🔍 Check dependencies and setup")
        print("2. 🧪 Run tests")
        print("3. 📝 Run example")
        print("4. 🌐 Start web interface")
        print("5. 💻 Run CLI analysis")
        print("6. 📚 Show help")
        print("0. 👋 Exit")
        
        choice = input("\nEnter your choice (0-6): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            print("\n" + "-"*30)
            deps_ok = check_dependencies()
            api_ok = check_api_key() if deps_ok else False
            if deps_ok and api_ok:
                print("✅ Setup complete! You're ready to use the analyzer.")
            else:
                print("❌ Setup incomplete. Please fix the issues above.")
        elif choice == "2":
            print("\n" + "-"*30)
            run_tests()
        elif choice == "3":
            print("\n" + "-"*30)
            run_example()
        elif choice == "4":
            print("\n" + "-"*30)
            run_web_interface()
        elif choice == "5":
            print("\n" + "-"*30)
            repo = input("GitHub repository URL (or press Enter to skip): ").strip()
            directory = input("Local directory path (or press Enter to skip): ").strip()
            
            if not repo and not directory:
                print("❌ Please provide either a repository URL or directory path")
                continue
            
            output = input("Output file (optional, press Enter to print to console): ").strip()
            
            # Create a simple args object
            class Args:
                def __init__(self):
                    self.repo = repo if repo else None
                    self.directory = directory if directory else None
                    self.output = output if output else None
                    self.model = "claude-3-5-sonnet-20241022"
            
            run_cli_analysis(Args())
        elif choice == "6":
            show_help()
        else:
            print("❌ Invalid choice. Please enter a number between 0-6.")

def show_help():
    """Show help information"""
    help_text = """
🤖 Claude Code Analyzer - Help

OVERVIEW:
    A comprehensive tool for analyzing codebases using Claude AI.
    Supports multiple programming languages and provides detailed
    architecture analysis, component extraction, and AI-generated reports.

SETUP:
    1. Install Python 3.8+
    2. Install dependencies: pip install -r requirements.txt
    3. Set API key: export ANTHROPIC_API_KEY='your-key'

USAGE MODES:

    🌐 Web Interface (Recommended for beginners):
        python run.py
        Then choose option 4, or run:
        streamlit run claude_code_analyzer.py

    💻 Command Line:
        python claude_code_analyzer.py --repo https://github.com/user/repo
        python claude_code_analyzer.py --directory ./my-project

    📝 Python API:
        from claude_code_analyzer import ClaudeAnalyzer, AnalysisConfig
        # See example_usage.py for details

FEATURES:
    ✅ Multi-language support (Python, JS, TS, Java, C++, Go, Rust, etc.)
    ✅ GitHub repository analysis
    ✅ Local directory analysis
    ✅ Architecture pattern detection
    ✅ Function and class extraction
    ✅ AI-generated summary reports
    ✅ Vector database integration
    ✅ Web and CLI interfaces

EXAMPLES:
    Analyze a Python project:
        python claude_code_analyzer.py --repo https://github.com/pallets/flask

    Analyze local directory:
        python claude_code_analyzer.py --directory ./my-app --output results.json

    Start web interface:
        python run.py (then choose option 4)

SUPPORT:
    📁 Check README.md for detailed documentation
    🧪 Run tests with: python run.py (option 2)
    📝 Try examples with: python run.py (option 3)
"""
    print(help_text)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Claude Code Analyzer - Launcher Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                                    # Interactive menu
  python run.py --test                             # Run tests
  python run.py --example                          # Run example
  python run.py --web                              # Start web interface
  python run.py --repo https://github.com/user/repo  # Analyze repository
  python run.py --directory ./project              # Analyze directory
        """
    )
    
    parser.add_argument("--test", action="store_true", help="Run tests")
    parser.add_argument("--example", action="store_true", help="Run example")
    parser.add_argument("--web", action="store_true", help="Start web interface")
    parser.add_argument("--repo", help="GitHub repository URL to analyze")
    parser.add_argument("--directory", help="Local directory to analyze")
    parser.add_argument("--output", help="Output file for results")
    parser.add_argument("--model", default="claude-3-5-sonnet-20241022", help="Claude model to use")
    parser.add_argument("--check", action="store_true", help="Check dependencies and setup")
    
    args = parser.parse_args()
    
    # If no arguments provided, show interactive menu
    if len(sys.argv) == 1:
        show_interactive_menu()
        return
    
    # Handle specific commands
    if args.check:
        deps_ok = check_dependencies()
        api_ok = check_api_key() if deps_ok else False
        sys.exit(0 if (deps_ok and api_ok) else 1)
    
    if args.test:
        success = run_tests()
        sys.exit(0 if success else 1)
    
    if args.example:
        success = run_example()
        sys.exit(0 if success else 1)
    
    if args.web:
        success = run_web_interface()
        sys.exit(0 if success else 1)
    
    if args.repo or args.directory:
        success = run_cli_analysis(args)
        sys.exit(0 if success else 1)
    
    # If we get here, show help
    parser.print_help()

if __name__ == "__main__":
    main()