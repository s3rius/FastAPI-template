import enum
from typing import Optional, Callable, Any

from pydantic import BaseModel
import click
import abc
from simple_term_menu import TerminalMenu
from collections import UserDict


class Database(BaseModel):
    name: str
    image: Optional[str]
    driver: Optional[str]
    async_driver: Optional[str]
    port: Optional[int]
    driver_short: Optional[str]


class MenuEntry(BaseModel):
    code: str
    cli_name: Optional[str]
    user_view: str
    description: str
    is_hidden: Optional[Callable[["BuilderContext"], bool]]
    additional_info: Any

    @property
    def generated_name(self) -> str:
        """
        Property to generate parameter name.

        It checks if cli_name is present,
        otherwise, code is used.

        :return: string to use in CLI.
        """
        if self.cli_name:
            return self.cli_name
        return self.code


SKIP_ENTRY = MenuEntry(
    code="skip",
    user_view="skip",
    description="skip",
)


class BaseMenuModel(BaseModel, abc.ABC):
    title: str
    entries: list[MenuEntry]

    def _preview(self, current_value: str):

        for entry in self.entries:
            if entry.user_view == current_value:
                return entry.description
        return "Unknown value"

    @abc.abstractmethod
    def get_cli_options(self) -> list[click.Option]:
        pass

    @abc.abstractmethod
    def ask(self, context: "BuilderContext") -> Optional["BuilderContext"]:
        pass

    @abc.abstractmethod
    def need_ask(self, context: "BuilderContext") -> bool:
        pass

    def after_ask(self, context: "BuilderContext") -> "BuilderContext":
        """Function run after the menu finished work."""
        return context


class SingularMenuModel(BaseMenuModel):
    code: str
    cli_name: Optional[str]
    description: str
    before_ask_fun: Optional[Callable[["BuilderContext"], Optional[MenuEntry]]]
    after_ask_fun: Optional[
        Callable[["BuilderContext", "SingularMenuModel"], "BuilderContext"]
    ]
    parser: Optional[Callable[[str], Any]]

    def get_cli_options(self) -> list[click.Option]:
        cli_name = self.code
        if self.cli_name is not None:
            cli_name = self.cli_name
        choices = [entry.generated_name for entry in self.entries]
        return [
            click.Option(
                param_decls=[f"--{cli_name}", self.code],
                type=click.Choice(choices, case_sensitive=False),
                default=None,
                help=self.description,
            )
        ]

    def need_ask(self, context: "BuilderContext") -> bool:
        if getattr(context, self.code, None) is None:
            return True
        return False

    def ask(self, context: "BuilderContext") -> Optional["BuilderContext"]:
        chosen_entry = None
        if self.before_ask_fun is not None:
            chosen_entry = self.before_ask_fun(context)

        ctx_value = context.dict().get(self.code)
        if ctx_value:
            for entry in self.entries:
                if entry.code == ctx_value:
                    chosen_entry = entry

        if not chosen_entry:
            available_entries = []
            for entry in self.entries:
                if entry.is_hidden is None:
                    available_entries.append(entry)
                elif not entry.is_hidden(context):
                    available_entries.append(entry)

            menu = TerminalMenu(
                title=self.title,
                menu_entries=[entry.user_view for entry in available_entries],
                multi_select=False,
                preview_title="Description",
                preview_command=self._preview,
                preview_size=0.5,
            )
            idx = menu.show()
            if idx is None:
                return None

            chosen_entry = available_entries[idx]

        if chosen_entry == SKIP_ENTRY:
            return

        setattr(context, self.code, chosen_entry.code)

        return context

    def after_ask(self, context: "BuilderContext") -> "BuilderContext":
        if self.after_ask_fun:
            return self.after_ask_fun(context, self)
        return super().after_ask(context)


class MultiselectMenuModel(BaseMenuModel):
    before_ask: Optional[Callable[["BuilderContext"], Optional[list[MenuEntry]]]]

    def get_cli_options(self) -> list[click.Option]:
        options = []
        for entry in self.entries:
            options.append(
                click.Option(
                    param_decls=[f"--{entry.generated_name}", entry.code],
                    is_flag=True,
                    help=entry.user_view,
                    default=None,
                )
            )
        return options

    def need_ask(self, context: "BuilderContext") -> bool:
        for entry in self.entries:
            if getattr(context, entry.code, None) is None:
                return True
        return False

    def ask(self, context: "BuilderContext") -> Optional["BuilderContext"]:
        chosen_entries = None
        if self.before_ask is not None:
            chosen_entries = self.before_ask(context)

        if chosen_entries is None:
            unknown_entries = []
            for entry in self.entries:
                if not context.dict().get(entry.code):
                    unknown_entries.append(entry)

            visible_entries = []
            for entry in unknown_entries:
                if entry.is_hidden is None:
                    visible_entries.append(entry)
                elif not entry.is_hidden(context):
                    visible_entries.append(entry)

            menu = TerminalMenu(
                title=self.title,
                menu_entries=[entry.user_view for entry in visible_entries],
                multi_select=True,
                preview_title="Description",
                preview_command=self._preview,
            )

            idxs = menu.show()

            if idxs is None:
                return None

            chosen_entries = []
            for idx in idxs:
                chosen_entries.append(visible_entries[idx])

        if chosen_entries == [SKIP_ENTRY]:
            return context

        for entry in chosen_entries:
            setattr(context, entry.code, True)

        return context


class BuilderContext(UserDict):
    """Options for project generation."""

    def __init__(self, **kwargs: Any) -> None:
        self.__dict__["data"] = kwargs

    def __getattr__(self, name: str) -> Any:
        try:
            return self.__dict__["data"][name]
        except KeyError:
            cls_name = self.__class__.__name__
            raise AttributeError(f"'{cls_name}' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value

    def dict(self) -> str:
        return self.__dict__["data"]
