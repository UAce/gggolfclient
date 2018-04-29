class InputError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        value -- Error message
    """

    def __init__(self, value):
		self.value = value

    def __str__(self):
		return (self.value)


class NoResultException(Exception):

    def __init__(self, value):
		self.value = value

    def __str__(self):
		return (self.value)