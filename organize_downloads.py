from argparse import ArgumentParser
from pathlib import Path
import os
import shutil


FILE_TYPE_FOLDERS = {
	"Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".svg"},
	"Documents": {".pdf", ".doc", ".docx", ".odt", ".rtf"},
	"Spreadsheets": {".xls", ".xlsx", ".csv", ".ods"},
	"Presentations": {".ppt", ".pptx", ".odp"},
	"Text": {".txt", ".md", ".json", ".xml", ".yaml", ".yml", ".log"},
	"Audio": {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"},
	"Video": {".mp4", ".mkv", ".mov", ".avi", ".wmv", ".webm"},
	"Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
	"Code": {".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".sh", ".bat", ".ps1"},
	"Others": set(),
}


def get_default_downloads_folder():
	if os.name == "nt":
		base_folder = Path(os.environ.get("USERPROFILE", Path.home()))
	else:
		base_folder = Path.home()

	return base_folder / "Downloads"


def get_folder_name(file_path):
	extension = file_path.suffix.lower()

	for folder_name, extensions in FILE_TYPE_FOLDERS.items():
		if extension in extensions:
			return folder_name

	return "Others"


def get_unique_destination(destination_folder, file_name):
	destination_path = destination_folder / file_name

	if not destination_path.exists():
		return destination_path

	stem = destination_path.stem
	extension = destination_path.suffix
	count = 1

	while True:
		new_destination = destination_folder / f"{stem}_{count}{extension}"
		if not new_destination.exists():
			return new_destination
		count += 1


def organize_downloads(downloads_folder):
	if not downloads_folder.exists():
		print(f"Downloads folder not found: {downloads_folder}")
		return

	files_moved = 0

	for item in downloads_folder.iterdir():
		if item.is_dir():
			continue

		folder_name = get_folder_name(item)
		target_folder = downloads_folder / folder_name
		target_folder.mkdir(exist_ok=True)

		destination_path = get_unique_destination(target_folder, item.name)
		shutil.move(str(item), str(destination_path))
		files_moved += 1
		print(f"Moved: {item.name} -> {folder_name}/")

	print(f"Done. Moved {files_moved} file(s).")


def parse_arguments():
	parser = ArgumentParser(description="Organize files in the Downloads folder by file type.")
	parser.add_argument(
		"--downloads-folder",
		type=Path,
		default=get_default_downloads_folder(),
		help="Path to the Downloads folder. Defaults to the current user's Downloads folder.",
	)
	return parser.parse_args()


def main():
	args = parse_arguments()
	organize_downloads(args.downloads_folder)



main()