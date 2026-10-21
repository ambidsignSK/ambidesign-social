"""Jednorazová migrácia zvyšných októbrových príspevkov z Metricoolu do posts/."""
import json, pathlib, shutil, urllib.request
ROOT = pathlib.Path(__file__).resolve().parent.parent
VID = pathlib.Path("/home/claude/reel/out_text")
M = "https://static.metricool.com/planner/202610/4407237-file-"

FEED = [
 ("2026-10-22T09:00:00+02:00", "pribeh-restauracia", "post", ["3614625840592745597"], """Typický príbeh reštaurácie 🍽️

Je 11:45. Hladný človek v práci hľadá na mobile, kam ísť na obed. Nájde váš web. Klikne na menu… a začne sa sťahovať PDF. Malé písmo, treba zväčšovať, posúvať do strán. Telefónne číslo je schované až v pätičke.

Zavrie to. O dve minúty sedí u konkurencie, ktorá mala menu rovno na stránke.

✅ Čo v takej situácii meníme:
• menu ako text priamo na webe, nie PDF
• tlačidlá Zavolať a Rezervovať hneď navrchu
• denné menu aj v Google profile firmy
• web, ktorý sa na mobile načíta za pár sekúnd

Web nie je výklad. Je to čašník, ktorý víta hostí.

Ako máte menu na webe vy? 👇

#restauracia #gastro #webstranka #marketing #malefirmy #slovensko"""),
 ("2026-10-23T14:00:00+02:00", "post-anketa", "post", ["2821272067744613875"], """Piatková anketa pre podnikateľov 📊

Koľko percent z tržieb dávate na marketing a reklamu?

A) menej ako 2 %
B) 2 – 5 %
C) 5 – 10 %
D) viac ako 10 %
E) nič, všetko ide z odporúčaní

Stačí napísať písmeno do komentára 👇 Je to anonymné v tom zmysle, že nikto nechce čísla, len rozsah.

Pekný víkend! ☀️

#marketing #podnikanie #malefirmy #zivnostnik #slovensko"""),
 ("2026-10-26T15:00:00+01:00", "karusel-metriky", "carousel", ["11937258836542751230", "14062886479615765730", "3685103249203450067", "4041150218011141162", "5479891990464450872", "3792699808355060241", "3880023183269626875"], """Pozeráte sa v Google Ads len na počet klikov? 📉

Kliky sú pekné číslo do reportu. O tom, či reklama zarába, rozhodujú iné metriky:

1️⃣ Skóre kvality
2️⃣ Miera prekliku (CTR)
3️⃣ Cena za konverziu
4️⃣ Miera konverzie
5️⃣ Podiel zobrazení

Potiahnite doprava 👉 pri každej je, čo s ňou robiť.

📌 Uložte si to na ďalšiu kontrolu kampane.

Ktorú z týchto metrík sledujete vy? 👇

#googleads #ppc #marketing #reklama #malefirmy #slovensko"""),
 ("2026-10-27T13:00:00+01:00", "pribeh-blog", "post", ["17318521407810533333"], """Typický príbeh firemného blogu ✍️

Firma poctivo píše. Každý mesiac článok: „Otvorili sme novú prevádzku“, „Boli sme na veľtrhu“, „Máme nového kolegu“. Po roku je na webe desiatky článkov… a z Googlu na ne nechodí takmer nikto.

Problém nie je v tom, že píšu. Problém je, o čom píšu. Píšu o sebe. Zákazníci však na Googli hľadajú odpovede na svoje otázky.

✅ Čo v takej situácii meníme:
• pred písaním zistíme, čo ľudia v danom odbore reálne hľadajú
• článok odpovedá na konkrétnu otázku zákazníka
• staré články aktualizujeme namiesto písania nových
• novinky o firme dávame na sociálne siete, nie na blog

Blog nie je firemná nástenka. Je to odpoveď na otázku, ktorú si zákazník práve zadal do Googlu.

O čom píšete na blogu vy? 👇

#seo #blog #obsahovymarketing #marketing #malefirmy #slovensko"""),
 ("2026-10-28T13:00:00+01:00", "post-mytus-vsade", "post", ["3570195029064412654"], """Mýtus: firma musí byť na každej sociálnej sieti. ❌

Facebook, Instagram, TikTok, LinkedIn, YouTube… a na každom posledný príspevok spred pol roka. Taký profil pôsobí horšie, ako keby ste tam neboli vôbec.

Čo funguje lepšie:
• vyberte 1 až 2 siete, kde sú vaši zákazníci
• publikujte pravidelne, aj keď menej často
• odpovedajte na komentáre a správy
• ostatné siete pridajte, až keď máte kapacitu

Jedna dobre vedená sieť porazí päť polomŕtvych.

📌 Uložte si to, keď vás znova napadne „mali by sme byť aj na…“

Na koľkých sieťach je vaša firma? 👇

#socialnesiete #marketing #facebook #instagram #malefirmy #slovensko"""),
 ("2026-10-29T09:00:00+01:00", "karusel-vianoce", "carousel", ["8556528401741042782", "8566824653654321747", "18312398064402871003", "11220177869530716539", "15391556282260348355", "7347838043224665844", "4297743375814736492"], """Na Vianoce je ešte ďaleko? Pre reklamu nie. 🎄

Kto začne s vianočnou reklamou v decembri, platí najdrahšie kliky a súťaží s každým. Kto sa pripraví v októbri, má v sezóne náskok.

5 vecí, ktoré pripraviť ešte tento mesiac:

1️⃣ Sezónne kľúčové slová
2️⃣ Publikum na remarketing
3️⃣ Funkčné meranie objednávok
4️⃣ Vianočná stránka s ponukou
5️⃣ Kreatívy pripravené vopred

Potiahnite doprava 👉 ku každému bodu je konkrétny krok.

Pošlite tento post tomu, kto u vás rieši marketing. 📩

#vianoce #eshop #googleads #metaads #marketing #slovensko"""),
 ("2026-10-30T14:00:00+01:00", "pribeh-eshop-vianoce", "post", ["1220103055209020161"], """Typický príbeh e-shopu pred Vianocami 🎁

Na začiatku decembra majiteľ zistí, že konkurencia už týždne beží s vianočnou reklamou. Narýchlo sa robia bannery, kampaň sa spúšťa v polovici decembra.

Čo sa stane:
• kliky sú v tom čase najdrahšie v roku
• algoritmus sa ešte len učí, a sezóna sa už končí
• zákazníci majú darčeky dávno nakúpené
• posledné objednávky nestihnú doručenie

Výsledok: veľa minutých peňazí a sklamanie z reklamy.

✅ Čo v takej situácii meníme:
• vianočnú kampaň plánujeme už v októbri
• od novembra zbierame publikum na remarketing
• kreatívy a vianočnú stránku máme hotové vopred
• termíny doručenia komunikujeme jasne a včas

Vianoce neprídu nečakane. Každý rok sú v rovnakom termíne. 😉

Kedy začínate s vianočnou reklamou vy? 👇

#eshop #vianoce #reklama #marketing #malefirmy #slovensko"""),
]
REELS = {
 "21": "Nie každý, kto uvidí reklamu, je rovnako cenný. 🎯\n\nNajlepšie výsledky prináša reklama na ľudí, ktorí vás už poznajú: návštevníci webu, diváci videí, existujúci zákazníci.\n\nCielite reklamu aj na nich? 👇\n\n#metaads #facebookreklama #retargeting #marketing #slovensko",
 "22": "Hladný zákazník na mobile nečaká. 📱\n\nMenu priamo na webe, tlačidlo Zavolať hneď navrchu a aktuálny profil v Google Mapách. Tri veci, ktoré rozhodnú, kde bude obedovať.\n\nAko vyzerá váš web na mobile? 👇\n\n#gastro #restauracia #webstranka #googlemapy #slovensko",
 "23": "Nejde o to minúť na reklamu čo najviac. 📊\n\nIde o to vedieť, čo každé euro prináša. Bez merania je aj dobrá kampaň len odhad.\n\nMeriate návratnosť svojej reklamy? 👇\n\n#marketing #reklama #podnikanie #malefirmy #slovensko",
 "24": "Zákazník sa opýta AI a dostane jednu odpoveď. 🤖\n\nBudete v nej? Jasné odpovede na webe, recenzie a zmienky o vás na iných weboch zvyšujú šancu, že vás AI odporučí.\n\nSkúšali ste sa opýtať ChatGPT na svoju firmu? 👇\n\n#aivyhladavanie #chatgpt #seo #marketing #slovensko",
 "25": "Keď vás niekto hľadá v okolí, rozhoduje Google profil. 📍\n\nAktuálne otváracie hodiny, fotky a recenzie s odpoveďami. To je vaša výkladná skriňa na mape.\n\nKedy ste naposledy aktualizovali ten svoj? 👇\n\n#lokalneseo #googlemapy #recenzie #malefirmy #slovensko",
 "26": "Kliky nie sú výsledok. 📈\n\nPozerajte sa na cenu za konverziu, mieru konverzie a skóre kvality. Tieto čísla rozhodujú, či reklama zarába.\n\nKtoré číslo sledujete ako prvé? 👇\n\n#googleads #ppc #reklama #marketing #slovensko",
 "27": "Blog, ktorý nikto nečíta, nemá problém v písaní, ale v témach. 📝\n\nPíšte o tom, čo zákazníci hľadajú – nie o tom, čo sa deje vo firme.\n\nO čom píšete vy? 👇\n\n#seo #blog #obsahovymarketing #marketing #slovensko",
 "28": "Päť sietí s posledným príspevkom spred pol roka? 🙈\n\nLepšie je mať jednu, ktorú vediete poriadne a pravidelne.\n\nKoľko sietí reálne zvládate? 👇\n\n#socialnesiete #facebook #instagram #marketing #slovensko",
 "29": "Vianoce v reklame sa začínajú teraz. 🎄\n\nKľúčové slová, publikum na remarketing, meranie a kreatívy. Kto to má hotové v októbri, má v decembri náskok.\n\nMáte už vianočnú kampaň v pláne? 👇\n\n#vianoce #eshop #googleads #metaads #slovensko",
 "30": "Kampaň spustená v polovici decembra = najdrahšie kliky a málo času. ⏰\n\nVianočný predaj sa pripravuje vopred, nie na poslednú chvíľu.\n\nKedy začínate s vianočnou reklamou vy? 👇\n\n#eshop #vianoce #reklama #marketing #slovensko",
 "31": "Október v skratke: SEO, reklama, publiká, metriky, web a príprava na Vianoce. ✅\n\nKtorá téma vám dala najviac?\n\nNapíšte do komentára, o čom chcete viac v novembri 👇\n\n#marketing #seo #googleads #metaads #slovensko",
}

