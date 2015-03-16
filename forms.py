__author__ = 'deekras'



from wtforms.validators import DataRequired, Required
from wtforms import SelectMultipleField, RadioField, SubmitField, widgets, Form

from models import topics, learning_modes


learning_modes_choices = [(k[0], k[1]) for k in learning_modes]

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class Search(Form):
    search_learning_modes = MultiCheckboxField(label = "My preferred learning mode:",
                                 choices= learning_modes_choices,
                                 default=['Video'],
                                 validators=[DataRequired()])

    search_topics = MultiCheckboxField(label= "Topics I'm interested in:",
                                 choices = topics,
                                 default=[ 'Resumes & Cover Letters',
                                            'Productivity',
                                            'Finding Your Passion',
                                            'Networking',
                                            'Interviewing for a Job',
                                            'Career Advancement',
                                            'Social Media',
                                            'Job Search',
                                            'Social Media & Community'],
                                 validators=[DataRequired()])

    submit = SubmitField(label= "Find me resources!")






