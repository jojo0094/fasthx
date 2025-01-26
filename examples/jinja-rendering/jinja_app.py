import os

from fastapi import FastAPI, Response
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from fasthx import Jinja


# Pydantic model of the data the example API is using.
class User(BaseModel):
    first_name: str
    last_name: str


basedir = os.path.abspath(os.path.dirname(__file__))

# Create the app instance.
app = FastAPI()

# Create a FastAPI Jinja2Templates instance. This will be used in FastHX Jinja instance.
templates = Jinja2Templates(directory=os.path.join(basedir, "templates"))

# FastHX Jinja instance is initialized with the Jinja2Templates instance.
jinja = Jinja(templates)


@app.get("/user-list")
@jinja.hx("user-list.html")  # Render the response with the user-list.html template.
def htmx_or_data(response: Response) -> dict:
    response.headers["my-response-header"] = "works"
    return {
        "users": (
            User(first_name="Peter", last_name="Volfxxxxx"),
            User(first_name="Hasan", last_name="Tasan"),
        ),
        "extra_info": "This is extra context data!"
    }
# def htmx_or_data(response: Response) -> tuple[User, ...]:
#     """This route can serve both JSON and HTML, depending on if the request is an HTMX request or not."""
#     response.headers["my-response-header"] = "works"
#     return (
#         User(first_name="Peter", last_name="Volf"),
#         User(first_name="Hasan", last_name="Tasan"),
#     )


@app.get("/admin-list")
@jinja.hx("user-list.html", no_data=True)  # Render the response with the user-list.html template.
def htmx_only() -> list[User]:
    """This route can only serve HTML, because the no_data parameter is set to True."""
    return [User(first_name="John", last_name="Doe")]

# Example data (you can replace this with actual data source)
countries_and_cities = {
    "USA": ["New York", "Los Angeles", "Chicago"],
    "Canada": ["Toronto", "Vancouver", "Montreal"],
    "Germany": ["Berlin", "Munich", "Frankfurt"]
}
@app.get("/get-countries")
@jinja.hx("dropdown.html")  # Render the response with the countries.html template
def get_countries(response: Response) -> dict:
    response.headers["my-response-header"] = "works"
    countries = list(countries_and_cities.keys())
    return {"countries": countries}

@app.get("/get-cities") # dont need to pass param as it is dynamically passed using hx-param# update commit message
@jinja.hx("cities.html")  # Render the response with the cities.html template
def get_cities(response: Response, country: str) -> dict:
    response.headers["my-response-header"] = "works"
    if country:
        cities = countries_and_cities.get(country, [])
        return {"cities": cities, "selected_country": country}
    else:
        return {"cities": [], "selected_country": "No country selected"}

@app.get("/")
@jinja.page("index.html")
def index() -> None:
    """This route serves the index.html template."""
    ...


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)


