from .models import Student, Assignment

def update_weights(curr_course, new_weights):
    updated = curr_course.course_weights
    for assignment_type in new_weights.keys():
        updated[assignment_type]['weight'] = int(new_weights[assignment_type][0])
    curr_course.course_weights = updated
    curr_course.is_curved = False
    curr_course.save(update_fields=['course_weights', 'is_curved'])
    generate_dist(curr_course)

def generate_dist(curr_course):
    update_student_grades(curr_course)
    update_grade_dist(curr_course)

def update_student_grades(curr_course):
    weights = curr_course.course_weights
    letter_dist = {'a' : 0, 'a_minus' : 0, 
			    'b_plus' : 0, 'b' : 0, 'b_minus' : 0,
			    'c_plus' : 0, 'c' : 0, 'c_minus' : 0,
		    	'd_plus' : 0, 'd' : 0, 'd_minus' : 0,
			    'f' : 0}

    gradelines = curr_course.gradelines
    students = Student.objects.filter(course = curr_course)
    assignments = Assignment.objects.filter(course = curr_course).values('type_key', 'max_pts', 'avg_score')

    assignment_weight = []
    for a in assignments: 
        if (weights[a['type_key']]['assignment_num'] != 0):
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
        assignment_avg = assignments[i]['avg_score']

        course_avg += assignment_avg * assignment_weight[i]

    curr_course.average_grade = course_avg
    curr_course.letter_grade_dist = letter_dist
    curr_course.save(update_fields=['letter_grade_dist', 'average_grade'])
    
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

def update_grade_dist(curr_course):
    students = Student.objects.filter(course = curr_course).values()
    temp = [0] * 101
    for student in students:
        if (student['grade'] > 100.0): 
            temp[100] += 1
        else:
            grade = int(student['grade'])
            temp[grade] += 1
    curr_course.grade_dist = temp
    curr_course.save(update_fields=['grade_dist'])

def weights_valid(weights):
    weight_sum = 0
    for value in weights.values():
        weight_sum += int(value[0])
        if weight_sum > 100:
            return False
    return weight_sum == 100