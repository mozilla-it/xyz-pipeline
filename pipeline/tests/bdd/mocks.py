from pipeline.api.orchestrate import PipelineTask, PipelineData, PipelineAndOrRuleTask


class OneAndOrTaskMock(PipelineAndOrRuleTask):
    def execute(self, pipeline_data: PipelineData):
        pipeline_data.add("one", True)


class TwoAndOrTaskMock(PipelineAndOrRuleTask):
    def execute(self, pipeline_data: PipelineData):
        pipeline_data.add("two", True)


class ThreeAndOrTaskMock(PipelineAndOrRuleTask):
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
