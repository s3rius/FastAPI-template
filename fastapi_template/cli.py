import re
import shutil
from importlib.metadata import version
from typing import Any, Callable, List, Optional

from click import Command, Option
from prompt_toolkit import prompt
from prompt_toolkit.document import Document
from prompt_toolkit.validation import ValidationError, Validator
from termcolor import colored

from fastapi_template.input_model import (
    SKIP_ENTRY,
    BaseMenuModel,
    BuilderContext,
    Database,
    MenuEntry,
    MultiselectMenuModel,
    SingularMenuModel,
)


class SnakeCaseValidator(Validator):
    def validate(self, document: Document):
        text = document.text
        if not text or re.fullmatch(r"[a-zA-Z][\w\_\d]*", text) is None:
            raise ValidationError(message="Must be a valid snake_case name.")


def db_menu_update_info(ctx: BuilderContext, menu: SingularMenuModel) -> BuilderContext:
    for entry in menu.entries:
        if entry.code == ctx.db:
            ctx.db_info = entry.additional_info.dict()
    return ctx


def disable_orm(ctx: BuilderContext) -> MenuEntry:
    if ctx.db == "none":
        ctx.orm = "none"
        return SKIP_ENTRY
    return None


def do_not_ask_features_if_quite(ctx: BuilderContext) -> Optional[List[MenuEntry]]:
    if ctx.quite:
        return [SKIP_ENTRY]
    return None


def check_db(allowed_values: List[str]) -> Callable[[BuilderContext], bool]:
    def checker(ctx: BuilderContext) -> bool:
        return ctx.db not in allowed_values

    return checker


def check_orm(allowed_values: List[str]) -> Callable[[BuilderContext], bool]:
    def checker(ctx: BuilderContext) -> bool:
        return ctx.orm not in allowed_values

    return checker


api_menu = SingularMenuModel(
    title="API type",
    code="api_type",
    cli_name="api-type",
    description="Select API type for your application",
    entries=[
        MenuEntry(
            code="rest",
            user_view="REST API",
            description=(
                "Choose this option if you want to create a service with {name}.\n"
                "It's more suitable for {generic} web-services or services without databases.".format(
                    name=colored("REST API", color="green"),
                    generic=colored("generic", color="cyan", attrs=["underline"]),
                )
            ),
        ),
        MenuEntry(
            code="graphql",
            user_view="GrapQL API",
            pydantic_v1=True,
            description=(
                "Choose this option if you want to create a service with {name}.\n"
                "It's more suitable for services with {reason} and deep nesting.".format(
                    name=colored("GraphQL", color="green"),
                    reason=colored(
                        "lots of entities", color="cyan", attrs=["underline"]
                    ),
                )
            ),
        ),
    ],
)

db_menu = SingularMenuModel(
    title="Database",
    code="db",
    description="Select a database for your app",
    after_ask_fun=db_menu_update_info,
    entries=[
        MenuEntry(
            code="none",
            user_view="No database",
            description="This project doesn't need a database.",
            additional_info=Database(
                name="none",
                image=None,
                driver=None,
                async_driver=None,
                port=None,
            ),
        ),
        MenuEntry(
            code="sqlite",
            user_view="SQLite database",
            description=(
                "{name} is a good embeddable database.\n"
                "This option will be a great fit for {small} systems where you are "
                "going to run {how_many} of your application.".format(
                    name=colored("SQLite", color="green"),
                    small=colored("small", color="cyan", attrs=["underline"]),
                    how_many=colored(
                        "only one instance",
                        color="red",
                        attrs=["bold", "underline"],
                    ),
                )
            ),
            additional_info=Database(
                name="sqlite",
                image=None,
                async_driver="sqlite+aiosqlite",
                driver_short="sqlite",
                driver="sqlite",
                port=None,
            ),
        ),
        MenuEntry(
            code="mysql",
            user_view="MySQL database",
            description=(
                "{name} is the most popular database made by oracle.\n"
                "It's a good fit for {prod} application.".format(
                    name=colored("MySQL", color="green"),
                    prod=colored("production-grade", color="cyan", attrs=["underline"]),
                )
            ),
            additional_info=Database(
                name="mysql",
                image="bitnami/mysql:8.0.30",
                async_driver="mysql+aiomysql",
                driver_short="mysql",
                driver="mysql",
                port=3306,
            ),
        ),
        MenuEntry(
            code="postgresql",
            user_view="PostgreSQL database",
            description=(
                "{name} is second most popular open-source relational database.\n"
                "It's a good fit for {prod} application.".format(
                    name=colored("PostgreSQL", color="green"),
                    prod=colored("production-grade", color="cyan", attrs=["underline"]),
                )
            ),
            additional_info=Database(
                name="postgresql",
                image="postgres:13.8-bullseye",
                async_driver="postgresql+asyncpg",
                driver_short="postgres",
                driver="postgresql",
                port=5432,
            ),
        ),
    ],
)

