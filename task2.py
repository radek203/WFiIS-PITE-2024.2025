import logging
import random
import time
from enum import Enum
from multiprocessing import Process


def random_element_with_gaussian(arr):
    elements_count = len(arr)
    random_index = int(random.gauss(elements_count / 2, elements_count / 2))
    random_index = max(0, min(elements_count - 1, random_index))
    return arr[random_index]


class ActionType(Enum):
    SPEED_UP = 0
    SPEED_DOWN = 1
    TURN_LEFT = 2
    TURN_RIGHT = 3
    REFUEL = 4


class Action:

    def __init__(self, action_type, duration):
        self.action_type = action_type
        self.duration = duration


class EnvironmentType(Enum):
    ROAD = 0
    OFF_ROAD = 1
    HIGHWAY = 2
    CITY = 3
    CITY_SNOW = 4


class Environment:

    def __init__(self, environment_type):
        self.environment_type = environment_type

    def generate_action(self):
        while True:
            action_type = random_element_with_gaussian(list(ActionType))
            duration = random.gauss(6, 5)
            duration = max(1, min(10, int(duration)))
            yield Action(action_type, duration)

    def get_fuel_factor(self):
        factors = [1, 2, 0.5, 1.5, 2]
        return factors[self.environment_type.value]

    def get_speed_factor(self):
        factors = [1, 0.5, 1.5, 1, 0.5]
        return factors[self.environment_type.value] * self.get_time_modifier() * self.get_road_quality()

    def get_road_quality(self):
        qualities = ["good", "fair", "poor"]
        quality = random_element_with_gaussian(qualities)
        if quality == "good":
            if self.environment_type == EnvironmentType.HIGHWAY:
                return 2
            if self.environment_type == EnvironmentType.CITY_SNOW:
                return 0.5
            return 1.5
        elif quality == "fair":
            return 1
        else:
            return 0.5

    def get_time_modifier(self):
        times = ["Morning", "Midday", "Afternoon", "Night"]
        day_time = random_element_with_gaussian(times)
        if day_time == "Morning":
            return 0.7
        elif day_time == "Midday":
            return 1.2
        elif day_time == "Afternoon":
            return 0.8
        else:
            if self.environment_type == EnvironmentType.CITY_SNOW:
                return 0.5
            return 1.4


class Car:

    def __init__(self, name):
        self.environment = None
        self.name = name
        self.speed = 0
        self.wheel_angle = 0
        self.fuel = 0
        self.events = []

    def set_environment(self, environment):
        self.environment = environment

    def event_listener(self, event):
        self.events.append(event)

    def event_processor(self):
        events = [self.speed_up, self.speed_down, self.turn_left, self.turn_right, self.refuel]
        for event in self.events:
            for _ in range(event.duration):
                events[event.action_type.value]()

    def speed_up(self):
        self.speed += 15 * self.environment.get_speed_factor()
        self.speed = min(500, self.speed)
        self.fuel -= 5 * self.environment.get_fuel_factor()
        self.fuel = max(0, self.fuel)
        self.wheel_angle = 0

    def speed_down(self):
        self.speed -= 6 * self.environment.get_speed_factor()
        self.speed = max(0, self.speed)

    def turn_left(self):
        self.speed_down()
        self.wheel_angle -= 20

    def turn_right(self):
        self.speed_down()
        self.wheel_angle += 20

    def refuel(self):
        self.fuel += 10
        self.fuel = min(150, self.fuel)

    def __str__(self):
        return f"Car: {self.name} speed: {self.speed}, Steering wheel angle: {self.wheel_angle}, Fuel: {self.fuel}"


if __name__ == '__main__':
    logging.basicConfig(filename="task.log", filemode="w", format="%(asctime)s %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


    def run_car(some_car, environment_type):
        env = Environment(environment_type)
        some_car.set_environment(env)
        action_generator = env.generate_action()

        while True:
            action = next(action_generator)
            some_car.event_listener(action)
            time.sleep(1)
            some_car.event_processor()
            logger.info(some_car)


    def create_and_run(car_name, environment_type):
        car = Car(car_name)
        p = Process(target=run_car, args=(car, environment_type))
        p.daemon = True
        p.start()


    create_and_run("Ferrari", EnvironmentType.ROAD)
    create_and_run("Lamborghini", EnvironmentType.OFF_ROAD)
    create_and_run("Bugatti", EnvironmentType.HIGHWAY)
    create_and_run("Audi", EnvironmentType.CITY)
    create_and_run("BMW", EnvironmentType.CITY_SNOW)

    input("Press any key to stop cars")
    print("STOPPED")
