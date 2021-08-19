import re
from argparse import ArgumentParser
from operator import attrgetter

from prompt_toolkit import prompt
from prompt_toolkit.document import Document
from prompt_toolkit.shortcuts import checkboxlist_dialog, radiolist_dialog
from prompt_toolkit.validation import ValidationError, Validator

from fastapi_template.input_model import BuilderContext, Database, DatabaseType, CIType


class SnakeCaseValidator(Validator):
    def validate(self, document: Document):
        text = document.text
        if not text or re.fullmatch(r"[a-zA-Z][\w\_\d]*", text) is None:
            raise ValidationError(message="Must be a valid snake_case name.")


DB_INFO = {
    DatabaseType.none: Database(
        name="none",
        image="none",
        driver=None,
        port=None,
    ),
    DatabaseType.postgresql: Database(
        name=DatabaseType.postgresql.value,
        image="postgres:13.4-buster",
        driver="postgresql+asyncpg",
        port=5432,
    ),
    DatabaseType.mysql: Database(
        name=DatabaseType.mysql.value,
        image="bitnami/mysql:8.0.26",
        driver="mysql+aiomysql",
        port=3306,
    ),
    DatabaseType.sqlite: Database(
        name=DatabaseType.sqlite.value, image=None, driver="sqlite+aiosqlite", port=None
    ),
}


def parse_args():
    parser = ArgumentParser(
        prog="FastAPI template",
    )
    parser.add_argument(
        "--name",
        type=str,
        dest="project_name",
        help="Name of your awesome project",
    )
    parser.add_argument(
        "--description",
        type=str,
        dest="project_description",
        help="Project description",
    )
    parser.add_argument(
        "--db",
        help="Database",
        type=DatabaseType,
        choices=list(DatabaseType),
        default=None,
        dest="db",
    )
    parser.add_argument(
        "--ci",
        help="Choose CI support",
        default=None,
        type=CIType,
        choices=list(CIType),
        dest="ci_type",
    )
    parser.add_argument(
        "--redis",
        help="Add redis support",
        action="store_true",
        default=None,
        dest="enable_redis",
    )
    parser.add_argument(
        "--alembic",
        help="Add alembic support",
        action="store_true",
        default=None,
        dest="enable_alembic",
    )
    parser.add_argument(
        "--kube",
        help="Add kubernetes configs",
        action="store_true",
        default=None,
        dest="enable_kube",
    )
    parser.add_argument(
        "--force",
        help="Owerrite directory if it exists",
        action="store_true",
        default=False,
        dest="force",
    )

    return parser.parse_args()


def ask_features(current_context: BuilderContext) -> BuilderContext:
    features = {
        "Redis support": {
            "name": "enable_redis",
            "value": current_context.enable_redis,
        },
        "Kubernetes": {
            "name": "enable_kube",
            "value": current_context.enable_kube,
        },
    }
    if current_context.db != DatabaseType.none:
        features["Alembic migrations"] = {
            "name": "enable_alembic",
            "value": current_context.enable_alembic,
        }
    checkbox_values = []
    for feature_name, feature in features.items():
        if feature["value"] is None:
            setattr(current_context, feature["name"], False)
            checkbox_values.append((feature["name"], feature_name))
    if checkbox_values:
        results = checkboxlist_dialog(
            title="Features",
            text="What features do you wanna add?",
            values=checkbox_values,
        ).run()
        if results is None:
            raise KeyboardInterrupt()
        for feature in results:
            setattr(current_context, feature, True)
    return current_context


def read_user_input(current_context: BuilderContext) -> BuilderContext:
    if current_context.project_name is None:
        current_context.project_name = prompt(
            "Project name: ", validator=SnakeCaseValidator()
        )
    if current_context.project_description is None:
        current_context.project_description = prompt("Project description: ")
    if current_context.db is None:
        current_context.db = radiolist_dialog(
            "Databases",
            text="Which database do you want?",
            values=[(db, db.value) for db in list(DatabaseType)],
        ).run()
        if current_context.db is None:
            raise KeyboardInterrupt()
        if current_context.db == DatabaseType.none:
            current_context.enable_alembic = False
    if current_context.ci_type is None:
        current_context.ci_type = radiolist_dialog(
            "CI",
            text="Which CI/CD do you want?",
            values=[(ci, ci.value) for ci in list(CIType)],
        ).run()
        if current_context.ci_type is None:
            raise KeyboardInterrupt()
    ask_features(current_context)
    return current_context


def get_context() -> BuilderContext:
    args = parse_args()
    context = BuilderContext.from_orm(args)
    context = read_user_input(context)
    context.db_info = DB_INFO[context.db]
    return context
