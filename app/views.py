import os

from flask import Blueprint, current_app, jsonify, render_template, request

from app.editor import ConfigEditorError, read_backup, read_raw, write_atomic

bp = Blueprint("dashboard", __name__)


@bp.get("/health")
def health():
    return "OK", 200


@bp.route("/config")
def view_config():
    loader = current_app.extensions["dashboard_loader"]
    _config, error = loader.get()

    if error is not None:
        return render_template("config.html", error=error), 200

    try:
        raw_config = read_raw(loader.path)
    except ConfigEditorError as exc:
        return render_template("config.html", error=str(exc)), 200

    writable = os.access(loader.path, os.W_OK)
    backup_exists = _backup_exists(loader.path)

    return render_template(
        "config.html",
        raw_config=raw_config,
        editing_enabled=loader.editor_enabled(),
        writable=writable,
        config_path=loader.path,
        backup_exists=backup_exists,
        config_mtime=_config_mtime(loader.path),
        error=None,
    )


@bp.post("/config/save")
def save_config():
    loader = current_app.extensions["dashboard_loader"]
    if not loader.editor_enabled():
        return jsonify({"ok": False, "error": "Config editing is disabled."}), 403

    payload = request.get_json(silent=True) or {}
    content = payload.get("content")
    if content is None:
        return jsonify({"ok": False, "error": "Missing content."}), 400

    expected_mtime = payload.get("config_mtime")
    if expected_mtime is not None:
        try:
            expected_mtime = int(expected_mtime)
        except (TypeError, ValueError):
            expected_mtime = None
    if expected_mtime is not None:
        current_mtime = _config_mtime(loader.path)
        if current_mtime != expected_mtime:
            return (
                jsonify(
                    {
                        "ok": False,
                        "error": (
                            "The config changed on disk since you opened it. "
                            "Reload the page before saving to avoid overwriting newer changes."
                        ),
                    }
                ),
                409,
            )

    try:
        write_atomic(loader.path, content)
    except ConfigEditorError as exc:
        return _write_error_response(exc)

    return (
        jsonify({"ok": True, "message": "Saved. The dashboard will reflect the change."}),
        200,
    )


def _backup_exists(config_path):
    return os.path.exists(config_path + ".backup.yaml")


def _write_error_response(exc):
    """Map a ConfigEditorError to the contract's HTTP response.

    Validation problems (bad YAML / format) are client errors (400); server-side
    read/write failures are 500. The previous config is left untouched either way.
    """
    message = str(exc).lower()
    if "could not write" in message or "could not read" in message:
        return jsonify({"ok": False, "error": "Could not write the config file."}), 500
    return jsonify({"ok": False, "error": str(exc)}), 400


def _config_mtime(config_path):
    try:
        return os.stat(config_path).st_mtime_ns
    except OSError:
        return None


@bp.post("/config/restore")
def restore_backup():
    loader = current_app.extensions["dashboard_loader"]
    if not loader.editor_enabled():
        return jsonify({"ok": False, "error": "Config editing is disabled."}), 403

    backup_content = read_backup(loader.path)
    if backup_content is None:
        return jsonify({"ok": False, "error": "No last-known-good backup exists."}), 400

    try:
        write_atomic(loader.path, backup_content)
    except ConfigEditorError as exc:
        return _write_error_response(exc)

    return jsonify({"ok": True, "content": backup_content}), 200


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
        editing_enabled=loader.editor_enabled(),
    )
