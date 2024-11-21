import gymnasium
import pygame

from display import draw_board
import game 

class DotsAndBoxes(gymnasium.Env):
    metadata = {"render_modes": ["human"]}
    action_space = None
    observation_space = None
    reward_range = (-1, 1)

    screen = None
    clock = None
    running = False

    _rewards = {
        '*': 0.0, # Game not over yet
        '1/2-1/2': 0.0, # Draw
        '1-0': +1.0, # Player 1 wins
        '0-1': -1.0, # Player 2 wins
    }

    def __init__(self):
        self.game = None

    def reset(self) -> game.Board:
        self.game = game.DotsAndBoxes()
        self.screen = None
        self.clock = None
        self.running = False
        return self.game.board 
    
    def step(self, action: int):
        if action not in self.game.legal_moves:
            raise ValueError(f"Illegal line {action}")

        self.game.set_line(action)

        observation = self.game.board.copy()
        reward = self._reward()
        done = self.game.game_info.finished

        return observation, reward, done, None
        
    
    def render(self):
        if self.screen is None:
            pygame.init()
            pygame.display.set_caption('Dots & Boxes')
            self.screen = pygame.display.set_mode((400, 400))
            self.clock = pygame.time.Clock()
            self.running = True

        self.screen.fill("white")
        draw_board(self.game, self.screen)
        pygame.display.flip()
        self.clock.tick(60) 
    
    def _reward(self) -> float:
        if self.game.game_info.finished:
            p1 = self.game.game_info.get_player_one_points()
            p2 = self.game.game_info.get_player_one_points()
            if p1 == p2:
                return self._rewards['1/2-1/2']
            elif p1 > p2:
                return self._rewards['1-0']
            else:
                return self._rewards['0-1']
        return self._rewards['*']

    def close(self):
        if self.screen is not None:
            pygame.display.quit()
            pygame.quit()

        
