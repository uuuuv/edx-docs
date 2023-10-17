from tutor import hooks

hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-production-settings",
        "CORS_ORIGIN_ALLOW_ALL = True",
    )
)