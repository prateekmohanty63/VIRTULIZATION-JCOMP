from rest_framework import serializers

from .models import DocAppointment,Doctor

from PIL import Image

class AppointmentSerializers(serializers.ModelSerializer):
    class Meta:
        model=DocAppointment
        fields='__all__'


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Doctor
        fields='__all__'
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    