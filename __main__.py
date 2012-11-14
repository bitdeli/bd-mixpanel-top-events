from bitdeli import Profiles, Description, Title
from collections import Counter
from datetime import datetime

TOP_N = 3
text = {}

def stats(profiles):
    events = {}
    for profile in profiles:
        for event, hourly in profile['events'].iteritems():
            counter = events.get(event)
            if counter == None:
                events[event] = counter = Counter()
            for hour, freq in hourly:
                counter[hour] += freq
    total = 0
    for event, counter in events.iteritems():
        esum = sum(counter.itervalues())
        total += esum
        yield esum, counter, event
    text['total'] = total

def top_events(profiles):
    top = list(sorted(stats(profiles), reverse=True))[:TOP_N]
    for i, (total, counter, event) in enumerate(top):
        text['top%d' % i] = event.capitalize()
        data = [(datetime.utcfromtimestamp(hour * 3600).isoformat(), freq)
                for hour, freq in sorted(counter.iteritems())]
        yield {'type': 'line',
               'label': event.capitalize(),
               'size': (10, 2),
               'data': data}
        yield {'type': 'text',
               'size': (2, 1),
               'label': 'total',
               'color': 2,
               'data': {'head': total}}

Profiles().map(top_events).show()

Title('{total:,} events aggregated', text)
Description("""
The top three events are {top0}, {top1} and {top2}.
""", text)
