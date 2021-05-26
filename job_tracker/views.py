from datetime import timedelta

from django.shortcuts import render

from job_tracker.models.task import Task


def get_total_html(total):
    if total['level']:
        total[total['level'] - 1] += total[total['level']]
    html = '<li class="list-item total-day">'
    html += '<span class="total-day-val">{}</span>'.format(
        total[total['level']]
    )
    html += '</li>'
    return html


def build_html(items, total):
    html = '<ul class="list-unstyled">'
    # is_task = False
    total[total['level']] = timedelta(0)
    for item in items:
        if isinstance(item, int):
            total['level'] += 1
            html += '<li class="list-item">'
            html += f'<input id="p-{item}" type="checkbox" class="list-chbox">'
            html += f'<label class="list-label" for="p-{item}"></label>'
            html += '<span class="list-val">{}</span>'.format(item)
            html += build_html(items[item], total)
            html += '</li>'
            html += get_total_html(total)
            total['level'] -= 1
        else:
            #is_task = True
            total[total['level']] += item.time
            html += '<li class="list-item task">'
            html += '<span class="task-time">{}</span>'.format(item.time)
            html += '<span class="task-name">{}</span>'.format(item.name)
            if item.actions:
                html += '<p class="task-actions">{}</p>'.format(item.actions)
            html += '</li>'
    html += '</ul>'
    return html


def index(request):
    total = {
        'level': 0,  # year
        'time': [timedelta(0), timedelta(0), timedelta(0)]
    }
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

    data = {'html': build_html(tree, total)}
    return render(request, 'index.html', data)
