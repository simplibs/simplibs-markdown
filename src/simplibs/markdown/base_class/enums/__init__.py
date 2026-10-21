from .NodeLevel import NodeLevel


_DESIGN_NOTES = """
# base_class enums — Shared Vocabulary of the Node Tree

Plain imports, no `__all__` (the package root decides what is public).

## Internal Components Registry

| Component  | Type | Description                                              |
| :--------- | :--- | :------------------------------------------------------- |
| `NodeLevel`| Enum | Whether a node lives inside a line or as a block of its own. |
"""
