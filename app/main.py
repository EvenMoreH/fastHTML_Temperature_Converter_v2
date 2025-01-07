from fasthtml.common import * # type: ignore
from fasthtml.common import (
    Div, Form, Input, Button, Html, Head, Body, Title, Script, Link, Meta, H2, serve,
)
import re

# for docker
app, rt = fast_app(static_path="static") # type: ignore

# for local
# app, rt = fast_app(static_path="app/static") # type: ignore


def string_cleaner(temperature: str):
    global clean_string
    characters_to_remove = " "
    replace_dictionary = {",":"."}

    clean_string = temperature.translate(str.maketrans('', '', characters_to_remove))
    for old_character, new_character in replace_dictionary.items():
        clean_string = clean_string.replace(old_character, new_character)
    return clean_string

temperature_form = Form(
    method="post",
    action="/convert"
    )(
        Div(
            H2("Temperature",
                style="font-variant-caps: petite-caps;"
            ),
            Button(
                "Reset",
                hx_get="/",
                hx_target="body",
                hx_push_url="true",
                cls="reset",
            ),
            cls="row",
            style="margin-bottom: -1vw; gap: 2vw; justify-content: space-around; max-width: 400px;",
        ),
        Input(
            id="temperature",
            name="temperature",
            type="text",
            pattern="^-?\d+(\.\d+)?$",
            title="Enter a valid floating-point number",
            required="true",
            cls="test",
        ),
        Div(cls="spacing"),
        Div(
            Button("°F → °C",
                id="fc-button",
                hx_get="/FC",
                hx_target="#ftc",
                hx_include="#temperature",
                hx_swap="outerHTML",
                type="button",
            ),
            Div(id="ftc", cls="output"),
            cls="row",
        ),
        Div(
            Button("°F → °K",
                hx_get="/FK",
                hx_target="#ftk",
                hx_include="#temperature",
                hx_swap="outerHTML",
                type="button",
            ),
            Div(id="ftk", cls="output"),
            cls="row",
        ),
        Div(
            Button("°C → °F",
                hx_get="/CF",
                hx_target="#ctf",
                hx_include="#temperature",
                hx_swap="outerHTML",
                type="button",
            ),
            Div(id="ctf", cls="output"),
            cls="row",
        ),
        Div(
            Button("°C → °K",
                hx_get="/CK",
                hx_target="#ctk",
                hx_include="#temperature",
                hx_swap="outerHTML",
                type="button",
            ),
            Div(id="ctk", cls="output"),
            cls="row",
        ),
        Div(
            Button("°K → °C",
                hx_get="/KC",
                hx_target="#ktc",
                hx_include="#temperature",
                hx_swap="outerHTML",
                type="button",
            ),
            Div(id="ktc", cls="output"),
            cls="row",
        ),
        Div(
            Button("°K → °F",
                hx_get="/KF",
                hx_target="#ktf",
                hx_include="#temperature",
                hx_swap="outerHTML",
                type="button",
            ),
            Div(id="ktf", cls="output"),
            cls="row",
        ),
        cls="container",
    )

