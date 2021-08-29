from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, FormView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Course, Student, Assignment
from json import dumps
from .forms import AddAssignmentForm, DropAssignmentForm, UploadFileForm, UpdateWeightForm, CategoryForm, GradelineForm, IdealDistributionForm
from .logic_csv_reader import csv_process
from .logic_assignments import update_assignments
from .logic_weights import update_weights, weights_valid
from .logic_gradelines import update_gradelines, gradelines_are_valid, add_category
from .logic_curves import distribution_valid, find_curve, index_dict
from .logic_tool_menu import add_assignment
from .apply_curve import apply_curve
from django.core.paginator import Paginator

class CourseListView(ListView):
	template_name = 'stats/home.html'

	def get(self, request, *args, **kwargs):
		queryset = []
		if (self.request.user.is_authenticated):
			queryset = Course.objects.filter(professor = request.user)		
		return render(request, self.template_name, {'courses' : queryset})

class CourseDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
	model = Course

	def test_func(self):
		course = self.get_object()
		return self.request.user == course.professor
	
	def get(self, request, *args, **kwargs):
		course = self.get_object()
		averages = Assignment.objects.filter(course = course).values('title', 'avg_score')
		assignmentTitles = [a['title'] for a in averages]							#FIXME
		oldWeights = [round(a['avg_score'], 2) for a in averages]					#FIXME
		assignment_types = list(self.get_object().course_weights.keys())
		CATEGORY_CHOICES = [(c, c) for c in assignment_types]

		view_data = {'course' : course,
					'assignment_titles' : assignmentTitles,
					'assignment_avgs' : oldWeights,
					'jsonTitles' : dumps(list(assignmentTitles)), 
					'jsonAvg' : dumps(list(oldWeights)),
					'hasGrades' : course.grade_dist != [],
					'gradeDist' : course.grade_dist,
					'curve_form' : IdealDistributionForm(),
					'add_assignment_form' : AddAssignmentForm(CATEGORY_CHOICES),
					'drop_assignment_form' : DropAssignmentForm(CATEGORY_CHOICES)}
		self.add_detail(view_data)

		if (course.detailed):
			page = request.GET.get('page', 1)
			paginator = Paginator(Student.objects.filter(course = self.get_object()), 25)
			view_data['students'] = paginator.page(page)
		return render(request, 'stats/course_detail.html', view_data)

	def add_detail(self, view_data):
		dist = self.get_object().letter_grade_dist
		checking_order = ['a', 'a_minus', 
						'b_plus', 'b', 'b_minus', 
						'c_plus', 'c', 'c_minus', 
						'd_plus', 'd', 'd_minus', 
						'f']
		num_checks = len(checking_order)
		letter_grade_dist = [0] * num_checks
		for i in range(num_checks):
			code = checking_order[i]
			letter_grade_dist[i] = dist[code]
		view_data['letterGradeLabels'] = dumps(['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F'])
		view_data['letterGradeDist'] = dumps(letter_grade_dist)
		
	def post(self, request, *args, **kwargs):
		request_data = dict(request.POST)		
		request_data.pop('csrfmiddlewaretoken')

		if 'curve_name' in request_data:
			return self.post_curve_apply(request, request_data)
		else:
			post_type = request_data['item_type'][0]
			request_data.pop('item_type')
			if post_type == 'curve':
				return self.post_curve_form(request, request_data)

			elif post_type == 'undo':
				weights = self.get_object().course_weights
				curr_weights = {}
				for i in weights:
					curr_weights[i] = [weights[i]['weight']]
				update_weights(self.get_object(), curr_weights)
			elif post_type == 'add':
				add_assignment(self.get_object(), request_data)
			elif post_type == 'drop':								# TODO: Finish drop
				print("drop")
			return redirect(request.META.get("HTTP_REFERER"))
		
	def post_curve_apply(self, request, curve_dict):
		apply_curve(curve_dict['curve_name'][0], self.get_object())
		return self.get(request)

	def post_curve_form(self, request, desired_distribution):
		if (distribution_valid(desired_distribution)):
			if (self.get_object().grade_dist != []):
				gradelines = self.get_object().gradelines
				grade_dist = self.get_object().letter_grade_dist
				students = Student.objects.filter(course=self.get_object()).order_by('grade').values('name', 'grade')
				curve_results = find_curve(students, desired_distribution, gradelines, grade_dist, self.get_object().average_grade)
				curve_indexes = index_dict(curve_results)
				return render(request, 'stats/curve_results.html', {'title' : self.get_object().title, 
															  		'id' : self.get_object().id, 
															  		'results' : curve_results,
																	'indexesJSON' : dumps(dict(curve_indexes)),
																	'resultsJSON' : dumps(list(curve_results))})
			else:
				messages.warning(request, "Weights not defined, cannot generate a curve!")
				return redirect('/')
		else:
			messages.warning(request, "Invalid distribution, cannot generate a curve!")
			return redirect('/')

class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Course 
	success_url = '/'
	
	def test_func(self):
		course = self.get_object()
		return self.request.user == course.professor

class CourseCreateView(LoginRequiredMixin, CreateView):
	model = Course
	fields = ['title', 'term', 'description']

	def form_valid(self, form):
		form.instance.professor = self.request.user
		return super().form_valid(form)

