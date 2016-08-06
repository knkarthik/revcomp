from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field
from django import forms


class FastaForm(forms.Form):
    seq = forms.CharField(widget=forms.Textarea(attrs={'rows':10, 'cols':100}), label="Fasta sequence", required=False)
    fastafile = forms.FileField(required=False, label="Select Fasta file")

    def __init__(self, *args, **kwargs):
        super(FastaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-2'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('seq', placeholder='''>Example seq
GCAAATGCCGAGTCA'''),
            HTML("<br></br>"),
                'fastafile',
                FormActions(
                        Submit('submit', 'Submit', css_class='btn-primary')))

