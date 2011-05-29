from questionnaire.models import Question, Product, Questionnaire, PendingUser, Response, ResponseSet
from django.contrib import admin

admin.site.register(Product)
admin.site.register(PendingUser)
admin.site.register(Response)
admin.site.register(ResponseSet)

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class QuestionnaireAdmin(admin.ModelAdmin):
    fieldsets = [
                 (None,         {'fields': ['name']}),
                 ('Product',    {'fields': ['product']}),
                 ]
    inlines = [QuestionInline]
    list_display = ('name', 'product')

admin.site.register(Questionnaire, QuestionnaireAdmin)