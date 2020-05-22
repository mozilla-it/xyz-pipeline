from pipeline.api.orchestrate import Rule, PipelineData


class AndPassRule(Rule):
    def execute(self, data: PipelineData) -> bool:
        return True


class AndDONTPassRule(Rule):
    def execute(self, data: PipelineData) -> bool:
        return False


class OrPassRule(Rule):
    def execute(self, data: PipelineData) -> bool:
        return True


class OrDONTPassRule(Rule):
    def execute(self, data: PipelineData) -> bool:
        return False
