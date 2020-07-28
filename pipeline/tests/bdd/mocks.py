from pipeline.api.orchestrate import PipelineTask, PipelineData


class OneAndOrTaskMock(PipelineTask):
    def execute(self, pipeline_data: PipelineData):
        pipeline_data.add("one", True)


class AddTaskMock(PipelineTask):
    def __init__(self, key, value):
        super().__init__()
        self.key = key
        self.value = value

    def execute(self, pipeline_data: PipelineData):
        pipeline_data.add(self.key, self.value)


class UpdateTaskMock(PipelineTask):
    def __init__(self, key, value):
        super().__init__()
        self.key = key
        self.value = value

    def execute(self, pipeline_data: PipelineData):
        pipeline_data.update(self.key, self.value)


class TwoAndOrTaskMock(PipelineTask):
    def execute(self, pipeline_data: PipelineData):
        pipeline_data.add("two", True)


class ThreeAndOrTaskMock(PipelineTask):
    def execute(self, pipeline_data: PipelineData):
        pipeline_data.add("three", True)


class ExceptionTaskMock(PipelineTask):
    def execute(self, pipeline_data: PipelineData):
        raise Exception("Test me")


class OneTaskMock(PipelineTask):
    def execute(self, pipeline_data: PipelineData):
        pipeline_data.add("one", True)


class TwoTaskMock(PipelineTask):
    def execute(self, pipeline_data: PipelineData):
        pipeline_data.add("two", True)


class ThreeTaskMock(PipelineTask):
    def execute(self, pipeline_data: PipelineData):
        pipeline_data.add("three", True)


class OneTaskObjectMock(PipelineTask):
    def execute(self, pipeline_data: PipelineData):
        pipeline_data.add("one-object", OneObjectValueMock())


class TwoTaskObjectMock(PipelineTask):
    def execute(self, pipeline_data: PipelineData):
        pipeline_data.add("two-object", TwoObjectValueMock())


class ThreeTaskObjectMock(PipelineTask):
    def execute(self, pipeline_data: PipelineData):
        pipeline_data.add("three-object", ThreeObjectValueMock())


class AlertTaskObjectMock(PipelineTask):
    def execute(self, pipeline_data: PipelineData):
        pipeline_data.add_alert("alerting")


class OneObjectValueMock:
    @staticmethod
    def get():
        return "one-object"


class TwoObjectValueMock:
    @staticmethod
    def get():
        return "two-object"


class ThreeObjectValueMock:
    @staticmethod
    def get():
        return "three-object"
