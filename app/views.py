from flask import Blueprint, current_app, render_template

bp = Blueprint("dashboard", __name__)


@bp.get("/health")
def health():
    return "OK", 200


@bp.get("/")
def home():
    loader = current_app.extensions["dashboard_loader"]
    config, error = loader.get()

    if error is not None:
        return render_template("error.html", message=error), 200

    return render_template(
        "index.html",
        title=config.title,
        services=config.services,
        bookmark_groups=config.bookmark_groups,
    )
