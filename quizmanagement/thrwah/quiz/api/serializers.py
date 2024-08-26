from rest_framework import serializers
from quiz.models import Level, Quiz, Question, Choice, Submission, Answer

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

    def create(self, validated_data):
        # Custom logic for grading a submission
        submission = super().create(validated_data)
        total_score = 0
        correct_answers = 0
        for answer in submission.answers.all():
            if answer.question.question_type == 'MC' or answer.question.question_type == 'TF':
                if answer.selected_choice and answer.selected_choice.is_correct:
                    correct_answers += 1
            elif answer.question.question_type in ['SA', 'ES']:
                # Handle short answer or essay grading logic here
                pass
        if correct_answers:
            total_score = correct_answers / submission.answers.count() * 100
        submission.score = total_score
        submission.graded = True
        submission.save()

        # Check if the student should advance to the next level
        if total_score >= 70:  # Assume 70% is the passing score
            current_level = submission.student.profile.current_level
            next_level = Level.objects.filter(level_number=current_level.level_number + 1).first()
            if next_level:
                submission.student.profile.current_level = next_level
                submission.student.profile.save()
        return submission

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
