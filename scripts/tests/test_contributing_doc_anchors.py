"""Stable HTML anchors in CONTRIBUTING.md and maintainer-hub deep links."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

from doc_link_fragment_scan import collect_doc_link_offenders

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_MD = REPO_ROOT / "AGENTS.md"
CONTRIBUTING = REPO_ROOT / "CONTRIBUTING.md"
PR_TEMPLATE = REPO_ROOT / ".github" / "pull_request_template.md"
MAINTAINER_HUB = REPO_ROOT / "maintainer-hub.html"
INDEX_HTML = REPO_ROOT / "index.html"
ANALYSIS_HUB = REPO_ROOT / "analysis-hub.html"
EVOLUTION_LOOP_HTML = REPO_ROOT / "evolution-loop.html"
NEXUS_HTML = REPO_ROOT / "nexus.html"
SYNTHESIS_HTML = REPO_ROOT / "synthesis.html"
LAB_HTML = REPO_ROOT / "lab.html"
DECADE_HTML = REPO_ROOT / "decade.html"
MODULES_MAP_HTML = REPO_ROOT / "modules-map.html"
EVOLUTION_TRIAD_HTML = REPO_ROOT / "evolution-triad.html"
EDU_NEXUS_HTML = REPO_ROOT / "edu-nexus.html"
DECADE_SCENES_HTML = REPO_ROOT / "decade-scenes.html"
TIMELINE_HTML = REPO_ROOT / "timeline.html"
PAST_FUTURE_HTML = REPO_ROOT / "past-future.html"
DECADE_US_HTML = REPO_ROOT / "decade-us.html"
INTELLIGENT_EVOLUTION_HTML = REPO_ROOT / "intelligent-evolution.html"
SMART_OVERHAUL_HTML = REPO_ROOT / "smart-overhaul.html"
EVOLVABLE_ARCHITECTURE_HTML = REPO_ROOT / "evolvable-architecture.html"
WORK_INFRA_ENERGY_HTML = REPO_ROOT / "work-infra-energy.html"
RISK_GEO_HTML = REPO_ROOT / "risk-geo.html"
NET_BIZ_CAPITAL_HTML = REPO_ROOT / "net-biz-capital.html"
NATIONAL_STRATEGY_OPINION_HTML = REPO_ROOT / "national-strategy-opinion.html"
SOCIAL_RESPONSIBILITY_EVOLUTION_HTML = REPO_ROOT / "social-responsibility-evolution.html"
SYNTHESIS_EXTENSIONS_HTML = REPO_ROOT / "synthesis-extensions.html"
SYNTHESIS_METHODS_HTML = REPO_ROOT / "synthesis-methods.html"
ARCHITECTURE_HTML = REPO_ROOT / "architecture.html"
MODEL_HTML = REPO_ROOT / "model.html"
LEGACY_ALL_IN_ONE_HTML = REPO_ROOT / "legacy-all-in-one.html"
NOT_FOUND_404_HTML = REPO_ROOT / "404.html"
ADMIN_CONSOLE_INDEX_HTML = REPO_ROOT / "admin-console" / "static" / "index.html"
SPA_LAYOUT_TSX = REPO_ROOT / "spa" / "src" / "SpaLayout.tsx"

_HUB_MAIN_QUESTIONS_FRAG = "docs/HUB_MAIN_QUESTIONS.md#hub-main-questions"

_REQUIRED_CONTRIBUTING_ANCHORS = (
    "contributing-five-minute",
    "contributing-env-and-cmd",
    "contributing-change-to-command",
    "contributing-common-changes-checklist",
    "contributing-terminology",
    "contributing-pr-evidence-triad",
    "maintainer-reading-order",
)

class TestContributingDocAnchors(unittest.TestCase):
    def _assert_hub_main_questions_twice(self, html_path: Path, hint: str) -> None:
        body = html_path.read_text(encoding="utf-8")
        self.assertGreaterEqual(
            body.count(_HUB_MAIN_QUESTIONS_FRAG),
            2,
            f"{html_path.relative_to(REPO_ROOT)} should link {_HUB_MAIN_QUESTIONS_FRAG!r} "
            f"at least twice ({hint})",
        )

    def test_contributing_has_stable_html_anchors(self) -> None:
        text = CONTRIBUTING.read_text(encoding="utf-8")
        for aid in _REQUIRED_CONTRIBUTING_ANCHORS:
            needle = f'<a id="{aid}"></a>'
            self.assertIn(
                needle,
                text,
                f"Missing stable anchor {needle!r} in {CONTRIBUTING.relative_to(REPO_ROOT)}",
            )

    def test_maintainer_hub_links_contributing_env_section(self) -> None:
        fragment = "CONTRIBUTING.md#contributing-env-and-cmd"
        body = MAINTAINER_HUB.read_text(encoding="utf-8")
        self.assertGreaterEqual(
            body.count(fragment),
            2,
            f"{MAINTAINER_HUB.relative_to(REPO_ROOT)} should link {fragment!r} at least twice",
        )

    def test_maintainer_hub_links_contributing_five_minute(self) -> None:
        body = MAINTAINER_HUB.read_text(encoding="utf-8")
        self.assertIn(
            "CONTRIBUTING.md#contributing-five-minute",
            body,
            f"{MAINTAINER_HUB.relative_to(REPO_ROOT)} should link CONTRIBUTING "
            "#contributing-five-minute (开 PR 前速览)",
        )

    def test_maintainer_hub_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(
            MAINTAINER_HUB, "page-head · 关系视图"
        )

    def test_maintainer_hub_links_invariants_index_pr_triad_partials_sequence(
        self,
    ) -> None:
        body = MAINTAINER_HUB.read_text(encoding="utf-8")
        for frag in (
            "ARCHITECTURE_ONE_PAGER.md#architect-invariants-index",
            "CONTRIBUTING.md#contributing-pr-evidence-triad",
            "MERGE_AND_RELEASE_CHECKLIST.md#pre-merge-partials-sequence",
        ):
            with self.subTest(fragment=frag):
                self.assertIn(
                    frag,
                    body,
                    f"{MAINTAINER_HUB.relative_to(REPO_ROOT)} should link {frag!r}",
                )

    def test_index_html_links_invariants_index_and_pr_triad(self) -> None:
        body = INDEX_HTML.read_text(encoding="utf-8")
        for frag in (
            "docs/ARCHITECTURE_ONE_PAGER.md#architect-invariants-index",
            "CONTRIBUTING.md#contributing-pr-evidence-triad",
        ):
            with self.subTest(fragment=frag):
                self.assertGreaterEqual(
                    body.count(frag),
                    2,
                    f"{INDEX_HTML.relative_to(REPO_ROOT)} should link {frag!r} "
                    "at least twice (kicker + read-guide / 分区脚)",
                )

    def test_index_html_links_contributing_change_to_command(self) -> None:
        body = INDEX_HTML.read_text(encoding="utf-8")
        frag = "CONTRIBUTING.md#contributing-change-to-command"
        self.assertGreaterEqual(
            body.count(frag),
            2,
            f"{INDEX_HTML.relative_to(REPO_ROOT)} should link {frag!r} "
            "at least twice (page-head kicker · read-guide · hub-map foot)",
        )

    def test_index_html_links_contributing_five_minute(self) -> None:
        body = INDEX_HTML.read_text(encoding="utf-8")
        frag = "CONTRIBUTING.md#contributing-five-minute"
        self.assertGreaterEqual(
            body.count(frag),
            2,
            f"{INDEX_HTML.relative_to(REPO_ROOT)} should link {frag!r} "
            "at least twice (kicker · read-guide / 分区脚 · hub-map foot)",
        )

    def test_index_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(
            INDEX_HTML, "page-head kicker · read-guide"
        )

    def test_analysis_hub_html_links_invariants_index_and_pr_triad(self) -> None:
        body = ANALYSIS_HUB.read_text(encoding="utf-8")
        for frag in (
            "docs/ARCHITECTURE_ONE_PAGER.md#architect-invariants-index",
            "CONTRIBUTING.md#contributing-pr-evidence-triad",
        ):
            with self.subTest(fragment=frag):
                self.assertGreaterEqual(
                    body.count(frag),
                    2,
                    f"{ANALYSIS_HUB.relative_to(REPO_ROOT)} should link {frag!r} "
                    "at least twice (note-kicker + 架构与读数总线)",
                )

    def test_analysis_hub_html_links_contributing_change_to_command(self) -> None:
        body = ANALYSIS_HUB.read_text(encoding="utf-8")
        frag = "CONTRIBUTING.md#contributing-change-to-command"
        self.assertGreaterEqual(
            body.count(frag),
            2,
            f"{ANALYSIS_HUB.relative_to(REPO_ROOT)} should link {frag!r} "
            "at least twice (note-kicker + 架构与读数总线)",
        )

    def test_analysis_hub_html_links_contributing_five_minute(self) -> None:
        body = ANALYSIS_HUB.read_text(encoding="utf-8")
        frag = "CONTRIBUTING.md#contributing-five-minute"
        self.assertGreaterEqual(
            body.count(frag),
            2,
            f"{ANALYSIS_HUB.relative_to(REPO_ROOT)} should link {frag!r} "
            "at least twice (note-kicker + 架构与读数总线)",
        )

    def test_analysis_hub_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(
            ANALYSIS_HUB, "note-kicker + 架构与读数总线"
        )

    def test_evolution_loop_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(EVOLUTION_LOOP_HTML, "read-hint")

    def test_nexus_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(NEXUS_HTML, "read-hint")

    def test_synthesis_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(SYNTHESIS_HTML, "read-hint")

    def test_lab_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(LAB_HTML, "read-hint")

    def test_decade_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(DECADE_HTML, "read-hint")

    def test_modules_map_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(MODULES_MAP_HTML, "read-hint")

    def test_evolution_triad_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(EVOLUTION_TRIAD_HTML, "read-hint")

    def test_edu_nexus_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(EDU_NEXUS_HTML, "read-hint")

    def test_decade_scenes_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(DECADE_SCENES_HTML, "read-hint")

    def test_timeline_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(TIMELINE_HTML, "read-hint")

    def test_past_future_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(PAST_FUTURE_HTML, "read-hint")

    def test_decade_us_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(DECADE_US_HTML, "read-hint")

    def test_intelligent_evolution_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(INTELLIGENT_EVOLUTION_HTML, "read-hint")

    def test_smart_overhaul_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(SMART_OVERHAUL_HTML, "read-hint")

    def test_evolvable_architecture_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(EVOLVABLE_ARCHITECTURE_HTML, "read-hint")

    def test_work_infra_energy_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(WORK_INFRA_ENERGY_HTML, "read-hint")

    def test_risk_geo_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(RISK_GEO_HTML, "read-hint")

    def test_net_biz_capital_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(NET_BIZ_CAPITAL_HTML, "read-hint")

    def test_national_strategy_opinion_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(
            NATIONAL_STRATEGY_OPINION_HTML, "read-hint"
        )

    def test_social_responsibility_evolution_html_links_hub_main_questions(
        self,
    ) -> None:
        self._assert_hub_main_questions_twice(
            SOCIAL_RESPONSIBILITY_EVOLUTION_HTML, "read-hint"
        )

    def test_synthesis_extensions_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(SYNTHESIS_EXTENSIONS_HTML, "read-hint")

    def test_synthesis_methods_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(SYNTHESIS_METHODS_HTML, "read-hint")

    def test_architecture_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(ARCHITECTURE_HTML, "read-hint")

    def test_model_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(MODEL_HTML, "read-hint")

    def test_legacy_all_in_one_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(
            LEGACY_ALL_IN_ONE_HTML, "pagination-hint · read-hint 维护与契约"
        )

    def test_404_html_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(
            NOT_FOUND_404_HTML, "常用入口 · 维护者与契约"
        )

    def test_admin_console_static_index_links_hub_main_questions(self) -> None:
        self._assert_hub_main_questions_twice(
            ADMIN_CONSOLE_INDEX_HTML, "文档链 · 合并前对表"
        )

    def test_spa_layout_tsx_links_hub_main_questions(self) -> None:
        body = SPA_LAYOUT_TSX.read_text(encoding="utf-8")
        self.assertIn(
            _HUB_MAIN_QUESTIONS_FRAG,
            body,
            f"{SPA_LAYOUT_TSX.relative_to(REPO_ROOT)} should reference {_HUB_MAIN_QUESTIONS_FRAG!r}",
        )
        label = "枢纽主问题备忘"
        self.assertGreaterEqual(
            body.count(label),
            2,
            f"{SPA_LAYOUT_TSX.relative_to(REPO_ROOT)} should surface {label!r} "
            "at least twice (壳说明 · 维护脚注)",
        )

    def test_maintainer_hub_docs_readme_hrefs_have_url_fragments(self) -> None:
        body = MAINTAINER_HUB.read_text(encoding="utf-8")
        for m in re.finditer(r'href="(docs/README\.md[^"]*)"', body):
            url = m.group(1)
            self.assertIn(
                "#",
                url,
                f"{MAINTAINER_HUB.relative_to(REPO_ROOT)}: docs/README link missing "
                f"URL fragment: href={url!r}",
            )

    def test_maintainer_hub_hrefs_to_docs_markdown_have_url_fragments(self) -> None:
        body = MAINTAINER_HUB.read_text(encoding="utf-8")
        for m in re.finditer(r'href="(docs/[^"]+\.md[^"]*)"', body):
            url = m.group(1)
            self.assertIn(
                "#",
                url,
                f"{MAINTAINER_HUB.relative_to(REPO_ROOT)}: docs/*.md link missing "
                f"URL fragment: href={url!r}",
            )

    def test_no_contributing_markdown_or_href_without_fragment(self) -> None:
        offenders = collect_doc_link_offenders(REPO_ROOT, "CONTRIBUTING")
        self.assertEqual(
            offenders,
            [],
            "Found CONTRIBUTING.md links missing URL fragment "
            f"(use #contributing-env-and-cmd, #contributing-terminology, etc.): {offenders!r}",
        )

    def test_html_href_contributing_pr_pairing(self) -> None:
        """根目录 *.html 与 admin-console 静态壳：若出现 CONTRIBUTING 的 PR 证据三联或动手→命令速查片段，须与开 PR 前速览一并出现。"""
        triad = "CONTRIBUTING.md#contributing-pr-evidence-triad"
        cmd = "CONTRIBUTING.md#contributing-change-to-command"
        five = "CONTRIBUTING.md#contributing-five-minute"
        paths = list(REPO_ROOT.glob("*.html"))
        admin_index = REPO_ROOT / "admin-console" / "static" / "index.html"
        if admin_index.is_file():
            paths.append(admin_index)
        for path in sorted(paths, key=lambda p: str(p.relative_to(REPO_ROOT))):
            text = path.read_text(encoding="utf-8")
            has_t = triad in text
            has_c = cmd in text
            has_f = five in text
            if has_t or has_c:
                rel = path.relative_to(REPO_ROOT)
                with self.subTest(html=str(rel)):
                    self.assertTrue(
                        has_t and has_c and has_f,
                        f"{rel}: expected {triad!r}, {cmd!r}, and {five!r} together when "
                        "PR triad or command anchor appears",
                    )

    def test_cursor_rules_contributing_pr_pairing(self) -> None:
        """`.cursor/rules/*.mdc`：若出现 CONTRIBUTING 的 PR 证据三联或动手→命令片段，须含开 PR 前速览。"""
        triad = "CONTRIBUTING.md#contributing-pr-evidence-triad"
        cmd = "CONTRIBUTING.md#contributing-change-to-command"
        five = "CONTRIBUTING.md#contributing-five-minute"
        rules_dir = REPO_ROOT / ".cursor" / "rules"
        if not rules_dir.is_dir():
            self.skipTest("missing .cursor/rules")
        for path in sorted(rules_dir.glob("*.mdc")):
            text = path.read_text(encoding="utf-8")
            has_t = triad in text
            has_c = cmd in text
            has_f = five in text
            if has_t or has_c:
                rel = path.relative_to(REPO_ROOT)
                with self.subTest(rules=str(rel)):
                    self.assertTrue(
                        has_t and has_c and has_f,
                        f"{rel}: expected {triad!r}, {cmd!r}, and {five!r} together when "
                        "either appears",
                    )

    def test_agents_md_contributing_pr_pairing(self) -> None:
        """`AGENTS.md`：若出现 CONTRIBUTING 的 PR 证据三联或动手→命令片段，须含开 PR 前速览。"""
        triad = "CONTRIBUTING.md#contributing-pr-evidence-triad"
        cmd = "CONTRIBUTING.md#contributing-change-to-command"
        five = "CONTRIBUTING.md#contributing-five-minute"
        text = AGENTS_MD.read_text(encoding="utf-8")
        has_t = triad in text
        has_c = cmd in text
        has_f = five in text
        if has_t or has_c:
            self.assertTrue(
                has_t and has_c and has_f,
                f"{AGENTS_MD.relative_to(REPO_ROOT)}: expected {triad!r}, {cmd!r}, and "
                f"{five!r} together when either appears",
            )

    def test_pull_request_template_links_contributing_five_minute_triad_cmd(
        self,
    ) -> None:
        body = PR_TEMPLATE.read_text(encoding="utf-8")
        for frag in (
            "CONTRIBUTING.md#contributing-five-minute",
            "CONTRIBUTING.md#contributing-pr-evidence-triad",
            "CONTRIBUTING.md#contributing-change-to-command",
        ):
            self.assertIn(
                frag,
                body,
                f"{PR_TEMPLATE.relative_to(REPO_ROOT)} should link {frag!r}",
            )


if __name__ == "__main__":
    unittest.main()
