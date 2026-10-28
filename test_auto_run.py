import unittest
from unittest.mock import patch

from boy import Boy


class FakeClock:
    def __init__(self):
        self.now = 100.0

    def monotonic(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


class FakeImage:
    def __init__(self):
        self.draw_calls = []

    def clip_draw(self, *args):
        self.draw_calls.append(args)


class AutoRunTests(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock()
        self.image = FakeImage()
        for target, replacement in (
            ('boy.time.monotonic', self.clock.monotonic),
            ('boy.get_canvas_width', lambda: 800),
            ('boy.load_image', lambda path: self.image),
        ):
            patcher = patch(target, replacement)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.boy = Boy()

    def test_idle_a_starts_real_auto_run_state_and_draws_larger(self):
        self.assertIs(self.boy.machine.get_state('AUTORUN'), self.boy.auto_run)
        self.boy.press_auto_run()
        self.assertEqual(self.boy.state, 'AUTORUN')
        self.clock.advance(0.1)
        self.boy.update()
        self.assertAlmostEqual(self.boy.x, 430)
        self.boy.draw()
        self.assertEqual(self.image.draw_calls[-1][-2:], (150, 150))


if __name__ == '__main__':
    unittest.main()
