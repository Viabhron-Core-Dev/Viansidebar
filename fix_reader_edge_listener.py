with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "r") as f:
    content = f.read()

old_case = '"handle_reader_y", "handle_reader_width", "handle_reader_height", "handle_reader_color", "handle_reader_shape" -> {'
new_case = '"handle_reader_y", "handle_reader_width", "handle_reader_height", "handle_reader_color", "handle_reader_shape", "handle_reader_edge" -> {'

content = content.replace(old_case, new_case)

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "w") as f:
    f.write(content)
