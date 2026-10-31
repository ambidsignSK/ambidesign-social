import json, shutil, pathlib, sys
from PIL import Image
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import plan_november as p
ROOT = pathlib.Path(__file__).resolve().parent.parent; EXP = pathlib.Path('/home/claude/exports')
for x in p.PLAN:
    d = ROOT / 'posts' / x['id']; d.mkdir(parents=True, exist_ok=True)
    t = x['type']
    if t == 'reel':
        shutil.copy(EXP / 'reels' / f"{x['id']}.mp4", d / 'reel.mp4'); media = ['reel.mp4']
    elif t == 'story':
        Image.open(EXP / f"{x['id']}.png").convert('RGB').save(d / '01.jpg', quality=93); media = ['01.jpg']
    else:
        src = sorted((EXP / x['id']).glob('*.jpg'))
        for f in src: shutil.copy(f, d / f.name)
        media = [f.name for f in src]
    post = {"publish_at": x['at'], "type": t, "networks": ["facebook", "instagram"],
            "caption": x.get('caption', ''), "media": media}
    if t == 'reel': post['cover_ms'] = 1000
    (d / 'post.json').write_text(json.dumps(post, ensure_ascii=False, indent=2) + '\n')
    print(x['id'], t, len(media), 'link' if 'ambidesign.eu' in post['caption'] else ('-' if t == 'story' else 'NOLINK'))
