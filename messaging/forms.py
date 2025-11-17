from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from messaging.models import SMSLog


class SMSForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 5,
            "id": "messageBox",
            "onkeyup": "updateCount()"
        })
    )

    phone = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 5,
            "id": "messageBox",
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("message", css_class="col-md-6"),
            ),
            Row(
                Column("phone", css_class="col-md-6"),
            ),

            Submit("submit", "Send SMS", css_class="btn btn-primary w-100 mt-3")
        )