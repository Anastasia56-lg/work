analyze_size() {
  local path="$1"
  if [ -d "$path" ]; then
    local size=$(du -sb "$path" | cut -f1)
    echo "$size Directory: $path"
  elif [ -f "$path" ]; then
    local size=$(stat --format=%s "$path")
    echo "$size File: $path"
  fi
}
main() {
  local items=()
  for item in *; do
    items+=("$(analyze_size "$item")")
  done
  sorted_file=$(mktemp)
  printf "%s\n" "${items[@]}" | sort -nr > "$sorted_file"
  local total_items=$(wc -l < "$sorted_file")
  local index=0
  local batch_size=10
  display_results() {
    local line
    for (( i=0; i<$batch_size; i++ )); do
      if [ $index -ge $total_items ]; then
        echo "No more items to display."
        return
      fi
      line=$(sed -n "$((index + 1))p" "$sorted_file")
      local size=$(echo "$line" | cut -d' ' -f1)
      local type_and_path=$(echo "$line" | cut -d' ' -f2-)
      local size_kb=$((size / 1024))
      echo "$type_and_path, Size: $size_kb KB"
      index=$((index + 1))
    done
  }
  while [ $index -lt $total_items ]; do
    display_results
    if [ $index -lt $total_items ]; then
      read -p "Show next 10 results? (y/n): " choice
      if [ "$choice" != "y" ]; then
        break
      fi
    fi
  done
  rm "$sorted_file"
}
main