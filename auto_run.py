from transitions import State


class AutoRun(State):
    """State object for the boy's automatic run."""

    SPEED = 300
    SCALE = 1.5
    DURATION = 5.0
    FRAME_DURATION = 0.08

    def __init__(self):
        super().__init__('AUTORUN')
        self.started_at = None
        self.last_frame_time = None

    def begin(self, boy, now):
        self.started_at = now
        self.last_frame_time = now
        boy.frame = 0
        boy.last_update_time = now

    def move(self, boy, elapsed):
        boy.x += boy.face_dir * self.SPEED * elapsed
