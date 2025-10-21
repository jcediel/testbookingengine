from datetime import datetime
from django import forms
from django.forms import ModelForm

from .models import Booking, Customer


class RoomSearchForm(ModelForm):
    class Meta:
        model = Booking
        fields = ["checkin", "checkout", "guests"]
        labels = {"guests": "Huéspedes"}
        widgets = {
            "checkin": forms.DateInput(
                attrs={"type": "date", "min": datetime.today().strftime("%Y-%m-%d")}
            ),
            "checkout": forms.DateInput(
                attrs={
                    "type": "date",
                    "max": datetime.today()
                    .replace(month=12, day=31)
                    .strftime("%Y-%m-%d"),
                }
            ),
            "guests": forms.DateInput(attrs={"type": "number", "min": 1, "max": 4}),
        }


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        labels = {"name": "Nombre y apellido", "phone": "Teléfono"}


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"
        labels = {}
        widgets = {
            "checkin": forms.HiddenInput(),
            "checkout": forms.HiddenInput(),
            "guests": forms.HiddenInput(),
        }


class BookingFormExcluded(ModelForm):
    class Meta:
        model = Booking
        exclude = ["customer", "room", "code"]
        labels = {}
        widgets = {
            "checkin": forms.HiddenInput(),
            "checkout": forms.HiddenInput(),
            "guests": forms.HiddenInput(),
            "total": forms.HiddenInput(),
            "state": forms.HiddenInput(),
        }


class BookingDatesForm(ModelForm):
    class Meta:
        model = Booking
        fields = ["checkin", "checkout"]
        labels = {"checkin": "Fecha de entrada", "checkout": "Fecha de salida"}
        widgets = {
            "checkin": forms.DateInput(
                attrs={
                    "type": "date",
                    "min": datetime.today().strftime("%Y-%m-%d"),
                    "class": "form-control",
                }
            ),
            "checkout": forms.DateInput(
                attrs={
                    "type": "date",
                    "max": datetime.today()
                    .replace(month=12, day=31)
                    .strftime("%Y-%m-%d"),
                    "class": "form-control",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        checkin = cleaned_data.get("checkin")
        checkout = cleaned_data.get("checkout")
        if checkin and checkout and checkin >= checkout:
            raise forms.ValidationError(
                "La fecha de salida debe ser posterior a la de entrada"
            )
        return cleaned_data
