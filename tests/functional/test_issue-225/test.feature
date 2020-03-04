Feature: test

  Scenario: Appmesh module can use existing appmesh (should fail)
    Given I have aws_appmesh_virtual_node defined
    When its address is module.appmesh_existing.aws_appmesh_virtual_node.vn
    And its index is ui
    Then its mesh_name must be demo
