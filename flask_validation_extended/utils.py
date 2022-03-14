from flask import g


def invalidate():
	g.deactivate_validator = True