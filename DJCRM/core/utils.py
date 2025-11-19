class DataMixin:
    title = None
    extra_context = {}
    paginate_by = 10
    def __init__(self):
        if self.title:
            self.extra_context["title"] = self.title
    
    def get_mixin_context(self, context, **kwargs):
        context.update(**kwargs)
        return context