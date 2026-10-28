import math
import time

from pico2d import get_canvas_width, load_image
from transitions import Machine

class Boy:
    IDLE_FRAME_DURATION = 0.1
    RUN_FRAME_DURATION = 0.08
    RUN_SPEED = 200
    SLEEP_AFTER = 5.0
    FRAME_WIDTH = 100

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.idle_started_at = time.monotonic()
        self.last_frame_time = self.idle_started_at
        self.last_update_time = self.idle_started_at
        self.face_dir = 1
        self.held_directions = set()
        self.canvas_width = get_canvas_width()
        self.image = load_image('animation_sheet.png')
        self.machine = Machine(
            model=self,
            states=['IDLE', 'RUN', 'SLEEP'],
            transitions=[
                {'trigger': 'fall_asleep', 'source': 'IDLE', 'dest': 'SLEEP', 'after': 'begin_sleep'},
                {'trigger': 'wake_up', 'source': 'SLEEP', 'dest': 'IDLE', 'after': 'begin_idle'},
                {'trigger': 'start_running', 'source': ['IDLE', 'SLEEP'], 'dest': 'RUN', 'after': 'begin_run'},
                {'trigger': 'stop_running', 'source': 'RUN', 'dest': 'IDLE', 'after': 'begin_idle'},
            ],
            initial='IDLE',
            auto_transitions=False,
        )

    def begin_sleep(self):
        self.frame = 0

    def begin_idle(self):
        self.frame = 0
        self.idle_started_at = time.monotonic()
        self.last_frame_time = self.idle_started_at
        self.last_update_time = self.idle_started_at

    def begin_run(self):
        self.frame = 0
        self.last_frame_time = time.monotonic()
        self.last_update_time = self.last_frame_time

    def press_direction(self, direction):
        if direction in self.held_directions:
            return
        self.held_directions.add(direction)
        self.face_dir = direction
        if self.state in ('IDLE', 'SLEEP'):
            self.start_running()

    def release_direction(self, direction):
        self.held_directions.discard(direction)
        if self.state == 'RUN':
            if self.held_directions:
                self.face_dir = next(iter(self.held_directions))
            else:
                self.stop_running()

    def update(self):
        now = time.monotonic()
        elapsed = now - self.last_update_time
        self.last_update_time = now
        if self.state == 'IDLE':
            if now - self.idle_started_at >= self.SLEEP_AFTER:
                self.fall_asleep()
            elif now - self.last_frame_time >= self.IDLE_FRAME_DURATION:
                self.frame = (self.frame + 1) % 8
                self.last_frame_time = now
        elif self.state == 'RUN':
            self.x += self.face_dir * self.RUN_SPEED * elapsed
            self.x = max(self.FRAME_WIDTH / 2, min(self.canvas_width - self.FRAME_WIDTH / 2, self.x))
            if now - self.last_frame_time >= self.RUN_FRAME_DURATION:
                self.frame = (self.frame + 1) % 8
                self.last_frame_time = now

    def draw(self):
        idle_row = 300 if self.face_dir == 1 else 200
        if self.state == 'IDLE':
            self.image.clip_draw(self.frame * 100, idle_row, 100, 100, self.x, self.y)
        elif self.state == 'RUN':
            run_row = 100 if self.face_dir == 1 else 0
            self.image.clip_draw(self.frame * 100, run_row, 100, 100, self.x, self.y)
        elif self.state == 'SLEEP':
            # Head on the left and face upward, regardless of the standing direction.
            self.image.clip_composite_draw(
                0, 300, 100, 100, math.pi / 2, '', self.x, self.y - 13, 100, 100
            )
