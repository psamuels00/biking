#!/usr/bin/env python

from dotmap import DotMap

data = dict(
    colors=dict(
        red=1,
        green=2,
        blue=3,
    ),
    shapes=dict(
        square=2,
        circle=4,
        triangle=6,
    ),
    themes=dict(
        dark=dict(
            color="red",
            shape="circle",
        ),
        light=dict(
            color="lightred",
            shape="ellipse",
        ),
    ),
)
data = DotMap(data)

assert data.colors.red == 1
assert data.shapes.circle == 4
assert data.themes.dark.color == "red"
assert data.themes.light.shape == "ellipse"
assert data.themes.dark == dict(color="red", shape="circle")
assert data.themes == dict(
    dark=dict(color="red", shape="circle"),
    light=dict(color="lightred", shape="ellipse"),
)


def update_dotmap(dotmap, key, value):
    parts = key.split(".")[1:]
    *parts, last_part = parts

    p = dotmap
    for part in parts:
        p = p[part]

    p[last_part] = value


def test_update_dotmap(data):
    update_dotmap(data, "data.themes.light.shape", "square")
    assert data.themes.light.shape == "square"

    update_dotmap(data, "data.themes.dark", dict(color="blue", shape="trapezoid"))
    assert data.themes.dark == dict(color="blue", shape="trapezoid")

    update_dotmap(data.copy(), "data.themes.light.shape", "star")
    assert data.themes.light.shape == "square"


test_update_dotmap(data)

