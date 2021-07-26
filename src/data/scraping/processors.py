"""
This module complements `itemloaders.processors`
with custom processors.
"""


class TakeMax:
    """Returns the maximum of the list of values."""
    def __call__(self, values):
        return max(values)
