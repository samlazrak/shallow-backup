import json
from printing import *
from compatibility import *
from utils import home_prefix


def get_config_path():
	return home_prefix(".shallow-backup")


def get_config():
	"""
	Returns the config.
	:return: dictionary for config
	"""
	with open(get_config_path()) as f:
		config = json.load(f)
	return config


def write_config(config):
	"""
	Write to config file
	"""
	with open(get_config_path(), 'w') as f:
		json.dump(config, f, indent=4)


def prepare_config_path():
	"""
	Get compatible config paths, format them as [(LOC, DEST), ...]
	"""
	config_paths = get_config_paths()
	translations = {
		"terminal_plist": "plist/com.apple.Terminal.plist"
	}

	# Swap out keys for dest_paths
	for key, dest_path in translations.items():
		if key in config_paths:
			config_paths[dest_path] = config_paths[key]
			del config_paths[key]

	return dict([(v, k) for k, v in config_paths.items()])


def get_default_config():
	"""
	Returns a default, platform specific config.
	"""
	return {
		"backup_path"      : "~/shallow-backup",
		"dotfiles"         : [
			".bashrc",
			".bash_profile",
			".gitconfig",
			".profile",
			".pypirc",
			".shallow-backup",
			".vimrc",
			".zshrc"
		],
		"dotfolders"       : [
			".ssh",
			".vim"
		],
		"default-gitignore": [
			"dotfiles/.ssh",
			"packages/",
			"dotfiles/.pypirc",
		],
		"config_mapping"   : prepare_config_path()
	}


def safe_create_config():
	"""
	Creates config file if it doesn't exist already.
	"""
	backup_config_path = get_config_path()
	if not os.path.exists(backup_config_path):
		print_path_blue("Creating config file at:", backup_config_path)
		backup_config = get_default_config()
		write_config(backup_config)


def show_config():
	"""
	Print the config. Colorize section titles and indent contents.
	"""
	print_section_header("SHALLOW BACKUP CONFIG", Fore.RED)
	for section, contents in get_config().items():
		# Hide gitignore config
		if section == "default-gitignore":
			continue
		# Print backup path on same line
		elif section == "backup_path":
			print_path_red("Backup Path:", contents)
		elif section == "config_mapping":
			print_red_bold("Configs Path to Dest Mapping: ")
			for path, dest in contents.items():
				print("    {} -> {}".format(path, dest))
		# Print section header and intent contents. (Dotfiles/folders)
		else:
			print_red_bold("\n{}: ".format(section.capitalize()))
			for item in contents:
				print("    {}".format(item))

	print()
