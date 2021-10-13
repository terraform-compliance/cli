Feature: Tag things
    @exclude_.*datadog_monitor.*
    Scenario Outline: Ensure that specific tags are defined
        Given I have resource that supports tags defined
        When it contains tags
        Then it must contain <tags>
        And its value must match the "<value>" regex
        Examples:
            | tags           | value                        |
            | Name           | .+                           |
