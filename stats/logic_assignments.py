from .models import Course, Student, Assignment
from .logic_weights import generate_dist, update_weights

def update_assignments(curr_course, updated_vals, assignments):
	categories_to_delete = list(curr_course.course_weights.keys())

	updated_items = []
	for assignment in assignments:
		if (assignment.type_key != updated_vals[assignment.title][0]):
			updated_items.append({'title' : assignment.title, 
								  'original_key' : assignment.type_key, 
								  'new_key' : updated_vals[assignment.title][0]})
			assignment.type_key = updated_vals[assignment.title][0]
			assignment.save(update_fields=['type_key'])

		if (assignment.type_key in categories_to_delete):
			categories_to_delete.remove(assignment.type_key)

	if (updated_items != []):
		update_course_weight(curr_course, updated_items)

		if (weights_are_initialized(curr_course)):
		    generate_dist(curr_course) 

	# Delete unused categories
	if (categories_to_delete != []):
		for category in categories_to_delete:
			curr_course.course_weights.pop(category)
		curr_course.save(update_fields=['course_weights'])

def update_course_weight(curr_course, updated_items):
    updated_weights = curr_course.course_weights

    for item in updated_items:
        updated_weights[item['original_key']]['titles'].remove(item['title'])
        updated_weights[item['new_key']]['titles'].append(item['title'])
    
    for weight in updated_weights.keys():
        updated_weights[weight]['assignment_num'] = len(updated_weights[weight]['titles'])

    curr_course.course_weights = updated_weights
    curr_course.is_curved = False
    curr_course.save(update_fields=['course_weights', 'is_curved'])

def weights_are_initialized(curr_course):
    weight_types = curr_course.course_weights
    initialized = False
    for curr_type in weight_types:
        if (weight_types[curr_type]['weight'] != 0):
            initialized = True
            break
    return initialized

def drop_assignment(curr_course, request_data):
	return None