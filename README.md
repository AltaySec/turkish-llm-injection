# 🇹🇷 AltaySec Turkish LLM Prompt Injection Dataset

> Türkiye'nin ilk Türkçe-öncelikli, kategorize edilmiş LLM prompt injection veri seti.
> 120 elle hazırlanmış payload, 12 kategori, OWASP LLM Top 10 (2025) eşlemeli.

[![HuggingFace](https://img.shields.io/badge/🤗-AltaySec/turkish--llm--injection-yellow)](https://huggingface.co/datasets/AltaySec/turkish-llm-injection)
[![License](https://img.shields.io/badge/license-CC--BY--4.0-22C55E)](LICENSE)
[![Website](https://img.shields.io/badge/web-altaysec.com.tr-EF4444)](https://altaysec.com.tr)
[![Companion](https://img.shields.io/badge/multi--turn-altayduel--transcripts-3B82F6)](https://huggingface.co/datasets/AltaySec/altayduel-transcripts)

## 🚀 Hızlı kullanım

```bash
pip install datasets
```

```python
from datasets import load_dataset

ds = load_dataset("AltaySec/turkish-llm-injection", split="train")
print(ds[0])
# Kategori bazlı filtre:
critical = ds.filter(lambda x: x["severity"] == "critical")
```

Veya `data/train.jsonl` dosyasını doğrudan oku:

```python
import json
with open("data/train.jsonl") as f:
    payloads = [json.loads(line) for line in f]
```

## 📦 Bu repo'da ne var

| Dosya | İçerik |
|-------|--------|
| `data/train.jsonl` | 120 prompt injection payload (her satır 1 örnek) |
| `TAXONOMY.md` | 12 kategori için detaylı tanım, gerçek dünya tetikleyicileri, karşı savunmalar |
| `build_dataset.py` | Dataset'i yeniden üretmek için pipeline |
| `validate.py` | Schema + duplicate + hash doğrulama |
| `example_usage.py` | Garak/PyRIT/llm-guard ile örnek entegrasyon |
| `CITATION.cff` | Akademik atıf metadata'sı |

## 🎯 12 Kategori (kısaca)

**AltayDuel arena gözlemli 5 kalıp:**

1. `authority_urgency` — KVKK denetçisi, BDDK müfettişi, padişah fermanı
2. `confirmation_trap` — secret'ı saldırgan yazıp sadece onay isteme
3. `echo_translation` — çeviri/OCR bahanesi ile aynen tekrar zorlama
4. `roleplay_theater` — DAN, kurgu yazarı, Atatürk persona
5. `system_prompt_extract` — direkt veya YAML format ile sızdırma

**Türkçe-özel 7 yan kategori 🇹🇷:**

6. `morphological_bypass` — "unutmuş olmalısın", "-iver", "-casına", şart+miş
7. `politeness_escalation` — crescendo nezaket → manipülasyon
8. `code_switching` — TR/EN karışık komut+context
9. `indirect_injection` — HTML, e-posta PS, CSV, OCR
10. `encoding_obfuscation` — base64, ROT13, zalgo, zero-width
11. `cultural_manipulation` — vatani görev, fıkıh zaruret, futbol taraftarlığı
12. `pii_exfiltration` — TC kimlik, IBAN, KVKK Madde 6

Detaylı taksonomi: [`TAXONOMY.md`](TAXONOMY.md)

## 📊 İstatistikler

| Metrik | Değer |
|--------|-------|
| Toplam payload | 120 |
| Kategori | 12 |
| Her kategori | 10 payload |
| Kritik ciddiyet | 17 |
| Dil | TR (~95%), TR-EN (~5%) |
| Versiyon | v0.1 (seed) |

## 🔬 Companion: Multi-turn arena transcripts

Bu repo **single-payload** dataset'tir. **Multi-turn** versiyonu (3-8 round dialog, 17 senaryo, 5 LLM provider) ayrı bir dataset'te:

📦 [`AltaySec/altayduel-transcripts`](https://huggingface.co/datasets/AltaySec/altayduel-transcripts) — 648 düello transkripti

İkisi birlikte kullanılmak üzere tasarlandı: payload set başlangıç, transcript set ileri seviye savunma testi.

## ⚠️ Etik kullanım

Bu veri seti **savunma odaklı**:

✅ LLM guardrail testi · adversarial fine-tuning · akademik araştırma · system prompt sertleştirme
❌ İzinsiz üretim sistemine saldırı · gerçek PII üretme

KVKK Madde 6 örnekleri **niyet** yansıtır, **gerçek veri içermez**. Tüm TC/IBAN/telefon değerleri uydurma format-only.

## 🤝 Katkı

Yeni payload önerin var mı? PR aç:

1. Fork et
2. `data/train.jsonl`'a yeni satır ekle (şema: `TAXONOMY.md`'de)
3. `python validate.py` ile doğrula
4. PR başlığı: `[contribution] [kategori]: kısa açıklama`

5+ payload kabul edilen katkıcılar README'de listelenir. 20+ payload → arXiv paper'da co-author değerlendirmesi.

## 📚 Atıf

```bibtex
@misc{altaysec_tr_llm_injection_2026,
  author       = {Yurtsevenler, Fevzi Ege},
  title        = {{AltaySec Turkish LLM Prompt Injection Dataset (v0.1)}},
  year         = {2026},
  publisher    = {AltaySec},
  howpublished = {\url{https://huggingface.co/datasets/AltaySec/turkish-llm-injection}},
  note         = {Seed dataset of 120 hand-curated Turkish prompt injection
                  payloads across 12 categories, mapped to OWASP LLM Top 10.}
}
```

## 🔗 İlgili kaynaklar

- 🌐 [altaysec.com.tr](https://altaysec.com.tr) · Şirket sitesi
- 🥊 [duel.altaysec.com.tr](https://duel.altaysec.com.tr) · AltayDuel arena
- 📚 [Araştırma yazıları](https://altaysec.com.tr/arastirmalar/) · 35+ derinleştirilmiş yazı
- 🤗 [HuggingFace org](https://huggingface.co/AltaySec) · Tüm dataset'ler

## 📄 Lisans

[CC-BY-4.0](LICENSE) — atıf vererek serbest kullanım.

---

**Yazar:** [Fevzi Ege Yurtsevenler](https://www.linkedin.com/in/fevziege) · AltaySec Kurucusu
