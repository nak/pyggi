# -*- coding: utf-8 -*-

import time

html_escape_table = {
	"&": "&amp;",
	'"': "&quot;",
	"'": "&apos;",
	">": "&gt;",
	"<": "&lt;",
}


def format_datetime(value, format='iso8601'):
	# convert format to iso8601 compliant
	if format == 'iso8601':
		format = "%Y-%m-%d %H:%M:%S"
	
	# convert format to iso8601 compliant (full)
	if format == 'iso8601-full':
		format = "%a %b %d %H:%M:%S %Z %Y"

	return time.strftime(format, value)

def format_filesize(value):
	for x in ['bytes', 'kb', 'mb', 'gb', 'tb']:
		if value < 1024.0:
			return "%3.1f %s" % (value, x)
		value /= 1024.0

def format_diff(value):
	# escape HTML, because format_diff shall be used with 'safe'
	value = "".join(html_escape_table.get(c,c) for c in value)

	if value.startswith("+") and not value.startswith("+++"):
		return '<div class="diff-add">%s&nbsp;</div>' % value
	elif value.startswith("-") and not value.startswith("---"):
		return '<div class="diff-remove">%s&nbsp;</div>' % value
	elif value.startswith("@@"):
		return '<div class="diff-change">%s&nbsp;</div>' % value

	return '<div>%s</div>' % value

def is_git_tree(value):
	from git import Tree
	return isinstance(value, Tree)