def tz(day): return "+02:00" if int(day) < 25 or (int(day) == 25 and False) else "+01:00"

def write(folder, post):
    d = ROOT / "posts" / folder; d.mkdir(parents=True, exist_ok=True)
    (d / "post.json").write_text(json.dumps(post, ensure_ascii=False, indent=2) + "\n")
    return d

for when, slug, typ, files, cap in FEED:
    folder = when[:16].replace(":", "-").replace("T", "_") + "_" + slug
    d = ROOT / "posts" / folder; d.mkdir(parents=True, exist_ok=True)
    names = []
    for i, f in enumerate(files, 1):
        n = f"{i:02d}.jpg"; names.append(n)
        if not (d / n).exists():
            urllib.request.urlretrieve(M + f + ".jpeg", d / n)
    write(folder, {"publish_at": when, "type": typ, "networks": ["facebook", "instagram"], "caption": cap, "media": names})

for day, cap in REELS.items():
    off = "+02:00" if int(day) <= 24 else "+01:00"
    for kind, hh in (("reel", "18:00"), ("story", "11:00")):
        if day == "21" and kind == "story":
            continue  # už publikované
        folder = f"2026-10-{day}_{hh.replace(':', '-')}_{kind}"
        d = ROOT / "posts" / folder; d.mkdir(parents=True, exist_ok=True)
        shutil.copy(VID / f"{kind}-{day}.mp4", d / "video.mp4")
        post = {"publish_at": f"2026-10-{day}T{hh}:00{off}", "type": kind, "networks": ["facebook", "instagram"], "media": ["video.mp4"]}
        if kind == "reel":
            post.update(caption=cap, cover_ms=2500)
        write(folder, post)
print(len(list((ROOT / "posts").glob("*/post.json"))), "príspevkov")
