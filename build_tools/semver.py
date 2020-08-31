import click, re


class SemverParamType(click.ParamType):
    name = "semver"
    re_pattern = r"^((([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?)(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?)$"

    def convert(self, value: str, param, ctx) -> str:
        try:
            pattern = re.compile(self.re_pattern)
            matched = pattern.match(value)

            return str(value)
        except Exception as e:
            self.fail(e)


SEMVER = SemverParamType()
