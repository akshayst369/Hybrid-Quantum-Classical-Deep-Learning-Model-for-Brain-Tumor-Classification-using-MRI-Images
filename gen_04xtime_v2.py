"""
04 Xtime GF multiplier — QCA layout generator (v2)

Clones the mentor's verified, published 9-cell XOR gate (from Mangalam,
Rajasekar, Sakthivel 2026, J. Comput. Electron.) six times for the five
XOR terms needed (one term, b'4, needs 2 cascaded XORs since it has 3
operands), and adds three straight 20nm-pitch wire passthroughs built
from scratch with a real INPUT cell, real OUTPUT cell, and correctly
spaced NORMAL cells in between -- not reused/hacked XOR-template
geometry like v1.

Logic source: Rajasekar, Mangalam, Shakthi Murugan, Kalaiselvi (2025),
J. Comput. Electron., Table 1, "04 multiplication" column:
    b'0 = b6
    b'1 = b6 XOR b7
    b'2 = b0 XOR b7
    b'3 = b1 XOR b6
    b'4 = b2 XOR b6 XOR b7   (cascade: t4 = b2 XOR b6;  b'4 = t4 XOR b7)
    b'5 = b3 XOR b7
    b'6 = b4
    b'7 = b5

All 6 XOR instances are exact geometric clones of the reference cell
(same relative dot positions / charges), just translated on Y so each
instance sits on its own row -- no overlap, no coupling between rows
(row pitch 260nm, far beyond the 80nm default radius of effect).
"""

import re

REF_PATH = "9cell_original.qca"
OUT_PATH = "04xtime_multiplier_v2.qca"

CELL_PITCH = 20.0  # standard QCA cell-to-cell distance (confirmed by QCADesigner-E manual)

HEADER = "[VERSION]\r\nqcadesigner_version=2.000000\r\n[#VERSION]\r\n[TYPE:DESIGN]\r\n"
MAIN_LAYER_OPEN = "[TYPE:QCADLayer]\r\ntype=1\r\nstatus=0\r\npszDescription=Main Cell Layer\r\n"
FOOTER = "[#TYPE:QCADLayer]\r\n[#TYPE:DESIGN]\r\n"


def substrate_block(cx, cy, w, h):
    return (
        "[TYPE:QCADLayer]\r\ntype=3\r\nstatus=1\r\npszDescription=Drawing Layer\r\n[#TYPE:QCADLayer]\r\n"
        "[TYPE:QCADLayer]\r\ntype=0\r\nstatus=1\r\npszDescription=Substrate\r\n[TYPE:QCADSubstrate]\r\n"
        "[TYPE:QCADStretchyObject]\r\n[TYPE:QCADDesignObject]\r\n"
        f"x={cx:.6f}\r\ny={cy:.6f}\r\nbSelected=FALSE\r\n"
        "clr.red=65535\r\nclr.green=65535\r\nclr.blue=65535\r\n"
        "bounding_box.xWorld=0.000000\r\nbounding_box.yWorld=0.000000\r\n"
        f"bounding_box.cxWorld={w:.6f}\r\nbounding_box.cyWorld={h:.6f}\r\n"
        "[#TYPE:QCADDesignObject]\r\n[#TYPE:QCADStretchyObject]\r\n"
        "grid_spacing=20.000000\r\n[#TYPE:QCADSubstrate]\r\n[#TYPE:QCADLayer]\r\n"
    )


def parse_cells(text):
    cells = []
    pattern = re.compile(r'\[TYPE:QCADCell\](.*?)\[#TYPE:QCADCell\]', re.DOTALL)
    for m in pattern.finditer(text):
        body = m.group(1)
        x = float(re.search(r'\nx=([\d.]+)', body).group(1))
        y = float(re.search(r'\ny=([\d.]+)', body).group(1))
        func = re.search(r'cell_function=(\S+)', body).group(1)
        label_m = re.search(r'psz=(\S+)', body)
        label = label_m.group(1) if label_m else None
        cells.append({'x': x, 'y': y, 'func': func, 'label': label, 'raw': body})
    return cells


def shift_and_relabel(raw_body, dx, dy, new_label=None, force_func=None):
    # Normalize internal newlines to \r\n
    raw_body = raw_body.replace("\r\n", "\n").replace("\n", "\r\n")

    def shift_coord(m):
        prefix = m.group(1)
        val = float(m.group(2))
        if prefix in ('x', 'bounding_box.xWorld'):
            new_val = val + dx
        else:
            new_val = val + dy
        return f"{prefix}={new_val:.6f}"

    # Shift cell and label centers (x, y) and bounding boxes (bounding_box.xWorld, bounding_box.yWorld)
    body = re.sub(r'(bounding_box\.xWorld|bounding_box\.yWorld|\bx|\by)=(-?[\d.]+)', shift_coord, raw_body)
    if force_func is not None:
        body = re.sub(r'cell_function=\S+', f'cell_function={force_func}', body)
    if new_label is not None and 'psz=' in body:
        body = re.sub(r'psz=\S+', f'psz={new_label}', body)
    return f"[TYPE:QCADCell]{body}[#TYPE:QCADCell]\r\n"


