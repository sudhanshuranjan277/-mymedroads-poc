import re

with open("output/page.html", "r", encoding="utf-8") as f:
    html = f.read()

patterns = [
    r'fetch\((.*?)\)',
    r'\$.ajax\((.*?)\)',
    r'\$.get\((.*?)\)',
    r'\$.post\((.*?)\)',
    r'url\s*:\s*["\'](.*?)["\']',
    r'/api/.*?',
    r'GetDoctors.*?',
    r'Doctor.*?ashx',
    r'Doctor.*?asmx',
    r'Doctor.*?svc',
]

for p in patterns:
    print("=" * 80)
    print("Pattern:", p)
    matches = re.findall(p, html, flags=re.I | re.S)
    print(matches[:20])