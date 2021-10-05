from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime, timedelta


def passcard_info_view(request, passcode):
    # Программируем здесь

    def get_duration(visit):
        if visit.leaved_at:
            delta = visit.leaved_at - visit.entered_at
        else:
            delta = 0
        return timedelta(seconds=delta.seconds)

    def is_visit_long(duration, minutes=60):
        tdelta = timedelta(minutes=minutes)
        if duration > tdelta:
            return True
        return False

    def get_passcard_visits_context(query):
        this_passcard_visits = []
        for visit in query:
            entered_at = visit.entered_at
            duration = get_duration(visit)
            is_strange = is_visit_long(duration)

            this_passcard_visits.append(
                {
                    'entered_at': entered_at,
                    'duration': duration,
                    'is_strange': is_strange,
                }
            )
        return this_passcard_visits

    passcard = Passcard.objects.get(passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard.id)

    context = {
        'passcard': passcard,
        'this_passcard_visits': get_passcard_visits_context(visits)
    }
    return render(request, 'passcard_info.html', context)

# this_passcard_visits = [
    #     {
    #         'entered_at': '11-04-2018',
    #         'duration': '25:03',
    #         'is_strange': False
    #     },
    # ]
