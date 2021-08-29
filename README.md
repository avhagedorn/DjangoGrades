# 📈 Django Grades

A grades visualization tool built with Django. 

### Built using ###

Python, Django, Chart.js, Bootstrap 4, PostgreSQL

### Features ###

* Graphs of assignment trends, grade distribution, and more!
* Customizable gradelines and assignment weights.
* Grading curves ordered by most to least optimal given an ideal distribution.
* Future projection of added assignments based on previous course history.

### Building and Running ###

Instructions coming soon, this section is currently under construction. 👷

### Issues ###

Due to this being my first medium-sized project, I was not aware of the importance of app architecture.

Because of this, the code follows a pattern of View -> logic_[item].py -> Model, where logic_[item].py is a file containing functions which do the heavy lifting. When I find some free time, I would like to fix this.
