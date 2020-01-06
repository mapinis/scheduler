from scheduler import scheduler, Person, ttm, mtt, optimized

DATA = [
    Person("Mark", ttm(10, 30), 30, 25),
    Person("Jesse", ttm(10, 30), 10, 15),
    Person("Andrew", ttm(10, 30), 5, 20),
    Person("Kevin", ttm(9,15), 50, 20),
    Person("Aalia", ttm(9,15), 5, 40),
    Person("Jason", ttm(9, 15), 10, 10)
]

#for event in reversed(sorted(scheduler(list(DATA)), key=lambda e: e.start)):
#    print(f'{event.name}: {mtt(event.start)} -> {mtt(event.done)}')

for event in optimized(list(DATA)):
    print(f'{event.name}: {mtt(event.start)} -> {mtt(event.done)}')