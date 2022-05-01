class InvalidStateUpdateError(Exception):
    pass


class AppState(object):
    STARTING = "starting"
    RESUMING = "resuming"
    RUNNING = "running"
    PAUSING = "pausing"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"
