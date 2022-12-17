"""
Custom model fields.
"""
from datetime import datetime

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils import simplejson as json

try:
    from south.modelsinspector import add_introspection_rules
    HAS_SOUTH = True
except ImportError:
    HAS_SOUTH = False

class ListField(models.TextField):
    """
    Store a list of values in a Model field.
    """
    __metaclass__ = models.SubfieldBase
 
    def __init__(self, *args, **kwargs):
        self.separator = kwargs.pop('separator', ',')
        super(ListField, self).__init__(*args, **kwargs)
 
    def to_python(self, value):
        if not value: return

        return value if isinstance(value, list) else value.split(self.separator)
 
    def get_db_prep_value(self, value):
        if not value: return

        if isinstance(value, (list, tuple)):
            return self.separator.join([unicode(s) for s in value])
        else:
            raise ValueError('Value for ListField must be either a list or tuple.')
 
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)

        return self.get_db_prep_value(value)

if HAS_SOUTH:
    add_introspection_rules([
        (
            [ListField],
            [],
            {
                "separator": ["separator", {"default": ","}],
            },
        ),
    ], ["^boundaries\.lib\.fields\.ListField"])

class JSONField(models.TextField):
    """
    Store arbitrary JSON in a Model field.
    """
    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        """
        Convert string value to JSON after its loaded from the database.
        """
        if value == "":
            return None

        try:
            if isinstance(value, basestring):
                return json.loads(value)
        except ValueError:
            pass

        return value

    def get_prep_value(self, value):
        """
        Convert our JSON object to a string before being saved.
        """
        if value == "":
            return None

        if isinstance(value, (dict, list)):
            value = json.dumps(value, cls=DjangoJSONEncoder)

        return super(JSONField, self).get_prep_value(value)

    def value_to_string(self, obj):
        """
        Called by the serializer.
        """
        value = self._get_val_from_obj(obj)

        return self.get_db_prep_value(value)

if HAS_SOUTH:
    add_introspection_rules([], ["^boundaries\.lib\.fields\.JSONField"])
