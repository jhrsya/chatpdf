#!/usr/bin/env python3
"""
Basic tests for Claude Code Analyzer
Tests core functionality that doesn't require API calls.
"""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from claude_code_analyzer import (
    AnalysisConfig, 
    CodeFile, 
    CodeProcessor, 
    ClaudeAnalyzer,
    GitHubRepository
)

class TestAnalysisConfig(unittest.TestCase):
    """Test the AnalysisConfig dataclass"""
    
    def test_config_creation(self):
        """Test basic config creation"""
        config = AnalysisConfig(api_key="test-key")
        
        self.assertEqual(config.api_key, "test-key")
        self.assertEqual(config.model, "claude-3-5-sonnet-20241022")
        self.assertEqual(config.max_tokens, 4096)
        self.assertEqual(config.temperature, 0.1)
        self.assertEqual(config.chunk_size, 8000)
        self.assertEqual(config.overlap_size, 200)
        self.assertEqual(config.vector_db_path, "./chroma_db")
    
    def test_custom_config(self):
        """Test config with custom values"""
        config = AnalysisConfig(
            api_key="test-key",
            model="claude-3-opus-20240229",
            max_tokens=2048,
            temperature=0.5
        )
        
        self.assertEqual(config.model, "claude-3-opus-20240229")
        self.assertEqual(config.max_tokens, 2048)
        self.assertEqual(config.temperature, 0.5)

class TestCodeFile(unittest.TestCase):
    """Test the CodeFile dataclass"""
    
    def test_code_file_creation(self):
        """Test basic CodeFile creation"""
        code_file = CodeFile(
            path="test.py",
            content="print('hello')",
            language="python",
            size=14,
            lines=1
        )
        
        self.assertEqual(code_file.path, "test.py")
        self.assertEqual(code_file.content, "print('hello')")
        self.assertEqual(code_file.language, "python")
        self.assertEqual(code_file.size, 14)
        self.assertEqual(code_file.lines, 1)

class TestCodeProcessor(unittest.TestCase):
    """Test the CodeProcessor class"""
    
    def setUp(self):
        """Set up test environment"""
        self.config = AnalysisConfig(api_key="test-key")
        self.processor = CodeProcessor(self.config)
    
    def test_language_detection(self):
        """Test programming language detection"""
        test_cases = [
            ("test.py", "python"),
            ("app.js", "javascript"),
            ("component.tsx", "typescript"),
            ("Main.java", "java"),
            ("program.cpp", "cpp"),
            ("script.sh", "bash"),
            ("data.json", "json"),
            ("config.yaml", "yaml"),
            ("unknown.xyz", "text")
        ]
        
        for file_path, expected_lang in test_cases:
            with self.subTest(file_path=file_path):
                detected_lang = self.processor.detect_language(file_path)
                self.assertEqual(detected_lang, expected_lang)
    
    def test_read_file_safely(self):
        """Test safe file reading"""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write("Test content\nLine 2")
            temp_path = f.name
        
        try:
            content = self.processor.read_file_safely(temp_path)
            self.assertEqual(content, "Test content\nLine 2")
        finally:
            os.unlink(temp_path)
    
    def test_read_nonexistent_file(self):
        """Test reading non-existent file"""
        content = self.processor.read_file_safely("nonexistent_file.txt")
        self.assertIsNone(content)
    
    def test_extract_code_files(self):
        """Test code file extraction from directory"""
        # Create a temporary directory with test files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            test_files = [
                ("test.py", "print('hello')", "python"),
                ("app.js", "console.log('hello')", "javascript"),
                ("README.md", "# Test", "text"),
                ("config.json", '{"test": true}', "json")
            ]
            
            for filename, content, _ in test_files:
                file_path = os.path.join(temp_dir, filename)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Extract code files
            code_files = self.processor.extract_code_files(temp_dir)
            
            # Verify results
            self.assertEqual(len(code_files), 4)
            
            # Check if all files are detected correctly
            file_names = [f.path for f in code_files]
            self.assertIn("test.py", file_names)
            self.assertIn("app.js", file_names)
            self.assertIn("README.md", file_names)
            self.assertIn("config.json", file_names)
    
    def test_chunk_text(self):
        """Test text chunking functionality"""
        # Create a long text that needs chunking
        long_text = "This is a test. " * 1000  # Repeat to make it long
        
        chunks = self.processor.chunk_text(long_text)
        
        # Should create multiple chunks
        self.assertGreater(len(chunks), 1)
        
        # Each chunk should be non-empty
        for chunk in chunks:
            self.assertTrue(len(chunk.strip()) > 0)

