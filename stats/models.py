from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.urls import reverse

# Initializes unique dict
def init_grade_dist():
	return {'a' : 0, 'a_minus' : 0, 
			'b_plus' : 0, 'b' : 0, 'b_minus' : 0,
			'c_plus' : 0, 'c' : 0, 'c_minus' : 0,
			'd_plus' : 0, 'd' : 0, 'd_minus' : 0,
			'f' : 0}

#Standard gradelines
def init_gradelines():
	return {'a' : 93, 'a_minus' : 90, 
			'b_plus' : 87, 'b' : 83, 'b_minus' : 80,
			'c_plus' : 77, 'c' : 73, 'c_minus' : 70,
			'd_plus' : 67, 'd' : 63, 'd_minus' : 60,
			'f' : 0}

class Course(models.Model):
	professor = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length = 20)
	term = models.CharField(max_length = 20)        
	description = models.CharField(max_length = 75)
	detailed = models.BooleanField(default=True)					#TODO: If more user preferences, make new userprefs table
	is_curved = models.BooleanField(default=False)					# Indicates status of data curve. 
	course_weights = models.JSONField(default=dict) 				# Dictionary formatted as { 'assignment_type' : integer_weight ... }
	grade_dist = models.JSONField(default=list)						# List of length 101 containing the number of students at each truncated %
	letter_grade_dist = models.JSONField(default=init_grade_dist)	# Slightly redundant (grade_dist already exists), but saves time and doesn't occupy much space
	average_grade = models.FloatField(default=0.0)					# Numerical average grade
	gradelines = models.JSONField(default=init_gradelines)			# Dictionary relating a letter grade to the minimum numerical grade 

	def get_absolute_url(self):
		return reverse('course-detail', kwargs={'pk':self.pk})

	def __str__(self):
		return self.title
	
	class Meta:
		ordering = ['pk']

class Student(models.Model):
	name = models.CharField(max_length=100)
	student_id = models.CharField(max_length=30)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	grade = models.FloatField(default=0.0)
	grades_raw = models.JSONField(default=list)
	sis_user_id = models.CharField(max_length=100, default="")
	sis_login_id = models.CharField(max_length=100, default="")
	section = models.CharField(max_length=100, default="")
	letter_grade = models.CharField(max_length=2, default='F')

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['pk']

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    type_key = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    max_pts = models.SmallIntegerField()
    avg_score = models.FloatField()
    
    def __str__(self):
        return self.title
	
    class Meta:
        ordering = ['pk']