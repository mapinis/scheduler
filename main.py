from scheduler import scheduler, Person, ttm, mtt

DATA = [
    Person("Mark", ttm(10, 30), 30, 20),
    Person("Jesse", ttm(10, 30), 30, 15),
    Person("Andrew", ttm(10, 30), 20, 20),
    Person("Olivia", ttm(10, 30), 10, 20)
]

for event in sorted(scheduler(DATA), key=lambda e: e.start):
    print(f'{event.name}: {mtt(event.start)} -> {mtt(event.done)}')