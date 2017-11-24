from django.test import TestCase, SimpleTestCase
from django import forms
from django.core import exceptions
from django.forms.renderers import DjangoTemplates
from ..fields import DynamicSplitArrayField, DynamicSplitArrayWidget,\
                     ItemTextWidget


class TestSplitFormField(TestCase):

    def test_valid(self):
        class SplitForm(forms.Form):
            array = DynamicSplitArrayField(forms.CharField(), max_size=3)

        data = {'array_0': 'a', 'array_1': 'b', 'array_2': 'c'}
        form = SplitForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, {'array': ['a', 'b', 'c']})

    def test_required(self):
        class SplitForm(forms.Form):
            array = DynamicSplitArrayField(forms.CharField(),
                                           required=True, max_size=3)

        data = {'array_0': '', 'array_1': '', 'array_2': ''}
        form = SplitForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'array': ['This field is required.']})

    def test_remove_nulls(self):
        class SplitForm(forms.Form):
            array = DynamicSplitArrayField(forms.CharField(required=False),
                                           max_size=5, remove_nulls=True)

        data = {'array_0': 'a', 'array_1': '', 'array_2': 'b', 'array_3': ''}
        form = SplitForm(data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data, {'array': ['a', 'b']})

    def test_remove_nulls_not_required(self):
        class SplitForm(forms.Form):
            array = DynamicSplitArrayField(
                forms.CharField(required=False),
                max_size=2,
                remove_nulls=True,
                required=False,
            )

        data = {'array_0': '', 'array_1': ''}
        form = SplitForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, {'array': []})

    def test_required_field(self):
        class SplitForm(forms.Form):
            array = DynamicSplitArrayField(forms.CharField(), max_size=3)

        data = {'array_0': 'a', 'array_1': 'b', 'array_2': ''}
        form = SplitForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'array':
                                       ['Item 3 in the array did not validate:'
                                        ' This field is required.']})

    def test_rendering(self):
        class SplitForm(forms.Form):
            array = DynamicSplitArrayField(forms.CharField(
                widget=ItemTextWidget), max_size=3)
        self.assertHTMLEqual(str(SplitForm()), '''
            <tr>
              <th>
                <label for="id_array_0">Array:</label>
              </th>
              <td>
                <ul class="input-list" required id="id_array">
                  <li class="input-list-item">
                    <div class="input-group">
                      <input type="text" name="array_0"
                             aria-label="Item number 1"
                             required id="id_array_0"/>
                      <span class="input-group-btn">
                        <button class="btn btn-secondary" type="button"
                                onclick="add_item(this)"
                                aria-label="add item">+</button>
                      </span>
                    </div>
                  </li>
                </ul>
              </td>
            </tr>
        ''')

    def test_invalid_char_length(self):
        field = DynamicSplitArrayField(forms.CharField(max_length=2),
                                       max_size=3)
        with self.assertRaises(exceptions.ValidationError) as cm:
            field.clean(['abc', 'c', 'defg'])
        self.assertEqual(cm.exception.messages, [
            'Item 1 in the array did not validate: '
            'Ensure this value has at most 2 characters (it has 3).',
            'Item 3 in the array did not validate: '
            'Ensure this value has at most 2 characters (it has 4).',
        ])


class TestSplitFormWidget(SimpleTestCase):

    def check_html(self, widget, name, value, html='', attrs=None, **kwargs):
        output = widget.render(name, value, attrs=attrs,
                               renderer=DjangoTemplates(), **kwargs)
        self.assertHTMLEqual(output, html)

    def test_get_context(self):
        self.assertEqual(
            DynamicSplitArrayWidget(forms.TextInput(),
                                    max_size=3).get_context('name',
                                                            ['val1', 'val2']),
            {'widget':
             {'template_name': 'widgets/split_array_list.html',
              'required': False,
              'value': "['val1', 'val2']",
              'is_hidden': False,
              'name': 'name',
              'attrs': {},
              'subwidgets': [
                  {'template_name': 'django/forms/widgets/text.html',
                   'required': False,
                   'value': 'val1',
                   'is_hidden': False,
                   'is_last': False,
                   'type': 'text',
                   'name': 'name_0',
                   'attrs': {'aria-label': 'Item number 1'}
                   },
                  {'template_name': 'django/forms/widgets/text.html',
                   'required': False,
                   'value': 'val2',
                   'is_hidden': False,
                   'is_last': False,
                   'type': 'text',
                   'name': 'name_1',
                   'attrs': {'aria-label': 'Item number 2'}
                   },
                  {'template_name': 'django/forms/widgets/text.html',
                   'required': False,
                   'value': None,
                   'is_hidden': False,
                   'is_last': True,
                   'type': 'text',
                   'name': 'name_2',
                   'attrs': {'aria-label': 'Item number 3'}
                   }]
              }
             }
        )

    def test_render(self):
        self.check_html(
            DynamicSplitArrayWidget(forms.TextInput(), max_size=2),
            'array',
            None,
            """
            <ul class="input-list" >
            <input type="text" name="array_0" aria-label="Item number 1" />
            </ul>
            """
        )

    def test_render_attrs_values(self):
        self.check_html(
            DynamicSplitArrayWidget(forms.TextInput(), max_size=2),
            'array', ['val1', 'val2'], attrs={'id': 'foo'},
            html=(
                """
                <ul class="input-list" id="foo">
                <input type="text" name="array_0" value="val1" id="foo_0"
                       aria-label="Item number 1" />
                <input type="text" name="array_1" value="val2" id="foo_1"
                       aria-label="Item number 2" />
                <input type="text" name="array_2" id="foo_2"
                       aria-label="Item number 3" />
                </ul>
                """
            )
        )

    def test_value_omitted_from_data(self):
        widget = DynamicSplitArrayWidget(forms.TextInput(), max_size=2)
        self.assertIs(widget.value_omitted_from_data({}, {}, 'field'), True)
        self.assertIs(widget.value_omitted_from_data({'field_0': 'value'},
                                                     {},
                                                     'field'),
                      False)
        self.assertIs(widget.value_omitted_from_data({'field_1': 'value'},
                                                     {},
                                                     'field'),
                      False)
        self.assertIs(widget.value_omitted_from_data({'field_0': 'value',
                                                      'field_1': 'value'},
                                                     {},
                                                     'field'),
                      False)
