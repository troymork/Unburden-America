#!/usr/bin/env python3
import os, sys, datetime as dt

TEMPLATE = "certificate_template.svg"

def next_id(counter_file="counter.txt", prefix="ITEM"):
    n = 1
    if os.path.exists(counter_file):
        with open(counter_file) as f:
            try:
                n = int(f.read().strip()) + 1
            except:
                n = 1
    with open(counter_file,"w") as f:
        f.write(str(n))
    return f"{prefix}-{n:08d}"

def render(name, out_dir="out", date=None, cert_id=None, prefix="ITEM"):
    os.makedirs(out_dir, exist_ok=True)
    if cert_id is None:
        cert_id = next_id(os.path.join(out_dir,"counter.txt"), prefix=prefix)
    date = date or dt.date.today().isoformat()
    with open(TEMPLATE) as f:
        svg = f.read()
    svg = svg.replace("{{NAME}}", name).replace("{{DATE}}", date).replace("{{CERT_ID}}", cert_id)
    out_svg = os.path.join(out_dir, f"{cert_id}.svg")
    with open(out_svg, "w") as f:
        f.write(svg)
    print(out_svg)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: gen_cert.py 'Full Name' [PREFIX]")
        sys.exit(1)
    name = sys.argv[1]
    prefix = sys.argv[2] if len(sys.argv) > 2 else "ITEM"
    render(name, prefix=prefix)
