Feature: Something

  Scenario Outline: AWS KMS Key Policy is too permissive
    Given I have aws_kms_key defined
    When it contains policy
    Then it must contain Statement
    Then it must contain Action
    Then its value must match the "<value>" regex

    Examples:
    | value |
    | abc123  |