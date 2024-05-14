from resources import *

def generate():
    model = CommandModel()
    lines = list()

    def append(line=""):
        if line is None:
            return

        lines.append(line)

    append("#### Contents")
    append()
    append(f"- [Global options](#global-options)")

    for group in model.groups:
        append(f"- [{group.title}](#{group.id})")

        for command in group.commands:
            append(f"  - [{command.title}](#{command.id})")

    append()

    append(f"## Global options")
    append()

    for argument in model.global_arguments:
        generate_argument(argument, append)

    for group in model.groups:
        append(f"## {group.title}")
        append()

        for command in group.commands:
            generate_command(command, append)

    markdown = read("config/commands.md.in")
    markdown = markdown.replace("@content@", "\n".join(lines))

    write("input/commands.md", markdown)

def generate_command(command, append):
    debug(f"Generating {command}")

    append(f"### {command.title}")
    append()
    append(command.description)
    append()

    if command.usage:
        append("#### Usage")
        append()
        append("~~~ shell")
        append(f"$ {command.usage.strip()}")

        if command.output:
            append(command.output.strip())

        append("~~~")
        append()

    if command.examples:
        append("#### Examples")
        append()
        append("~~~")
        append(command.examples.strip())
        append("~~~")
        append()

    if command.arguments:
        append("#### Arguments")
        append()

        for argument in command.arguments:
            generate_argument(argument, append)

    if command.errors:
        append("#### Errors")
        append()

        for error in command.errors:
            append(f"- **{error.message}**")
            append()

            if error.description:
                description = "\n".join(f"  {line}" for line in error.description.split("\n"))

                append(description)
                append()

    if command.notes:
        notes = "\n".join(f"_{line}_ " for line in command.notes.strip().split("\n"))

        append("#### _Notes_")
        append()
        append(notes)
        append()

def generate_argument(argument, append):
    assert argument.property_ or argument.name

    debug(f"Generating {argument}")

    title = f"**{argument.name}**"

    if argument.variable:
        title = f"**{argument.name}** _{argument.variable}_"

    append(f"- {title}")
    append()

    if argument.default is not None:
        default = argument.default

        if argument.default in (True, False):
            default = str(argument.default).lower()

        append(f"  _Default:_ {default}")
        append()

    if argument.description:
        description = "\n".join(f"  {line}" for line in argument.description.split("\n"))

        append(description)
        append()

    if argument.notes:
        notes = "\n".join(f"  _{line}_" for line in argument.notes.strip().split("\n"))

        append("  ##### _Notes_")
        append()
        append(notes)
        append()

class CommandModel:
    def __init__(self):
        self.data = read_yaml("config/commands.yaml")
        self.global_arguments = list()
        self.groups = list()

        for argument_data in self.data["global_arguments"]:
            self.global_arguments.append(Argument(self, self, argument_data))

        for group_data in self.data["groups"]:
            self.groups.append(Group(self, group_data))

        self.resource_model = ResourceModel()

    def __repr__(self):
        return "command model"

class Group:
    def __init__(self, model, data):
        self.model = model
        self.data = data
        self.commands = list()

        for command_data in self.data["commands"]:
            self.commands.append(Command(self.model, self, command_data))

    def __repr__(self):
        return f"group '{self.title}'"

    @property
    def id(self):
        return fragment_id(self.title)

    @property
    def title(self):
        return self.data["title"]

    @property
    def description(self):
        return self.data.get("description")

class Command:
    def __init__(self, model, parent, data):
        self.model = model
        self.parent = parent
        self.data = data
        self.arguments = list()
        self.errors = list()

        for argument_data in self.data.get("arguments", []):
            self.arguments.append(Argument(self.model, self, argument_data))

        for error_data in self.data.get("errors", []):
            self.errors.append(Error(self, error_data))

    def __repr__(self):
        return f"command '{self.title}'"

    @property
    def id(self):
        return fragment_id(self.title)

    @property
    def title(self):
        return self.data["title"]

    @property
    def resource(self):
        if "resource" in self.data:
            return self.model.resource_model.resources[self.data["resource"]]

    @property
    def description(self):
        description = self.data.get("description")

        if description and self.resource and self.resource.description:
            description = description.replace("@resource_description@", self.resource.description)

        return description

    @property
    def examples(self):
        return self.data.get("examples")

    @property
    def usage(self):
        return self.data.get("usage")

    @property
    def output(self):
        return self.data.get("output")

    @property
    def notes(self):
        return self.data.get("notes")

class Argument:
    def __init__(self, model, command, data):
        self.model = model
        self.command = command
        self.data = data

    def __repr__(self):
        return f"argument '{self.name}'"

    @property
    def property_(self):
        if "property" in self.data:
            assert self.command.resource is not None

            try:
                return self.command.resource.properties[self.data["property"]]
            except KeyError:
                pprint(self.data)
                pprint(self.command.resource.properties)

    @property
    def name(self):
        default = argument_name(self.property_.name, self.positional) if self.property_ else None
        return self.data.get("name", default)

    @property
    def variable(self):
        default = self.property_.type if self.property_ else None
        return self.data.get("variable", default)

    @property
    def default(self):
        default = self.property_.default if self.property_ else None

        # XXX
        if default is None and self.variable == "boolean":
            default = False

        return self.data.get("default", default)

    @property
    def required(self):
        default = self.property_.required if self.property_ else None
        return self.data.get("required", default)

    @property
    def positional(self):
        return self.data.get("positional")

    @property
    def description(self):
        default = self.property_.description if self.property_ else None
        value = self.data.get("description", default)

        if self.property_ and self.property_.description:
            value = value.replace("@property_description@", self.property_.description)

        return value

    @property
    def notes(self):
        return self.data.get("notes")

class Error:
    def __init__(self, model, data):
        self.model = model
        self.data = data

    def __repr__(self):
        return f"error '{self.message}'"

    @property
    def message(self):
        return self.data["message"]

    @property
    def description(self):
        return self.data.get("description")

    @property
    def notes(self):
        return self.data.get("notes")

def fragment_id(title):
    return title.lower().replace(" ", "-")

def argument_name(property_name, positional):
    chars = list()

    if not positional:
        chars.append("--")

    chars.append(property_name[0].lower())

    for char in property_name[1:]:
        if char.isupper():
            chars.append(f"-{char.lower()}")
        else:
            chars.append(char)

    return "".join(chars)
