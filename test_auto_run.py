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
        self.assertFalse(self.boy.is_invincible)
        self.boy.press_auto_run()
        self.assertEqual(self.boy.state, 'AUTORUN')
        self.assertTrue(self.boy.is_invincible)
        self.clock.advance(0.1)
        self.boy.update()
        self.assertAlmostEqual(self.boy.x, 445)
        self.boy.draw()
        self.assertEqual(self.image.draw_calls[-1][-3], 105)
        self.assertEqual(self.image.draw_calls[-1][-2:], (150, 150))

    def test_auto_run_turns_at_both_screen_edges(self):
        self.boy.press_auto_run()
        self.boy.x = 720
        self.clock.advance(0.1)
        self.boy.update()
        self.assertEqual((self.boy.x, self.boy.face_dir), (725, -1))

        self.boy.x = 80
        self.clock.advance(0.1)
        self.boy.update()
        self.assertEqual((self.boy.x, self.boy.face_dir), (75, 1))

    def test_auto_run_returns_to_idle_after_five_seconds(self):
        self.boy.press_auto_run()
        self.clock.advance(4.99)
        self.boy.update()
        self.assertEqual(self.boy.state, 'AUTORUN')

        self.clock.advance(0.01)
        self.boy.update()
        self.assertEqual(self.boy.state, 'IDLE')
        self.assertFalse(self.boy.is_invincible)
        self.assertEqual(self.boy.idle_started_at, self.clock.now)
        self.boy.draw()
        self.assertEqual(len(self.image.draw_calls[-1]), 6)

    def test_direction_key_cancels_auto_run_and_uses_normal_run(self):
        self.boy.press_auto_run()
        self.boy.press_direction(-1)
        self.assertEqual((self.boy.state, self.boy.face_dir), ('RUN', -1))
        self.assertFalse(self.boy.is_invincible)

        starting_x = self.boy.x
        self.clock.advance(0.1)
        self.boy.update()
        self.assertAlmostEqual(self.boy.x, starting_x - 20)
        self.boy.draw()
        self.assertEqual(len(self.image.draw_calls[-1]), 6)

        self.boy.release_direction(-1)
        self.assertEqual(self.boy.state, 'IDLE')

    def test_a_is_ignored_outside_idle_and_does_not_reset_timer(self):
        self.boy.press_auto_run()
        started_at = self.boy.auto_run.started_at
        self.clock.advance(2)
        self.boy.press_auto_run()
        self.assertEqual(self.boy.auto_run.started_at, started_at)

        self.boy.press_direction(1)
        self.boy.press_auto_run()
        self.assertEqual(self.boy.state, 'RUN')

        self.boy.release_direction(1)
        self.clock.advance(5)
        self.boy.update()
        self.assertEqual(self.boy.state, 'SLEEP')
        self.boy.press_auto_run()
        self.assertEqual(self.boy.state, 'SLEEP')
        self.boy.wake_up()
        self.assertEqual(self.boy.state, 'IDLE')


if __name__ == '__main__':
    unittest.main()
