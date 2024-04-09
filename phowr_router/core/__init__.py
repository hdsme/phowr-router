import os
import re
from fastapi import APIRouter
import importlib
METHODS = ["get", "post", "put", "delete"]


class DynamicRouter(APIRouter):
    def __init__(
        self,
        base: str = "apps",
        file: str = 'api.py',
        *args,
        **kwargs,
    ):
        self._base = base
        self._file = file
        super().__init__(*args, **kwargs)
        self.build_router()

    def build_router(self):
        file_list = []
        for root, dirs, files in os.walk(os.path.join(os.getcwd(), self.base)):
            for file in files:
                if re.match(f'{self._file}$', str(file)):
                    _file = os.path.join(root, file)
                    _file_router = re.sub('.py', '', str(_file))
                    file_list.append(os.path.join(root, file))
                    route_file = importlib.import_module(
                        os.path.relpath(root).replace("/", ".").replace('\\', '.') + "." + re.sub('.py', '', str(file))
                    )
                    find_routes = [r for r in dir(route_file) if r in METHODS]
                    if find_routes:
                        if os.path.basename(root) == self.base:
                            tags = ["default"]
                        else:
                            tags = [re.sub("[\/]api$", "", str(os.path.relpath(_file_router, self.base)).replace("\\", "/"))]
                        
                        # Replace \\ in window
                        uri = str(os.path.relpath(_file_router, self.base)).replace("\\", "/")
                        uri = re.sub("[\/]api$", "", uri)
                        _router = APIRouter(
                            prefix="/" + uri,
                            tags=tags,
                        )

                        for r in find_routes:
                            _router.add_api_route("/", getattr(route_file, r), methods=[r])

                        self.include_router(_router)

    def build_prod_router(self):
        pass

    def build_configuration(self):
        pass

    def convert_to_lower_with_hyphen(filename):
        lower_router = filename[0].lower()
        for char in filename[1:]:
            if char.isupper():
                lower_router += '-' + char.lower()
            else:
                lower_router += char

        return lower_router

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, value):
        self._base = value
