import unittest

from task_main import Car


class TestCar(unittest.TestCase):
    def test_init(self):
        car = Car()
        self.assertEqual(car.wheel_angle, 0)
        self.assertEqual(car.speed, 50)
        self.assertTrue(car.if_engine_work)

    def test_decrease_speed(self):
        car = Car()
        car.decrease_speed(5)
        self.assertEqual(car.speed, 40)

    def test_turn_wheel(self):
        car = Car()
        car.turn_wheel(10, 5)
        self.assertEqual(car.wheel_angle, 50)

    def test_optimize_parameter(self):
        car = Car()
        car.optimize_parameter()
        self.assertEqual(car.speed, 50)
        self.assertEqual(car.wheel_angle, 0)

    def test_stop_car(self):
        car = Car()
        car.stop_car()
        self.assertEqual(car.speed, 0)
        self.assertFalse(car.if_engine_work)


if __name__ == '__main__':
    unittest.main()
