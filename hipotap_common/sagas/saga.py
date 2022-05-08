class Saga:
    def __init__(self, name):
        self.name = name
        self.steps = []

    def add_step(self, step: callable, roblack: callable):
        self.steps.append((step, roblack))

    def run(self):

        rollback_step = None

        for i, (step, rollback) in enumerate(self.steps):
            print(f"Saga {self.name}: running step {i+1}.")
            if not step():
                print(f"Saga {self.name} failed at step {i+1}")
                rollback_step = i
                break

        if rollback_step is not None:
            for i in reversed(range(rollback_step + 1)):
                # execute rollback step
                print(f"Saga {self.name}: running rollback step {i+1}.")
                if not self.steps[i][1]():
                    raise Exception(f"Saga {self.name} failed at rollback step {i+1}")
            return False

        return True
