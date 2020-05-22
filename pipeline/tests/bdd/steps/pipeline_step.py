import importlib
import unittest

from behave import *

from pipeline.api.exceptions import PipelineTaskException
from pipeline.api.orchestrate import Pipeline, PipelineData, PipelineTask

# WE NEED THIS LINE. WE ARE LOADING MOCKS BY NAME.

data = PipelineData()


class PipelineTest(unittest.TestCase):

    @staticmethod
    def sort_out_rules(task: PipelineTask, rules: str):
        _rules = rules.split(",")
        module_mocks_rules = importlib.import_module("mocks_rules")
        for rule in _rules:
            r = rule.strip()
            attr = getattr(module_mocks_rules, r)
            if r.startswith("And"):
                task.add_and_rule(attr())
            elif r.startswith("Or"):
                task.add_or_rule(attr())
            else:
                raise Exception("Your Rules MUST start with either 'And' or 'Or' just for the tests!")

    @given("tasks")
    def tasks(self):
        self.tasks = list()
        module_mocks = importlib.import_module("mocks")

        for row in self.table:
            class_ = getattr(module_mocks, row["name"])
            c = class_()

            try:
                c.__and_rules = list()
                c.__or_rules = list()
                PipelineTest.sort_out_rules(c, row["rules"])
            except Exception as e:
                pass

            self.tasks.append(c)

    @when("the pipeline runs")
    def the_pipeline_runs(self):
        Pipeline(tasks=self.tasks, pipeline_data=data).execute()

    @then("tasks execute")
    def task_execute(self):
        for row in self.table:
            assert data.get(row[0]) is True

    @then("tasks execute with object values")
    def tasks_execute_with_object_values(self):
        for row in self.table:
            assert data.get(row[0]).get() == row[0]

    @when("the pipeline runs and throws exception")
    def the_pipeline_runs_and_throws_exception(self):
        got_exception = False
        try:
            Pipeline(tasks=self.tasks, pipeline_data=data).execute()
        except PipelineTaskException as e:
            got_exception = True

        assert got_exception

    @given("we reset pipeline data")
    def step_impl(self):
        global data
        data = PipelineData()