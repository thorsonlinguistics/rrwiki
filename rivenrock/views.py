from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from rivenrock.forms import ZodiacForm

import datetime
import math
import svgwrite

OFFSET = 10000

class RootView(RedirectView):

    permanent = False
    query_string = False
    pattern_name = 'wiki:root'

class ZodiacView(FormView):
    """
    Displays a tool for viewing the Rivenrock Zodiac at a particular day and
    time.
    """

    template_name = "rivenrock/zodiac.html"
    form_class = ZodiacForm

    def form_valid(self, form):

        time = form.cleaned_data['time']
        day = form.cleaned_data['day']
        month = MONTHS[form.cleaned_data['month']]
        year = form.cleaned_data['year']

        signs = get_signs(month, day, year, time)
        drawing = draw_signs(month, day, year, time)

        return self.render_to_response(
            self.get_context_data(form=form, signs=signs,
                drawing=drawing.tostring())
        )

class Sign:
    """
    Represents one of the seven Rivenrock Zodiac signs. Each sign is associated
    with a particular celestial body, which also provides the sign with a
    period of days over which the celestial body completes one orbit around
    Rivenrock. Each sign is also associated with one of the seven elements and
    one of the Steep Axioms. 
    """

    def __init__(self, sign, element, axiom, body, period, color):

        self.sign = sign
        self.element = element
        self.axiom = axiom
        self.body = body
        self.period = period
        self.color = color
        self.description = ""

    def __str__(self):

        return self.sign

    def __repr__(self):

        return self.sign

    def get_filename(self):

        return "rivenrock/img/%s.png" % self.sign

    def get_angle_on_day(self, total_days):
        """
        Gets the angle (in degrees) of the sign on a particular day since the
        Advent of Magic. 
        """

        remainder = total_days % self.period
        return (remainder / self.period) * 360

def get_signs(month, day, year, time):
    """
    Gets the list of signs that are possessed by an individual born at the
    given date and time. 
    """

    total_days = day
    total_days += month * 30
    total_days += (year + OFFSET) * 360

    time = time
    hour = time.hour
    mins = time.minute
    decimal = mins / 60.0
    percentage = (hour + decimal) / 24.0
    total_days += percentage

    sun_position = SIGNS[-2].get_angle_on_day(total_days)
    sky_start = (percentage * 360 + (sun_position - 270)) % 360
    sky_end = (sky_start + 180) % 360

    signs = []
    for sign in SIGNS:
        position = sign.get_angle_on_day(total_days)
        if sky_end - 180 < 0 and (position >= sky_start or position < sky_end):
            signs.append(sign)
        elif sky_start <= position <= sky_end:
            signs.append(sign)
        else:
            pass

    return signs

SIGNS = [
    Sign("wolf", "earth", "merge", "járnviðr", 14, "brown"),
    Sign("bear", "water", "flow", "hlér", 32, "blue"),
    Sign("spider", "iron", "bind", "urd", 64, "slategrey"),
    Sign("cat", "knowledge", "seek", "helheim", 2, "black"),
    Sign("raven", "rust", "release", "lidskjalf", 148, "darkorange"),
    Sign("ape", "fire", "feed", "muspelheim", 360, "red"),
    Sign("serpent", "air", "move", "niflheim", 28, "white"),
]

MONTHS = {
    'january': 0,
    'jan': 0,
    'february': 1,
    'feb': 1,
    'march': 2,
    'mar': 2,
    'april': 3,
    'apr': 3,
    'may': 4,
    'june': 5,
    'jun': 5,
    'july': 6,
    'jul': 6,
    'august': 7,
    'aug': 7,
    'september': 8,
    'sep': 8, 
    'october': 9,
    'oct': 9,
    'november': 10,
    'nov': 10,
    'december': 11,
    'dec': 11,
}

def draw_signs(month, day, year, time):
    """
    Draws all of the Zodiac signs in their current positions in an SVG
    drawing.
    """

    drawing = svgwrite.Drawing(filename="zodiac.svg",
        size=("550px", "550px"))

    total_days = day
    total_days += month * 30
    total_days += (year + OFFSET) * 360

    time = time
    hour = time.hour
    mins = time.minute
    decimal = mins / 60.0
    percentage = (hour + decimal) / 24.0
    total_days += percentage

    sun_position = SIGNS[-2].get_angle_on_day(total_days)
    sky_start = (percentage * 360 + (sun_position - 270)) % 360
    sky_end = (sky_start + 180) % 360

    start_rad = sky_start * 0.0174532925
    end_rad = sky_end * 0.0174532925

    start_x = 225 * math.cos(start_rad)
    start_y = 225 * math.sin(start_rad)
    end_x = 225 * math.cos(end_rad)
    end_y = 225 * math.sin(end_rad)

    position1 = "%d,%d" % (275 + start_x, 275 + start_y)
    position2 = "%d,%d" % (275 + end_x, 275 + end_y)

    drawing.add(drawing.path(d="M275,275 L%s A100,100 1 0,1 %s z" 
        % (position1, position2), stroke='none', fill='yellow'))

    drawing.add(drawing.circle(center=(275,275), r=50,
        stroke_width=1, stroke="black", fill="purple"))
    drawing.add(drawing.text("Rivenrock", insert=(275, 280),
        style="text-anchor: middle"))

    current_radius = 50
    sorted_signs = sorted(SIGNS, key=lambda x: x.period)
    for sign in sorted_signs:

        current_radius += 20

        angle_rad = sign.get_angle_on_day(total_days) * 0.0174532925

        x = current_radius * math.cos(angle_rad)
        y = current_radius * math.sin(angle_rad)

        drawing.add(drawing.circle(center=(275, 275), r=current_radius,
            stroke_width=1, stroke="black", fill='none'))

        new_center = (275 + x, 275 + y)

        drawing.add(drawing.circle(center=new_center, r=5, stroke_width=1,
            stroke='black', fill=sign.color))
        drawing.add(drawing.text(sign.body.capitalize(), insert=(275+x+10, 275+y)))

    return drawing
