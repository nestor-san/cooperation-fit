from rest_framework.serializers import ValidationError


class GenericValidator:
    """A generic validator to be expanded for any model, if required"""

    # This part is the same for all validators

    def __init__(self, other_field):
        self.other_field = other_field  # Name of parameter

    def set_context(self, serializer_field):
        # name of field where validator is defined
        self.serializer_field = serializer_field

    def make_validation(self, field, other_field):
        pass

    def __call__(self, value):
        field = value
        serializer = self.serializer_field.parent
        # Data about the "other field"
        raw_other_field = serializer.initial_data[self.other_field]

        try:
            other_field = serializer.fields[self.other_field].run_validation(
                raw_other_field)
        except ValidationError:
            return

    # Here is the only part that changes

        self.make_validation(field, other_field)


class ProjectValidator(GenericValidator):
    """Validates the data of a new project, to ensure the user is the owner
    of the organization"""

    def make_validation(self, organization, user):
        message = 'The user isn\'t the owner of the organization'
        if organization.user.id != user.id:
            raise ValidationError(message)


class CooperationValidator(GenericValidator):
    """Validate the data of a cooperation, to ensure the user is owner of
    the organization"""

    def make_validation(self, project, user):
        message = """The user ins\'t the owner of the organization
                     related with this project"""
        if project.user.id != user.id:
            raise ValidationError(message)
