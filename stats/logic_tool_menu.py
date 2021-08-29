from .logic_curves import distribution_valid, find_curve
from .models import Student, Assignment

def predict_score(assignments):
	i = 0
	projected_grade = 0
	for assignment in assignments:
		projected_grade += assignment['avg_score'] / assignment['max_pts']
		i += 1
		if i == 3: break
	return round(assignments[0]['max_pts'] * projected_grade / min(len(assignments), 3), 2)

def add_assignment(curr_course, request_data):
	assignment_type = request_data['assignment_type'][0]
	assignment_title = request_data['title'][0]
	students = Student.objects.filter(course=curr_course)
	assignments = Assignment.objects.filter(course=curr_course, type_key=assignment_type).reverse().values('title', 'avg_score', 'max_pts')

	# Determine assignment grade
	if request_data['projected_avg'][0] == '':
		projected_grade = predict_score(assignments)
	else:
		projected_grade = float(request_data['projected_avg'][0])

	# Create new assignment
	new_assignment = Assignment(course=curr_course, 
								type_key=assignment_type, 
								title=assignment_title, 
								max_pts=assignments[0]['max_pts'],
								avg_score=projected_grade)	
	new_assignment.save()

	# Update student's raw grades
	for student in students:
		student.grades_raw.append(projected_grade)

	# Update course
	curr_course.course_weights[assignment_type]['titles'].append(assignment_title)
	curr_course.course_weights[assignment_type]['assignment_num'] += 1

	# Save course / update grades
	if curr_course.grade_dist == []:
		students.bulk_update(students, ['grades_raw'])
		curr_course.save(update_fields=['course_weights'])
	else:
		update_student_grades(curr_course, students)
		update_grade_dist(curr_course, students)
		curr_course.save(update_fields=['letter_grade_dist', 'average_grade', 'course_weights', 'is_curved', 'grade_dist'])

def update_student_grades(curr_course, students):
	weights = curr_course.course_weights
	letter_dist = {'a' : 0, 'a_minus' : 0, 
				'b_plus' : 0, 'b' : 0, 'b_minus' : 0,
				'c_plus' : 0, 'c' : 0, 'c_minus' : 0,
				'd_plus' : 0, 'd' : 0, 'd_minus' : 0,
				'f' : 0}

	gradelines = curr_course.gradelines
	assignments = Assignment.objects.filter(course = curr_course).values('type_key', 'max_pts', 'avg_score')

	assignment_weight = []
	for a in assignments: 
		assignment_weight.append(weights[a['type_key']]['weight'] / (weights[a['type_key']]['assignment_num'] * a['max_pts']))

	# Updates each student's numerical and letter grade
	for student in students:
		grade = 0
		for i in range(len(assignments)):
			grade += student.grades_raw[i] * assignment_weight[i] 
		student.grade = grade
		student.letter_grade = find_letter_grade(gradelines, grade, letter_dist)
	students.bulk_update(students, ['grade', 'letter_grade', 'grades_raw'])

	# Translates to %
	percentage_ratio = 100/len(students)
	for letter in letter_dist:
		letter_dist[letter] = round((letter_dist[letter] * percentage_ratio), 2)

	# Updates the average numerical course grade
	course_avg = 0.0
	for i in range(len(assignments)):
		course_avg += assignments[i]['avg_score'] * assignment_weight[i]

	curr_course.is_curved = False
	curr_course.average_grade = course_avg
	curr_course.letter_grade_dist = letter_dist
    
#TODO: Fix this
def find_letter_grade(gradelines, numerical_grade, letter_grade_dist):
    checking_order = ['a', 'a_minus', 
                      'b_plus', 'b', 'b_minus', 
                      'c_plus', 'c', 'c_minus', 
                      'd_plus', 'd', 'd_minus', 
                      'f']

    for code in checking_order:
        if (numerical_grade >= gradelines[code]):
            translated_code = ''
            if (len(code) == 1):
                translated_code = code.upper()
            elif (len(code) == 7):
                translated_code = code[0].upper() + '-'
            else:
                translated_code = code[0].upper() + '+'

            letter_grade_dist[code] += 1
            return translated_code

def update_grade_dist(curr_course, students):
    temp = [0] * 101
    for student in students:
        if (student.grade > 100.0): 
            temp[100] += 1
        else:
            grade = int(student.grade)
            temp[grade] += 1
    curr_course.grade_dist = temp