from __future__ import annotations

from typing import Optional

from enum import Enum

from aocd import get_data


class PulseState(Enum):
    LOW = 0
    HIGH = 1


class DeviceType(Enum):
    BROADCASTER = 0
    FLIP_FLOP = 1
    CONJUNCTION = 2
    NOP = 3


class Device:
    def __init__(self, name: str, device_type: DeviceType) -> None:
        self.name = name
        self.device_type = device_type
        self.pulse_state = PulseState.LOW

        self.prev_state: Optional[PulseState] = None
        self.sources: list[Device] = []
        self.targets: list[Device] = []

    def pulse(self, pulse_state: PulseState) -> list[tuple[Device, PulseState]]:
        # Update previous state
        self.prev_state = pulse_state

        # Handle pulse transitions
        if self.device_type == DeviceType.FLIP_FLOP and pulse_state == PulseState.LOW:
            # Update pulse if input pulse is low
            self.pulse_state = (
                PulseState.LOW
                if self.pulse_state == PulseState.HIGH
                else PulseState.HIGH
            )
        elif self.device_type == DeviceType.CONJUNCTION:
            self.pulse_state = (
                PulseState.LOW
                if all(source.pulse_state == PulseState.HIGH for source in self.sources)
                else PulseState.HIGH
            )

        # Apply pulse transitions to target devices
        return [(target, self.pulse_state) for target in self.targets]


data = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""
data = get_data(year=2023, day=20)

devices: dict[str, Device] = {}
for row in data.split("\n"):
    label, _ = row.split(" -> ")
    if label[0] == "%":
        devices[label[1:]] = Device(label[1:], DeviceType.FLIP_FLOP)
    elif label[0] == "&":
        devices[label[1:]] = Device(label[1:], DeviceType.CONJUNCTION)
    else:
        devices[label] = Device(label, DeviceType.BROADCASTER)

for row in data.split("\n"):
    label, targets = row.split(" -> ")
    label = label.strip("&%")
    targets = targets.split(", ")

    target_devices = []
    for t in targets:
        if t in devices:
            # Get target devices
            target_device = devices[t]

            # Register sources for all devices
            target_device.sources.append(devices[label])

            # Append to list
            target_devices.append(target_device)
        else:
            devices[t] = Device(t, DeviceType.NOP)
            target_devices.append(devices[t])

    # Register target devices
    devices[label].targets = target_devices

# Perform series of 1000 pulses
cnt: dict[PulseState, int] = {PulseState.LOW: 0, PulseState.HIGH: 0}
for i in range(1000):
    evaluate: list[tuple[Device, PulseState]] = [(devices["broadcaster"], PulseState.LOW)]
    cnt[PulseState.LOW] += 1

    while len(evaluate):
        # Keep track of to-be-evaluated devices
        evaluate_new: list[tuple[Device, PulseState]] = []

        for device, pulse_state in evaluate:
            # Perform pulse and add to evaluation for next loop
            evaluate_new.extend(device.pulse(pulse_state))

            # Summarize statistics
            cnt[device.pulse_state] += len(device.targets)

        # Assign new evaluations
        evaluate = evaluate_new

# Print answer to part 1
print(cnt[PulseState.LOW] * cnt[PulseState.HIGH])

# Part 2
# for device in devices.values():
#     device.state = PulseState.LOW

# rx = devices["rx"]
# assert isinstance(rx, Nop)

# cnt = 0
# while rx.last_received != PulseState.LOW:
#     evaluate: list[Device] = [devices["broadcaster"]]
#     cnt += 1

#     while len(evaluate):
#         # Keep track of to-be-evaluated devices
#         evaluate_new: list[Device] = []

#         for device in evaluate:
#             # Perform pulse and add to evaluation for next loop
#             evaluate_new += device.pulse()

#         # Assign new evaluations
#         evaluate = evaluate_new

# print(cnt)


# from __future__ import annotations

# from abc import ABC, abstractmethod
# from enum import Enum

# from aocd import get_data


# class PulseState(Enum):
#     LOW = 0
#     HIGH = 1


# class Device(ABC):
#     def __init__(self, name: str):
#         self.name: str = name
#         self.state: PulseState = PulseState.LOW
#         self.targets: list[Device] = []

#     @abstractmethod
#     def pulse(self) -> list[Device]:
#         pass


# class Broadcaster(Device):
#     def __init__(self, name: str):
#         super().__init__(name)

