import importlib
import unittest
from typing import List

from behave import *

from pipeline.api.exceptions import PipelineTaskException
from pipeline.api.orchestrate import Pipeline, PipelineData, PipelineTask, Rule


class PipelineTest(unittest.TestCase):
    data = PipelineData()

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
        self.tasks: List[PipelineTask] = list()
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
        Pipeline(tasks=self.tasks, pipeline_data=PipelineTest.data).execute()

    @then("tasks execute with bool values")
    def task_execute(self):
        for row in self.table:
            assert PipelineTest.data.get(row[0]) is True

    @then("tasks alert {msg}")
    def task_execute(self, msg):
        assert PipelineTest.data.get_alerts()[0] == msg

    @then("tasks execute with object values")
    def tasks_execute_with_object_values(self):
        for row in self.table:
            assert PipelineTest.data.get(row[0]).get() == row[0]

    @when("the pipeline runs and throws exception")
    def the_pipeline_runs_and_throws_exception(self):
        got_exception = False
        try:
            Pipeline(tasks=self.tasks, pipeline_data=PipelineTest.data).execute()
        except PipelineTaskException as e:
            got_exception = True

        assert got_exception

    @given("we reset pipeline data")
    def step_impl(self):
        selfdata = PipelineData()

    @when("we extend")
    def extend(self):
        mocks_rules = importlib.import_module("mocks_rules")

        ands: List[Rule] = list()
        ors: List[Rule] = list()
        for r in self.table:
            classes = r["rules"].split(",")

            if r["type"] == "ands":
                for c in classes:
                    class_ = getattr(mocks_rules, c)
                    ands.append(class_())

                self.tasks[0].add_and_rules(ands)
            elif r["type"] == "ors":
                for c in classes:
                    class_ = getattr(mocks_rules, c)
                    ors.append(class_())

                self.tasks[0].add_or_rules(ors)

    @then("verify proper extension")
    def step_impl(self):
        ands: List[Rule] = self.tasks[0].and_rules()
        ors: List[Rule] = self.tasks[0].or_rules()

        for r in self.table:
            classes = r["rules"].split(",")
            if r["type"] == "ands":
                assert len(classes) == len(ands)
            elif r["type"] == "ors":
                assert len(classes) == len(ors)

    @then("executed tasks report")
    def executed_tasks_report(self):
        for r in self.table:
            assert r["task_name"] in PipelineTest.data.get_executed_tasks()

    @given("clear executed tasks")
    def step_impl(context):
        PipelineTest.data = PipelineData()