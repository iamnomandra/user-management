from fastapi.routing import APIRoute


def custom_generate_unique_id(route: APIRoute) -> str:
    if(route.name != "favicon"):
        return f"{route.tags[0]}-{route.name}"
    return ""