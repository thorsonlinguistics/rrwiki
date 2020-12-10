import pickle

from django import forms
from django.conf import settings
from django.utils.translation import gettext as _
from strata.models import Character

class CharacterFormBase(forms.ModelForm):

    #name = forms.CharField(label=_("Name"), required=False)
    #race = forms.CharField(label=_("Race"), initial=_("Dwarf"), required=False)
    #advantage = forms.IntegerField(label=_("Advantage"), initial=0,
    #        min_value=0, required=False)
    #disadvantage = forms.IntegerField(label=_("Disadvantage"), initial=0,
    #        min_value=0, required=False)
    #shock = forms.IntegerField(label=_("Shock"), initial=0, min_value=0,
    #        required=False)

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop('user')

        instance = kwargs.get('instance')
        if instance:
            initial = kwargs.get('initial', {})
            data = instance.data
            crafts = {craft.lower() + 'craft': ranks for (craft, ranks) in
                    pickle.loads(data).items()}

            initial.update(crafts)

            kwargs['initial'] = initial

        super().__init__(*args, **kwargs)

    def save(self, commit=True):

        instance = super().save(commit=False)

        data = {}

        for wellspring in settings.CRAFTS:
            self.get_craft_data(wellspring, data)

        instance.data = pickle.dumps(data)
        instance.owner = self.user

        if commit:
            instance.save()

        return instance

    def get_craft_data(self, wellspring, data):

        craft_name = wellspring[0]
        field_name = craft_name.lower() + 'craft'
        data[craft_name] = self.cleaned_data[field_name]

        for subcraft in wellspring[1]:
            self.get_craft_data(subcraft, data)

    class Meta:
        model = Character
        exclude = ['data', 'owner']

def get_new_fields():

    fields = {'Meta': CharacterFormBase.Meta}

    for wellspring in settings.CRAFTS:
        _get_new_fields(wellspring, fields)

    return fields

def _get_new_fields(crafts, fields):

    current_craft = crafts[0].lower() + _('craft')

    fields[current_craft] = forms.IntegerField(
            label=current_craft.capitalize(), initial=0,
            required=False)

    for craft in crafts[1]:

        _get_new_fields(craft, fields)

CharacterForm = type('CharacterForm', (CharacterFormBase,), get_new_fields())

# def add_crafts(crafts):
# 
#     current_craft = crafts[0].lower() + _('craft')
# 
#     setattr(CharacterForm,
#             current_craft,
#             forms.IntegerField(label=_(current_craft.capitalize()),
#             initial=0, required=False))
# 
#     for craft in crafts[1]:
# 
#         add_crafts(craft)
