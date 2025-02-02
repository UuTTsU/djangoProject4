from rest_framework import permissions, generics
from .models import WorkoutPlan, WorkoutSession
from .serializers import WorkoutPlanSerializer, WorkoutSessionSerializer

class WorkoutPlanListCreateView(generics.ListCreateAPIView):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WorkoutPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkoutPlan.objects.filter(user=self.request.user)


class WorkoutSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        workout_plan_id = self.kwargs.get('workout_plan_id')
        return WorkoutSession.objects.filter(workout_plan_id=workout_plan_id)

    def perform_create(self, serializer):
        workout_plan_id = self.kwargs.get('workout_plan_id')
        serializer.save(workout_plan_id=workout_plan_id)


class WorkoutSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkoutSession.objects.all()
    serializer_class = WorkoutSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