ci_menu = SingularMenuModel(
    title="CI|CD",
    code="ci_type",
    cli_name="ci",
    description="Select a CI for your app",
    entries=[
        MenuEntry(
            code="none",
            user_view="Do not add CI/CD.",
            description="This project doesn't need to have CI/CD.",
        ),
        MenuEntry(
            code="gitlab_ci",
            user_view="Gitlab CI",
            description=(
                "Use this option if you use gitlab as your VCS.\n"
                "This option will add test jobs in your {file} file.\n"
                "({warn}).".format(
                    file=colored(
                        "`.gitlab-ci.yml`",
                        color="cyan",
                    ),
                    warn=colored(
                        "To use it please use docker or kubernetes executors",
                        color="red",
                        attrs=["underline"],
                    ),
                )
            ),
        ),
        MenuEntry(
            code="github",
            user_view="Github Actions",
            description=(
                "Use this option if you use github as your VCS.\n"
                "This option will create {file} file that adds test jobs for your project.".format(
                    file=colored(
                        "`.github/workflows/tests.yml`",
                        color="cyan",
                    )
                )
            ),
        ),
    ],
)

orm_menu = SingularMenuModel(
    title="ORM",
    code="orm",
    description="Choose Object–Relational Mapper lib",
    cli_name="orm",
    before_ask_fun=disable_orm,
    entries=[
        MenuEntry(
            code="none",
            user_view="Whithout ORMs",
            description=(
                "If you select this option, you will get only {what}.\n"
                "The rest {warn}.".format(
                    what=colored("raw database", color="green"),
                    warn=colored("is up to you", color="red", attrs=["underline"]),
                )
            ),
        ),
        MenuEntry(
            code="ormar",
            user_view="Ormar",
            pydantic_v1=True,
            description=(
                "{what} is a great {feature} ORM.\n"
                "It's compatible with pydantic models and alembic migrator.".format(
                    what=colored("Ormar", color="green"),
                    feature=colored("SQLAlchemy-based", color="cyan"),
                )
            ),
        ),
        MenuEntry(
            code="sqlalchemy",
            user_view="SQLAlchemy",
            description=(
                "{what} is the most popular python ORM.\n"
                "It has a {feature} and a big community around it.".format(
                    what=colored("SQLAlchemy", color="green"),
                    feature=colored("great documentation", color="cyan"),
                )
            ),
        ),
        MenuEntry(
            code="tortoise",
            user_view="Tortoise",
            description=(
                "{what} is a great {feature} ORM.\n"
                "It's easy to use, it has it's own migration tooling.".format(
                    what=colored("Tortoise", color="green"),
                    feature=colored("fully-async", color="cyan"),
                )
            ),
        ),
        MenuEntry(
            code="psycopg",
            user_view="PsycoPG",
            is_hidden=check_db(["postgresql"]),
            description=(
                "{what} is a {feature} for Postgresql.\n"
                "It's async and can work with pydantic types.".format(
                    what=colored("PsycoPG", color="green"),
                    feature=colored("raw driver", color="cyan"),
                )
            ),
        ),
        MenuEntry(
            code="piccolo",
            user_view="Piccolo",
            pydantic_v1=True,
            is_hidden=check_db(["postgresql", "sqlite"]),
            description=(
                "{what} is a great ORM for Postgresql and SQLite.\n"
                "It's very flexible and fully {feature}.".format(
                    what=colored("Piccolo", color="green"),
                    feature=colored("tab-completable", color="cyan"),
                )
            ),
        ),
    ],
)

