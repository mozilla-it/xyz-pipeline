# Created by jspiropulo at 5/8/20
Feature: Pipeline alerts

  Scenario: I implement a pipeline with string values
    Given tasks
      | name                |
      | AlertTaskObjectMock |
    When the pipeline runs
    Then tasks alert alerting