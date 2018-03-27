from django import template
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.core.urlresolvers import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from ..models import SensoryModule

register = template.Library()


@register.filter
def get_display_value(choices, request_key):
    """
    Returns the display value of an item of a ChoiceArrayField.

    This is because the standard django way <field_name>_display doesn't
    work in this case.
    Needs the choices tuple and the key one wants the display_value of.

    example usage::

        {% for item in module.field_name %}
            {{ module.CHOICES|get_display_value:item }}
        {% endfor %}

    """
    for key, value in choices:
        if key == request_key:
            return value
    return ""


@register.filter
def verbose_name(obj):
    """
    Returns the verbose name of the model this object is an instance of.
    """
    return obj._meta.verbose_name


# need to be there for senses to be translatable
pgettext_lazy("sensitivity description", "sound")
pgettext_lazy("sensitivity description", "light")
pgettext_lazy("sensitivity description", "smell")
pgettext_lazy("sensitivity description", "temperature")


@register.filter
def sensitivity_desc(value, sense):
    """
    Returns a verbose and localised sensitivity description

    Needs a value that is part of :class:`pages.models.SensoryModule` RANGE
    and a string sense: (sound, light, smell or temperature)

    example usage::

        {{ module.light|sensitivity_desc:"light" }}

    """
    if value == SensoryModule.SENS_V_LOW:
        return _("I am much less sensitive to %(sense)s than most people.") \
                % {'sense': sense}
    if value == SensoryModule.SENS_LOW:
        return _("I am less sensitive to %(sense)s than most people.") \
                % {'sense': sense}
    if value == SensoryModule.SENS_MED:
        return _("My sensitivity to %(sense)s is average.") \
                % {'sense': sense}
    if value == SensoryModule.SENS_HIGH:
        return _("I am more sensitive to %(sense)s than most people.") \
                % {'sense': sense}
    if value == SensoryModule.SENS_V_HIGH:
        return _("I am much more sensitive to %(sense)s than most people.") \
                % {'sense': sense}
    return ""


@register.filter
def sensitivity_img(value, sense):
    """
    Returns the svg image belonging to the sensitivity value and sense.

    Needs a value that is part of :class:`pages.models.SensoryModule` RANGE
    and a string sense: (sound, light, smell or temperature)

    example usage::

        {{ module.light|sensitivity_img:"light" }}

    """
    if value == SensoryModule.SENS_V_LOW:
        return "img/very_low_sensitive_{}.svg".format(sense)
    if value == SensoryModule.SENS_LOW:
        return "img/low_sensitive_{}.svg".format(sense)
    if value == SensoryModule.SENS_MED:
        return "img/average_sensitive_{}.svg".format(sense)
    if value == SensoryModule.SENS_HIGH:
        return "img/high_sensitive_{}.svg".format(sense)
    if value == SensoryModule.SENS_V_HIGH:
        return "img/very_high_sensitive_{}.svg".format(sense)
    return ""


@register.filter
def get_position_field(form, position):
    """
    Given a form and a position n(1-based), return the forms n'th visible field
    """
    return_val = form.visible_fields()[position - 1]
    return return_val


@register.filter
def tokenurl(request, page):
    """
    Returns the absolute tokenurl of a :class:`pages.models:Page`.

    needs the request to be able to generate an absolute url.

    Example usage::

        {{ request|tokenurl:page }}

    """
    if not page.token:
        return ""
    uid = urlsafe_base64_encode(force_bytes(page.pk))
    return request.build_absolute_uri(reverse("pages:viewpage",
                                              args=[uid,
                                                    page.token]))
