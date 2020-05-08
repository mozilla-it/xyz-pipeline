class PipelineTaskException(Exception):
    def __init__(self, e):
        super(Exception, self).__init__(e)
