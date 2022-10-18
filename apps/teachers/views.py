from rest_framework import generics, status
from rest_framework.response import Response
from apps.students.models import Assignment
import json

from apps.teachers.serializers import TeacherAssignmentSerializer
# Create your views here.


class TeacherAssignmentView(generics.RetrieveUpdateAPIView):
    serializer_class = TeacherAssignmentSerializer

    def patch(self, request, *args, **kwargs):
        assignment = None
        print(request.data)
        try:
            assignment = Assignment.objects.get(id=request.data['id'])
        except Assignment.DoesNotExist:
            return Response(
                data={'error': 'Assignment does not exist/permission denied'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(
            assignment, data=request.data, partial=True)

        # Teacher cannot change content of the assignment
        if 'content' in request.data:
            return Response(data={'non_field_errors': ["Teacher cannot change the content of the assignment"]}, status=status.HTTP_400_BAD_REQUEST)

        # Graded assignments cannot be graded again
        if 'grade' in request.data and assignment.state == "GRADED":
            return Response(data={'non_field_errors': ["GRADED assignments cannot be graded again"]}, status=status.HTTP_400_BAD_REQUEST)

        # Teacher can grade only submitted assignments
        if 'grade' in request.data and assignment.state != "SUBMITTED":
            return Response(data={'non_field_errors': ["SUBMITTED assignments can only be graded"]}, status=status.HTTP_400_BAD_REQUEST)

        # Teacher cannot grade assignments of other teacher
        if 'grade' in request.data and request.user.id != assignment.teacher.id:
            return Response(data={'non_field_errors': ["Teacher cannot grade for other teachers assignment"]}, status=status.HTTP_400_BAD_REQUEST)

        # Teacher cannot change the student who submitted the assignment
        if 'student' in request.data and request.data['student'] != assignment.student.id:
            return Response(data={'non_field_errors': ["Teacher cannot change the student who submitted the assignment"]},  status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(
            assignment, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, *args, **kwargs):
        assignments = Assignment.objects.filter(teacher__user=request.user)
        return Response(
            data=self.serializer_class(assignments, many=True).data,
            status=status.HTTP_200_OK
        )
