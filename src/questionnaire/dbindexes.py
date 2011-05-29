from models import Question, Questionnaire
from dbindexer.lookups import StandardLookup
from dbindexer.api import register_index

register_index(Question, {'questionnaire__product__uniqueName': StandardLookup()})
register_index(Questionnaire, {'product__uniqueName': StandardLookup()})