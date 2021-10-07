from datacenter.models import Passcard
from datacenter.models import Visit, get_duration
from django.shortcuts import render
from django.utils.timezone import timedelta


def passcard_info_view(request, passcode):

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
    this_passcard_visits = get_passcard_visits_context(visits)

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
