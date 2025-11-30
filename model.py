import math

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.discrete_space import OrthogonalVonNeumannGrid

from agent import Rabbit, Fox
from mesa.experimental.devs import ABMSimulator


class Environment(Model):
    """Predation Model.

    A model for simulating foxes and rabbits (predator-prey) ecosystem modelling.
    """

    description = (
        "A model for simulating fox and rabbit (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        width=50,
        height=50,
        initial_rabbits=1,
        initial_foxes=1,
        seed=None,
        simulator: ABMSimulator = None,
    ):
        """Create a new Environment model with the given parameters.

        Args:
            height: Height of the grid
            width: Width of the grid
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            seed: Random seed
            simulator: ABMSimulator instance for event scheduling
        """
        super().__init__(seed=seed)
        self.simulator = simulator
        self.simulator.setup(self)

        # Initialize model parameters
        self.height = height
        self.width = width

        # Create grid using experimental cell space
        self.grid = OrthogonalVonNeumannGrid(
            [self.height, self.width],
            torus=True,
            capacity=math.inf,
            random=self.random,
        )

        # Set up data collection
        model_reporters = {
            "Foxes": lambda m: len(m.agents_by_type[Fox]),
            "Rabbits": lambda m: len(m.agents_by_type[Rabbit]),
        }
        self.datacollector = DataCollector(model_reporters)

        # Create rabbits:
        Rabbit.create_agents(
            self,
            initial_rabbits,
            cell=self.random.choices(self.grid.all_cells.cells, k=initial_rabbits),
            # TODO implement spawning with clustering behavior?
        )
        # Create Foxes:
        Fox.create_agents(
            self,
            initial_foxes,
            cell=self.random.choices(self.grid.all_cells.cells, k=initial_foxes),
            # TODO interesting to see both clustering and territorial behavior?
        )

        # Collect initial data
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """Execute one step of the model."""
        # First activate all prey, then all predators, both in random order
        self.agents_by_type[Rabbit].shuffle_do("step")
        self.agents_by_type[Fox].shuffle_do("step")


        # Collect data
        self.datacollector.collect(self)
