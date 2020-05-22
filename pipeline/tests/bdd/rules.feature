# Created by jspiropulo at 5/22/20
Feature: Rules

  Background:
    Given we reset pipeline data

  Scenario: All AND rules pass all task execute
    Given tasks
      | name               | rules                                 |
      | OneAndOrTaskMock   | AndPassRule, AndPassRule              |
      | TwoAndOrTaskMock   | AndPassRule                           |
      | ThreeAndOrTaskMock | AndPassRule, AndPassRule, AndPassRule |
    When the pipeline runs
    Then tasks execute
      | name  |
      | one   |
      | two   |
      | three |

  Scenario: Some AND rules pass one task executes
    Given tasks
      | name               | rules                                     |
      | OneAndOrTaskMock   | AndPassRule, AndDONTPassRule              |
      | TwoAndOrTaskMock   | AndPassRule                               |
      | ThreeAndOrTaskMock | AndPassRule, AndPassRule, AndDONTPassRule |
    When the pipeline runs
    Then tasks execute
      | name |
      | two  |


  Scenario: All OR rules pass
    Given tasks
      | name               | rules                              |
      | OneAndOrTaskMock   | OrPassRule, OrPassRule             |
      | TwoAndOrTaskMock   | OrPassRule                         |
      | ThreeAndOrTaskMock | OrPassRule, OrPassRule, OrPassRule |
    When the pipeline runs
    Then tasks execute
      | name  |
      | one   |
      | two   |
      | three |


  Scenario: Some OR rules pass but all tasks exeute
    Given tasks
      | name               | rules                                      |
      | OneAndOrTaskMock   | OrPassRule, OrDONTPassRule                 |
      | TwoAndOrTaskMock   | OrDONTPassRule, OrPassRule                 |
      | ThreeAndOrTaskMock | OrDONTPassRule, OrDONTPassRule, OrPassRule |
    When the pipeline runs
    Then tasks execute
      | name  |
      | one   |
      | two   |
      | three |

  Scenario: Some OR rules pass and some tasks execute
    Given tasks
      | name               | rules                                      |
      | OneAndOrTaskMock   | OrPassRule, OrDONTPassRule                 |
      | TwoAndOrTaskMock   | OrDONTPassRule, OrDONTPassRule             |
      | ThreeAndOrTaskMock | OrDONTPassRule, OrDONTPassRule, OrPassRule |
    When the pipeline runs
    Then tasks execute
      | name  |
      | one   |
      | three |


  Scenario: All OR's pass and ALL AND's pass, all tasks execute
    Given tasks
      | name               | rules                                             |
      | OneAndOrTaskMock   | AndPassRule, OrPassRule,AndPassRule               |
      | TwoAndOrTaskMock   | AndPassRule, OrPassRule, OrPassRule, OrPassRule   |
      | ThreeAndOrTaskMock | AndPassRule, OrPassRule, AndPassRule, AndPassRule |
    When the pipeline runs
    Then tasks execute
      | name  |
      | one   |
      | two   |
      | three |

  Scenario: Some OR's pass and ALL AND's pass, all tasks execute
    Given tasks
      | name               | rules                                   |
      | OneAndOrTaskMock   | OrPassRule, OrDONTPassRule, AndPassRule |
      | TwoAndOrTaskMock   | OrPassRule, OrDONTPassRule, AndPassRule |
      | ThreeAndOrTaskMock | OrPassRule, OrDONTPassRule, AndPassRule |
    When the pipeline runs
    Then tasks execute
      | name  |
      | one   |
      | two   |
      | three |

  Scenario: ALL OR's fail and ALL AND's pass, some tasks execute
    Given tasks
      | name               | rules                                         |
      | OneAndOrTaskMock   | OrDONTPassRule, OrDONTPassRule, AndPassRule                  |
      | TwoAndOrTaskMock   | OrPassRule, OrDONTPassRule, AndPassRule                  |
      | ThreeAndOrTaskMock   | OrPassRule, OrDONTPassRule, AndPassRule                  |
    When the pipeline runs
    Then tasks execute
      | name  |
      | two   |
      | three   |

  Scenario: ALL OR pass and some AND's fail, one tasks execute
    Given tasks
      | name               | rules                                         |
      | OneAndOrTaskMock   | OrPassRule,  AndDONTPassRule                  |
      | TwoAndOrTaskMock   | OrPassRule, AndPassRule                  |
      | ThreeAndOrTaskMock   | OrPassRule, AndDONTPassRule                  |
    When the pipeline runs
    Then tasks execute
      | name  |
      | two   |
