from transitions import State


class AutoRun(State):
    """State object for the boy's automatic run."""

    def __init__(self):
        super().__init__('AUTORUN')
