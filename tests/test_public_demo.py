from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def test_public_demo_contains_brand_and_three_case_flow():
    html = (DOCS / "index.html").read_text(encoding="utf-8")
    assert "assets/fairchange-mark.svg" in html
    assert "req-defect" in html
    assert "req-revision" in html
    assert "req-addition" in html
    assert "Owner review" in html
    assert "Client acceptance" in html


def test_public_pages_disclose_synthetic_data_and_avoid_runtime_secrets():
    for path in (DOCS / "index.html", DOCS / "external-session.html"):
        html = path.read_text(encoding="utf-8").lower()
        assert "synthetic" in html
        assert "cognito" in html or "does not send data anywhere" in html
        assert "access_key_id" not in html
        assert "secret_access_key" not in html
        assert "authorization: bearer" not in html


def test_brand_mark_is_local_svg():
    svg = (DOCS / "assets" / "fairchange-mark.svg").read_text(encoding="utf-8")
    assert "<svg" in svg
    assert "<title>FairChange mark</title>" in svg
    assert "linearGradient" in svg
