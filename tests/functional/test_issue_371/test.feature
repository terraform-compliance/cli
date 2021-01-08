Feature: test

# @nofail
  Scenario: Ensure we  are always working on eu-west-1 (for e.g.)
    Given I have aws provider configured
    When it has region
    Then it must contain region
    Then its value must match the "us-(central|north|west)-\d" regex

  Scenario Outline: AWS Credentials should not be hardcoded
    Given I have aws provider configured
    When it has <key>
    Then its value must not match the "<regex>" regex

    Examples:
      | key        | regex                                                   |
      | access_key | (?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])                   |
      | secret_key | (?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=]) |
