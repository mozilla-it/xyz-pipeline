from abc import ABC, abstractmethod
from typing import Dict, Any

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


class PipelineTask(ABC):
    @abstractmethod
    def execute(self, pipeline_data: PipelineData):
        """
        This is a single execution task in a pipeline run.
        :param pipeline_data: The data that get's passed around from task to task. Only one instance per pipeline run.
        :return:
        """
        pass


class Pipeline:
    def __init__(self, tasks: [PipelineTask], pipeline_data: PipelineData = PipelineData()):
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
                task.execute(pipeline_data=self.data)
            except Exception as e:
                raise PipelineTaskException(e)
