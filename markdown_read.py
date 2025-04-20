def get_lines(file_path):
    lines = []
    with open(file_path, "r", encoding='utf-8') as file:
        for line in file:
            lines.append(line.strip())
    return lines