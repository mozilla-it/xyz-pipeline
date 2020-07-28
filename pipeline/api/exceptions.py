class PipelineTaskException(Exception):
    def __init__(self, e):
        super(Exception, self).__init__(e)


class PipelineDataKeyExistsException(Exception):
    def __init__(self, e):
        super(Exception, self).__init__(e)


class PipelineDataKeyDoesNotExistsException(Exception):
    def __init__(self, e):
        super(Exception, self).__init__(e)
