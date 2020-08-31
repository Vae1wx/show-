from django.apps import AppConfig


class CommentsConfig(AppConfig):
    name = 'comments'

    def ready(self):
    	super(CommentsConfig, self).ready()
    	from . import signals
