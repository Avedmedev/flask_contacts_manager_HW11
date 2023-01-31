import uuid
from datetime import datetime, timedelta

from flask import (
    render_template,
    session,
    request,
    redirect,
    url_for,
    make_response,
    flash, jsonify,
)
from marshmallow import ValidationError

from . import app
from .libs.validation_schema import RegistrationSchema, LoginSchema, ContactSchema
from .repository import owners, persons


@app.route("/healthcheck")
def healthcheck():
    return "Hello, I'm working!!!"


@app.route("/", strict_slashes=False)
def index():
    auth = True if "username" in session else False
    return render_template("pages/index.html", title="CONTACTS MANAGER", auth=auth)


@app.route("/registration", methods=["GET", "POST"], strict_slashes=False)
def registration():
    auth = True if "username" in session else False
    if auth:
        return redirect(url_for("index"))

    if request.method == "POST":
        try:
            RegistrationSchema().load(request.form)
        except ValidationError as err:
            return render_template("pages/registration.html", messages=err.messages)
        email = request.form.get("email")
        password = request.form.get("password")
        nick = request.form.get("nick")
        owners.create_owner(email, password, nick)
        return redirect(url_for("login"))

    return render_template("pages/registration.html")


@app.route("/login", methods=["GET", "POST"], strict_slashes=False)
def login():
    auth = True if "username" in session else False

    if request.method == "POST":
        try:
            LoginSchema().load(request.form)
        except ValidationError as err:
            return render_template("pages/login.html", messages=err.messages)

        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") == "on" else False

        owner = owners.login(email, password)

        if owner is None:
            return render_template(
                "pages/login.html",
                messages={"err": "Invalid credentials. Go to administration"},
            )

        session["username"] = {"username": owner.login, "id": owner.id}
        response = make_response(redirect(url_for("index")))

        if remember:
            token = str(uuid.uuid4())
            expire_data = datetime.now() + timedelta(days=60)
            response.set_cookie("username", token, expires=expire_data)
            owners.set_token(owner, token)

        return response
    if auth:
        return redirect(url_for("index"))
    else:
        return render_template("pages/login.html")


@app.route("/logout", strict_slashes=False)
def logout():
    auth = True if "username" in session else False
    if not auth:
        return redirect(request.url)
    session.pop("username")
    response = make_response(redirect(url_for("index")))
    response.set_cookie("username", "", expires=-1)

    return response


@app.route("/contacts", strict_slashes=False)
def contacts():
    auth = True if "username" in session else False
    if not auth:
        return redirect(request.url)
    contacts_owner = persons.get_persons_owner(session["username"]["id"])
    return render_template("pages/contacts.html", auth=auth, contacts=contacts_owner)


@app.route("/contact/<contact_id>", strict_slashes=False)
def contact(contact_id):
    auth = True if "username" in session else False
    if not auth:
        return redirect(request.url)

    contact_owner = persons.get_contact_user(session["username"]["id"], contact_id)

    return render_template("pages/contact.html", auth=auth, contact=contact_owner)


@app.route("/contacts/add", methods=["GET", "POST"], strict_slashes=False)
def contacts_add():
    auth = True if "username" in session else False
    if not auth:
        return redirect(request.url)

    if request.method == "POST":
        try:
            ContactSchema().load(request.form)
        except ValidationError as err:
            return render_template(
                "pages/add_contact.html", auth=auth, messages=err.messages
            )
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        phone_number = request.form.get("phone_number")
        email = request.form.get("email")

        persons.add_contact(
            session["username"]["id"], first_name, last_name, phone_number, email
        )

        return redirect(url_for("contacts_add"))
    return render_template("pages/add_contact.html", auth=auth)


@app.route("/contacts/delete/<contact_id>", methods=["POST"], strict_slashes=False)
def delete_contact(contact_id):
    auth = True if "username" in session else False
    if not auth:
        return redirect(request.url)

    owner_id = session["username"]["id"]
    persons.delete_contact_owner(owner_id, contact_id)
    flash("Deleted successfully")
    return redirect(url_for("contacts"))


@app.route("/contacts/edit/<contact_id>", methods=["GET", "POST"], strict_slashes=False)
def edit_picture(contact_id):
    auth = True if "username" in session else False
    if not auth:
        return redirect(request.url)

    owner_id = session["username"]["id"]
    person = persons.get_contact_user(owner_id, contact_id)

    if request.method == "POST":
        try:
            ContactSchema().load(request.form)
        except ValidationError as err:
            return render_template(
                "pages/edit.html", auth=auth, contact=person, messages=err.messages
            )

        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        phone_number = request.form.get("phone_number")
        email = request.form.get("email")

        persons.update_person(
            contact_id, owner_id, first_name, last_name, phone_number, email
        )
        flash("Successfully")
        return redirect(url_for("contacts"))
    return render_template("pages/edit.html", auth=auth, contact=person)
