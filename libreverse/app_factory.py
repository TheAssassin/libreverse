import os

from flask import Flask, safe_join


def create_app(config: dict = None) -> Flask:
    """
    Idiomatic Flask way allowing to create different applications. This allows for creating more app objects, e.g.,
    for unit testing or some special deployments.
    :return: configured Flask app
    """

    app = Flask(__name__)

    app.config.setdefault("FREEZER_DESTINATION", os.path.join(os.getcwd(), "frozen"))

    # load configuration from current working directory, if any
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))

    if config is not None:
        app.config.update(config)

    try:
        if not os.path.isdir(app.config["MODELS_DIR"]):
            raise IOError("Could not find models dir %s" % app.config["MODELS_DIR"])

    except KeyError:
        raise ValueError("MODELS_DIR not configured")

    # register views
    from .views import bp
    app.register_blueprint(bp)

    # make some Python functions available in Jinja2
    app.jinja_env.globals.update(
        safe_join=safe_join,
    )

    return app
