from django.contrib import admin
from hackday.models import Event, Script, Thread, Post, Log

admin.site.register(Event)
admin.site.register(Script)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(Log)
