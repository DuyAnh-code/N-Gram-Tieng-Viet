import threading

class TaskManager:
    def __init__(self):
        self.reset()
        self.thread = None
        self.stop_event = threading.Event()

    def reset(self):
        self.status = {
            "is_running": False,
            "progress": 0,
            "total": 0,
            "message": "",
            "logs": [],
            "error": None
        }

    def start(self, target, *args, **kwargs):
        if self.status["is_running"]:
            return False
        
        self.reset()
        self.status["is_running"] = True
        self.stop_event.clear()
        
        self.thread = threading.Thread(target=self._run_wrapper, args=(target,) + args, kwargs=kwargs)
        self.thread.daemon = True
        self.thread.start()
        return True

    def _run_wrapper(self, target, *args, **kwargs):
        try:
            target(self, *args, **kwargs)
        except Exception as e:
            self.update(msg=f"Error: {str(e)}")
            self.status["error"] = str(e)
            import traceback
            traceback.print_exc()
        finally:
            self.status["is_running"] = False

    def stop(self):
        if self.status["is_running"]:
            self.stop_event.set()
            return True
        return False

    def update(self, progress=None, total=None, msg=""):
        if progress is not None:
            self.status["progress"] = progress
        if total is not None:
            self.status["total"] = total
        if msg:
            self.status["message"] = msg
            self.status["logs"].append(msg)
            # Keep only last 100 logs
            if len(self.status["logs"]) > 100:
                self.status["logs"] = self.status["logs"][-100:]

crawler_manager = TaskManager()
preprocess_manager = TaskManager()
build_manager = TaskManager()
