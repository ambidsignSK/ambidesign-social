# Ambi Design – publikovanie na Facebook a Instagram

Vlastný plánovač príspevkov cez Meta Graph API. Beží zadarmo na GitHub Actions,
každých 10 minút skontroluje priečinok `posts/` a zverejní všetko, čo je na rade.

## Ako naplánovať príspevok

Vytvor priečinok `posts/<RRRR-MM-DD_HH-MM_nazov>/` a v ňom `post.json` + médiá:

```json
{
  "publish_at": "2026-11-03T13:00:00+01:00",
  "type": "post",
  "networks": ["facebook", "instagram"],
  "caption": "Text príspevku…",
  "media": ["01.jpg"]
}
```

| type | médiá | poznámka |
|---|---|---|
| `post` | 1 obrázok (JPG) | klasický príspevok |
| `carousel` | 2–10 obrázkov (JPG) | na FB ako príspevok s viacerými fotkami |
| `reel` | 1 video MP4 (9:16) | `cover_ms` = titulný snímok v ms |
| `story` | 1 video MP4 alebo JPG | `caption` sa nezobrazuje |

Čas je vždy s časovou zónou (+02:00 letný, +01:00 zimný čas SR).
Commit + push do vetvy `main` a hotovo.

## Stav

`state/published.json` – výsledok pre každý príspevok a sieť (ID, odkaz, prípadná chyba).
Neúspešné publikovanie sa skúša max. 3×; pri chybe GitHub pošle e-mail o zlyhanom behu.
Príspevky staršie ako 36 h, ktoré sa nepodarilo zverejniť, sa vynechajú.

Ručné spustenie: **Actions → Publikovanie FB + IG → Run workflow** (`check` overí token).

## Nastavenie (raz)

1. Secret `META_PAGE_TOKEN` (Settings → Secrets and variables → Actions) – trvalý
   prístupový token stránky AmbiDesign s oprávneniami `pages_show_list`, `pages_read_engagement`,
   `pages_manage_posts`, `instagram_basic`, `instagram_content_publish`, `business_management`.
2. Repo musí byť **verejné** – Instagram si médiá sťahuje z verejnej URL (raw.githubusercontent.com).
