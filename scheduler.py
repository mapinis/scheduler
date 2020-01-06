from collections import namedtuple

# ALL TIMES ARE IN MINUTES AFTER 6:00 AM

def mtt(minutes): # minutes to time, for printing purposes
    return f'{6 + minutes // 60}:{"0" + str(minutes % 60) if minutes % 60 < 10 else minutes % 60}'

def ttm(hour, minutes): # time to minutes
    return (hour - 6) * 60 + minutes

# Goal: Maximize possible sleep

# A Person is a data point
Person = namedtuple("Person", "name class_time ready_time buffer")
# A Candidate has a list of Events and the person added
Candidate = namedtuple("Candidate", "events added")
# An Event is the wake-up event, who and when, start time and finish time
Event = namedtuple("Event", "name start done")

# The Algorithm:
#   Start with 1 person. Choose the one that maximizes sleep (will be the the one that maximizes first_class - ready_time)
#   With each additional person, use the previous best maximizer, 
#   and place each next person either before or after the current schedule, pushing other down as needed
#   For each new list of events, generate a sleep score, and store it. 
#   After each iteration, choose the one with highest sleep score
#   Move on with this one, until data is empty. Use buffer.

# previous_best is a list of events, data is a least of people
def scheduler(data, previous_best = []):
    if len(data) == 0:
        return previous_best
    
    candidates = []
    for person in data:
        if len(previous_best) == 0:
            candidates.append(Candidate(
                [Event(
                    person.name,
                    person.class_time - person.buffer - person.ready_time,
                    person.class_time - person.buffer
                )],
                person
            ))
        else:
            candidates.append(Candidate(combine_before(person, previous_best), person))
            candidates.append(Candidate(combine_after(person, previous_best), person))

    best = max(candidates, key=lambda c: calculate_sleep(c.events))
    data.remove(best.added)

    return scheduler(data, best.events)

# Put the event before the current events
def combine_before(person, events):
    # find the earliest use of the bathroom.
    earliest = min(events, key=lambda e: e.start)

    # find how much earlier this person needs to wake up
    diff = max([person.class_time - person.buffer - earliest.start, 0])
    
    return events + [Event(
        person.name,
        person.class_time - person.buffer - person.ready_time - diff,
        person.class_time - person.buffer - diff
    )]

# Put the event after the current events
def combine_after(person, events):
    # find the latest use of the bathroom
    latest = max(events, key=lambda e: e.done)

    # find how much everyone else needs to be pushed down
    diff = max([latest.done - (person.class_time - person.buffer - person.ready_time), 0])
    
    return list(map(lambda e: Event(
        e.name,
        e.start - diff,
        e.done - diff
    ), events)) + [Event(
        person.name,
        person.class_time - person.buffer - person.ready_time,
        person.class_time - person.buffer
    )]

# give a list of events, return the total sleep achieved
def calculate_sleep(events):
    return sum(map(lambda e: e.start, events))


def optimized(data, so_far = []):
    if len(data) == 0:
        return so_far

    if len(so_far) == 0:
        best = max(data, key=lambda p: p.class_time - p.buffer - p.ready_time)
        data.remove(best)
        return optimized(data, [Event(
            best.name,
            best.class_time - best.buffer - best.ready_time,
            best.class_time - best.buffer
        )])

    latest = so_far[-1]
    best = max(data, key=lambda p: helper(p, latest))

    diff = max([best.class_time - best.buffer - latest.start, 0])
    so_far.append(Event(
        best.name,
        best.class_time - best.buffer - best.ready_time - diff,
        best.class_time - best.buffer - diff
    ))
    data.remove(best)

    return optimized(data, so_far)

# return the start time of the events if this person goes before latest
def helper(person, latest):
    diff = max([person.class_time - person.buffer - latest.start, 0])
    return person.class_time - person.buffer - person.ready_time - diff
