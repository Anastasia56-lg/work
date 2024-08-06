import os
import stat
import tempfile
import subprocess

def analyze_size(path):
    if os.path.isdir(path):
        try:
            size = int(subprocess.check_output(['du', '-sb', path]).split()[0].decode('utf-8'))
            return f"{size} Directory: {path}"
        except subprocess.CalledProcessError as e:
            print(f"Error reading size of directory: {path}", file=sys.stderr)
            return None
    elif os.path.isfile(path):
        try:
            size = os.stat(path).st_size
            return f"{size} File: {path}"
        except OSError as e:
            print(f"Error reading size of file: {path}", file=sys.stderr)
            return None
    return None

def display_results(sorted_items, start_index, batch_size):
    for i in range(batch_size):
        if start_index >= len(sorted_items):
            print("No more items to display.")
            return start_index
        item = sorted_items[start_index]
        size = int(item.split(' ')[0])
        type_and_path = ' '.join(item.split(' ')[1:])
        size_kb = size // 1024
        print(f"{type_and_path}, Size: {size_kb} KB")
        start_index += 1
    return start_index

def main():
    items = []
    for item in os.listdir('.'):
        result = analyze_size(item)
        if result:
            items.append(result)

    if not items:
        print("No items to process.")
        return

    sorted_items = sorted(items, key=lambda x: int(x.split(' ')[0]), reverse=True)

    index = 0
    batch_size = 10

    while index < len(sorted_items):
        index = display_results(sorted_items, index, batch_size)
        if index < len(sorted_items):
            choice = input("Show next 10 results? (y/n): ").strip().lower()
            if choice != 'y':
                break

if __name__ == "__main__":
    main()