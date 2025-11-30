import random
import math
from mesa.discrete_space import CellAgent, FixedAgent
from helper import cell_dist


class Animal(CellAgent):
    """Base animal class."""

    def __init__(self, model, energy=20, cell=None):
        """Initialize an animal.

        Args:
            model: Model instance
            energy: Starting amount of energy
            cell: Cell in which the animal starts
        """
        super().__init__(model)
        self.energy = energy
        self.cell = cell

    def move(self):
        """Abstract method to be implemented in subclasses"""
    
    def feed(self):
        """Abstract method to be implemented in subclasses"""
    
    def step(self):
        """Execute one step of the animal's behavior."""
        # Execute eat
        self.feed()

        # Execute movement pattern
        self.move()


        # Handle death and reproduction
        if self.energy < 0:
            self.remove()


class Rabbit(Animal):
    """A prey agent with basic behaviors."""

    def move(self):
        """Move."""
        possible_cells = self.cell.get_neighborhood()
        self.cell = possible_cells.select_random_cell()



class Fox(Animal):
    """A predator agent."""
    
    def feed(self):
        """Feeding/hunting behavior for predator."""
        rabbits = [obj for obj in self.cell.agents if isinstance(obj, Rabbit)]
        if rabbits:
            # pick a random rabbit and kill it. give the fox 3 energy
            to_be_eaten = self.random.choice(rabbits)
            to_be_eaten.remove()
            self.energy += 10 #TODO make this a hyperparameter


    def move(self):
        """Move behaviour."""
        # collect all cells n away (inclusive) where there is a rabbit
        prey_cells = self.cell.get_neighborhood(radius=5, include_center=True).select(
            lambda cell: any(isinstance(obj, Rabbit) for obj in cell.agents))

        if len(prey_cells) == 0: # if no nearby prey, make a random move (including staying still)
            old_cell = self.cell
            self.cell = self.cell.get_neighborhood(include_center=True).select_random_cell()
            # print("Mark 2")
            if old_cell != self.cell: # if moved cells reduce energy by 1
                self.energy -= 1
                print("Fox Moved!")
        else: # try to move to the closest rabbit
            # Determine the closest prey's location
            closest_prey = math.inf
            closest_prey_coords = None
            for cell in prey_cells:
                dist = cell_dist(self.cell, cell)
                if dist < closest_prey:
                    closest_prey = dist
                    closest_prey_coords = cell.coordinate

            dx = closest_prey_coords[0] - self.cell.coordinate[0]
            dy = closest_prey_coords[1] - self.cell.coordinate[1]
            print(f"dx: {dx},  dy: {dy}")

             # normalization
            if abs(dx) > abs(dy):
                step_x = 0
                step_y = (dy > 0) - (0 > dy)
            else:
                step_x = (dx > 0) - (0 > dx)
                step_y = 0
            # step_x = (dx > 0) - (0 > dx)
            # step_y = (dy > 0) - (0 > dy)
            if step_x + step_y != 0:
                self.move_relative((step_x, step_y))


            # if move_x == 0 and move_y == 0:
            #     # do nothing
            #     pass
            # elif move_x == 0:
            #     self.cell.coordinate = [self.cell.coordinate[0], (self.cell.coordinate[1] + int(math.copysign(1, move_y))) % self.model.grid.height]
            # elif move_y == 0:
            #     self.cell.coordinate = [(self.cell.coordinate[0] + int(math.copysign(1, move_x))) % self.model.grid.width, self.cell.coordinate[1]]
            # elif abs(move_x) < abs(move_y): # shorter x dist
            #     self.cell.coordinate = [(self.cell.coordinate[0] + int(math.copysign(1, move_x))) % self.model.grid.width, self.cell.coordinate[1]]
            # else: # shorter y dist
            #     self.cell.coordinate = [self.cell.coordinate[0], (self.cell.coordinate[1] + int(math.copysign(1, move_y))) % self.model.grid.height]
            
            

        
# class BerryBush(FixedAgent):
#     """A stationary food agent for prey."""

