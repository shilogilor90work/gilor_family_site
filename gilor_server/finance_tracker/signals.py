# finance_tracker/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import FamilyMember

@receiver(post_save, sender=User)
def create_family_member_for_new_user(sender, instance, created, **kwargs):
    """
    Signal handler to create a FamilyMember profile whenever a new User is created.
    It expects 'family_member_name' to be present in the instance's '_meta.serializer_fields'
    if created via the registration serializer, otherwise it defaults to the username.
    """
    if created:
        # Check if the 'family_member_name' was passed during user creation
        # This is a bit of a hacky way to get data from serializer to signal,
        # A more robust solution might be to pass it explicitly or use a custom manager.
        # For simplicity, we'll try to get it from a temporary attribute set by the serializer (if possible)
        # or from the serializer's validated_data if we custom-handle the create in the serializer.
        # Given our UserRegistrationSerializer's create method already pops it,
        # we need to pass it explicitly to the signal if we want to use it here for the name.
        # A simpler default for now:
        family_member_name = getattr(instance, '_family_member_name_from_registration', instance.username)

        # To get family_member_name from the serializer, you'd need to pass it from serializer.create
        # For this setup, the serializer handles the pop and creation of the user.
        # The serializer's `create` method pops `family_member_name`.
        # So, we'll try to extract it from the serializer's context or fall back to username.
        # Let's adjust the serializer to attach the name to the user instance temporarily.
        # Alternatively, we just use the username as the default member name upon user creation.
        # Let's assume the serializer passed the name to the instance temporarily.

        # Retrieve the family_member_name that was associated with the serializer
        # This is passed from the serializer's create method in the UserRegistrationSerializer.
        # (See the modified UserRegistrationSerializer.create method that adds this attribute)
        family_member_name = kwargs.get('family_member_name_from_serializer', instance.username)


        # Create the FamilyMember instance
        FamilyMember.objects.create(user=instance, name=family_member_name)