from rest_framework import serializers

from .models import DocAppointment

class AppointmentSerializers(serializers.ModelSerializer):
    class Meta:
        model=DocAppointment
        fields='__all__'