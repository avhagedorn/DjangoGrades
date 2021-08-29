import re

#Common keywords
legend = {
    'homework' : 'Homework',
    'assignment' : 'Homework',
    'project' : 'Homework',
    'exam' : 'Exam',
    'midterm' : 'Exam',
    'test' : 'Exam',
    'paper' : 'Paper',
    'essay' : 'Paper',
    'quiz' : 'Quiz',
    'attendance' : 'Participation',
    'discussion' : 'Participation',
    'lab' : 'Lab',
    'final' : 'Final'
}

# Groups assignments by matching keywords
#   title: string of assignment name
#   weights: dictionary containing 'weights', 'assignment_num', and 'titles'
def classifier(title, weights):
    pattern = r'[0-9]'
    words = re.sub(pattern, '', title).lower().split(' ')
    assignment_group = 'Undefined'
    for word in words:
        if (word in legend): 
            assignment_group = legend[word]
            break
    if (assignment_group in weights):
        curr_group = weights[assignment_group]
        curr_group['assignment_num'] += 1
        curr_group['titles'].append(title)
    else:
        weights[assignment_group] = {'assignment_num' : 1, 
                                     'weight' : 0, 
                                     'titles' : [title]}
    return assignment_group

