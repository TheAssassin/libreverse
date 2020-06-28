import os

from flask import Flask, safe_join


def create_app(config: dict = None) -> Flask:
    """
    Idiomatic Flask way allowing to create different applications. This allows for creating more app objects, e.g.,
    for unit testing or some special deployments.
    :return: configured Flask app
    """

    app = Flask(__name__)

    app.config.setdefault("MODELS_DIR", os.path.join(os.path.dirname(__file__), "..", "models"))
    app.config.setdefault("FREEZER_DESTINATION", os.path.join(os.path.dirname(__file__), "..", "frozen"))

    if config is not None:
        app.config.update(config)

    if not os.path.isdir(app.config["MODELS_DIR"]):
        raise IOError("Could not find models dir %s" % app.config["MODELS_DIR"])

    # register views
    from .views import bp
    app.register_blueprint(bp)

    # make some Python functions available in Jinja2
    app.jinja_env.globals.update(
        safe_join=safe_join,
    )

    return app
