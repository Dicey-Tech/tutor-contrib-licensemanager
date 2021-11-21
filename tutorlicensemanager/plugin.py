from glob import glob
import os
import pkg_resources

from .__about__ import __version__

templates = pkg_resources.resource_filename(
    "tutorlicensemanager", "templates"
)

config = {
    "add": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 24|random_string }}",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
        "OAUTH2_SECRET_SSO": "{{ 8|random_string }}",
    },
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}diceytech/license-manager:{{ LICENSEMANAGER_VERSION }}",
        "HOST": "licensemanager.{{ LMS_HOST }}",
        "MYSQL_DATABASE": "licensemanager",
        "MYSQL_USERNAME": "licensemanager",
        "OAUTH2_KEY": "licensemanager",
        "OAUTH2_KEY_DEV": "licensemanager-dev",
        "OAUTH2_KEY_SSO": "licensemanager-sso",
        "OAUTH2_KEY_SSO_DEV": "licensemanager-sso-dev",
        "CACHE_REDIS_DB": "{{ OPENEDX_CACHE_REDIS_DB }}",
    }
}

hooks = {
    "build-image": {"licensemanager": "{{ LICENSEMANAGER_DOCKER_IMAGE }}"},
    "init": ["mysql", "licensemanager", "lms"],
}


def patches():
    all_patches = {}
    patches_dir = pkg_resources.resource_filename(
        "tutorlicensemanager", "patches"
    )
    for path in glob(os.path.join(patches_dir, "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
