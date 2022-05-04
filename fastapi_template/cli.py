import re
from argparse import ArgumentParser
from operator import attrgetter
from termcolor import cprint

from prompt_toolkit import prompt
from prompt_toolkit.document import Document
from prompt_toolkit.shortcuts import checkboxlist_dialog, radiolist_dialog
from prompt_toolkit.validation import ValidationError, Validator

from fastapi_template.input_model import (
    SUPPORTED_ORMS,
    ORMS_WITHOUT_MIGRATIONS,
    ORM,
    APIType,
    BuilderContext,
    DB_INFO,
    DatabaseType,
    CIType,
)
from importlib.metadata import version


class SnakeCaseValidator(Validator):
    def validate(self, document: Document):
        text = document.text
        if not text or re.fullmatch(r"[a-zA-Z][\w\_\d]*", text) is None:
            raise ValidationError(message="Must be a valid snake_case name.")


def parse_args():
    parser = ArgumentParser(
        prog="FastAPI template",
    )
    parser.add_argument(
        "--version", "-V", action="store_true", help="Prints current version"
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
        default=None,
        dest="project_description",
        help="Project description",
    )
    parser.add_argument(
        "--api-type",
        help="API type",
        type=str,
        choices=list(map(attrgetter("value"), APIType)),
        default=None,
        dest="api_type",
    )
    parser.add_argument(
        "--db",
        help="Database",
        type=str,
        choices=list(map(attrgetter("value"), DatabaseType)),
        default=None,
        dest="db",
    )
    parser.add_argument(
        "--orm",
        help="ORM",
        type=str,
        choices=[orm.value for orm in ORM if orm != ORM.none],
        default=None,
        dest="orm",
    )
    parser.add_argument(
        "--ci",
        help="Choose CI support",
        default=None,
        type=str,
        choices=[ci.value for ci in CIType],
        dest="ci_type",
    )
    parser.add_argument(
        "--redis",
        help="Add Redis support",
        action="store_true",
        default=None,
        dest="enable_redis",
    )
    parser.add_argument(
        "--rabbit",
        help="Add RabbitMQ support",
        action="store_true",
        default=None,
        dest="enable_rmq",
    )
    parser.add_argument(
        "--migrations",
        help="Add migrations support",
        action="store_true",
        default=None,
        dest="enable_migrations",
    )
    parser.add_argument(
        "--kube",
        help="Add Kubernetes configs",
        action="store_true",
        default=None,
        dest="enable_kube",
    )
    parser.add_argument(
        "--dummy",
        "--dummy-model",
        help="Add dummy model",
        action="store_true",
        default=None,
        dest="add_dummy",
    )
    parser.add_argument(
        "--routers",
        help="Add example routers",
        action="store_true",
        default=None,
        dest="enable_routers",
    )
    parser.add_argument(
        "--swagger",
        help="Enable self-hosted Swagger",
        action="store_true",
        default=None,
        dest="self_hosted_swagger",
    )
    parser.add_argument(
        "--force",
        help="Owerrite directory if it exists",
        action="store_true",
        default=False,
        dest="force",
    )
    parser.add_argument(
        "--quite",
        help="Do not ask for features during generation",
        action="store_true",
        default=False,
        dest="quite",
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
        "Demo routers": {
            "name": "enable_routers",
            "value": current_context.enable_routers,
        },
        "Self-hosted swagger": {
            "name": "self_hosted_swagger",
            "value": current_context.self_hosted_swagger,
        },
        "RabbitMQ integration": {
            "name": "enable_rmq",
            "value": current_context.enable_rmq,
        },
    }
    if current_context.db != DatabaseType.none:
        features["Migrations support"] = {
            "name": "enable_migrations",
            "value": current_context.enable_migrations,
        }
        features["Add dummy model"] = {
            "name": "add_dummy",
            "value": current_context.add_dummy,
        }
    checkbox_values = []
    for feature_name, feature in features.items():
        if feature["value"] is None:
            setattr(current_context, feature["name"], False)
            checkbox_values.append((feature["name"], feature_name))
    if checkbox_values and not current_context.quite:
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
    current_context.kube_name = current_context.project_name.replace("_", "-")
    if current_context.project_description is None:
        current_context.project_description = prompt("Project description: ")
    if current_context.api_type is None:
        current_context.api_type = radiolist_dialog(
            "API type",
            text="Which api type do you want?",
            values=[(api, api.value) for api in list(APIType)],
        ).run()
        if current_context.api_type is None:
            raise KeyboardInterrupt()
    if current_context.db is None:
        current_context.db = radiolist_dialog(
            "Databases",
            text="Which database do you want?",
            values=[(db, db.value) for db in list(DatabaseType)],
        ).run()
        if current_context.db is None:
            raise KeyboardInterrupt()
    if current_context.db == DatabaseType.none:
        current_context.enable_migrations = False
        current_context.add_dummy = False
        current_context.orm == ORM.none
    elif current_context.orm is None:
        current_context.orm = radiolist_dialog(
            "ORM",
            text="Which ORM do you want?",
            values=[(orm, orm.value) for orm in SUPPORTED_ORMS[current_context.db]],
        ).run()
        if current_context.orm is None:
            raise KeyboardInterrupt()
    if (
        current_context.orm is not None 
        and current_context.orm != ORM.none 
        and current_context.orm not in SUPPORTED_ORMS.get(current_context.db, [])
    ):
        cprint("This ORM is not supported by chosen database.", "red")
        raise KeyboardInterrupt()
    if current_context.orm in ORMS_WITHOUT_MIGRATIONS:
        current_context.enable_migrations = False
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
    if args.version:
        print(version("fastapi_template"))
        exit(0)
    context = BuilderContext.from_orm(args)
    context = read_user_input(context)
    context.db_info = DB_INFO[context.db]
    return context