@rt("/")
def homepage():
    return Html(
        Head(
            Title("Temperature Converter"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Script(src="https://unpkg.com/htmx.org"),
            Link(rel="stylesheet", href="styles.css"),
            Link(rel="icon", href="images/favicon.ico", type="image/x-icon"),
            Link(rel="icon", href="images/favicon.png", type="image/png"),
        ),
        Body(temperature_form)
    )

@rt("/FC")
def FC(temperature: str):
    string_cleaner(temperature)

    if temperature == "":
        return Div("Please enter a valid floating-point number.", id="ftc", cls="output", style="color: rgba(187, 25, 25, 0.8) !important;")

    if not re.match(r"^-?\d+(\.\d+)?$", clean_string):
        return Div("Invalid Input. Please enter a valid floating-point number.", id="ftc", cls="output", style="color: rgba(187, 25, 25, 0.8) !important;")

    temperature_float = float(clean_string)

    fc = (temperature_float - 32) * (5/9)
    result = f"{temperature_float}°F equals to {fc:.2f}°C"

    return Div(result, id="ftc", cls="output")

@rt("/FK")
def FK(temperature: str):
    string_cleaner(temperature)

    if temperature == "":
        return Div("Please enter a valid floating-point number.", id="ftk", cls="output", style="color: rgba(187, 25, 25, 0.8) !important;")

    if not re.match(r"^-?\d+(\.\d+)?$", temperature):
        return Div("Invalid Input. Please enter a valid floating-point number.", id="ftk", cls="output", style="color: rgba(187, 25, 25, 0.8) !important;")

    temperature_float = float(temperature)

    fk = ((temperature_float - 32) * (5/9)) + 273.15
    result = f"{temperature_float}°F equals to {fk:.2f}°K"

    return Div(result, id="ftk", cls="output")

@rt("/CF")
def CF(temperature: str):
    string_cleaner(temperature)

    if temperature == "":
        return Div("Please enter a valid floating-point number.", id="ctf", cls="output", style="color: rgba(187, 25, 25, 0.8) !important;")

    if not re.match(r"^-?\d+(\.\d+)?$", temperature):
        return Div("Invalid Input. Please enter a valid floating-point number.", id="ctf", cls="output", style="color: rgba(187, 25, 25, 0.8) !important;")

    temperature_float = float(temperature)

    cf = (temperature_float * (9/5)) + 32
    result = f"{temperature_float}°C equals to {cf:.2f}°F"

    return Div(result, id="ctf", cls="output")

@rt("/CK")
def CK(temperature: str):
    string_cleaner(temperature)

    if temperature == "":
        return Div("Please enter a valid floating-point number.", id="ctk", cls="output", style="color: rgba(187, 25, 25, 0.8) !important;")

    if not re.match(r"^-?\d+(\.\d+)?$", temperature):
        return Div("Invalid Input. Please enter a valid floating-point number.", id="ctk", cls="output", style="color: rgba(187, 25, 25, 0.8) !important;")

    temperature_float = float(temperature)

    ck = temperature_float - 273.15
    result = f"{temperature_float}°C equals to {ck:.2f}°K"

    return Div(result, id="ctk", cls="output")

@rt("/KC")
def KC(temperature: str):
    string_cleaner(temperature)

    if temperature == "":
        return Div("Please enter a valid floating-point number.", id="ktc", cls="output", style="color: rgba(187, 25, 25, 0.8) !important;")

    if not re.match(r"^-?\d+(\.\d+)?$", temperature):
        return Div("Invalid Input. Please enter a valid floating-point number.", id="ktc", cls="output", style="color: rgba(187, 25, 25, 0.8) !important;")

    temperature_float = float(temperature)

    kc = temperature_float + 273.15
    result = f"{temperature_float}°K equals to {kc:.2f}°C"

    return Div(result, id="ktc", cls="output")

@rt("/KF")
def KF(temperature: str):
    string_cleaner(temperature)

    if temperature == "":
        return Div("Please enter a valid floating-point number.", id="ktf", cls="output", style="color: rgba(187, 25, 25, 0.8) !important;")

    if not re.match(r"^-?\d+(\.\d+)?$", temperature):
        return Div("Invalid Input. Please enter a valid floating-point number.", id="ktf", cls="output", style="color: rgba(187, 25, 25, 0.8) !important;")

    temperature_float = float(temperature)

    kf = ((temperature_float - 273.15) * (9/5)) + 32
    result = f"{temperature_float}°K equals to {kf:.2f}°F"

    return Div(result, id="ktf", cls="output")


if __name__ == '__main__':
    # Important: Use host='0.0.0.0' to make the server accessible outside the container
    serve(host='0.0.0.0', port=5002) # type: ignore