class CourseUploadView(LoginRequiredMixin, UserPassesTestMixin, DetailView, FormView):
	model = Course
	template_name = 'stats/data_upload_form.html'
	form_class = UploadFileForm
	success_url = '/'

	def file_valid(self, f):
		try:
			return f['file'].name.endswith('.csv')
		except:
			return False

	def test_func(self):
		course = self.get_object()
		return self.request.user == course.professor

	def post(self, request, *args , **kwargs):
		form = UploadFileForm(request.POST, request.FILES)
		if self.file_valid(request.FILES):	
			try:
				csv_process(request.FILES['file'], self.get_object())
			except:
				messages.warning(request, "Unexpected error occurred, make sure the csv matches the expected format!")
				return redirect('/')
			messages.success(request, "Successfully uploaded course data!")
		else:
			messages.warning(request, "Unexpected error occurred, make sure you upload a csv!")
		return self.form_valid(form)
	
class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Course
	fields = ['title', 'term', 'description', 'detailed']
	template_name = 'stats/course_update.html'

	def form_valid(self, form):
		form.instance.professor = self.request.user
		return super().form_valid(form)
	
	def test_func(self):
		course = self.get_object()
		return self.request.user == course.professor
	
class EvalWeightForm(LoginRequiredMixin, UserPassesTestMixin, DetailView, FormView):
	model = Course
	success_url = '/'

	def test_func(self):
		course = self.get_object()
		return self.request.user == course.professor

	def get(self, request, *args, **kwargs):
		weights = self.get_object().course_weights
		curr_weights = {}
		for i in weights:
			curr_weights[i] = int(weights[i]['weight'])
		return render(request, 'stats/weight_config_form.html', {'form' : UpdateWeightForm(weights.keys(), initial=curr_weights), 
																 'title_dict' : weights, 
																 'id' : self.get_object().id,
																 'is_curved' : self.get_object().is_curved})

	def post(self, request, *args, **kwargs): 
		form = UpdateWeightForm(request.POST)
		if self.form_valid(form):
			weights = dict(request.POST)
			weights.pop('csrfmiddlewaretoken')
			if (weights_valid(weights)):
				update_weights(self.get_object(), weights)
			else:
				messages.warning(request, "Invalid weights, changes have been reverted.")
		return super().form_valid(form)

class CourseCategoryForm(LoginRequiredMixin, UserPassesTestMixin, DetailView, FormView):
	model = Course
	success_url = '/'

	def test_func(self):
		course = self.get_object()
		return self.request.user == course.professor

	def get(self, request, *args, **kwargs):
		assignment_types = list(self.get_object().course_weights.keys())
		title_vals = Assignment.objects.filter(course = self.get_object()).values('title', 'type_key')
		CATEGORY_CHOICES = [(c, c) for c in assignment_types]
		default = {}
		for assignment in title_vals:
			default[assignment['title']] = assignment['type_key']
		return render(request, 'stats/configure_categories_form.html', {'id' : self.get_object().id, 
																		'form' : CategoryForm(assignments=title_vals, categories=CATEGORY_CHOICES, initial=default),
																		'is_curved' : self.get_object().is_curved})

	def post(self, request, *args, **kwargs):
		form = UpdateWeightForm(request.POST)
		new_values = dict(request.POST)
		new_values.pop('csrfmiddlewaretoken')

		if 'categoryTitle' not in new_values:
			assignments = Assignment.objects.filter(course = self.get_object())
			update_assignments(self.get_object(), new_values, assignments)
			return super().form_valid(form)

		else: 
			add_category(self.get_object(), new_values)
			return redirect(request.META.get("HTTP_REFERER"))

class StudentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
	model = Student

	def test_func(self):
		curr_student = self.get_object()
		return self.request.user == curr_student.course.professor

	def get(self, request, *args, **kwargs):
		qset = Assignment.objects.filter(course = self.get_object().course).values('title', 'avg_score')
		titles = [a['title'] for a in qset]
		avg_scores = [a['avg_score'] for a in qset]
		curr_student = self.get_object()
		return render(request, 'stats/student_detail.html', {'student' : curr_student, 
															 'numerical_grade' : round(curr_student.grade, 2),
															 'titles' : titles,
															 'avgScores' : avg_scores,
															 'relative_grade' : round(curr_student.grade - curr_student.course.average_grade, 2),
															 'titlesJSON' : dumps(titles),
															 'rawData' : curr_student.grades_raw, 
															 'avgData' : dumps(avg_scores)})

class CourseGradelineForm(LoginRequiredMixin, UserPassesTestMixin, DetailView, FormView):
	model = Course
	success_url = '/'

	def test_func(self):
		course = self.get_object()
		return course.professor == self.request.user

	def get(self, request, *args, **kwargs):
		return render(request, 'stats/gradeline_form.html', {'form' : GradelineForm(initial=self.get_object().gradelines)})

	def post(self, request, *args, **kwargs):
		form = GradelineForm(request.POST)
		new_gradelines = dict(request.POST)
		new_gradelines.pop('csrfmiddlewaretoken')
		if (gradelines_are_valid(new_gradelines)):
			update_gradelines(course=self.get_object(), gradelines=new_gradelines)
		else: 
			messages.warning(request, "Invalid gradelines, changes have been reverted.")
		return super().form_valid(form)

def about(request):
	return render(request, "stats/about.html")

def demo(request):
	return render(request, "stats/demo.html")

def curves(request):
	return render(request, "stats/curves.html")