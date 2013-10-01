from utils.aux_utils import produce_resized_image, transliterate
from tradenplay.settings import CATEGORY_BANNER_SIZE, THUMBNAIL_SIZE


def add_m2m_connections(sender, **kwargs):
    """
    This function is called every time, the save signal is called on a model.
    Currently works only with catalog model(fields hardcoded) but can be easily
    generalized to work with any category.
    It is only acceptable to use this function for staff and development needs.
    In high-load production it will be ineffective because of the (at-least)
    triple db hit
    """

    # Create function-wide variables.
    instance = kwargs.get('instance')
    instance_parent_keys = instance.parent_categories.values('pk')
    instance_child_keys = instance.child_categories.values('pk')

    # Connect with parents.
    for item in instance_parent_keys:
        object = instance.__class__.objects.get(pk=item['pk'])
        object.child_categories.add(instance)
    # Connect with children.
    for item in instance_child_keys:
        object = instance.__class__.objects.get(pk=item['pk'])
        object.parent_categories.add(instance)

    # Check and remove any obsolette(broken) connections.
    for item in instance.__class__.objects.all():
        # Create block-wide variables so to make the following code more slim.
        item_key = {'pk': item.pk}
        item_parent_keys = item.parent_categories.values('pk')
        item_child_keys = item.child_categories.values('pk')
        instance_key = {'pk': instance.pk}

        # Check if there are any disconnected children.
        if (item_key not in instance_parent_keys and
                instance_key in item_child_keys):
            item.child_categories.remove(instance)
        elif (item_key not in instance_child_keys and
                instance_key in item_parent_keys):
            item.parent_categories.remove(instance)


def remove_m2m_connections(sender, **kwargs):

    instance = kwargs.get('instance')

    for item in instance.parent_categories.values('pk'):
        object = instance.__class__.objects.get(pk=item['pk'])
        object.child_categories.remove(instance)

    for item in instance.child_categories.values('pk'):
        object = instance.__class__.objects.get(pk=item['pk'])
        object.parent_categories.remove(instance)


def create_thumbnail(sender, **kwargs):

    instance = kwargs.get('instance')

    if instance.image and not instance.thumbnail:
        simple_uploaded_file = produce_resized_image(
            instance.image, THUMBNAIL_SIZE)
        instance.thumbnail.save(
            'thumbnail' + simple_uploaded_file.name + '.png', simple_uploaded_file, save=False)


def create_category_banner(sender, **kwargs):

    instance = kwargs.get('instance')
    if instance.image and not instance.banner:
        newname = transliterate(instance.name[0:20])
        simple_uploaded_file = produce_resized_image(
            instance.image, CATEGORY_BANNER_SIZE)
        instance.banner.save(
            'banner' + newname + '.png', simple_uploaded_file, save=True)
