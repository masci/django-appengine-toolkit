import pkg_resources
import os
import sys


class RequirementNotFoundError(Exception):
    pass


def collect_dependency_paths(package_name):
    """
    TODO docstrings
    """
    deps = []
    try:
        dist = pkg_resources.get_distribution(package_name)
    except (pkg_resources.DistributionNotFound, ValueError):
        message = "Distribution '{}' not found.".format(package_name)
        raise RequirementNotFoundError(message)

    if dist.has_metadata('top_level.txt'):
        for line in dist.get_metadata('top_level.txt').split():
            deps.append(os.path.join(dist.location, line))

    for req in dist.requires():
        deps.extend(collect_dependency_paths(req.project_name))

    return deps
