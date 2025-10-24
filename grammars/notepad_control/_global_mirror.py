# -*- coding: utf-8 -*-
# _global_mirror.py — Miroir style Dragon Capture (navigateur)
# - Non exclusif (les commandes Dragon "Cliquer …" restent actives)
# - Injection robuste via keys_slow (+ fallback)
# - Majuscule auto (y compris tout premier mot d'un champ), espace auto entre dictées
# - Fix apostrophe/ponctuation (pas d'espace avant , . ! ? …)
# - Aucune sélection du caractère précédent (pas de Shift+Left)
# - Sélection vocale: "sélectionner <mot> à gauche|à droite" (+ variantes)

import sys
import os
from pathlib import Path

# Add core module to path for logging
current_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(current_dir))

try:
    from core.logging_config import get_logger

    log = get_logger(__name__)
    log.info(">>> [_global_mirror] module loading...")
except ImportError:
    # Fallback to log.info if logging module is not available
    import logging

    log = logging.getLogger(__name__)
    log.info(">>> [_global_mirror] module loading...")

from dragonfly import (
    Grammar,
    MappingRule,
    Dictation,
    Function,
    Text,
    Key,
    Clipboard,
    AppContext,
    Window,
)
import time, re

# -----------------------------
# Réglages principaux
# -----------------------------
BROWSERS = ("chrome", "msedge", "firefox")  # exécutables sans .exe
ENABLED_BROWSERS_ONLY = True  # n'agir que dans le navigateur
INJECTION_MODE = "keys_slow"  # "paste" | "keys" | "keys_slow" | "mixed"
SPACE_FIX = True
ENTER_STROKE = "enter"  # ou "s-enter" selon l'éditeur web
DEBUG_LOG = False


def _dbg(msg):
    if DEBUG_LOG:
        try:
            log.debug(f"[GM] {msg}")
        except Exception:
            pass


# Auto-format
AUTO_CAPITALIZE_SENTENCES = True
PREPEND_SPACE_IF_NEEDED = True

# État persistant
_prev_ended_with_space = True
_prev_ended_with_newline = False
_prev_ended_sentence = True
_prev_last_char = ""  # dernier caractère non-blanc injecté
_has_injected_once = False
_force_capital_next = True  # <-- majuscule forcée sur toute première dictée du champ

# Pilotage micro via Natlink
try:
    import natlink

    HAVE_NATLINK = True
except Exception:
    HAVE_NATLINK = False

# -----------------------------
# Clipboard helpers (compat)
# -----------------------------
try:
    _CLIP = Clipboard()  # certaines versions exigent l'instance
except Exception:
    _CLIP = None


def _clip_set(s: str):
    try:
        if _CLIP:
            _CLIP.set_text(s)
        else:
            try:
                Clipboard.set_text(content=s)
            except TypeError:
                Clipboard.set_text(s)
    except Exception:
        pass


def _clip_get() -> str:
    try:
        if _CLIP:
            return _CLIP.get_text() or ""
        else:
            return Clipboard.get_text() or ""
    except Exception:
        return ""


# -----------------------------
# Helpers texte
# -----------------------------
def _clean_text(s: str) -> str:
    if not SPACE_FIX:
        return s
    # Espaces mal placés autour de ponctuation
    s = s.replace(" ,", ",").replace(" .", ".").replace(" ;", ";").replace(" :", ":")
    s = s.replace(" !", "!").replace(" ?", "?").replace(" )", ")").replace("( ", "(")
    # Ajoute espace manquant après ponctuation si collée
    s = re.sub(r"([,;:!?])(?!\s)", r"\1 ", s)
    s = re.sub(r"([\.?!…])(?!\s)", r"\1 ", s)
    # Fix apostrophe (jamais d’espace après ')
    s = re.sub(r"'\s+([a-zà-öø-ÿ])", r"'\1", s)
    # Réduit espaces multiples
    s = re.sub(r" {2,}", " ", s)
    return s


def _apply_commands_to_text(s: str) -> str:
    patterns = [
        (r"(?i)\b(?:a|à)\s+la\s+ligne\b", "\n"),
        (r"(?i)\bretour(?:\s+à\s+la\s+ligne)?\b", "\n"),
        (r"(?i)\bnouvelle?\s+ligne\b", "\n"),
        (r"(?i)\bnouveau\s+paragraphe\b", "\n\n"),
        (r"(?i)\btabulation\b", "\t"),
        (r"(?i)\bligne\s+suivante\b", "\n"),
        (r"(?i)\bsaut\s+de\s+ligne\b", "\n"),
        (r"(?i)\bretour\s+ligne\b", "\n"),
        (r"(?i)\baller\s+à\s+la\s+ligne\b", "\n"),
    ]
    out = s
    for pat, rep in patterns:
        out = re.sub(pat, rep, out)
    return out


