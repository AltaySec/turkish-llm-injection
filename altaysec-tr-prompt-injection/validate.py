"""
validate.py — Yükleme öncesi sanity check
========================================

HuggingFace'e yüklemeden önce data/train.jsonl'ı doğrular:
- Schema uyumu
- Tekrar yok
- Zorunlu alanlar dolu
- Severity / language enum'ları geçerli
- Kategori dengesi
- Karakter encoding
"""

import json
from pathlib import Path
from collections import Counter
import sys

REQUIRED_FIELDS = [
    "id", "prompt", "category", "subcategory",
    "owasp_llm_top10", "severity", "language",
    "context", "expected_failure_mode", "tactic_family",
    "morphology_notes", "source", "hash",
]

VALID_SEVERITIES = {"low", "medium", "high", "critical"}
VALID_LANGUAGES = {"tr", "tr-en", "en"}
VALID_CATEGORIES = {
    "authority_urgency", "confirmation_trap", "echo_translation",
    "roleplay_theater", "system_prompt_extract", "morphological_bypass",
    "politeness_escalation", "code_switching", "indirect_injection",
    "encoding_obfuscation", "cultural_manipulation", "pii_exfiltration",
}


def validate():
    data_path = Path(__file__).parent / "data" / "train.jsonl"
    if not data_path.exists():
        print(f"❌ Veri dosyası bulunamadı: {data_path}")
        sys.exit(1)

    records = []
    errors = []
    seen_ids = set()
    seen_hashes = set()
    seen_prompts = set()

    with open(data_path, encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"L{ln}: JSON decode hatası — {e}")
                continue

            # Zorunlu alanlar
            for field in REQUIRED_FIELDS:
                if field not in rec:
                    errors.append(f"L{ln}: '{field}' alanı eksik")
                elif not rec[field] and field != "morphology_notes":
                    errors.append(f"L{ln}: '{field}' boş")

            # ID benzersizliği
            if rec.get("id") in seen_ids:
                errors.append(f"L{ln}: ID tekrarı — {rec['id']}")
            seen_ids.add(rec.get("id"))

            # Hash benzersizliği
            if rec.get("hash") in seen_hashes:
                errors.append(f"L{ln}: Hash tekrarı — {rec['hash']}")
            seen_hashes.add(rec.get("hash"))

            # Prompt benzersizliği (text-level dedupe)
            prompt = rec.get("prompt", "").strip().lower()
            if prompt in seen_prompts:
                errors.append(f"L{ln}: Prompt tekrarı (text-level)")
            seen_prompts.add(prompt)

            # Enum kontrolleri
            if rec.get("severity") not in VALID_SEVERITIES:
                errors.append(f"L{ln}: Geçersiz severity — {rec.get('severity')}")
            if rec.get("language") not in VALID_LANGUAGES:
                errors.append(f"L{ln}: Geçersiz language — {rec.get('language')}")
            if rec.get("category") not in VALID_CATEGORIES:
                errors.append(f"L{ln}: Geçersiz category — {rec.get('category')}")

            # Prompt uzunluğu
            if len(rec.get("prompt", "")) < 10:
                errors.append(f"L{ln}: Prompt çok kısa (<10 char) — {rec.get('id')}")
            if len(rec.get("prompt", "")) > 2000:
                errors.append(f"L{ln}: Prompt çok uzun (>2000 char) — {rec.get('id')}")

            records.append(rec)

    # ÖZET
    print(f"📄 Toplam kayıt: {len(records)}")
    print(f"❌ Hata: {len(errors)}")

    if errors:
        print("\nHATALAR:")
        for e in errors[:20]:
            print(f"  {e}")
        if len(errors) > 20:
            print(f"  ... ve {len(errors)-20} daha")
        sys.exit(1)

    # Kategori dengesi
    cat_counts = Counter(r["category"] for r in records)
    print("\n📊 Kategori dağılımı:")
    for cat, n in sorted(cat_counts.items()):
        bar = "█" * n
        print(f"   {cat:30s} {n:3d} {bar}")

    # Severity dağılımı
    sev_counts = Counter(r["severity"] for r in records)
    print("\n⚠️  Severity dağılımı:")
    for sev in ["low", "medium", "high", "critical"]:
        n = sev_counts.get(sev, 0)
        print(f"   {sev:10s} {n:3d}")

    # Dil dağılımı
    lang_counts = Counter(r["language"] for r in records)
    print("\n🌐 Dil dağılımı:")
    for lang, n in lang_counts.most_common():
        print(f"   {lang:10s} {n:3d}")

    # Context dağılımı
    ctx_counts = Counter(r["context"] for r in records)
    print("\n🎯 Context dağılımı:")
    for ctx, n in ctx_counts.most_common():
        print(f"   {ctx:25s} {n:3d}")

    # OWASP dağılımı
    print("\n🛡  OWASP LLM Top 10 eşlemesi:")
    owasp_counts = Counter()
    for r in records:
        for tag in r["owasp_llm_top10"].split(","):
            owasp_counts[tag.strip()] += 1
    for tag, n in owasp_counts.most_common():
        print(f"   {tag:50s} {n:3d}")

    print("\n✅ Tüm validasyonlar başarılı — yüklemeye hazır.")


if __name__ == "__main__":
    validate()
