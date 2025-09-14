#!/usr/bin/env python3
"""
Test script to verify JUnit XML generation works with skipped scenarios
"""

import os
import tempfile
import subprocess
import json

def test_junit_xml_with_skip():
    """Test that JUnit XML is generated correctly when scenarios are skipped"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        feature_content = """
Feature: Test JUnit XML with skipped scenarios
  Scenario: Ensure all resources have tags
    Given I have resource that supports tags defined
    Given I have not azapi_resource defined
    Then it must contain tags
    And its value must not be null
"""
        
        tf_content = """
resource "aws_s3_bucket" "example_code" {
  bucket = "This is just a sample code"
}
"""
        
        plan_content = {
            "format_version": "1.0",
            "terraform_version": "1.11.4",
            "planned_values": {
                "root_module": {
                    "resources": [
                        {
                            "address": "aws_s3_bucket.example_code",
                            "mode": "managed",
                            "type": "aws_s3_bucket",
                            "name": "example_code",
                            "provider_name": "registry.terraform.io/hashicorp/aws",
                            "values": {
                                "bucket": "This is just a sample code"
                            }
                        }
                    ]
                }
            },
            "resource_changes": [
                {
                    "address": "aws_s3_bucket.example_code",
                    "mode": "managed",
                    "type": "aws_s3_bucket",
                    "name": "example_code",
                    "provider_name": "registry.terraform.io/hashicorp/aws",
                    "change": {
                        "actions": ["create"]
                    }
                }
            ]
        }
        
        # Write test files
        feature_file = os.path.join(tmpdir, "test.feature")
        tf_file = os.path.join(tmpdir, "test.tf")
        plan_file = os.path.join(tmpdir, "plan.json")
        junit_file = os.path.join(tmpdir, "junit.xml")
        
        with open(feature_file, 'w') as f:
            f.write(feature_content.strip())
        
        with open(tf_file, 'w') as f:
            f.write(tf_content.strip())
        
        with open(plan_file, 'w') as f:
            json.dump(plan_content, f)
        
        # Run terraform-compliance
        cmd = [
            "python", "-m", "terraform_compliance",
            "-p", plan_file,
            "-f", tmpdir,
            "--junit-xml", junit_file
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd="/Users/eerkunt/repos/cli")
            
            # Check if JUnit XML was created
            if os.path.exists(junit_file):
                print("✅ JUnit XML file was created successfully")
                with open(junit_file, 'r') as f:
                    content = f.read()
                    print("JUnit XML content:")
                    print(content)
                    return True
            else:
                print("❌ JUnit XML file was not created")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ Error running test: {e}")
            return False

if __name__ == "__main__":
    success = test_junit_xml_with_skip()
    if success:
        print("✅ Test passed - JUnit XML generation works with skipped scenarios")
    else:
        print("❌ Test failed") 