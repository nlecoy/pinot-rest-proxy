import os
import subprocess


def get_revision():
    revision = os.environ.get("BUILD_REVISION")
    if revision:
        return revision

    package_dir = os.path.dirname(__file__)
    checkout_dir = os.path.normpath(os.path.join(package_dir, os.pardir))
    path = os.path.join(checkout_dir, ".git")
    if os.path.exists(path):
        try:
            out = subprocess.check_output("git rev-parse HEAD", cwd=path, shell=True)
        except Exception:
            return None
        return out.strip().decode("utf-8")
    return None


def get_version():
    try:
        version = __import__("pkg_resources").get_distribution("pinot-rest-proxy").version
    except Exception:
        version = "unknown"
    return version


__build__ = get_revision()
__version__ = get_version()
