"""
Custom JUnit XML writer extension for terraform-compliance
Fixes the UnboundLocalError when scenarios are skipped
"""

import os
import sys
from datetime import datetime
from xml.etree import ElementTree as ET
from radish.extensions import CodeGenerator
from radish.model import ScenarioLoop, ScenarioOutline
from radish.hookregistry import after
from radish import config


class FixedJUnitXMLWriter(CodeGenerator):
    """
    Fixed JUnit XML writer that properly handles skipped scenarios
    """
    
    OPTIONS = [
        (
            "--junit-xml=<PATH>",
            "write JUnit XML result file after run to <PATH>",
        )
    ]
    
    def __init__(self):
        # Disable the default radish JUnit XML writer
        self.junit_xml_path = None
        
    def get_junit_xml_path(self):
        """Get the JUnit XML output path from configuration"""
        return config().junit_xml
    
    @after.each_feature
    def generate_junit_xml(self, feature):
        """Generate JUnit XML report for the feature"""
        junit_xml_path = self.get_junit_xml_path()
        if not junit_xml_path:
            return
            
        # Create testsuite element
        testsuite = ET.Element("testsuite")
        testsuite.set("name", feature.sentence)
        testsuite.set("tests", str(len(feature.scenarios)))
        testsuite.set("time", str(feature.duration))
        
        # Count results
        failures = 0
        errors = 0
        skipped = 0
        
        for scenario in feature.scenarios:
            if isinstance(scenario, (ScenarioLoop, ScenarioOutline)):
                scenarios = scenario.scenarios
            else:
                scenarios = [scenario]
                
            for actual_scenario in scenarios:
                # Create testcase element for each scenario
                testcase = ET.SubElement(testsuite, "testcase")
                testcase.set("classname", feature.sentence)
                testcase.set("name", actual_scenario.sentence)
                testcase.set("time", str(actual_scenario.duration))
                
                # Handle different scenario states
                if actual_scenario.state == "skipped":
                    skipped += 1
                    skipped_elem = ET.SubElement(testcase, "skipped")
                    if hasattr(actual_scenario, 'skip_reason'):
                        skipped_elem.set("message", str(actual_scenario.skip_reason))
                elif actual_scenario.state == "failed":
                    failures += 1
                    failure_elem = ET.SubElement(testcase, "failure")
                    if hasattr(actual_scenario, 'failure_reason'):
                        failure_elem.set("message", str(actual_scenario.failure_reason))
                    if hasattr(actual_scenario, 'failure_traceback'):
                        failure_elem.text = str(actual_scenario.failure_traceback)
                elif actual_scenario.state == "untested":
                    errors += 1
                    error_elem = ET.SubElement(testcase, "error")
                    error_elem.set("message", "Scenario was not tested")
        
        # Update testsuite attributes
        testsuite.set("failures", str(failures))
        testsuite.set("errors", str(errors))
        testsuite.set("skipped", str(skipped))
        
        # Write XML file
        try:
            tree = ET.ElementTree(testsuite)
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(junit_xml_path) or '.', exist_ok=True)
            tree.write(junit_xml_path, encoding="utf-8", xml_declaration=True)
        except Exception as e:
            print(f"Error writing JUnit XML: {e}", file=sys.stderr)


# Register the extension
def load_radish_extensions():
    """Load the fixed JUnit XML writer extension"""
    return [FixedJUnitXMLWriter] 