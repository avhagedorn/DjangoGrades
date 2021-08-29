from .models import Course, Student
from .logic_weights import find_letter_grade

def update_gradelines(course, gradelines):
	new_gradelines = {}
	for letter, val in gradelines.items():
		new_gradelines[letter] = int(val[0])
	update_letter_grades(course, new_gradelines)
	course.gradelines = new_gradelines
	course.save(update_fields=['gradelines', 'letter_grade_dist'])

def gradelines_are_valid(gradelines):
    checking_order = ['a', 'a_minus', 
                      'b_plus', 'b', 'b_minus', 
                      'c_plus', 'c', 'c_minus', 
                      'd_plus', 'd', 'd_minus', 
                      'f']

    for i in range(1, len(checking_order)):
        if (gradelines[checking_order[i]] > gradelines[checking_order[i-1]]):
            return False
    return True

def update_letter_grades(course, gradelines):
    grade_dist = {'a' : 0, 'a_minus' : 0, 
			    'b_plus' : 0, 'b' : 0, 'b_minus' : 0,
			    'c_plus' : 0, 'c' : 0, 'c_minus' : 0,
		    	'd_plus' : 0, 'd' : 0, 'd_minus' : 0,
			    'f' : 0}
    students = Student.objects.filter(course=course)

    for student in students: 
        student.letter_grade = find_letter_grade(gradelines, student.grade, grade_dist)

    percentage_ratio = 100/len(students)
    for grade in grade_dist:
        grade_dist[grade] *= percentage_ratio

    for grade in grade_dist:
        grade_dist[grade] = round(grade_dist[grade], 2)

    students.bulk_update(students, ['letter_grade'])
    course.letter_grade_dist = grade_dist

def add_category(course, form_data):
    category_title = form_data['categoryTitle'][0]
    if category_title  not in course.course_weights:
        course.course_weights[category_title] = {'titles' : [], 'num_assignments' : 0, 'weight' : 0}
        course.save(update_fields=['course_weights'])