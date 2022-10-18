from attr import attr
from rest_framework import serializers
from apps.students.models import Assignment


class TeacherAssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = '__all__'

    def validate(self, attrs):
        attrs['state'] = "GRADED"
        return super().validate(attrs)
