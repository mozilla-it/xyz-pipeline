# Created by jspiropulo at 5/8/20
Feature: Pipeline archives

  Scenario: I implement a pipeline with default archive message
    Given tasks
      | name                  |
      | ArchiveTaskObjectMock |
    When the pipeline runs
    Then tasks archive archiving