class TestGitHubRepository(unittest.TestCase):
    """Test GitHub repository operations"""
    
    @patch('claude_code_analyzer.Repo')
    def test_clone_repository_success(self, mock_repo):
        """Test successful repository cloning"""
        mock_repo.clone_from.return_value = MagicMock()
        
        result = GitHubRepository.clone_repository(
            "https://github.com/test/repo", 
            "/tmp/test_repo"
        )
        
        self.assertTrue(result)
        mock_repo.clone_from.assert_called_once_with(
            "https://github.com/test/repo", 
            "/tmp/test_repo"
        )
    
    @patch('claude_code_analyzer.Repo')
    def test_clone_repository_failure(self, mock_repo):
        """Test repository cloning failure"""
        mock_repo.clone_from.side_effect = Exception("Clone failed")
        
        result = GitHubRepository.clone_repository(
            "https://github.com/test/repo", 
            "/tmp/test_repo"
        )
        
        self.assertFalse(result)
    
    @patch('claude_code_analyzer.requests')
    @patch('claude_code_analyzer.zipfile')
    @patch('claude_code_analyzer.tempfile')
    def test_download_repository_zip(self, mock_tempfile, mock_zipfile, mock_requests):
        """Test ZIP repository download"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"fake zip content"
        mock_requests.get.return_value = mock_response
        
        # Mock temporary file
        mock_temp_file = MagicMock()
        mock_temp_file.name = "/tmp/test.zip"
        mock_tempfile.NamedTemporaryFile.return_value.__enter__.return_value = mock_temp_file
        
        # Mock zipfile
        mock_zip = MagicMock()
        mock_zipfile.ZipFile.return_value.__enter__.return_value = mock_zip
        
        result = GitHubRepository.download_repository_zip(
            "https://github.com/test/repo",
            "/tmp/extract"
        )
        
        self.assertTrue(result)
        mock_requests.get.assert_called_once_with("https://github.com/test/repo/archive/main.zip")
        mock_zip.extractall.assert_called_once_with("/tmp/extract")

class TestClaudeAnalyzer(unittest.TestCase):
    """Test ClaudeAnalyzer class (without API calls)"""
    
    def setUp(self):
        """Set up test environment"""
        self.config = AnalysisConfig(api_key="test-key")
    
    @patch('claude_code_analyzer.anthropic.Anthropic')
    @patch('claude_code_analyzer.chromadb.PersistentClient')
    def test_analyzer_initialization(self, mock_chroma, mock_anthropic):
        """Test analyzer initialization"""
        analyzer = ClaudeAnalyzer(self.config)
        
        self.assertEqual(analyzer.config, self.config)
        mock_anthropic.assert_called_once_with(api_key="test-key")
        mock_chroma.assert_called_once()
    
    @patch('claude_code_analyzer.anthropic.Anthropic')
    @patch('claude_code_analyzer.chromadb.PersistentClient')
    def test_prepare_code_context(self, mock_chroma, mock_anthropic):
        """Test code context preparation"""
        analyzer = ClaudeAnalyzer(self.config)
        
        # Create test code files
        code_files = [
            CodeFile("main.py", "print('main')", "python", 13, 1),
            CodeFile("utils.py", "def helper(): pass", "python", 18, 1),
            CodeFile("test.js", "console.log('test')", "javascript", 19, 1)
        ]
        
        context = analyzer._prepare_code_context(code_files)
        
        # Check if context contains expected sections
        self.assertIn("=== PROJECT STRUCTURE ===", context)
        self.assertIn("=== KEY FILES CONTENT ===", context)
        self.assertIn("main.py", context)
        self.assertIn("utils.py", context)
        self.assertIn("test.js", context)

def run_basic_tests():
    """Run all basic tests"""
    print("🧪 Running basic tests for Claude Code Analyzer...")
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestAnalysisConfig,
        TestCodeFile,
        TestCodeProcessor,
        TestGitHubRepository,
        TestClaudeAnalyzer
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
    else:
        print(f"\n❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        
        for failure in result.failures:
            print(f"FAIL: {failure[0]}")
            print(failure[1])
        
        for error in result.errors:
            print(f"ERROR: {error[0]}")
            print(error[1])
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_basic_tests()
    exit(0 if success else 1)