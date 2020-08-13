Feature: Feature for issue 348


	Scenario: Scenario for issue 348
		Given I have aws_kms_key defined
	    When it has policy
	    Then it must contain policy
	    When it has Statement
	    Then it must contain Statement
	    When its Effect is Allow
	    And it has Principal
	    Then it must contain Principal
	    Then its value must not match the "\*" regex