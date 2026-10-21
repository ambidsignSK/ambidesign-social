#!/usr/bin/env python3
"""Ambi Design – publikovanie na Facebook stránku a Instagram cez Meta Graph API.

Každý príspevok je priečinok v posts/<id>/ so súborom post.json:
{
  "publish_at": "2026-10-22T09:00:00+02:00",   # ISO 8601 s časovou zónou
  "type": "post" | "carousel" | "reel" | "story",
  "networks": ["facebook", "instagram"],
  "caption": "text príspevku",                  # pri story sa ignoruje
  "media": ["01.jpg", "02.jpg"],                # súbory v priečinku alebo absolútne https URL
  "cover_ms": 2500                              # voliteľné, titulný obrázok reelu (ms)
}

Stav publikovania sa zapisuje do state/published.json (commitne ho workflow).
Spustenie:  python publisher/publish.py            # publikuje všetko, čo je na rade
            python publisher/publish.py --check    # overí token, stránku a IG účet
            python publisher/publish.py --dry-run  # vypíše, čo by publikoval
"""
import json, os, sys, time, datetime as dt, pathlib, urllib.parse
import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "config.json").read_text())
GRAPH = f"https://graph.facebook.com/{CONFIG.get('graph_version', 'v23.0')}"
RUPLOAD = f"https://rupload.facebook.com/video-upload/{CONFIG.get('graph_version', 'v23.0')}"
PAGE_ID = CONFIG["page_id"]
TOKEN = os.environ.get("META_PAGE_TOKEN", "")
STATE_FILE = ROOT / "state" / "published.json"
MAX_ATTEMPTS = 3
GRACE_HOURS = 36  # starší nepublikovaný príspevok už nepublikujeme (aby nevyšlo niečo neaktuálne)


class GraphError(Exception):
    pass


def api(method, path, **params):
    url = path if path.startswith("http") else f"{GRAPH}/{path}"
    params["access_token"] = TOKEN
    r = requests.request(method, url, data=params if method == "POST" else None,
                         params=params if method == "GET" else None, timeout=120)
    try:
        js = r.json()
    except ValueError:
        raise GraphError(f"{r.status_code} {r.text[:300]}")
    if r.status_code >= 400 or "error" in js:
        err = js.get("error", {})
        raise GraphError(f"{err.get('code')}/{err.get('error_subcode')} {err.get('message')}")
    return js


def media_url(post_dir, name):
    if name.startswith("http"):
        return name
    rel = post_dir.relative_to(ROOT).as_posix()
    return f"https://raw.githubusercontent.com/{CONFIG['repo']}/{CONFIG.get('branch', 'main')}/{rel}/{urllib.parse.quote(name)}"


def ig_user_id():
    js = api("GET", PAGE_ID, fields="instagram_business_account{id,username}")
    acc = js.get("instagram_business_account")
    if not acc:
        raise GraphError("Stránka nemá prepojený Instagram business účet")
    return acc["id"]


# ------------------------------------------------------------------ Instagram
def ig_wait(container_id, timeout=600):
    start = time.time()
    while time.time() - start < timeout:
        st = api("GET", container_id, fields="status_code,status").get("status_code")
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            info = api("GET", container_id, fields="status").get("status")
            raise GraphError(f"IG kontajner {st}: {info}")
        time.sleep(10)
    raise GraphError("IG kontajner sa nespracoval včas")


def ig_publish(ig, post, urls):
    t, cap = post["type"], post.get("caption", "")
    if t == "post":
        c = api("POST", f"{ig}/media", image_url=urls[0], caption=cap)["id"]
    elif t == "carousel":
        kids = [api("POST", f"{ig}/media", image_url=u, is_carousel_item="true")["id"] for u in urls]
        for k in kids:
            ig_wait(k, 120)
        c = api("POST", f"{ig}/media", media_type="CAROUSEL", children=",".join(kids), caption=cap)["id"]
    elif t == "reel":
        p = dict(media_type="REELS", video_url=urls[0], caption=cap, share_to_feed="true")
        if post.get("cover_ms") is not None:
            p["thumb_offset"] = str(post["cover_ms"])
        c = api("POST", f"{ig}/media", **p)["id"]
    elif t == "story":
        if is_video(urls[0]):
            c = api("POST", f"{ig}/media", media_type="STORIES", video_url=urls[0])["id"]
        else:
            c = api("POST", f"{ig}/media", media_type="STORIES", image_url=urls[0])["id"]
    else:
        raise GraphError(f"Neznámy typ {t}")
    ig_wait(c)
    mid = api("POST", f"{ig}/media_publish", creation_id=c)["id"]
    link = api("GET", mid, fields="permalink").get("permalink", "")
    return {"id": mid, "url": link}


