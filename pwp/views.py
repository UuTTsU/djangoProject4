from rest_framework import permissions, generics
from .models import WorkoutPlan, WorkoutSession, WeightTracking, FitnessGoal, WorkoutProgress
from .serializers import WorkoutPlanSerializer, WorkoutSessionSerializer, WeightTrackingSerializer, FitnessGoalSerializer, WorkoutProgressSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import now

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


class StartWorkoutView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id):
        session = WorkoutSession.objects.get(id=session_id, user=request.user)

        if WorkoutProgress.objects.filter(workout_session=session).exists():
            return Response({"message": "Workout session already started!"}, status=400)

        exercises = session.workoutplan.exercises.all()
        if not exercises.exists():
            return Response({"message": "No exercises found for this workout plan."}, status=400)

        progress_entries = []
        for exercise in exercises:
            progress = WorkoutProgress.objects.create(
                workout_session=session,
                exercise=exercise,
                planned_sets=exercise.default_sets,
                planned_reps=exercise.default_reps
            )
            progress_entries.append(progress)

        serializer = WorkoutProgressSerializer(progress_entries[0])
        return Response(serializer.data, status=201)


class NextExerciseView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, session_id):
        session = WorkoutSession.objects.get(id=session_id, user=request.user)
        progress_entries = WorkoutProgress.objects.filter(workout_session=session, is_completed=False).order_by('id')

        if not progress_entries.exists():
            return Response({"message": "Workout complete!"}, status=200)

        serializer = WorkoutProgressSerializer(progress_entries.first())
        return Response(serializer.data)


class CompleteExerciseView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, progress_id):
        progress = WorkoutProgress.objects.get(id=progress_id, workout_session__user=request.user)
        progress.is_completed = True
        progress.end_time = now()
        progress.actual_sets = request.data.get("actual_sets", progress.planned_sets)
        progress.actual_reps = request.data.get("actual_reps", progress.planned_reps)
        progress.save()

        return Response({"message": f"{progress.exercise.name} marked as completed!", "next_exercise": NextExerciseView().get(request, progress.workout_session.id).data})


class AdjustExerciseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, progress_id):
        progress = WorkoutProgress.objects.get(id=progress_id, workout_session__user=request.user)

        progress.actual_sets = request.data.get("actual_sets", progress.actual_sets)
        progress.actual_reps = request.data.get("actual_reps", progress.actual_reps)
        progress.notes = request.data.get("notes", progress.notes)
        progress.save()

        return Response({"message": f"{progress.exercise.name} updated!", "updated_data": WorkoutProgressSerializer(progress).data})