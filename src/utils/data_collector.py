from game import FlappyEnv
import csv, os

class dataColl():
    def __init__(self):
        self.colected_data = []

        self.pipe_dist_x = None
        self.action = None

    def get_state(self, flappy_env):
        bird_x = flappy_env.bird.x

        # Find active pipe ahead
        target = None
        for p in flappy_env.pillars:
            if p.x + p.image_bottom.get_width() > bird_x:
                target = p
                break

        if target:
            self.pipe_dist_x = target.x - bird_x
            self.pipe_dist_y = flappy_env.bird.y - target.passage_y
        else:
            self.pipe_dist_x = flappy_env.SCREEN_WIDTH * flappy_env.GAME_SCALE
            self.pipe_dist_y = 0

        self.action = flappy_env.bird.action
        self.vel_y = flappy_env.bird.velocity_y
        self.y = flappy_env.bird.y

        if self.action == 1 and len(self.colected_data) > 0:
            self.colected_data[-1]["action"] = 1

        return {
            "pipe_dist_x": self.pipe_dist_x,
            "pipe_dist_y": self.pipe_dist_y,
            "bird_y": self.y,
            "bird_vel": self.vel_y,
            "action": 0,
        }

    def showcase_step(self):
        print((f"Pipe distance on the X axis: {self.pipe_dist_x}\nPipe distance on the Y axis: {self.pipe_dist_y}\nBird velocity across the Y axis: {self.vel_y}\nAction: {self.action}"))

    def run(self, flappy_env):
        if not flappy_env.bird.die:
            state = self.get_state(flappy_env)
            self.colected_data.append(state)

        else:
            if len(self.colected_data) >= 60:
                del self.colected_data[-60:]  # Remove the last 60 frames of data before the bird dies
                self.save_to_csv()
                self.colected_data = []  # Clear all data after saving to CSV
            else:
                self.colected_data = []  # If there are less than 60 frames, clear all data

    def save_to_csv(self):
        with open(os.path.join(r"c:\Users\thrix\Documents\flappy-rf", "data", "raw", "dataset.csv"), 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["pipe_dist_x", "pipe_dist_y", "bird_y", "bird_vel", "action"])
            writer.writerows(self.colected_data)