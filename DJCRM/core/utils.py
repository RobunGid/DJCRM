class DataMixin:
    title = None
    header = None
    extra_context = {}
    paginate_by = 10
    def __init__(self):
        if self.title:
            self.extra_context["title"] = self.title
        if self.header:
            self.extra_context["header"] = self.header
    
    def get_mixin_context(self, context, **kwargs):
        context.update(**kwargs)
        return context