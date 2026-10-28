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
        half_width = boy.FRAME_WIDTH * self.SCALE / 2
        left_edge = half_width
        right_edge = boy.canvas_width - half_width
        if boy.x >= right_edge:
            boy.x = right_edge
            boy.face_dir = -1
        elif boy.x <= left_edge:
            boy.x = left_edge
            boy.face_dir = 1

    def animate(self, boy, now):
        if now - self.last_frame_time >= self.FRAME_DURATION:
            boy.frame = (boy.frame + 1) % 8
            self.last_frame_time = now

    def draw(self, boy):
        run_row = 100 if boy.face_dir == 1 else 0
        size = boy.FRAME_WIDTH * self.SCALE
        # Keep the sprite's feet near the same grass line after scaling.
        draw_y = boy.y + 15
        boy.image.clip_draw(
            boy.frame * boy.FRAME_WIDTH, run_row,
            boy.FRAME_WIDTH, boy.FRAME_WIDTH,
            boy.x, draw_y, size, size,
        )

    def expired(self, now):
        return now - self.started_at >= self.DURATION
