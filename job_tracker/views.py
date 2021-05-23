from django.shortcuts import render

from job_tracker.models.task import Task


def build_html(items):
    html = '<ul>'
    for item in items:
        if isinstance(item, int):
            html += '<li>'
            html += '<div>{}</div>'.format(item)
            html += build_html(items[item])
            html += '</li>'
        else:
            html += '<li>'
            html += '<span>{}</span>'.format(item.name)
            html += '<span>{}</span>'.format(item.time)
            html += '</li>'
    html += '</ul>'
    return html


def index(request):
    tree = {}
    tasks = Task.objects.order_by('job_day')
    for task in tasks:
        year = task.job_day.year
        month = task.job_day.month
        day = task.job_day.day
        if year not in tree.keys():
            tree[year] = {}
        if month not in tree[year].keys():
            tree[year][month] = {}
        if day not in tree[year][month].keys():
            tree[year][month][day] = []
        tree[year][month][day].append(task)

    data = {'html': build_html(tree)}
    return render(request, 'index.html', data)
