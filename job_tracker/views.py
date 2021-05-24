from datetime import timedelta

from django.shortcuts import render

from job_tracker.models.task import Task


def build_html(items):
    html = '<ul class="list-unstyled">'
    is_task = False
    t_day = timedelta(0)
    for item in items:
        if isinstance(item, int):
            html += '<li class="list-item">'
            html += f'<input id="p-{item}" type="checkbox" class="list-chbox">'
            html += f'<label class="list-label" for="p-{item}"></label>'
            html += '<span class="list-val">{}</span>'.format(item)
            html += build_html(items[item])
            html += '</li>'
        else:
            is_task = True
            t_day += item.time
            html += '<li class="list-item task">'
            html += '<span class="task-time">{}</span>'.format(item.time)
            html += '<span class="task-name">{}</span>'.format(item.name)
            if item.actions:
                html += '<p class="task-actions">{}</p>'.format(item.actions)
            html += '</li>'
    if is_task:
        html += '<li class="list-item total-day">'
        html += '<span class="total-day-val">{}</span>'.format(t_day)
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
