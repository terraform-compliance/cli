"""
Unit tests for the fixed JUnit XML writer
"""

import pytest
import tempfile
import os
from unittest.mock import Mock, patch
from xml.etree import ElementTree as ET

from terraform_compliance.extensions.junit_xml_fix import FixedJUnitXMLWriter


class TestFixedJUnitXMLWriter:
    
    def test_junit_xml_generation_with_skipped_scenario(self):
        """Test that JUnit XML is generated correctly when scenarios are skipped"""
        with tempfile.TemporaryDirectory() as tmpdir:
            junit_path = os.path.join(tmpdir, "junit.xml")
            
            # Create mock objects
            mock_scenario = Mock()
            mock_scenario.sentence = "Test scenario"
            mock_scenario.duration = 0.5
            mock_scenario.state = "skipped"
            mock_scenario.skip_reason = "Resource type not found"
            
            mock_feature = Mock()
            mock_feature.sentence = "Test feature"
            mock_feature.duration = 1.0
            mock_feature.scenarios = [mock_scenario]
            
            # Create writer and generate XML
            writer = FixedJUnitXMLWriter()
            
            with patch('terraform_compliance.extensions.junit_xml_fix.world') as mock_world:
                mock_world.config = Mock()
                mock_world.config.junit_xml = junit_path
                
                writer.generate_junit_xml(mock_feature)
                
            # Verify XML was created
            assert os.path.exists(junit_path)
            
            # Parse and verify XML content
            tree = ET.parse(junit_path)
            root = tree.getroot()
            
            assert root.tag == "testsuite"
            assert root.get("name") == "Test feature"
            assert root.get("tests") == "1"
            assert root.get("skipped") == "1"
            
            # Check testcase
            testcases = root.findall("testcase")
            assert len(testcases) == 1
            
            testcase = testcases[0]
            assert testcase.get("name") == "Test scenario"
            assert testcase.get("time") == "0.5"
            
            # Check skipped element
            skipped = testcase.find("skipped")
            assert skipped is not None
            assert skipped.get("message") == "Resource type not found"
    
    def test_junit_xml_generation_with_passed_scenario(self):
        """Test that JUnit XML is generated correctly for passed scenarios"""
        with tempfile.TemporaryDirectory() as tmpdir:
            junit_path = os.path.join(tmpdir, "junit.xml")
            
            # Create mock objects
            mock_scenario = Mock()
            mock_scenario.sentence = "Test scenario"
            mock_scenario.duration = 0.5
            mock_scenario.state = "passed"
            
            mock_feature = Mock()
            mock_feature.sentence = "Test feature"
            mock_feature.duration = 1.0
            mock_feature.scenarios = [mock_scenario]
            
            # Create writer and generate XML
            writer = FixedJUnitXMLWriter()
            
            with patch('terraform_compliance.extensions.junit_xml_fix.world') as mock_world:
                mock_world.config = Mock()
                mock_world.config.junit_xml = junit_path
                
                writer.generate_junit_xml(mock_feature)
                
            # Verify XML was created
            assert os.path.exists(junit_path)
            
            # Parse and verify XML content
            tree = ET.parse(junit_path)
            root = tree.getroot()
            
            assert root.tag == "testsuite"
            assert root.get("name") == "Test feature"
            assert root.get("tests") == "1"
            assert root.get("failures") == "0"
            assert root.get("errors") == "0"
            assert root.get("skipped") == "0" 