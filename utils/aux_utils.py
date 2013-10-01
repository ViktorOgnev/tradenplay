# -*- coding: utf-8 -*-

import re
import os
import hashlib
import random
from string import letters
from cStringIO import StringIO

from django.utils.translation import ugettext_lazy as _
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from tradenplay.settings import IMG_UPLD_DIR


# utility functions that can possibly be common for several models
def _make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))


def make_hash(string1, string2, salt=None):
    if not salt:
        salt = _make_salt()
    hash = hashlib.sha256(string1 + string2 + salt).hexdigest()
    return '%s,%s' % (salt, hash)


# "TODO: implement image name using hashlib""
def get_image_path(instance, filename):
    """
    This one depends on the existence of the
    instance's name.
    Build a path like "IMG_UPLD_DIR/instance_title/filename".
    """
    try:
        obj_name = instance.name
    except AttributeError:
        try:
            obj_name = instance.title
        except AttributeError:
            return _("Please reconstruct your model so that it has a 'title' or"
                     "'name' property"
                     )

    instance_subdir = space_to_underscore(transliterate(obj_name[0:20]))
    newname = space_to_underscore(transliterate(filename))
    return os.path.join(IMG_UPLD_DIR, instance_subdir, newname)


def space_to_underscore(string):
    return string.replace(' ', '_').replace('%20', '_').replace('%22', '_')


def produce_resized_image(image_field, size):

    pw = image_field.width
    ph = image_field.height
    nw = size[0]
    nh = size[1]

    filename = str(image_field.path)
    image = Image.open(filename)

    # only do this if the image needs resizing
    if (pw, ph) != (nw, nh):

        pr = float(pw) / float(ph)
        nr = float(nw) / float(nh)

        if pr > nr:
            # image_field aspect is wider than destination ratio
            tw = int(round(nh * pr))
            image = image.resize((tw, nh), Image.ANTIALIAS)
            l = int(round((tw - nw) / 2.0))
            image = image.crop((l, 0, l + nw, nh))
        elif pr < nr:
            # image_field aspect is taller than destination ratio
            th = int(round(nw / pr))
            image = image.resize((nw, th), Image.ANTIALIAS)
            t = int(round((th - nh) / 2.0))
            #print((0, t, nw, t + nh))
            image = image.crop((0, t, nw, t + nh))
        else:
            # image_field aspect matches the destination ratio
            image = image.resize(size, Image.ANTIALIAS)

    # Save the image
    temp_handle = StringIO()
    image.save(temp_handle, 'png')
    temp_handle.seek(0)

    return SimpleUploadedFile(os.path.split(image_field.name)[-1],
                              temp_handle.read(), content_type='image/png')


def transliterate(string):

    capital_letters = {u'А': u'A',
                       u'Б': u'B',
                       u'В': u'V',
                       u'Г': u'G',
                       u'Д': u'D',
                       u'Е': u'E',
                       u'Ё': u'E',
                       u'З': u'Z',
                       u'И': u'I',
                       u'Й': u'Y',
                       u'К': u'K',
                       u'Л': u'L',
                       u'М': u'M',
                       u'Н': u'N',
                       u'О': u'O',
                       u'П': u'P',
                       u'Р': u'R',
                       u'С': u'S',
                       u'Т': u'T',
                       u'У': u'U',
                       u'Ф': u'F',
                       u'Х': u'H',
                       u'Ъ': u'',
                       u'Ы': u'Y',
                       u'Ь': u'',
                       u'Э': u'E', }

    capital_letters_transliterated_to_multiple_letters = {u'Ж': u'Zh',
                                                          u'Ц': u'Ts',
                                                          u'Ч': u'Ch',
                                                          u'Ш': u'Sh',
                                                          u'Щ': u'Sch',
                                                          u'Ю': u'Yu',
                                                          u'Я': u'Ya', }

    lower_case_letters = {u'а': u'a',
                          u'б': u'b',
                          u'в': u'v',
                          u'г': u'g',
                          u'д': u'd',
                          u'е': u'e',
                          u'ё': u'e',
                          u'ж': u'zh',
                          u'з': u'z',
                          u'и': u'i',
                          u'й': u'y',
                          u'к': u'k',
                          u'л': u'l',
                          u'м': u'm',
                          u'н': u'n',
                          u'о': u'o',
                          u'п': u'p',
                          u'р': u'r',
                          u'с': u's',
                          u'т': u't',
                          u'у': u'u',
                          u'ф': u'f',
                          u'х': u'h',
                          u'ц': u'ts',
                          u'ч': u'ch',
                          u'ш': u'sh',
                          u'щ': u'sch',
                          u'ъ': u'',
                          u'ы': u'y',
                          u'ь': u'',
                          u'э': u'e',
                          u'ю': u'yu',
                          u'я': u'ya', }

    capital_and_lower_case_letter_pairs = {}

    for capital_letter, capital_letter_translit in \
        capital_letters_transliterated_to_multiple_letters.iteritems():

        for lowercase_letter, lowercase_letter_translit in lower_case_letters.iteritems():
            capital_and_lower_case_letter_pairs[u"%s%s" % (capital_letter,
                                                lowercase_letter)] = \
                u"%s%s" % (capital_letter_translit, lowercase_letter_translit)

    for dictionary in (capital_and_lower_case_letter_pairs,
                       capital_letters, lower_case_letters):

        for cyrillic_string, latin_string in dictionary.iteritems():
            string = re.sub(cyrillic_string, latin_string, string)

    for cyrillic_string, latin_string in \
        capital_letters_transliterated_to_multiple_letters.iteritems():
        string = re.sub(cyrillic_string, latin_string.upper(), string)

    return string
