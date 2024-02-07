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

### Images:

![django_grades_1](https://github.com/avhagedorn/DjangoGrades/assets/66842958/61607d19-8e16-4689-861d-7b314463943c)

![django_grades_2](https://github.com/avhagedorn/DjangoGrades/assets/66842958/67ae4f42-3cd3-4640-9b6e-d3ac07797ac7)

![django_grades_3](https://github.com/avhagedorn/DjangoGrades/assets/66842958/bf53099b-023c-4ccc-9205-ad442270c685)


### Issues ###

Due to this being my first medium-sized project, I was not aware of the importance of app architecture.

Because of this, the code follows a pattern of View -> logic_[item].py -> Model, where logic_[item].py is a file containing functions which do the heavy lifting. When I find some free time, I would like to fix this.
