from rest_framework import permissions, generics
from .models import WorkoutPlan, WorkoutSession, WeightTracking, FitnessGoal
from .serializers import WorkoutPlanSerializer, WorkoutSessionSerializer, WeightTrackingSerializer, FitnessGoalSerializer

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



class WeightTrackingListCreateView(generics.ListCreateAPIView):
    serializer_class = WeightTrackingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WeightTracking.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WeightTrackingDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = WeightTrackingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WeightTracking.objects.filter(user=self.request.user)

class FitnessGoalListCreateView(generics.ListCreateAPIView):
    serializer_class = FitnessGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FitnessGoal.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FitnessGoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FitnessGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FitnessGoal.objects.filter(user=self.request.user)
