"""
Helper functions for using Kliko in combinaton with Django
"""
from django.forms import CharField, FloatField, FileField, BooleanField, IntegerField, ChoiceField
from django.contrib.postgres.fields import ArrayField
from form_utils.forms import BetterForm
from kliko.validate import list_regex


field_map = {
    'char': CharField,
    'float': FloatField,
    'file': FileField,
    'bool': BooleanField,
    'int': IntegerField,
    'choice': ChoiceField,
    'str': CharField,
}


def generate_form(parsed):
    """
    Generate a django form from a parsed kliko object

    args:
        params: A parsed kliko file.
    returns:
        form_utils.forms.BetterForm
    """
    all_fields = {}
    fieldsets = []
    for section in parsed['sections']:
        fields_in_section = []

        for field in section['fields']:
            kwargs = {}
            for kwarg in ('initial', 'max_length', 'label', 'help_text', 'file', 'required'):
                if kwarg in field:
                    kwargs[kwarg] = field[kwarg]
            if 'choices' in field:
                kwargs['choices'] = field['choices'].items()
            fields_in_section.append(field['name'])

            match = list_regex.match(field['type'])
            if match:
                type_ = match.group(1)
                djangofield = field_map[match.group(1)]
                all_fields[field['name']] = ArrayField(djangofield, **kwargs)
            else:
                djangofield = field_map[field['type']]
                all_fields[field['name']] = djangofield(**kwargs)

        fieldsets.append((section['name'],
                          {'fields': fields_in_section,
                           'description': section['description']}
                          ))

    Meta = type('Meta', (), {'fieldsets': fieldsets})
    all_fields['Meta'] = Meta

    return type('Form', (BetterForm,), all_fields)
