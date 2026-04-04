"""Tests for the profile preset library."""

from kim.profiles.library import list_presets

# All categories that may appear in the profiles/ directory tree.
# Includes the original built-in categories plus the four guest-type
# categories added when the source repos were merged.
_KNOWN_CATEGORIES = {
    # built-in presets
    "gpu", "audio", "display", "rocm", "nesting", "network",
    # guest-type categories (profiles/ directory)
    "generic", "macos", "windows", "waydroid",
}


def test_list_presets_returns_list() -> None:
    presets = list_presets()
    assert isinstance(presets, list)
    assert len(presets) > 0


def test_presets_have_required_fields() -> None:
    for preset in list_presets():
        assert "name"        in preset
        assert "description" in preset
        assert "category"    in preset
        assert "profile"     in preset


def test_preset_categories_are_known() -> None:
    for preset in list_presets():
        assert preset["category"] in _KNOWN_CATEGORIES, (
            f"Unknown category '{preset['category']}' in preset '{preset['name']}'"
        )


def test_preset_profile_has_name() -> None:
    for preset in list_presets():
        assert "name" in preset["profile"], (
            f"Profile in preset '{preset['name']}' missing 'name' field"
        )


# ── Guest-type category coverage ─────────────────────────────────────────────

def test_generic_profiles_present() -> None:
    """incusbox profiles are loaded from profiles/generic/."""
    categories = {p["category"] for p in list_presets()}
    assert "generic" in categories


def test_macos_profiles_present() -> None:
    """macOS KVM profile is loaded from profiles/macos/."""
    categories = {p["category"] for p in list_presets()}
    assert "macos" in categories


def test_windows_profiles_present() -> None:
    """Windows VM profiles are loaded from profiles/windows/."""
    categories = {p["category"] for p in list_presets()}
    assert "windows" in categories


def test_waydroid_profiles_present() -> None:
    """Waydroid profile is loaded from profiles/waydroid/."""
    categories = {p["category"] for p in list_presets()}
    assert "waydroid" in categories


def test_windows_desktop_profile_present() -> None:
    names = {p["name"] for p in list_presets()}
    assert "windows-desktop-x86_64" in names


def test_macos_kvm_profile_present() -> None:
    names = {p["name"] for p in list_presets()}
    assert "macos-kvm" in names


def test_waydroid_profile_present() -> None:
    names = {p["name"] for p in list_presets()}
    assert "waydroid" in names


def test_generic_base_profile_present() -> None:
    names = {p["name"] for p in list_presets()}
    assert "base" in names
