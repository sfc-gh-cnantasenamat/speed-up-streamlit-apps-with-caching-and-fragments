import os, re, zipfile
base = "/Users/cnantasenamat/Documents/Coco"
d = f"{base}/speed-up-streamlit-apps-with-caching-and-fragments"
md = open(f"{d}/speed-up-streamlit-apps-with-caching-and-fragments.md").read()
refs = re.findall(r"\]\((assets/[^)]+)\)", md)
print("missing:", [r for r in refs if not os.path.exists(f"{d}/{r}")], "refs:", len(refs))
print("dashes:", md.count("\u2014") + md.count("\u2013"))
z = f"{d}.zip"
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(d):
        dirs[:] = [x for x in dirs if not x.startswith(".") and x != "_local"]
        for f in files:
            if f.startswith("."):
                continue
            p = os.path.join(root, f)
            zf.write(p, os.path.relpath(p, base))
print("zip entries:", len(zipfile.ZipFile(z).namelist()))
