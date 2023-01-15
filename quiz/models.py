from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Quiz(models.Model):
    title = models.CharField("Quiz Title", max_length=50)

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.CharField('Question Title', max_length=500, null=False)
    quiz = models.ForeignKey("Quiz", related_name='questions', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def get_answer(self):
        for option in self.options:
            if option.answer:
                return option

        return None

    def __str__(self):
        return self.title


class Option(models.Model):
    question = models.ForeignKey(
        Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField("Text", max_length=500, null=False)
    answer = models.BooleanField("Is Answer?", default=False)

    class Meta:
        verbose_name = 'Option'
        verbose_name_plural = 'Options'

    def __str__(self):
        return self.text


class Attempt(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="attempts", on_delete=models.CASCADE)
    attempter = models.ForeignKey(User, related_name="attempts", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Attempt'
        verbose_name_plural = 'Attempts'

    def __str__(self):
        return f"{self.attempter.email} attempted {self.quiz.title}"
    

class Answer(models.Model):
    attempt = models.ForeignKey(Attempt, related_name="answers", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="attempted_answers", on_delete=models.CASCADE)
    selected = models.ForeignKey(Option, related_name="answer_selections", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return f"{self.attempt.quiz.title} {self.question.title} {self.question.selected.text}"
    