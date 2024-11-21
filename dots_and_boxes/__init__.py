from gym import register


register(
    id='dots_and_boxes/DotsAndBoxes-v0',
    entry_point='dots_and_boxes.envs:DotsAndBoxes',
    max_episode_steps=300,
)