features_menu = MultiselectMenuModel(
    title="Additional tweaks",
    code="features",
    description="Additional project features",
    multiselect=True,
    before_ask=do_not_ask_features_if_quite,
    entries=[
        MenuEntry(
            code="enable_redis",
            cli_name="redis",
            user_view="Add redis support",
            description=(
                "{name} is a cool and lightweight in-memory key-value store.\n"
                "It's good for {purpose1} or {purpose2}.".format(
                    name=colored(
                        "Redis",
                        color="green",
                    ),
                    purpose1=colored("caching", color="cyan"),
                    purpose2=colored("storing temporary variables", color="cyan"),
                )
            ),
        ),
        MenuEntry(
            code="enable_rmq",
            cli_name="rabbit",
            user_view="Add RabbitMQ support",
            description=(
                "{name} is a flexible message broker.\n"
                "It's used to create {purp1} systems or for {purp2}.".format(
                    name=colored("RabbitMQ", color="green"),
                    purp1=colored("event-based", color="cyan"),
                    purp2=colored("async computations", color="cyan"),
                )
            ),
        ),
        MenuEntry(
            code="enable_taskiq",
            cli_name="taskiq",
            user_view="Add Taskiq support",
            description=(
                "{what} is an async task manager.\n"
                "You can think of taskiq as a {celery}, but async.".format(
                    what=colored("Taskiq", color="green"),
                    celery=colored(
                        "celery",
                        color="cyan",
                    ),
                )
            ),
        ),
        MenuEntry(
            code="enable_migrations",
            cli_name="migrations",
            user_view="Add Migrations",
            is_hidden=lambda ctx: ctx.db == "none",
            description=(
                "Add database {what} config.\n"
                "This options adds ability to {why} database schema.".format(
                    what=colored("schema migration", color="green"),
                    why=colored("automatically update", color="cyan"),
                )
            ),
        ),
        MenuEntry(
            code="enable_kube",
            cli_name="kube",
            user_view="Add kubernetes configs",
            description=(
                "This option will add {what} manifests to your project.\n"
                "But this option is {warn}, since if you want to use k8s, please create helm.".format(
                    what=colored("kubernetes", color="green"),
                    warn=colored("deprecated", color="red", attrs=["underline"]),
                )
            ),
        ),
        MenuEntry(
            code="add_dummy",
            cli_name="dummy",
            user_view="Add dummy model",
            is_hidden=lambda ctx: ctx.orm == "none",
            description=(
                "This option creates {what} as an example of how to use chosen ORM.\n"
                "Also this option will generate you an example of {dao}.".format(
                    what=colored("dummy model", color="green"),
                    dao=colored("DAO class", color="cyan"),
                )
            ),
        ),
        MenuEntry(
            code="enable_routers",
            cli_name="routers",
            user_view="Add example routers",
            description=(
                "This option will add example {what} for your application.\n"
                "It checks for all enabled features and create views for them.".format(
                    what=colored("routers", color="green")
                )
            ),
        ),
        MenuEntry(
            code="self_hosted_swagger",
            cli_name="swagger",
            user_view="Add self hosted swagger",
            description=(
                "This option will place swagger UI {what} files inside the project.\n"
                "This is {crit} for systems where you cannot make external requests.".format(
                    what=colored("js and css", color="green"),
                    crit=colored("critical", color="red", attrs=["underline"]),
                )
            ),
        ),
        MenuEntry(
            code="prometheus_enabled",
            cli_name="prometheus",
            user_view="Add prometheus compatible metrics",
            description=(
                "{name} is a system that can collect metrics.\n"
                "This option will add a {path} route where you can find you app's metrics.".format(
                    name=colored("Prometheus", color="green"),
                    path=colored("`/metrics`", color="blue"),
                )
            ),
        ),
        MenuEntry(
            code="sentry_enabled",
            cli_name="sentry",
            user_view="Add sentry integration",
            description=(
                "{what} is super cool system that helps finding bugs.\n"
                "This feature will add sentry integration to your project. ({warn}).".format(
                    what=colored("Sentry", color="green"),
                    warn=colored(
                        "This option may decrease speed",
                        color="red",
                        attrs=["underline"],
                    ),
                )
            ),
        ),
        MenuEntry(
            code="enable_loguru",
            cli_name="loguru",
            user_view="Add loguru logger",
            description=(
                "{what} is a good drop-in replacement for default logger.\n"
                "It makes logs look {why}.".format(
                    what=colored("Loguru", color="green"),
                    why=colored(
                        "fancy and cool",
                        color="cyan",
                        attrs=["underline"],
                    ),
                )
            ),
        ),
        MenuEntry(
            code="otlp_enabled",
            cli_name="opentelemetry",
            user_view="Add opentelemetry integration",
            description=(
                "{what} is a new way to collect telemetry.\n"
                "It sends {why} and everything in collectors. Compatible with {comp}.".format(
                    what=colored("Opentelemetry", color="green"),
                    why=colored(
                        "traces, logs",
                        color="cyan",
                    ),
                    comp=colored(
                        "Jaeger",
                        color="cyan",
                    ),
                )
            ),
        ),
        MenuEntry(
            code="traefik_labels",
            cli_name="traefik",
            user_view="Adds traefik labels to docker container",
            description=(
                "{what} is successor of the nginx.\n"
                "This option adds {why} to docker containers and makes them {comp}.".format(
                    what=colored("Traefik", color="green"),
                    why=colored(
                        "labels",
                        color="cyan",
                    ),
                    comp=colored(
                        "discoverable",
                        color="cyan",
                    ),
                )
            ),
        ),
        MenuEntry(
            code="enable_kafka",
            cli_name="kafka",
            user_view="Add Kafka support",
            description=(
                "{what} is a message broker.\n"
                "Kafka doesn't have a fancy routing as RabbitMQ, but it's {why}.".format(
                    what=colored("Kafka", color="green"),
                    why=colored(
                        "super fast",
                        color="cyan",
                    ),
                )
            ),
        ),
        MenuEntry(
            code="gunicorn",
            cli_name="gunicorn",
            user_view="Add gunicorn server",
            description=(
                "This option adds {what} server for running application.\n"
                "It's more performant than uvicorn, and recommended for production.".format(
                    what=colored("gunicorn", color="green")
                )
            ),
        ),
    ],
)


