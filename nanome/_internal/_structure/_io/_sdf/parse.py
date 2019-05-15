from .content import Content
import re

def parse_file(path):
    try:
        with open(path) as f:
            lines = [line.rstrip() for line in f]
        content = parse_string(lines)
        return content
    except:
        print("Could not read sdf file: " + path)
        raise

def parse_string(lines):
    lines_by_model = []
    lines_by_model.append([])
    for line in lines:
        if "$$$$" in line:
            lines_by_model.append([])
        else:
            lines_by_model[-1].append(line)
    content = Content()
    for model_lines in lines_by_model:
        model = parse_model(model_lines)
        if len(model.atoms) > 0:
            content.models.append(model)
    return content


def parse_model(lines):
    # content
    try:
        model = Content.Model()
        version = "V2000"

        atom_serial = 0
        bond_serial = 0
        atom_counter = 0
        bond_counter = 0
        segment_stack = []

        line_counter = 0
        total_lines = len(lines)
        while (line_counter < total_lines):
            line = lines[line_counter]
            if line_counter == 0:
                model.name = line
            if line_counter == 1:
                model.author = line
            if line_counter == 2:
                model.comment = line
            if line_counter == 3:
                atom_counter = record_chunk_int(line, 1, 3)
                bond_counter = record_chunk_int(line, 4, 6)
                if ("V3000" in line):
                    version = "V3000"
            if line_counter > 3:
                if version == "V2000":
                    if atom_counter > 0:
                        atom_serial = atom_serial + 1
                        atom = Content.Atom()
                        atom.serial = atom_serial
                        atom.x = record_chunk_float(line, 1, 10)
                        atom.y = record_chunk_float(line, 11, 20)
                        atom.z = record_chunk_float(line, 21, 30)
                        atom.symbol = record_chunk_string(line, 31, 33)
                        model.atoms.append(atom)
                        atom_counter = atom_counter - 1
                    elif bond_counter > 0:
                        bond_serial = bond_serial + 1
                        bond = Content.Bond()
                        bond.serial = bond_serial
                        bond.serial_atom1 = record_chunk_int(line, 1, 3)
                        bond.serial_atom2 = record_chunk_int(line, 4, 6)
                        bond.bond_order = record_chunk_int(line, 7, 9)
                        model.bonds.append(bond)
                        bond_counter = bond_counter - 1
                    elif (line[0] == 'm'):
                        model.properties.append(line)
                elif version == "V3000":
                    parts = line.split()
                    if (len(parts) >= 4):
                        if parts[0] == "M" and parts[1] == "V30":
                            if parts[2] == "BEGIN":
                                segment_stack.append(parts[3])
                            elif parts[2] == "END":
                                segment_stack.pop()
                            else:
                                current_segment = segment_stack[-1]
                                if current_segment == "ATOM" and len(parts) >= 7:
                                    atom = Content.Atom()
                                    atom.x = float(parts[4])
                                    atom.y = float(parts[5])
                                    atom.z = float(parts[6])
                                    atom.serial = int(parts[2])
                                    atom.symbol = parts[3]
                                    model.atoms.append(atom)
                                elif current_segment == "BOND" and len(parts) >= 6:
                                    bond = Content.Bond()
                                    bond.serial = int(parts[2])
                                    bond.bond_order = int(parts[3])
                                    bond.serial_atom1 = int(parts[4])
                                    bond.serial_atom2 = int(parts[5])
                                    model.bonds.append(bond)
                if (line[0] == '>'):
                    regexpression = re.compile(r">\s+<(.+?)>")
                    title = re.match(regexpression, line).group(0)
                    line_counter = line_counter + 1
                    data = ""
                    # read line until you see another comment or the end of the molecule
                    while (line_counter < total_lines):
                        if len(lines[line_counter]) > 0:  #skip empty lines
                            if lines[line_counter][0] == '>' or "$$$$" in lines[line_counter]:
                                line_counter = line_counter - 1
                                break
                            else:
                                data = data + lines[line_counter]
                        line_counter = line_counter + 1
                    if title == "":
                        title = "misc"
                    if title in model._associated:
                        model._associated[title] = model._associated[title] + data
                    else:
                        model._associated[title] = data
            line_counter = line_counter + 1
        model.version = version
        return model
    except:
        print("SDF Parsing error")
        #           Logs.error("SDF Parsing error", e.Message + e.StackTrace)
        raise

def record_chunk_float(line, start, end):
    str = record_chunk_string(line, start, end)
    return float(str)


def record_chunk_int(line, start, end):
    str = record_chunk_string(line, start, end)
    return int(str)


def record_chunk_string(line, start, end):
    true_start = start - 1
    true_end = min(end, len(line))
    return line[true_start:true_end].strip()