def _delete_prev_word(times=1, pause=0.01):
    for _ in range(times):
        Key("c-backspace").execute()
        time.sleep(pause / 2)
        Key("cs-left").execute()
        time.sleep(pause / 2)
        Key("backspace").execute()
        time.sleep(pause / 2)


def _delete_prev_char(times=1, pause=0.005):
    for _ in range(times):
        Key("backspace").execute()
        time.sleep(pause)


# -----------------------------
# Envoi / injection
# -----------------------------
def _send_text_paste(s: str):
    old = None
    try:
        old = _clip_get()
        _clip_set(s)
        Key("c-v").execute()
        time.sleep(0.005)
    finally:
        _clip_set(old or "")


def _send_text_keys(s: str):
    Text(s).execute()


def _send_text_keys_slow(s: str, delay=0.01):
    for ch in s:
        if ch == "\n":
            Key(ENTER_STROKE).execute()
        elif ch == "\t":
            Key("tab").execute()
        else:
            Text(ch).execute()
        if delay:
            time.sleep(delay)


def _inject_text(s: str):
    try:
        if INJECTION_MODE == "paste":
            _send_text_paste(s)
        elif INJECTION_MODE == "keys":
            _send_text_keys(s)
        elif INJECTION_MODE == "keys_slow":
            _send_text_keys_slow(s)
        else:
            try:
                _send_text_paste(s)
            except Exception:
                _send_text_keys_slow(s)
    except Exception:
        try:
            Text(s).execute()
        except Exception:
            pass


def _in_browser() -> bool:
    try:
        exe = (Window.get_foreground().executable or "").lower()
        return any(exe.endswith(b + ".exe") for b in BROWSERS)
    except Exception:
        return False


# -----------------------------
# Capitalisation / état de fin
# -----------------------------
_SENT_END_CHARS = ".!?…"


def _first_alpha_index(s: str) -> int:
    for i, ch in enumerate(s):
        if ch.isalpha():
            return i
    return -1


def _capitalize_sentences(s: str) -> str:
    # Majuscule au tout début (1er envoi / début de nouvelle phrase/ligne)
    if (
        _force_capital_next
        or _prev_ended_sentence
        or _prev_ended_with_newline
        or (not _has_injected_once)
    ):
        i = _first_alpha_index(s)
        if i >= 0:
            s = s[:i] + s[i].upper() + s[i + 1 :]

    # Majuscule après ., !, ?, … + espaces/«(" éventuels
    def _cap_after(m):
        prefix = m.group(1)
        letter = m.group(2)
        return prefix + letter.upper()

    s = re.sub(r'([\.!\?…]\s+[«"(\[]*\s*)([a-zà-öø-ÿ])', _cap_after, s)
    return s


def _update_tail_state(injected_text: str):
    """Mémorise comment se termine le dernier envoi (espace, retour, fin de phrase, dernier char)."""
    global _prev_ended_with_space, _prev_ended_with_newline, _prev_ended_sentence, _prev_last_char, _force_capital_next
    if not injected_text:
        return
    last_char = injected_text[-1]
    _prev_ended_with_newline = last_char == "\n"
    _prev_ended_with_space = last_char.isspace()

    i = len(injected_text) - 1
    while i >= 0 and injected_text[i].isspace():
        i -= 1
    last_non_space = injected_text[i] if i >= 0 else ""
    _prev_last_char = last_non_space
    _prev_ended_sentence = last_non_space in _SENT_END_CHARS

    # Si on a effectivement injecté une lettre, on ne force plus la majuscule la prochaine fois
    if any(ch.isalpha() for ch in injected_text):
        _force_capital_next = False


# -----------------------------
# Commandes Dragon à laisser passer
# -----------------------------
_COMMAND_PATTERNS = [
    r"^au repos$",
    r"^au travail$",
    r"^réveille[- ]?toi$",
    r"^sélectionner tout$",
    r"^copier$",
    r"^coller$",
    r"^couper$",
    r"^annuler$",
    r"^rétablir$",
    r"^enregistrer$",
    r"^supprimer( ça| cela)?$",
    r"^effacer( (ça|cela))?$",
    r"^haut de page$",
    r"^bas de page$",
]
_COMMAND_VERBS = [
    "ouvrir",
    "lancer",
    "afficher",
    "basculer",
    "activer",
    "désactiver",
    "fermer",
    "sélectionner",
    "copier",
    "coller",
    "couper",
    "supprimer",
    "effacer",
    "annuler",
    "rétablir",
    "enregistrer",
    "imprimer",
    "rechercher",
    "aller",
    "déplacer",
    "cliquer",
    "scroll",
    "zoomer",
    "réduire",
    "agrandir",
]


