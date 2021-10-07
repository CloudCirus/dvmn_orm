from django.db import models
from django.utils.timezone import localtime, timedelta


def get_duration(visit):
    if visit.leaved_at:
        delta = visit.leaved_at - visit.entered_at
    else:
        delta = localtime() - visit.entered_at
    return timedelta(seconds=delta.seconds)


def format_duration(duration: timedelta):
    duration_string = str(duration)
    _list_with_time = duration_string.split(':')
    hours = _list_with_time[-3]
    minutes = _list_with_time[-2]
    if duration.days:
        return f'{duration.days}d {hours}:{minutes}'
    return f'{hours}:{minutes}'


class Passcard(models.Model):

    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved='leaved at ' +
            str(self.leaved_at) if self.leaved_at else 'not leaved'
        )
