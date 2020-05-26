# Created by jspiropulo at 5/8/20
Feature: Pipeline API

  Scenario: I implement a pipeline with string values
    Given tasks
      | name          |
      | OneTaskMock   |
      | TwoTaskMock   |
      | ThreeTaskMock |
    When the pipeline runs
    Then tasks execute
      | name  |
      | one   |
      | two   |
      | three |

  Scenario: A task throws an exception pipeline stops
    Given tasks
      | name              |
      | OneTaskMock       |
      | ExceptionTaskMock |
      | TwoTaskMock       |
    When the pipeline runs and throws exception
    Then tasks execute
      | name |
      | one  |

  Scenario: I implement a pipeline with Object values
    Given tasks
      | name                |
      | OneTaskObjectMock   |
      | TwoTaskObjectMock   |
      | ThreeTaskObjectMock |
    When the pipeline runs
    Then tasks execute with object values
      | name         |
      | one-object   |
      | two-object   |
      | three-object |

  Scenario: I implement a pipeline with strings and Object values
    Given tasks
      | name                |
      | OneTaskMock         |
      | TwoTaskMock         |
      | ThreeTaskMock       |
      | OneTaskObjectMock   |
      | TwoTaskObjectMock   |
      | ThreeTaskObjectMock |
    When the pipeline runs
    Then tasks execute with object values
      | name         |
      | one-object   |
      | two-object   |
      | three-object |
    Then tasks execute
      | name  |
      | one   |
      | two   |
      | three |