def _looks_like_command(s: str) -> bool:
    t = s.strip().lower()
    for pat in _COMMAND_PATTERNS:
        if re.fullmatch(pat, t):
            return True
    if re.match(
        r"^(cliquer|clique|cliquez|cliquer sur|clique sur|"
        r"sélectionner|selectionner|"
        r"copier|coller|couper|supprimer|effacer|"
        r"ouvrir|lancer|afficher|basculer|activer|désactiver|fermer|"
        r"annuler|rétablir|retablir|enregistrer|imprimer|rechercher|"
        r"aller|déplacer|deplacer)\b",
        t,
    ):
        return True
    words = t.split()
    return bool(words and words[0] in _COMMAND_VERBS and len(words) <= 7)


# -----------------------------
# Sélection par mot (à gauche/à droite)
# -----------------------------
_WORD_NORM_RE = re.compile(r"[^\wà-ÿ'-]+", re.IGNORECASE)


def _norm_word(s: str) -> str:
    if not s:
        return ""
    s = s.strip().lower()
    s = _WORD_NORM_RE.sub("", s)
    return s.strip("-'")


def _first_token(s: str) -> str:
    parts = re.split(r"\s+", str(s).strip())
    return parts[0] if parts else ""


def _get_selection_text() -> str:
    # Copie la sélection active sans rien modifier d'autre
    old = _clip_get()
    try:
        Key("c-c").execute()
        time.sleep(0.01)
        return _clip_get()
    finally:
        _clip_set(old or "")


def _select_word_left(target: str, max_words: int = 12):
    target = _norm_word(_first_token(target))
    if not target:
        return
    moves = 0
    success = False
    for _ in range(max_words):
        Key("c-left").execute()
        time.sleep(0.006)  # début mot précédent
        Key("cs-right").execute()
        time.sleep(0.006)  # sélectionner mot courant
        sel = _norm_word(_get_selection_text())
        if sel == target:
            success = True
            break
        Key("left").execute()
        time.sleep(0.004)  # reculer d'un caractère pour enchaîner
        moves += 1
    if not success:
        for _ in range(moves):
            Key("c-right").execute()


def _select_word_right(target: str, max_words: int = 12):
    target = _norm_word(_first_token(target))
    if not target:
        return
    moves = 0
    success = False
    for _ in range(max_words):
        Key("cs-right").execute()
        time.sleep(0.006)
        sel = _norm_word(_get_selection_text())
        if sel == target:
            success = True
            break
        Key("right").execute()
        time.sleep(0.004)
        moves += 1
    if not success:
        for _ in range(moves):
            Key("c-left").execute()


# -----------------------------
# Notepad function
# -----------------------------
def open_notepad_with_text():
    """Open Notepad with French text"""
    import subprocess
    import tempfile

    try:
        log.info("📝 Opening Notepad...")
        # Create a temporary file containing the French text and open it in Notepad.
        text = "salut comment ça va, c'est Sendhil"

        # Use a temp file so Notepad opens a file containing the text.
        # We write UTF-8 with BOM so Notepad (on Windows) displays accented characters correctly.
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as tf:
            # Write BOM for Notepad to auto-detect UTF-8
            tf.write("\ufeff")
            tf.write(text)
            temp_path = tf.name

        subprocess.Popen(["notepad.exe", temp_path])
        log.info(f"✅ Notepad launched successfully with file: {temp_path}")
    except Exception as e:
        log.error(f"❌ Failed to open Notepad: {e}")


# -----------------------------
# Action principale (avec correctif espace AVANT ponctuation)
# -----------------------------
_LEADING_PUNCT = set(",.;:!?)]}%»\"'")


def mirror_text(texte=None):
    global _has_injected_once, _force_capital_next

    if ENABLED_BROWSERS_ONLY and not _in_browser():
        return

    s = (str(texte) if texte is not None else "").strip()
    if not s:
        return

    if _looks_like_command(s):
        # Laisser Dragon exécuter ses commandes natives (ex: "Cliquer Valider")
        return

    # 1) nettoyage + commandes inline (retours/tab…)
    s = _clean_text(s)
    s = _apply_commands_to_text(s)

    # 2) espace auto sans lecture du champ
    if PREPEND_SPACE_IF_NEEDED and s:
        wants_space = (
            not s[0].isspace()
            and s[0] not in _LEADING_PUNCT
            and _has_injected_once
            and not _prev_ended_with_space
            and not _prev_ended_with_newline
        )
        if wants_space:
            s = " " + s
            s = _clean_text(s)

    # 3) majuscule auto (début, après fin de phrase, après retour, OU si flag forcé)
    if AUTO_CAPITALIZE_SENTENCES:
        s = _capitalize_sentences(s)

    # 4) injection + mise à jour d'état
    _inject_text(s)
    _update_tail_state(s)
    _has_injected_once = True
    # si on vient d'injecter uniquement de la ponctuation, on peut garder _force_capital_next à True


