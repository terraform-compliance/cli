Feature: Credentials should not be within the code  # /Users/s0045379/develop/terraform-compliance-rules/credentials.feature
    In order to prevent any credentials leakage
    As engineers
    We'll enforce credentials will not be hardcoded

    Scenario Outline: AWS Credentials should not be hardcoded
        Given I have aws provider configured
        When it contains <key>
        Then its value must not match the "<regex>" regex

    Examples:
        | key        | regex                                                   |
        | access_key | (?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])                   |
        | secret_key | (?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=]) |