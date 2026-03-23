import unittest
import numpy as np

import config
import environment
import model


class HoneyCoreTests(unittest.TestCase):
    def setUp(self):
        # Keep each test isolated from prior global state.
        environment.agent_pos = [0, 0]
        environment.food_pos = [1, 1]
        environment.poison_pos = [2, 2]

    def test_reset_world_positions_are_valid(self):
        for _ in range(200):
            environment.reset_world(silent=True)
            ax, ay = environment.agent_pos
            fx, fy = environment.food_pos
            px, py = environment.poison_pos

            self.assertTrue(0 <= ax < config.GRID_SIZE)
            self.assertTrue(0 <= ay < config.GRID_SIZE)
            self.assertTrue(0 <= fx < config.GRID_SIZE)
            self.assertTrue(0 <= fy < config.GRID_SIZE)
            self.assertTrue(0 <= px < config.GRID_SIZE)
            self.assertTrue(0 <= py < config.GRID_SIZE)

            self.assertNotEqual(environment.agent_pos, environment.food_pos)
            self.assertNotEqual(environment.agent_pos, environment.poison_pos)
            self.assertNotEqual(environment.food_pos, environment.poison_pos)

    def test_get_state_shape(self):
        state = environment.get_state()
        self.assertEqual(state.shape, (1, config.STATE_SIZE))

    def test_get_state_grid_and_vision_encoding(self):
        # Place entities at deterministic positions.
        environment.agent_pos = [0, 0]
        environment.food_pos = [1, 0]
        environment.poison_pos = [0, 1]

        state = environment.get_state()[0]
        flat_grid = state[: config.GRID_SIZE * config.GRID_SIZE]
        vision = state[-4:]

        food_index = environment.food_pos[1] * config.GRID_SIZE + environment.food_pos[0]
        poison_index = environment.poison_pos[1] * config.GRID_SIZE + environment.poison_pos[0]

        self.assertEqual(flat_grid[food_index], 1)
        self.assertEqual(flat_grid[poison_index], -1)

        # Agent at top-left: north and west are out-of-bounds => -2
        self.assertEqual(vision[0], -2)
        self.assertEqual(vision[2], -2)
        # South sees poison, east sees food.
        self.assertEqual(vision[1], -1)
        self.assertEqual(vision[3], 1)

    def test_step_wall_collision(self):
        environment.agent_pos = [0, 0]
        reward, done = environment.step(2)  # left

        self.assertTrue(done)
        self.assertAlmostEqual(reward, -0.2)
        self.assertEqual(environment.agent_pos, [0, 0])

    def test_step_food_reward(self):
        environment.agent_pos = [0, 0]
        environment.food_pos = [1, 0]
        environment.poison_pos = [4, 4]

        reward, done = environment.step(3)  # right

        self.assertTrue(done)
        self.assertAlmostEqual(reward, 1.0)
        self.assertEqual(environment.agent_pos, [1, 0])

    def test_step_poison_penalty(self):
        environment.agent_pos = [0, 0]
        environment.food_pos = [4, 4]
        environment.poison_pos = [1, 0]

        reward, done = environment.step(3)  # right

        self.assertTrue(done)
        self.assertAlmostEqual(reward, -1.0)
        self.assertEqual(environment.agent_pos, [1, 0])

    def test_build_model_output_shape(self):
        model.initialize_model()
        m = model.get_model()
        test_input = np.zeros((1, config.STATE_SIZE), dtype=np.float32)
        q_values = m.predict(test_input, verbose=0)
        self.assertEqual(q_values.shape, (1, config.NUM_ACTIONS))


if __name__ == '__main__':
    unittest.main()
