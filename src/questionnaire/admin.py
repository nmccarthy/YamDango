from questionnaire.models import Question, Product, Questionnaire
from django.contrib import admin

#admin.site.register(Question)
admin.site.register(Product)

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