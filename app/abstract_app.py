import displayio

from .app_state import AppState, InvalidStateUpdateError



DISPLAY = displayio.Group()

class App(object):

    def __init__(self, macropad, config):
        print("app created")
        self.macropad = macropad
        self.config = config
        self.name = "app"
        self.state = AppState.STOPPED
        self.display_group = DISPLAY

    def start(self):
        print("Start from base class ")
        if self.state is not AppState.STOPPED:
            raise InvalidStateUpdateError(f"Start called but the current app state is {self.state}")
        self.state = AppState.STARTING
        self._on_start()
        self.on_start()
        self.state = AppState.PAUSED

    def _on_start(self):
        pass

    def on_start(self):
        raise NotImplementedError("on_start not implemented")

    def resume(self):
        if self.state is not AppState.PAUSED:
            raise InvalidStateUpdateError(f"Resume called but the current app state is {self.state}")
        self.state = AppState.RESUMING
        self._on_resume()
        self.on_resume()
        self.state = AppState.RUNNING

    def _on_resume(self):
        pass

    def on_resume(self):
        raise NotImplementedError("on_resume not implemented")

    def pause(self):
        if self.state is not AppState.RUNNING:
            raise InvalidStateUpdateError(f"Pause called but the current app state is {self.state}")
        self.state = AppState.PAUSING
        self._on_pause()
        self.on_pause()
        self.state = AppState.PAUSED

    def _on_pause(self):
        self.macropad.keyboard.release_all()
        self.macropad.consumer_control.release()
        self.macropad.mouse.release_all()
        self.macropad.stop_tone()
        self.macropad.pixels.show()
        # self.macropad.display.refresh()

    def on_pause(self):
        raise NotImplementedError("on_pause not implemented")

    def loop(self):
        raise NotImplementedError("Not implemented")

    def stop(self):
        if self.state is not AppState.PAUSED:
            raise InvalidStateUpdateError(f"Stop called but the current app state is {self.state}")
        self.state = AppState.STOPPING
        self._on_stop()
        self.on_stop()
        self.state = AppState.STOPPED

    def _on_stop(self):
        pass

    def on_stop(self):
        raise NotImplementedError("on_stop not implemented.")
