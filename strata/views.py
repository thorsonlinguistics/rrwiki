from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.views import generic
from strata.forms import CharacterForm
from strata.models import Character

class CharacterMixin:

    template_name = 'strata/sheet.html'
    form_class = CharacterForm
    model = Character

    def get_context_data(self, *args, **kwargs):

        data = super().get_context_data(*args, **kwargs)

        modified_crafts = extend_crafts(data['form'])
        per_column = int(len(modified_crafts) / 2)

        data['crafts1'] = modified_crafts[:per_column]
        data['crafts2'] = modified_crafts[per_column:]

        return data

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})

        return kwargs

class CharacterCreateView(CharacterMixin, LoginRequiredMixin, generic.edit.CreateView):
    """
    Displays a character sheet for the Legends and Layers roleplaying game.
    """

    pass

class CharacterEditView(CharacterMixin, LoginRequiredMixin, generic.edit.UpdateView):
    """
    Displays a character sheet for the Legends and Layers roleplaying game.
    """

    pass

class CharacterListView(LoginRequiredMixin, generic.list.ListView):

    template_name = 'strata/list_chars.html'
    model = Character

    def get_queryset(self):

        return Character.objects.filter(owner=self.request.user)

def extend_crafts(form):

    return [_extend_crafts(form, craft, 0, 1) for craft in settings.CRAFTS]

def _extend_crafts(form, crafts, bonus, tier):

    current_craft = crafts[0].lower() + _('craft')
    craft_form_field = form[current_craft]
    if craft_form_field.value():
        new_bonus = int(craft_form_field.value()) * tier + bonus
    else:
        new_bonus = bonus
    children = [_extend_crafts(form, child, new_bonus, tier + 1) for child in crafts[1]]

    return (current_craft.capitalize(), craft_form_field, children, new_bonus)
