from .models import Course, Student, Assignment
from .logic_weights import find_letter_grade
import math

def distribution_valid(desired_distribution: dict) -> bool:
    distribution_check = 0
    for value in desired_distribution.values():
        distribution_check += int(value[0])
    return distribution_check == 100

# No curve
def calculate_error(current_scores: list, target_scores: list) -> float: 
    # A error
    error = abs(current_scores[0] + current_scores[1] - target_scores[0])
    # B, C, D error
    for i in range(1, len(target_scores)-1):
        letter_percentage = 0
        for j in range(i, i+3):
            letter_percentage += current_scores[j]
        error += abs(letter_percentage - target_scores[0])
    # F error
    error += abs(current_scores[-1] - target_scores[-1])
    return error

# Flat curve
# Adds (100 - max score) to every student's score
def flat_curve(students: list,  max_score: float, target_scores: list, checking_order: list, curr_dist: list) -> float:
    curved_grades = [0] * len(checking_order)
    if 100 - max_score > 0:
        curve = 100 - max_score
        student_weight = 100 / len(students)
        for student in students:
            adjusted_grade = student['grade'] + curve
            idx = grade_index(checking_order, adjusted_grade)
            curved_grades[idx] += student_weight
    else:
        curved_grades = curr_dist
    return {'distribution' : round_dist(curved_grades), 'error' : calculate_error(curved_grades, target_scores), 'title' : 'Flat Curve', 'id':'curve_flat'}

# Square root curve
# score = sqrt(uncurved_score) * 10
def sqrt_curve(students: list, target_scores: list, checking_order: list) -> float:
    curved_grades = [0] * len(checking_order)
    student_weight = 100 / len(students)
    for student in students:
        curved_grade = math.sqrt(student['grade']) * 10
        index = grade_index(checking_order, curved_grade)
        curved_grades[index] += student_weight
    return {'distribution' : round_dist(curved_grades), 'error' : calculate_error(curved_grades, target_scores), 'title' : 'Square Root Curve', 'id':'curve_sqrt'}

# Linear curve
# Score = ideal_max + (ideal_min - ideal_max) * (uncurved_score - real_max) / (real_min - real_max)
def linear_curve(students: list, target_scores: list, checking_order: list) -> float:
    NUM_STUDENTS = len(students)
    REAL_MAX = students[NUM_STUDENTS-1]['grade']
    REAL_MIN = students[0]['grade']
    IDEAL_MAX = 100
    IDEAL_MIN = 60

    curved_grades = [0] * len(checking_order)
    student_weight = 100 / NUM_STUDENTS
    PRECOMPUTED = (IDEAL_MIN - IDEAL_MAX) / (REAL_MIN - REAL_MAX)

    for student in students:
        curved_grade = IDEAL_MAX + PRECOMPUTED * (student['grade'] - REAL_MAX) 
        index = grade_index(checking_order, curved_grade)
        curved_grades[index] += student_weight
    return {'distribution' : round_dist(curved_grades), 'error' : calculate_error(curved_grades, target_scores), 'title' : 'Linear Curve', 'id':'curve_linear'}

# Normal distribution curve
# Score = const_1 + (const_2 * (score - avg_score) / standard_deviation)
def normal_curve(students: list, target_scores: list, checking_order: list, mean: float) -> float:
    CONST_1 = 85    # Standard constants
    CONST_2 = 10
    curved_grades = [0] * len(checking_order)
    student_weight = 100 / len(students)
    deviation = find_deviation(students, mean)
    for student in students:
        adjusted_grade = CONST_1 + (CONST_2 * (student['grade'] - mean) / deviation)
        idx = grade_index(checking_order, adjusted_grade)
        curved_grades[idx] += student_weight
    return {'distribution' : round_dist(curved_grades), 'error' : calculate_error(curved_grades, target_scores), 'title' : 'Normal Distribution Curve', 'id' : 'curve_normal'}

# Helper for normal_curve()
def find_deviation(students: list, mean: float) -> float:
    diff_sum = 0.0
    for student in students:
        diff_sum += abs(student['grade'] - mean) ** 2
    diff_sum /= len(students)
    return math.sqrt(diff_sum)

# Calls and sorts all other curves
def find_curve(students: list, target_dist: dict, gradelines: dict, current_dist: dict, mean: float) -> list:
    #Get ordered data from dictionary
    listing_order = ['a', 'a_minus', 'b_plus', 'b', 'b_minus', 'c_plus', 'c', 'c_minus', 'd_plus', 'd', 'd_minus', 'f']

    checking_order = [gradelines[key] for key in listing_order]
    current_dist_list = [current_dist[key] for key in listing_order]
    cleaned_target = [int(val[0]) for val in target_dist.values()]
    NUM_STUDENTS = len(students)
    MAX_SCORE = students[NUM_STUDENTS-1]['grade']
    
    no_curve_dict = {'distribution' : current_dist_list, 'error' : calculate_error(current_dist_list, cleaned_target), 'title' : 'No Curve', 'id':'curve_none'}

    flat_curve_dict = flat_curve(students, MAX_SCORE, cleaned_target, checking_order, current_dist_list)

    sqrt_curve_dict = sqrt_curve(students, cleaned_target, checking_order)

    linear_curve_dict = linear_curve(students, cleaned_target, checking_order)

    normal_curve_dict = normal_curve(students, cleaned_target, checking_order, mean)

    curves = [no_curve_dict, flat_curve_dict, sqrt_curve_dict, linear_curve_dict, normal_curve_dict]

    curves.sort(key=sort_func)
    return curves

def sort_func(e: dict) -> float:
    return e['error']

def index_dict(curves: dict) -> dict:
    indexes = {}
    i = 0
    for curve in curves:
        indexes[curve['id']] = i
        i += 1
    return indexes

def round_dist(grades: list) -> list:
    for i in range(len(grades)):
        grades[i] = round(grades[i], 2)
    return grades

# Determines the index the grade should occupy
def grade_index(checking_order: list, numerical_grade: float) -> int:
    for i in range(len(checking_order)):
        if (numerical_grade >= checking_order[i]):
            return i
    return len(checking_order) - 1    #Last index