def handle_cli(
    menus: List[BaseMenuModel],
    callback: Callable[[BuilderContext], None],
):
    def inner_callback(**cli_args: Any):
        if cli_args["version"]:
            print(version("fastapi_template"))
            exit(0)

        context = BuilderContext(**cli_args)

        if context.project_name is None:
            context.project_name = prompt(
                "Project name: ",
                validator=SnakeCaseValidator(),
            )
        context.kube_name = context.project_name.replace("_", "-")

        for menu in menus:
            if menu.need_ask(context):
                context = menu.ask(context)
                if context is None:
                    print("Project generation stopped. Goodbye!")
                    return
                context = BuilderContext(**context.dict())

            context = BuilderContext(**menu.after_ask(context=context).dict())

        callback(context)

    return inner_callback


def run_command(callback: Callable[[BuilderContext], None]) -> None:
    menus: "List[BaseMenuModel]" = [
        api_menu,
        db_menu,
        orm_menu,
        ci_menu,
        features_menu,
    ]

    cmd = Command(
        None,
        params=[
            Option(
                ["-n", "--name", "project_name"],
                help="Name of your awesome project",
            ),
            Option(
                ["-V", "--version", "version"],
                is_flag=True,
                help="Prints current version",
            ),
            Option(
                ["--force"],
                is_flag=True,
                help="Owerrite directory if it exists",
            ),
            Option(
                ["--quite"],
                is_flag=True,
                help="Do not ask for features during generation",
            ),
        ],
        callback=handle_cli(
            menus=menus,
            callback=callback,
        ),
    )
    for menu in menus:
        cmd.params.extend(menu.get_cli_options())
    required_commands = {
        "poetry": "https://python-poetry.org/docs/#installation",
        "git": "https://git-scm.com/",
    }
    for prog, link in required_commands.items():
        if shutil.which(prog) is None:
            print(
                "Please install {prog} before generating project. Link: {link}".format(
                    prog=colored(prog, "green"),
                    link=colored(link, "cyan"),
                ),
            )
            return

    cmd.main()
