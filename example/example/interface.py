from rests import interface

from .serializers import QuestionSerializer, ChoiceSerializer


class Interface(interface.Interface):

    questions = interface.Type(serializer_cls=QuestionSerializer)
    choices = interface.Type(serializer_cls=ChoiceSerializer)

