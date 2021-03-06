from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
# from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from bbapp.models import UserProfile, Bet


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('firstname','lastname')


# class BetForm(forms.ModelForm):
#     # text_input = forms.CharField()
#     #
#     # textarea = forms.CharField(
#     #     widget = forms.Textarea(),
#     # )

#     radio_buttons = forms.ChoiceField(
#         choices = (
#             ('home', "Home team"),
#             ('away', "Away team")
#         ),
#         widget = forms.RadioSelect,
#         initial = 'home',
#     )

#     checkboxes = forms.MultipleChoiceField(
#         choices = (
#             ('option_one', "Option one is this and that be sure to include why it's great"),
#             ('option_two', 'Option two can also be checked and included in form results'),
#             ('option_three', 'Option three can yes, you guessed it also be checked and included in form results')
#         ),
#         initial = 'option_one',
#         widget = forms.CheckboxSelectMultiple,
#         help_text = "<strong>Note:</strong> Labels surround all the options for much larger click areas and a more usable form.",
#     )

#     appended_text = forms.CharField(
#         help_text = "Here's more help text"
#     )

#     prepended_text = forms.CharField()

#     prepended_text_two = forms.CharField()

#     multicolon_select = forms.MultipleChoiceField(
#         choices = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')),
#     )

#     # Uni-form
#     helper = FormHelper()
#     helper.form_class = 'form-horizontal'
#     helper.layout = Layout(
#         Field('text_input', css_class='input-xlarge'),
#         Field('textarea', rows="3", css_class='input-xlarge'),
#         'radio_buttons',
#         Field('checkboxes', style="background: #FAFAFA; padding: 10px;"),
#         AppendedText('appended_text', '.00'),
#         PrependedText('prepended_text', '<input type="checkbox" checked="checked" value="" id="" name="">', active=True),
#         PrependedText('prepended_text_two', '@'),
#         'multicolon_select',
#         FormActions(
#             Submit('save_changes', 'Save changes', css_class="btn-primary"),
#             Submit('cancel', 'Cancel'),
#         )
#     )

    # def __init__(self, *args, **kwargs):
    #     super(BetForm, self).__init__(*args, **kwargs)
    # class Meta:
    #     model = Bet
    #     fields = ['bet_value']
    #     widgets = {'game': forms.HiddenInput(), 'user1': forms.HiddenInput(), 'user2': forms.HiddenInput(), 'bet_status': forms.HiddenInput()}
