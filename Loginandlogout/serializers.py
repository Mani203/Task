from rest_framework import serializers

from Loginandlogout.models import StudentData


class StudentDataSerializer(serializers.ModelSerializer):
    total_duration = serializers.SerializerMethodField()

    class Meta:
        model = StudentData
        fields = ('id', 'session', 'login_datetime', 'logout_datetime', 'created_date', "total_duration")

    def get_total_duration(self, ob):
        if ob.logout_datetime:
            return ob.logout_datetime - ob.login_datetime
        else:
            return None

