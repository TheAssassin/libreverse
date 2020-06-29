import os

import markdown as markdown
from flask import Blueprint, render_template, current_app, redirect, url_for, request, safe_join, send_file
from lxml import html
from lxml.etree import LxmlError
from markupsafe import Markup
from werkzeug.exceptions import NotFound

bp = Blueprint("views", __name__, static_folder="static", template_folder="templates")


def models_dir():
    return os.path.abspath(current_app.config["MODELS_DIR"])


def parse_readme(readme_path: str):
    with open(readme_path) as f:
        readme = markdown.markdown(f.read())

    try:
        readme_html = html.fromstring(readme)

    except LxmlError:
        raise ValueError("failed to parse README")

    # extract title from markdown document and delete it from the rest of the document
    try:
        readme_title = readme_html.cssselect("h1")[0]
    except IndexError:
        title = None
    else:
        title = readme_title.text
        readme_title.getparent().remove(readme_title)

    description = Markup(html.tostring(readme_html).decode())

    return title, description


@bp.route("/index.html")
@bp.route("/")
def index():
    categories = [i for i in os.listdir(models_dir()) if os.path.isdir(os.path.join(models_dir(), i))]
    return render_template("index.html", categories=categories)


def render_model_page(current_dir: str):
    abs_dir = safe_join(models_dir(), current_dir)

    try:
        title, description = parse_readme(safe_join(abs_dir, "README.md"))

    except (IOError, ValueError):
        title = description = None

    if not title:
        title = os.path.split(current_dir)[-1]

    if not description:
        description = "No description available"

    files = os.listdir(abs_dir)

    model_files = list(filter(lambda i: i.endswith(".scad") or i.endswith(".FCStd"), files))
    stl_files = list(filter(lambda i: i.endswith(".stl"), files))
    screenshot_files = list(filter(lambda i: i.endswith(".png") or i.endswith(".jpg"), files))

    return render_template(
        "model.html",
        title=title,
        description=description,
        current_dir=current_dir,
        screenshot_files=screenshot_files,
        model_files=model_files,
        stl_files=stl_files,
    )


def render_index_page(current_dir: str):
    abs_dir = safe_join(models_dir(), current_dir)

    try:
        title, description = parse_readme(safe_join(abs_dir, "README.md"))

    except (IOError, ValueError):
        title = description = None

    if not title:
        title = os.path.split(current_dir)[-1]

    items = [i for i in os.listdir(abs_dir) if os.path.isdir(safe_join(abs_dir, i))]

    return render_template(
        "category.html",
        title=title,
        description=description,
        current_dir=current_dir,
        items=items,
    )


@bp.route("/<path:path>/index.html")
@bp.route("/<path:path>")
@bp.route("/<path:path>/")
def router(path: str):
    """
    Custom router function that can differ between model pages and their parent directories (for which it needs to
    generate index pages).
    :param model:
    :return:
    """

    # support annoying double-slash URLs, redirecting to the real page
    original_path = str(path)

    while "//" in path:
        path = path.replace("//", "/")

    if path != original_path:
        return redirect(url_for("views.router", path=path))

    # resolve path inside models dir
    path = path.replace("/index.html", "")
    request_dir = safe_join(models_dir(), path)

    # if the directory doesn't exist, we emit a 404
    if not os.path.isdir(request_dir):
        raise NotFound("Could not find models dir")

    # let's see if this is an index page or a "content" dir
    # the detection works by checking for subdirectories; if there are any, we generate an index page, otherwise we
    # try to generate a model page
    dir_contents = os.listdir(request_dir)

    # completely empty directories should not be visible, similar like how Git works
    if not dir_contents:
        raise NotFound()

    has_subdirs = any([os.path.isdir(safe_join(request_dir, i)) for i in dir_contents])

    if has_subdirs:
        return render_index_page(path)

    else:
        return render_model_page(path)


@bp.route("/<path:path>/<filename>")
def static_files(path, filename):
    ext = os.path.splitext(filename)[-1]

    if ext not in [".png", ".jpg", ".stl", ".scad", ".FCStd"]:
        raise NotFound()

    abspath = safe_join(models_dir(), path, filename)

    try:
        return send_file(abspath)
    except IOError:
        raise NotFound()


@bp.errorhandler(404)
def not_found(exc):
    return render_template("errors/generic.html", exc=exc), exc.code
