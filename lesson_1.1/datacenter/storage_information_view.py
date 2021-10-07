from django.utils.timezone import localtime, timedelta
from datacenter.models import Visit
from django.shortcuts import render


def storage_information_view(request):

    all_visiters_inside = Visit.objects.filter(leaved_at=None)

    def get_duration(visiter):
        delta = localtime() - visiter.entered_at
        return timedelta(seconds=delta.seconds)

    def format_duration(duration: timedelta):
        duration_string = str(duration)
        _list_with_time = duration_string.split(':')
        hours = _list_with_time[-3]
        minutes = _list_with_time[-2]
        if duration.days:
            return f'{duration.days}d {hours}:{minutes}'
        return f'{hours}:{minutes}'

    non_closed_visits = []
    for visiter in all_visiters_inside:
        who_entered = visiter.passcard.owner_name
        entered_at = localtime(visiter.entered_at)
        duration = format_duration(get_duration(visiter))
        non_closed_visits.append(
            {
                'who_entered': who_entered,
                'entered_at': entered_at,
                'duration': duration,
            }
        )

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
