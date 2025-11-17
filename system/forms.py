from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from system.models.models import Farmer, PlantProductionManagement, SoilFertilityManagement


class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            # Row 1
            Row(
                Column('title', css_class='form-group col-md-6 mb-0'),
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.add_input(Submit('submit', 'Save'))


class PlantProductionManagementForm(forms.ModelForm):
    class Meta:
        model = PlantProductionManagement
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

class SoilFertilityManagementForm(forms.ModelForm):
    class Meta:
        model = SoilFertilityManagement
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))