# -----------------------------
# Commandes explicites
# -----------------------------
def cmd_line():
    Key(ENTER_STROKE).execute()


def cmd_new_paragraph():
    Key(ENTER_STROKE).execute()
    Key(ENTER_STROKE).execute()


def cmd_tab():
    Key("tab").execute()


def go_to_sleep():
    if HAVE_NATLINK:
        try:
            natlink.setMicState("sleeping")
        except Exception:
            pass


def wake_up():
    if HAVE_NATLINK:
        try:
            natlink.setMicState("on")
        except Exception:
            pass


class ControlRule(MappingRule):
    mapping = {
        # Retours/paragraphes
        "nouvelle ligne": Function(lambda: Key(ENTER_STROKE).execute()),
        "ligne suivante": Function(lambda: Key(ENTER_STROKE).execute()),
        "saut de ligne": Function(lambda: Key(ENTER_STROKE).execute()),
        "retour ligne": Function(lambda: Key(ENTER_STROKE).execute()),
        "aller à la ligne": Function(lambda: Key(ENTER_STROKE).execute()),
        "retour": Function(lambda: Key(ENTER_STROKE).execute()),
        "retour à la ligne": Function(lambda: Key(ENTER_STROKE).execute()),
        "nouveau paragraphe": Function(
            lambda: (Key(ENTER_STROKE).execute(), Key(ENTER_STROKE).execute())
        ),
        "tabulation": Function(lambda: Key("tab").execute()),
        # Effacements rapides
        "effacer ça": Function(lambda: _delete_prev_word(1)),
        "efface ça": Function(lambda: _delete_prev_word(1)),
        "effacer cela": Function(lambda: _delete_prev_word(1)),
        "supprimer ça": Function(lambda: _delete_prev_word(1)),
        "supprime ça": Function(lambda: _delete_prev_word(1)),
        # Sélections basiques
        "sélectionner le mot précédent": Function(lambda: Key("cs-left").execute()),
        "sélectionner le mot suivant": Function(lambda: Key("cs-right").execute()),
        "sélectionner tout": Function(lambda: Key("c-a").execute()),
        # Sélection par contenu (autour du curseur) — variantes tolérantes
        "sélectionner <cible> à gauche": Function(
            lambda cible: _select_word_left(cible)
        ),
        "selectionner <cible> a gauche": Function(
            lambda cible: _select_word_left(cible)
        ),
        "sélectionner le mot <cible> à gauche": Function(
            lambda cible: _select_word_left(cible)
        ),
        "selectionner le mot <cible> a gauche": Function(
            lambda cible: _select_word_left(cible)
        ),
        "sélectionner <cible> vers la gauche": Function(
            lambda cible: _select_word_left(cible)
        ),
        "sélectionner <cible> à droite": Function(
            lambda cible: _select_word_right(cible)
        ),
        "selectionner <cible> a droite": Function(
            lambda cible: _select_word_right(cible)
        ),
        "sélectionner le mot <cible> à droite": Function(
            lambda cible: _select_word_right(cible)
        ),
        "selectionner le mot <cible> a droite": Function(
            lambda cible: _select_word_right(cible)
        ),
        "sélectionner <cible> vers la droite": Function(
            lambda cible: _select_word_right(cible)
        ),
        # Notepad commands
        "melvin": Function(open_notepad_with_text),
        # Micro
        "au repos": Function(go_to_sleep),
        "au travail": Function(wake_up),
    }
    extras = [Dictation("cible")]
    defaults = {}


control_grammar = Grammar("global_mirror_control", context=None)
control_grammar.add_rule(ControlRule())
control_grammar.load()

# -----------------------------
# Grammaire de dictée
# -----------------------------
browser_context = None
for b in BROWSERS:
    ctx = AppContext(executable=b)
    browser_context = ctx if browser_context is None else (browser_context | ctx)


class MirrorRule(MappingRule):
    mapping = {"<texte>": Function(mirror_text)}
    extras = [Dictation("texte")]
    defaults = {}


dictation_grammar = Grammar("global_mirror_dictation", context=browser_context)
dictation_grammar.add_rule(MirrorRule())
dictation_grammar.load()

log.info(">>> [_global_mirror] loaded OK (Always ON, non-exclusive)")
