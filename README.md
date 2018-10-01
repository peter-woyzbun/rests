# res(ts)

`rests` generates TypeScript "models", and associated query sets, along
 with the required views and urls, from `django` models.

The basic idea is to define a `rests` "interface", using
`djangorestframework` serializers:

```python

class Interface(interface.Interface):
    questions = interface.Type(QuestionSerializer)
    choices = interface.Type(ChoiceSerializer)

```

then, in `urls.py`:

```python

from .interface import Interface

urlpatterns = Interface.urlpatterns()

```

