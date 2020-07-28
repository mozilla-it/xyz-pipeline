import traceback
from abc import ABC, abstractmethod
from typing import Dict, Any, List

from pipeline.api.exceptions import PipelineTaskException, PipelineDataKeyExistsException, \
    PipelineDataKeyDoesNotExistsException


class PipelineData:
    def __init__(self):
        """
        The PipelineData Object is a share resource throughout the pipeline run.
        """
        self.__values: Dict[str, Any] = dict()
        self.__executed_tasks: List[str] = list()
        self.__alerts: List[Any] = list()

    def add_alert(self, alert: Any):
        self.__alerts.append(alert)

    def get_alerts(self) -> List[Any]:
        return self.__alerts

    def add_executed_task(self, task_name: str):
        self.__executed_tasks.append(task_name)

    def get_executed_tasks(self) -> List[str]:
        return self.__executed_tasks

    def add(self, key: str, value: Any):
        """
        Add a value to the PipelineData. This value can be used by any task in the pipeline.
        :param key: The key for the value.
        :param value: The value.
        :raise: PipelineDataKeyExistsException
        """
        if key in self.__values.keys():
            raise PipelineDataKeyExistsException(f"Key {key} already exist.")

        self.__values[key] = value

    def update(self, key: str, value: Any):
        """
        Update a value to the PipelineData. This value can be used by any task in the pipeline.
        :param key: The key for the value.
        :param value: The value.
        :raise: PipelineDataKeyDoesNotExistsException
        """
        if key not in self.__values.keys():
            raise PipelineDataKeyDoesNotExistsException(f"Expected key {key} does not exist.")

        self.__values[key] = value

    def get(self, key: str) -> Any:
        """
        Get a value from the PipelineData. Any task can get any value in the PipelineData.
        :param key: The key for the value.
        :return:
        """
        return self.__values[key]


class Rule(ABC):
    @abstractmethod
    def execute(self, pipeline_data: PipelineData) -> bool:
        pass  # pragma: no cover


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
        pass  # pragma: no cover

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
                    self.data.add_executed_task(type(task).__name__)
            except Exception as e:
                traceback.print_exc()
                raise PipelineTaskException(e)

    def __run_rules(self, task: PipelineTask) -> bool:
        and_result: bool = True
        or_result: bool = False
        if not task.or_rules() and not task.and_rules():
            # This is likely the case when a child of PipelineTask doesn't call the super.
            return True
        or_rules: List[Rule] = task.or_rules()
        if len(or_rules) == 0:
            or_result = True
        else:
            for r in or_rules:
                if r.execute(pipeline_data=self.data):
                    or_result = True
                    break

        and_rules: List[Rule] = task.and_rules()
        for r in and_rules:
            if r.execute(pipeline_data=self.data) is False:
                and_result = False
                break

        return and_result and or_result
