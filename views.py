__author__ = 'deekras'

from flask import Flask, render_template, request, redirect
from flask_wtf.csrf import CsrfProtect
from os import urandom
import requests

from forms import Search
from models import learning_modes



CSRF_ENABLED = True
SECRET_KEY =  urandom(32)

app = Flask(__name__)
app.secret_key = urandom(32)
CsrfProtect(app)


@app.route('/', methods=['GET', 'POST'])
def search_form():
    form = Search()
    return render_template('search.html', form=form)


@app.route('/index', methods=['POST'])
def results():
    form = Search(request.form)
    search_topics = form.data['search_topics']
    search_learning_modes = form.data['search_learning_modes']
    search_results = []

    '''This api provides results only one page at a time.
    So need to gather the results from each page first and then present all at once.
    - First time, ask for page 0.
    - And then from the result, we see how many total pages. And run the api for each page (for loop - below).'''
    json_results = run_api(0, search_topics)
    append_select_fields(json_results, search_topics, search_learning_modes, search_results)
    pages = json_results['page_count']

    '''Now we know how many pages, so we run the api that many times,
    minus the first time we already ran it.'''
    for page_number in xrange(1, pages):
        json_results = run_api(page_number, search_topics)
        append_select_fields(json_results, search_topics, search_learning_modes, search_results)

    return render_template('results.html', search_results=search_results,
                                            search_learning_modes=search_learning_modes)

@app.route('/get_resource', methods = ['GET','POST'])
def display_resource():
    selected_resource = request.form['choose_resource']
    get_resource_api = "https://www.themuse.com/resources/{}".format(selected_resource)
    return redirect(get_resource_api)


def run_api(page_number, search_topics):
    '''
    This function builds the url for the api.
    Based on the search parameters specified by the user in the search form.
    '''

    api_prefix = 'https://www.themuse.com/api/v1/resources?'
    api_postfix = '&page={}&descending=true'.format(page_number)
    api_tag = 'tag%5B%5D='
    api_body = ''

    for topic in search_topics:
        add_topic = '+'.join(topic.split())
        api_body = api_body+api_tag+add_topic+'&'
    api = api_prefix+api_body+api_postfix
    return requests.get(api).json()


def append_select_fields(json_results, search_topics, search_learning_modes, search_results):
    '''
    This functions creates a search_results list of dictionaries - of only the relevant fields.
    And then appends each new entry.
    to be used in the results.html
    '''
    learning_modes_list = [k[0] for k in learning_modes] # the original learning_modes list has other data not
                            # relevant to this list, so just taking the data that is needed for this function.

    for entry in json_results['results']:
         new_entry = {
            'id' : entry['id'],
            'name' : entry['name'],
            'author_name' : entry['author_name'],
            'excerpt': entry['excerpt'],
            'update_date': entry['update_date'],
            'search_image': entry['search_image'],
            'topics': [topic for topic in search_topics if topic in entry[u'tags']],
            'preferred_modes': [mode for mode in search_learning_modes if mode in entry[u'tags']],
            'modes': [mode for mode in entry[u'tags'] if mode in learning_modes_list],
            'modes_icon': ['static/icons/'+x[2]+'.png' for x in learning_modes if x[0] in entry[u'tags']],
            'tags': entry['tags'],
            'short_name': entry['short_name']
            }
         search_results.append(new_entry)



if __name__ == "__main__":
    app.run(debug=  True)
