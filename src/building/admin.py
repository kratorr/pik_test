from django.contrib import admin

from building.models import Building, BricksTask

class BricksTaskTaskAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)


admin.site.register(Building)
admin.site.register(BricksTask, BricksTaskTaskAdmin)