import unittest
from behave import *

from pipeline.api.exceptions import PipelineTaskException
from pipeline.api.pipeline import Pipeline
# WE NEED THIS LINE. WE ARE LOADING MOCKS BY NAME.
from pipeline.tests.bdd.mocks import *
import importlib

data = PipelineData()


class PipelineTest(unittest.TestCase):

    @given("tasks")
    def tasks(self):
        self.tasks = list()
        module = importlib.import_module("mocks")

        for row in self.table:
            class_ = getattr(module, row[0])
            self.tasks.append(class_())

    @when("the pipeline runs")
    def runs(self):
        Pipeline(tasks=self.tasks, pipeline_data=data).execute()

    @then("tasks execute")
    def execute(self):
        for row in self.table:
            assert data.get(row[0]) is True

    @then("tasks execute with object values")
    def step_impl(self):
        for row in self.table:
            assert data.get(row[0]).get() == row[0]

    @when("the pipeline runs and throws exception")
    def exception(self):
        got_exception = False
        try:
            Pipeline(tasks=self.tasks, pipeline_data=data).execute()
        except PipelineTaskException as e:
            got_exception = True

        assert got_exception
