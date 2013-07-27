from tradenplay import settings

def project_constants(HttpRequest):
    return {'STATIC_URL': settings.STATIC_URL,
            'IMG_UPLD_DIR': settings.IMG_UPLD_DIR
           }