def clone_xor_block(template_cells, origin_x, origin_y, in_a_label, in_b_label, out_label):
    """Place an exact clone of the 9-cell XOR gate so its first Normal
    wire cell (template coords 100,160) lands at (origin_x, origin_y).
    Relabels only the A input, B input, and XOR output cells."""
    anchor_x, anchor_y = 100.0, 160.0
    dx, dy = origin_x - anchor_x, origin_y - anchor_y
    out = []
    for c in template_cells:
        label = c['label']
        new_label = None
        if label == 'A':
            new_label = in_a_label
        elif label == 'B':
            new_label = in_b_label
        elif label == 'XOR':
            new_label = out_label
        out.append(shift_and_relabel(c['raw'], dx, dy, new_label=new_label))
    return "".join(out)


def make_normal_cell_from_template(template_cells):
    """Grab one plain Normal cell's raw geometry (relative dot layout)
    to reuse as a stamp for wire cells."""
    normal = [c for c in template_cells if c['func'] == 'QCAD_CELL_NORMAL'][0]
    return normal['raw'], normal['x'], normal['y']


def make_io_cell_from_template(template_cells, which):
    """which = 'INPUT' or 'OUTPUT' -- grab a real Input or Output cell's
    raw geometry to reuse as a stamp."""
    if which == 'INPUT':
        c = [c for c in template_cells if c['func'] == 'QCAD_CELL_INPUT'][0]
    else:
        c = [c for c in template_cells if c['func'] == 'QCAD_CELL_OUTPUT'][0]
    return c['raw'], c['x'], c['y']


def build_wire(template_cells, start_x, start_y, in_label, out_label, n_normal=3):
    """Straight horizontal wire at 20nm pitch: INPUT -> n_normal x NORMAL -> OUTPUT.
    All cells placed on the same row (start_y), left to right, each exactly
    CELL_PITCH apart, using real cell geometry stamps (not hacked offsets)."""
    in_raw, in_tx, in_ty = make_io_cell_from_template(template_cells, 'INPUT')
    normal_raw, n_tx, n_ty = make_normal_cell_from_template(template_cells)
    out_raw, out_tx, out_ty = make_io_cell_from_template(template_cells, 'OUTPUT')

    parts = []
    x = start_x
    # input cell
    parts.append(shift_and_relabel(in_raw, x - in_tx, start_y - in_ty, new_label=in_label))
    x += CELL_PITCH
    # normal wire cells
    for _ in range(n_normal):
        parts.append(shift_and_relabel(normal_raw, x - n_tx, start_y - n_ty))
        x += CELL_PITCH
    # output cell (reuse OUTPUT stamp, relabel)
    parts.append(shift_and_relabel(out_raw, x - out_tx, start_y - out_ty, new_label=out_label))
    return "".join(parts)


def main():
    with open(REF_PATH, 'r', newline='') as f:
        ref_text = f.read()
    template_cells = parse_cells(ref_text)
    assert len(template_cells) == 9

    ROW_PITCH = 260.0   # generous vertical spacing between independent rows
    ROW_X = 100.0
    body_parts = []
    row = 0

    xor_specs = [
        ("b6", "b7", "b1_out"),
        ("b0", "b7", "b2_out"),
        ("b1", "b6", "b3_out"),
        ("b2", "b6", "t4"),        # intermediate
        ("t4", "b7", "b4_out"),    # cascaded 3-input XOR completion
        ("b3", "b7", "b5_out"),
    ]
    for a_lbl, b_lbl, out_lbl in xor_specs:
        oy = 160.0 + row * ROW_PITCH
        body_parts.append(clone_xor_block(template_cells, ROW_X, oy, a_lbl, b_lbl, out_lbl))
        row += 1

    wire_specs = [
        ("b6", "b0_out"),
        ("b4", "b6_out"),
        ("b5", "b7_out"),
    ]
    for in_lbl, out_lbl in wire_specs:
        oy = 160.0 + row * ROW_PITCH
        body_parts.append(build_wire(template_cells, ROW_X, oy, in_lbl, out_lbl))
        row += 1

    sub_w = 4000.0
    sub_h = 3000.0

    doc = (
        HEADER
        + substrate_block(sub_w / 2, sub_h / 2, sub_w, sub_h)
        + MAIN_LAYER_OPEN
        + "".join(body_parts)
        + FOOTER
    )

    with open(OUT_PATH, "wb") as f:
        f.write(doc.encode("ascii"))

    n_cells = doc.count("[TYPE:QCADCell]")
    print(f"Wrote {OUT_PATH}")
    print(f"Total cell count: {n_cells}  (expected 6*9 + 3*5 = 54+15 = 69)")


if __name__ == "__main__":
    main()
