from django import forms
from events.models import Event, Participant, Catagory
from django.forms.widgets import CheckboxSelectMultiple

class StyledFormMixing:
    
    '''widget using mixing'''
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widgets()


    default_classes = "w-full mt-2 px-4 py-2 mb-4 border-2 bg-gray-100  rounded-lg "

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            label_text = (field.label or '').lower()

            if isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': 'Enter your email address'
                })
            
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f'Enter {label_text}'
                })
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    'type': 'time',
                    'class': self.default_classes,
                    'placeholder': f'Select {label_text}'
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f'Enter {label_text}',
                    'rows': 5,
                    'style': 'resize: none;'
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    "class": self.default_classes,
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "mb-4 space-y-2"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })


class EventForm(StyledFormMixing, forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=Participant.objects.all(),
        widget=CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category', 'participants']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

        if self.instance.id:
            self.fields['participants'].initial = self.instance.participants.all()

    def save(self, commit=True):
        event_instance = super().save(commit=commit)
        if commit:
            selected_participants = self.cleaned_data.get('participants')
            current_participants = Participant.objects.filter(events=event_instance)
            to_remove = current_participants.difference(selected_participants)
            to_add = selected_participants.difference(current_participants)

            for participant in to_remove:
                participant.events.remove(event_instance)

            for participant in to_add:
                participant.events.add(event_instance)

        return event_instance
    
class ParticipantForm(StyledFormMixing, forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']
        widgets = {
            'events': forms.CheckboxSelectMultiple
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.apply_styled_widgets()

class CatagoryForm(StyledFormMixing, forms.ModelForm):
    class Meta:
        model = Catagory
        fields = ['name', 'description']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.apply_styled_widgets()

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Catagory.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Category with this name already exists.")
        return name