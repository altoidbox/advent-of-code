import argparse
from datetime import datetime
import re

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--part2", action="store_true")

args = parser.parse_args()


class Entry(object):
    def __init__(self, time, event, guard=None):
        self.time = time
        self.event = event
        self.guard = guard


class Guard(object):
    def __init__(self, id_):
        self.id = id_
        self.sleep_times = []
        self.wake_times = []
        self.minutes_asleep = 0
        self.sleep_map = []
        self.sleepiest_minute = 0

    def calc_sleepiest_minute(self):
        max_minute = 0
        for m, v in enumerate(self.sleep_map):
            if v > self.sleep_map[max_minute]:
                max_minute = m
        self.sleepiest_minute = max_minute

    def analyze(self):
        self.minutes_asleep = 0
        self.sleep_map = [0] * 60
        for start, end in map(lambda *args: tuple(args), self.sleep_times, self.wake_times):
            assert(start.hour == end.hour)
            assert(start.day == end.day)
            assert(start.minute < end.minute)
            self.minutes_asleep += end.minute - start.minute
            for m in range(start.minute, end.minute):
                self.sleep_map[m] += 1
        self.calc_sleepiest_minute()


def read_input(path):
    events = []
    with open(path, "r") as f:
        for line in f:
            #[1518-11-01 00:00] Guard #10 begins shift
            match = re.match(r'\[(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<minutes>\d+)\]',
                             line.strip())
            time = datetime(*map(int, match.groups()))
            guard = None
            match = re.match(r'\[.*\] Guard #(\d+) begins shift', line)
            if match is not None:
                guard = int(match.group(1))
                event = 'begin'
            elif 'wakes up' in line:
                event = 'wake'
            elif 'falls asleep' in line:
                event = 'sleep'
            else:
                raise Exception("Unknown event for {}".format(line))
            events.append(Entry(time, event, guard))
    events.sort(key=lambda e: e.time)
    guards = {}
    guard = None
    for e in events:
        if e.guard is not None:
            guard = guards.setdefault(e.guard, Guard(e.guard))
        else:
            if e.event is 'wake':
                guard.wake_times.append(e.time)
                assert(len(guard.wake_times) == len(guard.sleep_times))
            elif e.event is 'sleep':
                assert (len(guard.wake_times) == len(guard.sleep_times))
                guard.sleep_times.append(e.time)
    return guards, events


def part1(args):
    guards, events = read_input(args.input)
    for g in guards.values():
        g.analyze()

    sleepy = sorted(guards.values(), key=lambda g: g.minutes_asleep)[-1]

    print("Guard {} sleep {}, most at {}: {}".format(sleepy.id, sleepy.minutes_asleep, sleepy.sleepiest_minute,
                                                     sleepy.id * sleepy.sleepiest_minute))


def part2(args):
    guards, events = read_input(args.input)
    for g in guards.values():
        g.analyze()

    sleepy = sorted(guards.values(), key=lambda g: g.sleep_map[g.sleepiest_minute])[-1]

    print("Guard {} most at {}: {}".format(sleepy.id, sleepy.sleepiest_minute,
                                           sleepy.id * sleepy.sleepiest_minute))



if args.part2:
    part2(args)
else:
    part1(args)
