import pandas as pd
import os

raw_dataset_path = os.path.join(r"c:\Users\thrix\Documents\flappy-rf", "data", "raw", "raw_dataset.csv")
clean_dataset_path = os.path.join(r"c:\Users\thrix\Documents\flappy-rf", "data", "clean", "clean_dataset.csv")

headers = ["dist_x", "dist_y", "axis_y", "vel_y", "action"]
df = pd.read_csv(raw_dataset_path, names=headers, header=0)


idle_frames = df[df["dist_x"] == 256]
action_frames = df[df["dist_x"] < 256]

idle_sampled = idle_frames.sample(frac=0.15, random_state=42)

clean_df = pd.concat([action_frames, idle_sampled]).sample(
    frac=1, random_state=42
).reset_index(drop=True)

clean_df["dist_x"]   = (clean_df["dist_x"] // 16).astype(int)  # 0 to 256 -> 0 to 16
clean_df["dist_y"]   = (clean_df["dist_y"] // 20).astype(int)  # -300 to 300 -> -15 to 15
clean_df["axis_y"]   = (clean_df["axis_y"] // 20).astype(int)       # Height buckets
clean_df["vel_y"] = (clean_df["vel_y"] // 1).astype(int)       # Integer velocities

clean_df.to_csv(clean_dataset_path, index=False) 