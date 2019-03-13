import uvicorn
import typesystem
import databases
import sqlalchemy

from starlette.applications import Starlette
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from accounts.schema import UserSchema
from accounts.tables import metadata, user_table

DATABASE_URL = "sqlite:///app.db"
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
database = databases.Database(DATABASE_URL)
forms = typesystem.Jinja2Forms(package="bootstrap4")
templates = Jinja2Templates(directory="templates")
statics = StaticFiles(directory="statics", packages=["bootstrap4"])

app = Starlette(debug=True)
app.mount("/static", StaticFiles(directory="statics"), name="static")


@app.on_event("startup")
async def startup() -> None:
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()


@app.route("/", methods=["GET"])
async def homepage(request):
    form = forms.Form(UserSchema)
    query = user_table.select()
    rows = await database.fetch_all(query)
    users = [UserSchema(**dict(row)) for row in rows]
    context = {"request": request, "form": form, "users": users}
    return templates.TemplateResponse("index.html", context)


@app.route("/", methods=["POST"])
async def add_user(request):
    data = await request.form()
    user, errors = UserSchema.validate_or_error(data)

    if errors:
        form = forms.Form(UserSchema, values=data, errors=errors)
        query = user_table.select()
        rows = await database.fetch_all(query)
        users = [UserSchema(**dict(row)) for row in rows]
        context = {"request": request, "form": form, "users": users}
        return templates.TemplateResponse("index.html", context)

    query = user_table.insert()
    user_dict = dict(user)
    await database.execute(query, user_dict)
    return RedirectResponse(request.url_for("homepage"))


if __name__ == "__main__":
    uvicorn.run(app)
