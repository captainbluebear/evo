from agent import Rabbit, Fox
from model import Environment
from mesa.experimental.devs import ABMSimulator
from mesa.visualization import (
    CommandConsole,
    Slider,
    SolaraViz,
    SpaceRenderer,
    make_plot_component,
)
from mesa.visualization.components import AgentPortrayalStyle


def env_portrayal(agent):
    if agent is None:
        return

    portrayal = AgentPortrayalStyle(size=20, marker="o", zorder=2)

    if isinstance(agent, Fox):
        portrayal.update(("color", "#e16b0b"))
        portrayal.update(("marker", "^"))
    elif isinstance(agent, Rabbit):
        portrayal.update(("color", "#5F5337"))

    return portrayal


model_params = {
    "seed": {"type": "InputText", "value": 42, "label": "Random Seed"},
    "initial_rabbits": Slider("Initial Rabbit Population", 50, 1, 100), #100, 10, 300
    "initial_foxes": Slider("Initial Fox Population", 5, 1, 10),
}


def post_process_space(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])


def post_process_lines(ax):
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.9))


lineplot_component = make_plot_component(
    {"Foxes": "tab:red", "Rabbits": "tab:cyan"},
    post_process=post_process_lines,
)

simulator = ABMSimulator()
model = Environment(simulator=simulator)

renderer = SpaceRenderer(
    model,
    backend="matplotlib",
)
renderer.draw_agents(env_portrayal)
renderer.post_process = post_process_space

page = SolaraViz(
    model,
    renderer,
    components=[lineplot_component, CommandConsole],
    model_params=model_params,
    name="Fox-Rabbit Predation",
    simulator=simulator,
)
page  # noqa
