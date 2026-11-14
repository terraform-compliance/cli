Feature: Resources defining their own "references" block are parsed

  Scenario: Foreign key constraints point to a table
    Given I have snowflake_table_constraint defined
    Then it must have "snowflake_table.table" referenced
