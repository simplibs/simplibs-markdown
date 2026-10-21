from .LineBreakStyle import LineBreakStyle

_DESIGN_NOTES = """
# Markdown Common Enums Sub-Package

## Purpose
Enums used by more than one domain. An enum that one domain owns lives in that
domain's own `enums/`.

Plain imports, no `__all__` (the package root decides what is public).

## Internal Components Registry

| Component        | Type | Description                                     |
| :--------------- | :--- | :---------------------------------------------- |
| `LineBreakStyle` | Enum | How a hard line break is written.               |
"""
