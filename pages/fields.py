import copy
from itertools import chain

from django.forms import TextInput, Field, Widget
from django.contrib.postgres.utils import prefix_validation_error
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


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
        return [self.widget.value_from_datadict(data, files,
                                                '%s_%s' % (name, index))
                for index in range(self.max_size)]

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
