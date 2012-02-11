from django import forms

from locations.widgets import GoogleMap

class MapForm(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={}))


