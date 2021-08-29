from .logic_weights import find_letter_grade
from .models import Student, Assignment
import math

def apply_curve(curve_name, curr_course):
    if curve_name != 'curve_none':
        students = Student.objects.filter(course=curr_course).order_by('grade')
        MAX_SCORE = students[len(students)-1].grade
        STUDENT_WEIGHT = 100 / len(students)
        letter_dist = {'a' : 0, 'a_minus' : 0, 
			    'b_plus' : 0, 'b' : 0, 'b_minus' : 0,
			    'c_plus' : 0, 'c' : 0, 'c_minus' : 0,
		    	'd_plus' : 0, 'd' : 0, 'd_minus' : 0,
			    'f' : 0}
        grade_dist = 101 * [0]
        course_avg = 0

        if curve_name == 'curve_flat':
            course_avg = apply_flat(students, MAX_SCORE, letter_dist, grade_dist, curr_course)
        elif curve_name == 'curve_sqrt':
            course_avg = apply_sqrt(students, letter_dist, grade_dist, curr_course)
        elif curve_name == 'curve_normal':
            course_avg = apply_normal(students, letter_dist, grade_dist, curr_course)
        elif curve_name == 'curve_linear':
            course_avg = apply_linear(students, letter_dist, grade_dist, curr_course)
            
        for key in letter_dist:
            letter_dist[key] = round(STUDENT_WEIGHT * letter_dist[key], 2)

        curr_course.average_grade = course_avg / len(students)
        curr_course.letter_grade_dist = letter_dist
        curr_course.grade_dist = grade_dist
        curr_course.is_curved = True
        curr_course.save(update_fields=['letter_grade_dist', 'average_grade', 'grade_dist', 'is_curved'])

def apply_flat(students: list, max_score: float, letter_dist: dict, grade_dist: list, curr_course):
    course_avg = 0
    if 100 - max_score > 0:
        curve = 100 - max_score
        for student in students:
            new_grade = student.grade + curve
            student.grade = new_grade
            course_avg += new_grade
            grade_dist[int(new_grade)] += 1
            student.letter_grade = find_letter_grade(curr_course.gradelines, new_grade, letter_dist)
    students.bulk_update(students, ['grade', 'letter_grade'])
    return course_avg

def apply_sqrt(students: list, letter_dist: dict, grade_dist: list, curr_course):
    course_avg = 0
    for student in students:
        new_grade = math.sqrt(student.grade) * 10
        student.grade = new_grade
        course_avg += new_grade
        grade_dist[int(new_grade) if new_grade < 101 else 100] += 1
        student.letter_grade = find_letter_grade(curr_course.gradelines, new_grade, letter_dist)
    students.bulk_update(students, ['grade', 'letter_grade'])
    return course_avg

def apply_normal(students: list, letter_dist: dict, grade_dist: list, curr_course):
    course_avg = 0
    MEAN = curr_course.average_grade
    CONST_1 = 85    
    CONST_2 = 10
    deviation = 0.0
    for student in students:
        deviation += abs(student.grade - MEAN) ** 2
    deviation /= len(students)
    deviation = math.sqrt(deviation)

    for student in students:
        new_grade = CONST_1 + (CONST_2 * (student.grade - MEAN) / deviation)
        student.grade = new_grade
        course_avg += new_grade
        grade_dist[int(new_grade) if new_grade < 101 else 100] += 1
        student.letter_grade = find_letter_grade(curr_course.gradelines, new_grade, letter_dist)
    students.bulk_update(students, ['grade', 'letter_grade'])
    return course_avg

def apply_linear(students: list, letter_dist: dict, grade_dist: list, curr_course):
    course_avg = 0
    NUM_STUDENTS = len(students)
    REAL_MAX = students[NUM_STUDENTS-1].grade
    REAL_MIN = students[0].grade
    IDEAL_MAX = 100
    IDEAL_MIN = 60
    PRECOMPUTED = (IDEAL_MIN - IDEAL_MAX) / (REAL_MIN - REAL_MAX)

    for student in students:
        new_grade = IDEAL_MAX + PRECOMPUTED * (student.grade - REAL_MAX) 
        student.grade = new_grade
        course_avg += new_grade
        grade_dist[int(new_grade) if new_grade < 101 else 100] += 1
        student.letter_grade = find_letter_grade(curr_course.gradelines, new_grade, letter_dist)
    students.bulk_update(students, ['grade', 'letter_grade'])
    return course_avg