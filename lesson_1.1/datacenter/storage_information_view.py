from django.utils.timezone import localtime
from datacenter.models import Visit, get_duration, format_duration
from django.shortcuts import render


def storage_information_view(request):

    all_visiters_inside = Visit.objects.filter(leaved_at=None)

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
