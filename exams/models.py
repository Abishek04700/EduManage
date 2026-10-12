from django.db import models


class Exam(models.Model):
    name = models.CharField(max_length=100, help_text="e.g. Mid Term, Final Term")
    course = models.ForeignKey('academics.Course', on_delete=models.CASCADE, related_name='exams')
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} - {self.course}"


class Result(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, related_name='results')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['exam', 'subject']
        unique_together = ('exam', 'student', 'subject')

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.marks_obtained}/{self.max_marks}"

    @property
    def percentage(self):
        if self.max_marks:
            return round((self.marks_obtained / self.max_marks) * 100, 2)
        return 0

    @property
    def grade(self):
        p = self.percentage
        if p >= 90:
            return 'A+'
        if p >= 80:
            return 'A'
        if p >= 70:
            return 'B'
        if p >= 60:
            return 'C'
        if p >= 50:
            return 'D'
        return 'F'
