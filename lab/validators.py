"""Exécute les checks déclarés dans les modules .md (§5.2 du CDC).

Tous les chemins (file_exists, contains_text, cwd) sont résolus relativement
à la racine du dépôt (parent de ce fichier lab/, donc django-lab/).
"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

import requests

from loader import Check

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_TIMEOUT = 30


@dataclass
class CheckResult:
    passed: bool
    message: str
    detail: str = ""


def _resolve(relative_path: str) -> Path:
    return BASE_DIR / relative_path


def _run_shell(command: str, cwd: str, timeout: int) -> tuple[bool, str]:
    """Lance `command` dans cwd (relatif à BASE_DIR). Frontière de confiance : §5.2 du CDC."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=_resolve(cwd),
            timeout=timeout,
            capture_output=True,
            text=True,
        )
    except subprocess.TimeoutExpired:
        return False, f"Timeout dépassé ({timeout}s) pour : {command}"
    except FileNotFoundError as exc:
        return False, f"Dossier de travail introuvable ({cwd}) : {exc}"

    detail = (result.stdout or "") + (result.stderr or "")
    return result.returncode == 0, detail.strip()


def check_file_exists(check: Check) -> CheckResult:
    path = check.params["path"]
    if _resolve(path).exists():
        return CheckResult(passed=True, message=f"✅ {path} trouvé")
    return CheckResult(passed=False, message=f"❌ {check.message}", detail=f"Chemin testé : {path}")


def check_command_passes(check: Check) -> CheckResult:
    command = check.params["command"]
    cwd = check.params.get("cwd", ".")
    timeout = check.params.get("timeout", DEFAULT_TIMEOUT)
    passed, detail = _run_shell(command, cwd, timeout)
    if passed:
        return CheckResult(passed=True, message=f"✅ Commande réussie : {command}")
    return CheckResult(passed=False, message=f"❌ {check.message}", detail=detail)


def check_contains_text(check: Check) -> CheckResult:
    path = check.params["path"]
    text = check.params["text"]
    file_path = _resolve(path)
    if not file_path.exists():
        return CheckResult(passed=False, message=f"❌ {check.message}", detail=f"Fichier introuvable : {path}")
    content = file_path.read_text(encoding="utf-8")
    if text in content:
        return CheckResult(passed=True, message=f"✅ Texte trouvé dans {path}")
    return CheckResult(
        passed=False, message=f"❌ {check.message}", detail=f"{text!r} absent de {path}"
    )


def check_http_ok(check: Check) -> CheckResult:
    url = check.params["url"]
    expect_text = check.params.get("expect_text")
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as exc:
        return CheckResult(
            passed=False, message=f"❌ {check.message}", detail=f"Connexion impossible à {url} : {exc}"
        )
    if response.status_code != 200:
        return CheckResult(
            passed=False,
            message=f"❌ {check.message}",
            detail=f"Statut HTTP {response.status_code} pour {url}",
        )
    if expect_text and expect_text not in response.text:
        return CheckResult(
            passed=False,
            message=f"❌ {check.message}",
            detail=f"Texte attendu absent de la réponse : {expect_text!r}",
        )
    return CheckResult(passed=True, message=f"✅ {url} répond (200)")


def check_test_passes(check: Check) -> CheckResult:
    cwd = check.params.get("cwd", ".")
    test_path = check.params["test_path"]
    timeout = check.params.get("timeout", DEFAULT_TIMEOUT)
    command = f"python manage.py test {test_path}"
    passed, detail = _run_shell(command, cwd, timeout)
    if passed:
        return CheckResult(passed=True, message=f"✅ Tests réussis : {test_path}")
    return CheckResult(passed=False, message=f"❌ {check.message}", detail=detail)


CHECK_DISPATCH = {
    "file_exists": check_file_exists,
    "command_passes": check_command_passes,
    "contains_text": check_contains_text,
    "http_ok": check_http_ok,
    "test_passes": check_test_passes,
}


def run_check(check: Check) -> CheckResult:
    handler = CHECK_DISPATCH.get(check.type)
    if handler is None:
        return CheckResult(passed=False, message=f"❌ Type de check inconnu : {check.type}")
    return handler(check)
