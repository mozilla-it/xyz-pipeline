# Created by jspiropulo at 5/8/20
Feature: Pipeline API

  Background:
    Given clear executed tasks

  Scenario: overwrite pipeline data value
    Given tasks
      | name                 | key  | value |
      | AddTaskMock          | key1 | Hello |
      | AddOverwriteTaskMock | key1 | Bye   |
    When the pipeline runs
    Then executed tasks report
      | task_name            |
      | AddTaskMock          |
      | AddOverwriteTaskMock |

  Scenario: add or overwrite pipeline data value
    Given tasks
      | name                 | key  | value |
      | AddOverwriteTaskMock | key1 | Bye   |
    When the pipeline runs
    Then executed tasks report
      | task_name            |
      | AddOverwriteTaskMock |

  Scenario: update pipeline data value
    Given tasks
      | name           | key  | value |
      | AddTaskMock    | key1 | Hello |
      | UpdateTaskMock | key1 | Bye   |
    When the pipeline runs
    Then executed tasks report
      | task_name      |
      | AddTaskMock    |
      | UpdateTaskMock |

  Scenario: I implement a pipeline with string values
    Given tasks
      | name          |
      | OneTaskMock   |
      | TwoTaskMock   |
      | ThreeTaskMock |
    When the pipeline runs
    Then tasks execute with bool values
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
    Then tasks execute with bool values
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
    Then tasks execute with bool values
      | name  |
      | one   |
      | two   |
      | three |
    Then executed tasks report
      | task_name           |
      | OneTaskMock         |
      | TwoTaskMock         |
      | ThreeTaskMock       |
      | OneTaskObjectMock   |
      | TwoTaskObjectMock   |
      | ThreeTaskObjectMock |