#     def pulse(self) -> list[Device]:
#         nxt = []
#         for t in self.targets:
#             if isinstance(t, FlipFlop) and self.state == PulseState.LOW:
#                 t.state = (
#                     PulseState.LOW if t.state == PulseState.HIGH else PulseState.HIGH
#                 )
#                 nxt.append(t)
#             elif isinstance(t, Conjunction):
#                 t.update_state()
#                 nxt.append(t)
#             elif isinstance(t, Nop):
#                 t.last_received = self.state
#         return nxt


# class Nop(Device):
#     def __init__(self, name: str):
#         super().__init__(name)
#         self.last_received = None

#     def pulse(self) -> list[Device]:
#         return []


# class FlipFlop(Device):
#     def __init__(self, name: str):
#         super().__init__(name)

#     def pulse(self) -> list[Device]:
#         nxt = []
#         for t in self.targets:
#             if isinstance(t, FlipFlop) and self.state == PulseState.LOW:
#                 t.state = (
#                     PulseState.LOW if t.state == PulseState.HIGH else PulseState.HIGH
#                 )
#                 nxt.append(t)
#             elif isinstance(t, Conjunction):
#                 t.update_state()
#                 nxt.append(t)
#             elif isinstance(t, Nop):
#                 t.last_received = self.state
#         return nxt


# class Conjunction(Device):
#     def __init__(self, name: str):
#         super().__init__(name)
#         self.sources: list[Device] = []

#     def update_state(self):
#         self.state = (
#             PulseState.LOW
#             if all(s.state == PulseState.HIGH for s in self.sources)
#             else PulseState.HIGH
#         )

#     def pulse(self) -> list[Device]:
#         nxt = []
#         for t in self.targets:
#             if isinstance(t, FlipFlop) and self.state == PulseState.LOW:
#                 t.state = (
#                     PulseState.LOW if t.state == PulseState.HIGH else PulseState.HIGH
#                 )
#                 nxt.append(t)
#             elif isinstance(t, Conjunction):
#                 t.update_state()
#                 nxt.append(t)
#             elif isinstance(t, Nop):
#                 t.last_received = self.state
#         return nxt


# data = """broadcaster -> a, b, c
# %a -> b
# %b -> c
# %c -> inv
# &inv -> a"""
# data = get_data(year=2023, day=20)

# devices: dict[str, Device] = {}
# for row in data.split("\n"):
#     label, _ = row.split(" -> ")
#     if label[0] == "%":
#         devices[label[1:]] = FlipFlop(label[1:])
#     elif label[0] == "&":
#         devices[label[1:]] = Conjunction(label[1:])
#     else:
#         devices[label] = Broadcaster(label)

# for row in data.split("\n"):
#     label, targets = row.split(" -> ")
#     label = label.strip("&%")
#     targets = targets.split(", ")

#     target_devices = []
#     for t in targets:
#         if t in devices:
#             # Get target devices
#             target_device = devices[t]

#             # Register sources for all conjunction devices
#             if isinstance(target_device, Conjunction):
#                 target_device.sources.append(devices[label])

#             # Append to list
#             target_devices.append(target_device)
#         else:
#             devices[t] = Nop(t)
#             target_devices.append(devices[t])

#     # Register target devices
#     devices[label].targets = target_devices

# # Perform series of 1000 pulses
# cnt: dict[PulseState, int] = {PulseState.LOW: 0, PulseState.HIGH: 0}
# for i in range(1000):
#     evaluate: list[Device] = [devices["broadcaster"]]
#     cnt[PulseState.LOW] += 1

#     while len(evaluate):
#         # Keep track of to-be-evaluated devices
#         evaluate_new: list[Device] = []

#         for device in evaluate:
#             # Perform pulse and add to evaluation for next loop
#             evaluate_new += device.pulse()

#             # Summarize statistics
#             cnt[device.state] += len(device.targets)

#         # Assign new evaluations
#         evaluate = evaluate_new

# # Print answer to part 1
# print(cnt[PulseState.LOW] * cnt[PulseState.HIGH])

# # Part 2
# for device in devices.values():
#     device.state = PulseState.LOW

# rx = devices['rx']
# assert isinstance(rx, Nop)

# cnt = 0
# while rx.last_received != PulseState.LOW:
#     evaluate: list[Device] = [devices["broadcaster"]]
#     cnt += 1

#     while len(evaluate):
#         # Keep track of to-be-evaluated devices
#         evaluate_new: list[Device] = []

#         for device in evaluate:
#             # Perform pulse and add to evaluation for next loop
#             evaluate_new += device.pulse()

#         # Assign new evaluations
#         evaluate = evaluate_new

# print(cnt)
