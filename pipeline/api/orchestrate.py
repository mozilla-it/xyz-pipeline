from abc import ABC, abstractmethod
from typing import Dict, Any, List

from pipeline.api.exceptions import PipelineTaskException


class PipelineData:
    def __init__(self):
        """
        The PipelineData Object is a share resource throughout the pipeline run.
        """
        self.args: Dict[str, Any] = dict()

    def add(self, key: str, value: Any):
        """
        Add a value to the PipelineData. This value can be used by any task in the pipeline.
        :param key: The key for the value.
        :param value: The value.
        :return:
        """
        self.args[key] = value

    def get(self, key: str) -> Any:
        """
        Get a value from the PipelineData. Any task can get any value in the PipelineData.
        :param key: The key for the value.
        :return:
        """
        return self.args[key]


class Rule(ABC):
    @abstractmethod
    def execute(self, data: PipelineData) -> bool:
        pass


class PipelineTask(ABC):
    def __init__(self):
        self.__and_rules: List[Rule] = list()
        self.__or_rules: List[Rule] = list()

    @abstractmethod
    def execute(self, pipeline_data: PipelineData):
        """
        This is a single execution task in a pipeline run.
        :param pipeline_data: The data that get's passed around from task to task. Only one instance per pipeline run.
        :return:
        """
        pass

    def add_and_rule(self, rule: Rule):
        self.__and_rules.append(rule)
        return self

    def add_or_rule(self, rule: Rule):
        self.__or_rules.append(rule)
        return self

    def add_and_rules(self, rules: List[Rule]):
        self.__and_rules.extend(rules)
        return self

    def add_or_rules(self, rules: List[Rule]):
        self.__or_rules.extend(rules)
        return self

    def and_rules(self) -> List[Rule]:
        """
        :return: the rules
        """
        return self.__and_rules

    def or_rules(self) -> List[Rule]:
        """
        :return: the rules
        """
        return self.__or_rules


class Pipeline:
    def __init__(self, tasks: List[PipelineTask], pipeline_data: PipelineData = PipelineData()):
        """
        Initialize the pipeline.
        :param tasks: The list of tasks to execute.
        :param pipeline_data: The PipelineData. If none is provided an empty one will be created.
        """
        self.tasks = tasks
        self.data = pipeline_data

    def execute(self):
        """
        Execution of all pipeline tasks.
        """
        for task in self.tasks:
            try:
                if self.__run_rules(task):
                    task.execute(pipeline_data=self.data)
            except Exception as e:
                raise PipelineTaskException(e)

    def __run_rules(self, task: PipelineTask) -> bool:
        and_result: bool = True
        or_result: bool = False

        or_rules = task.or_rules()
        if len(or_rules) == 0:
            or_result = True
        else:
            for r in or_rules:
                if r.execute(self.data):
                    or_result = True
                    break

        and_rules = task.and_rules()
        for r in and_rules:
            if r.execute(self.data) is False:
                and_result = False
                break

        return and_result and or_result
