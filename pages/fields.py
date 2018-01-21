import copy
from itertools import chain

from django.forms import TextInput, Field, Widget, CheckboxSelectMultiple, \
                         TypedMultipleChoiceField, RadioSelect
from django.contrib.postgres.utils import prefix_validation_error
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text


class ItemTextWidget(TextInput):
    template_name = 'widgets/itemtext.html'

    class Media:
        js = ('js/add_listitem.js',)


class DynamicSplitArrayWidget(Widget):
    template_name = 'widgets/split_array_list.html'

    def __init__(self, widget, max_size, **kwargs):
        self.widget = widget() if isinstance(widget, type) else widget
        self.max_size = max_size
        super().__init__(**kwargs)

    @property
    def is_hidden(self):
        return self.widget.is_hidden

    def value_from_datadict(self, data, files, name):
        values = []
        for index in range(self.max_size):
            value = self.widget.value_from_datadict(data, files,
                                                    '%s_%s' % (name, index))
            if value:
                values.append(value)
        return values or None

    def value_omitted_from_data(self, data, files, name):
        return all(
            self.widget.value_omitted_from_data(data, files,
                                                '%s_%s' % (name, index))
            for index in range(self.max_size)
        )

    def id_for_label(self, id_):
        # See the comment for RadioSelect.id_for_label()
        if id_:
            id_ += '_0'
        return id_

    def _get_widget_context(self, name, value, id_, final_attrs, index,
                            is_last=False):
        widget_value = value
        if id_:
            final_attrs = dict(final_attrs, id='%s_%s' % (id_, index))
        final_attrs['aria-label'] = _("Item number %(n)d") % {"n": index + 1}
        widget_context = self.widget.get_context(name + '_%s' % index,
                                                 widget_value,
                                                 final_attrs)['widget']
        widget_context['is_last'] = is_last
        return widget_context

    def get_context(self, name, value, attrs=None):
        attrs = {} if attrs is None else attrs
        context = super().get_context(name, value, attrs)
        if self.is_localized:
            self.widget.is_localized = self.is_localized
        value = value or []
        context['widget']['subwidgets'] = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id')
        length = min(len(value), self.max_size)
        for i in range(length):
            context['widget']['subwidgets'].append(
                self._get_widget_context(name, value[i], id_, final_attrs, i)
            )
        # add an empty item als the last item
        context['widget']['subwidgets'].append(
            self._get_widget_context(name, None, id_, final_attrs, length,
                                     is_last=True))
        return context

    @property
    def media(self):
        return self.widget.media

    def __deepcopy__(self, memo):
        obj = super().__deepcopy__(memo)
        obj.widget = copy.deepcopy(self.widget)
        return obj

    @property
    def needs_multipart_form(self):
        return self.widget.needs_multipart_form


class DynamicSplitArrayField(Field):
    default_error_messages = {
        'item_invalid': _('Item %(nth)s in the array did not validate: '),
    }

    def __init__(self, base_field, max_size, remove_nulls=True, **kwargs):
        self.base_field = base_field
        self.max_size = max_size
        self.remove_nulls = remove_nulls
        widget = DynamicSplitArrayWidget(widget=base_field.widget,
                                         max_size=max_size)
        # if no widget seperately set in kwargs add default widget
        kwargs.setdefault('widget', widget)
        super().__init__(**kwargs)

    def clean(self, value):
        cleaned_data = []
        errors = []
        if not value:
            value = []
        if not any(value) and self.required:
            raise ValidationError(self.error_messages['required'])
        max_size = min(self.max_size, len(value))
        for index in range(max_size):
            item = value[index]
            try:
                cleaned_item = self.base_field.clean(item)
            except ValidationError as error:
                errors.append(prefix_validation_error(
                    error,
                    self.error_messages['item_invalid'],
                    code='item_invalid',
                    params={'nth': index + 1},
                ))
                cleaned_data.append(None)
            else:
                if not self.remove_nulls or \
                        cleaned_item not in self.base_field.empty_values:
                    cleaned_data.append(cleaned_item)
                errors.append(None)
        errors = list(filter(None, errors))
        if errors:
            raise ValidationError(list(chain.from_iterable(errors)))
        return cleaned_data


class ArraySelectMultiple(CheckboxSelectMultiple):
    template_name = 'widgets/bs_checkbox_select.html'
    option_template_name = 'widgets/bs_checkbox_option.html'

    def value_omitted_from_data(self, data, files, name):
        return False

    def create_option(self, name, value, label, selected, index,
                      subindex=None, attrs=None):
        if not attrs:
            attrs = {}
        classes = attrs.get('class', None)
        if classes:
            if "form-check-input" not in classes:
                attrs["class"] = classes + " form-check-input"
        else:
            attrs["class"] = "form-check-input"
        return super().create_option(name, value, label, selected, index,
                                     subindex=subindex, attrs=attrs)


class ChoiceArrayField(ArrayField):

    def formfield(self, **kwargs):
        defaults = {
            'form_class': TypedMultipleChoiceField,
            'choices': self.base_field.choices,
            'widget': ArraySelectMultiple
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely
        # as we don't care for it.
        # pylint:disable=bad-super-call
        return super(ArrayField, self).formfield(**defaults)


class RadioWithHelpSelect(RadioSelect):
    template_name = 'widgets/bs_checkbox_select.html'
    option_template_name = 'widgets/radio_option_with_help.html'

    def __init__(self, help_texts=None, attrs=None, choices=()):
        self.help_texts = help_texts if help_texts else {}
        super().__init__(attrs, choices)

    def optgroups(self, name, value, attrs=None):
        """Return a list of optgroups for this widget."""
        groups = []
        has_selected = False

        for index, (option_value, option_label) in \
                enumerate(chain(self.choices)):
            if option_value is None:
                option_value = ''

            subgroup = []
            if isinstance(option_label, (list, tuple)):
                group_name = option_value
                subindex = 0
                choices = option_label
            else:
                group_name = None
                subindex = None
                choices = [(option_value, option_label)]
            groups.append((group_name, subgroup, index))

            for subvalue, sublabel in choices:
                sub_help = self.help_texts.get(subvalue, None)
                selected = (
                    force_text(subvalue) in value and
                    (has_selected is False or self.allow_multiple_selected)
                )
                if selected is True and has_selected is False:
                    has_selected = True
                subgroup.append(self.create_option(
                    name, subvalue, sublabel, sub_help, selected, index,
                    subindex=subindex, attrs=attrs,
                ))
                if subindex is not None:
                    subindex += 1
        return groups

    def create_option(self, name, value, label, help_text, selected, index,
                      subindex=None, attrs=None):
        index = str(index) if subindex is None else "%s_%s" % (index, subindex)
        if attrs is None:
            attrs = {}
        option_attrs = self.build_attrs(self.attrs, attrs) \
            if self.option_inherits_attrs else {}
        classes = option_attrs.get('class', None)
        if classes:
            if "form-check-input" not in classes:
                option_attrs["class"] = classes + " form-check-input"
        else:
            option_attrs["class"] = "form-check-input"
        if selected:
            option_attrs.update(self.checked_attribute)
        if 'id' in option_attrs:
            option_attrs['id'] = self.id_for_label(option_attrs['id'], index)
        return {
            'name': name,
            'value': value,
            'label': label,
            'help_text': help_text,
            'selected': selected,
            'index': index,
            'attrs': option_attrs,
            'type': self.input_type,
            'template_name': self.option_template_name,
        }
