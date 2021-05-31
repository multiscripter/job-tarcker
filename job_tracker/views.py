from datetime import timedelta

from django.shortcuts import render

from job_tracker.models.task import Task


def get_time(td):
    seconds = td.total_seconds()
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '{:02}:{:02}'.format(int(hours), int(minutes))


def get_total_html(items, total, key):
    if total['level']:
        total[total['level'] - 1] += total[total['level']]
    html = '<li class="list-item list-item-total list-item-total-{}">'.format(
        total['level']
    )
    val = get_time(total[total['level']])
    psn = False
    if total['level'] == 2:
        plan = len(items[key]) * 8
        plan_m = plan * 60
        psn = (total[total['level']].total_seconds() / 60) / (plan_m / 100)
        psn = round(psn, 2)
        html += f'<span class="total-plan">{plan}</span>'
    html += f'<span class="total-val">'
    if psn:
        html += f'({psn})% '
    html += f'{val}</span>'
    html += '</li>'
    return html


def build_html(items, total):
    html = '<ul class="list-unstyled">'
    total[total['level']] = timedelta(0)
    for item in items:
        if isinstance(item, int):
            total['level'] += 1
            html += '<li class="list-item">'
            html += f'<input id="p-{item}" type="checkbox" class="list-chbox">'
            html += '<div class="list-chblock">'
            html += f'<label class="list-label" for="p-{item}">'
            html += f'<span class="list-val">{item}</span>'
            html += '</label>'
            html += '</div>'
            html += build_html(items[item], total)
            html += '</li>'
            html += get_total_html(items, total, item)
            total['level'] -= 1
        else:
            total[total['level']] += item.time
            t = get_time(item.time)
            html += '<li class="list-item task">'
            html += f'<span class="task-time">{t}</span>'
            html += f'<span class="task-name">{item.name}</span>'
            if item.actions:
                text = "<br />".join(item.actions.split("\n"))
                html += f'<p class="task-actions">{text}</p>'
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
