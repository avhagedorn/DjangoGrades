import pandas as pd
from .classifier import classifier
from .models import Student, Assignment

# Writes CSV to DB
def csv_process(file, curr_course):

    try: 
        frame = pd.read_csv(file).fillna(0)
        weights = curr_course.course_weights
        assignment_avg = frame[1:].mean()[1:]   # Excludes max_pts, excludes average ID
        students = frame.values.tolist()[1:]

        if len(students) == 0:
            raise

        eval_lst = [Assignment(course=curr_course, 
                            type_key=classifier(curr_title, weights),
                            title=curr_title, 
                            max_pts=frame[curr_title][0], 
                            avg_score=round(assignment_avg[curr_title], 2)) for curr_title in frame.columns[5:]] 
        Assignment.objects.bulk_create(eval_lst)

        student_lst = [Student(name=student[0], 
                            student_id=int(student[1]),
                            sis_user_id=student[2],
                            sis_login_id=student[3],
                            section=student[4], 
                            course=curr_course, 
                            grade=0.0,
                            grades_raw=student[5:]) for student in students]
        Student.objects.bulk_create(student_lst)

        curr_course.course_weights = weights
        curr_course.save(update_fields=['course_weights'])
    except:
        raise