# ------------------------------------------------------------------ Facebook
def fb_hosted_video(edge, url, finish_params):
    start = api("POST", f"{PAGE_ID}/{edge}", upload_phase="start")
    vid = start["video_id"]
    up = requests.post(start.get("upload_url", f"{RUPLOAD}/{vid}"),
                       headers={"Authorization": f"OAuth {TOKEN}", "file_url": url}, timeout=300)
    if up.status_code >= 400:
        raise GraphError(f"FB upload {up.status_code} {up.text[:300]}")
    res = api("POST", f"{PAGE_ID}/{edge}", upload_phase="finish", video_id=vid, **finish_params)
    return res.get("post_id") or vid


def fb_publish(post, urls):
    t, cap = post["type"], post.get("caption", "")
    if t == "post":
        r = api("POST", f"{PAGE_ID}/photos", url=urls[0], message=cap)
        pid = r.get("post_id", r["id"])
    elif t == "carousel":
        ids = [api("POST", f"{PAGE_ID}/photos", url=u, published="false")["id"] for u in urls]
        params = {"message": cap}
        for i, x in enumerate(ids):
            params[f"attached_media[{i}]"] = json.dumps({"media_fbid": x})
        pid = api("POST", f"{PAGE_ID}/feed", **params)["id"]
    elif t == "reel":
        pid = fb_hosted_video("video_reels", urls[0], {"video_state": "PUBLISHED", "description": cap})
    elif t == "story":
        if is_video(urls[0]):
            pid = fb_hosted_video("video_stories", urls[0], {})
        else:
            photo = api("POST", f"{PAGE_ID}/photos", url=urls[0], published="false")["id"]
            pid = api("POST", f"{PAGE_ID}/photo_stories", photo_id=photo).get("post_id", photo)
    else:
        raise GraphError(f"Neznámy typ {t}")
    return {"id": pid, "url": f"https://facebook.com/{pid}"}


def is_video(u):
    return u.lower().split("?")[0].endswith((".mp4", ".mov"))


# ------------------------------------------------------------------ main loop
def load_state():
    return json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}


def save_state(s):
    STATE_FILE.parent.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(s, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def due_posts(now):
    out = []
    for pj in sorted((ROOT / "posts").glob("*/post.json")):
        post = json.loads(pj.read_text())
        when = dt.datetime.fromisoformat(post["publish_at"])
        out.append((when, pj.parent, post))
    return [(w, d, p) for w, d, p in sorted(out, key=lambda x: x[0]) if w <= now]


def main():
    args = set(sys.argv[1:])
    if not TOKEN:
        print("META_PAGE_TOKEN zatiaľ nie je nastavený – nič nepublikujem.")
        return
    if "--check" in args:
        page = api("GET", PAGE_ID, fields="name,instagram_business_account{id,username}")
        print("Stránka:", page.get("name"))
        print("Instagram:", page.get("instagram_business_account"))
        dbg = requests.get(f"{GRAPH}/debug_token", params={"input_token": TOKEN, "access_token": TOKEN}, timeout=30).json()
        d = dbg.get("data", {})
        print("Token platný:", d.get("is_valid"), "| expiruje:", d.get("expires_at") or "nikdy", "| oprávnenia:", ",".join(d.get("scopes", [])))
        return
    if not CONFIG.get("active", True) and "--dry-run" not in args:
        print("Publikovanie je vypnuté (config.json: active=false).")
        return
    now = dt.datetime.now(dt.timezone.utc)
    state = load_state()
    ig = None
    failures = 0
    for when, pdir, post in due_posts(now):
        key = pdir.name
        st = state.setdefault(key, {})
        if now - when > dt.timedelta(hours=GRACE_HOURS) and not any(v.get("ok") for v in st.values()):
            if not st.get("_skipped"):
                st["_skipped"] = f"vynechané – príliš staré ({when.isoformat()})"; print("SKIP", key)
            continue
        urls = [media_url(pdir, m) for m in post["media"]]
        for net in post.get("networks", ["facebook", "instagram"]):
            ns = st.setdefault(net, {"attempts": 0})
            if ns.get("ok") or ns["attempts"] >= MAX_ATTEMPTS:
                continue
            if "--dry-run" in args:
                print("DRY", key, net, post["type"], urls); continue
            ns["attempts"] += 1
            try:
                if net == "instagram":
                    ig = ig or ig_user_id()
                    res = ig_publish(ig, post, urls)
                else:
                    res = fb_publish(post, urls)
                ns.update(ok=True, **res, at=dt.datetime.now(dt.timezone.utc).isoformat()); ns.pop("error", None)
                print("OK  ", key, net, res.get("url"))
            except Exception as e:  # noqa
                ns["error"] = str(e)[:500]; failures += 1
                print("FAIL", key, net, e)
            save_state(state)
    save_state(state)
    if failures:
        sys.exit(f"{failures} publikovanie(í) zlyhalo – pozri state/published.json")


if __name__ == "__main__":
    main()
