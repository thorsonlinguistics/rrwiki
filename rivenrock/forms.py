from django import forms
from django.utils.translation import gettext as _

class ZodiacForm(forms.Form):

    time = forms.TimeField(label=_("Time"))

    day = forms.IntegerField(label=_("Day"), min_value=1, max_value=30,
            initial=1)

    month = forms.ChoiceField(label=_("Month"), 
        choices=(
            ('jan', _("January")),
            ('feb', _("February")),
            ('mar', _("March")),
            ('apr', _("April")),
            ('may', _("May")),
            ('jun', _("June")),
            ('jul', _("July")),
            ('aug', _("August")),
            ('sep', _("September")),
            ('oct', _("October")),
            ('nov', _("November")),
            ('dec', _("December")),
        )
    )

    year = forms.IntegerField(label=_("Year"), initial=1181)
