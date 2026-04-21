/** 由 spa/nav.config.json + scripts/gen_nav_links_ts.py 生成；请勿手改。
 * 顺序与文案：编辑 spa/nav.config.json 后执行 python3 scripts/gen_nav_links_ts.py --write
 * 与 partials/site-nav.inc.html 对齐；path 为 React Router（无 .html）
 * 改根 *.html 后维护 SPA iframe：make spa-sync；见 ../docs/MERGE_AND_RELEASE_CHECKLIST.md#pre-merge · #pre-merge-partials-sequence · ../maintainer-hub.html#mh-spine-map · #mh-boundaries · #mh-reader-admin-matrix
 */
export const NAV_LINKS: { to: string; label: string }[] = [
  { to: "/", label: "总览" },
  { to: "/nexus", label: "立体联结" },
  { to: "/edu-nexus", label: "教育纵轴" },
  { to: "/evolution-triad", label: "人与AI演进" },
  { to: "/model", label: "分层模型" },
  { to: "/modules-map", label: "模块图谱" },
  { to: "/timeline", label: "历史演进" },
  { to: "/past-future", label: "廿年视角" },
  { to: "/decade", label: "十年展望" },
  { to: "/decade-scenes", label: "十年场景" },
  { to: "/decade-us", label: "十年之问" },
  { to: "/synthesis", label: "综合推演" },
  { to: "/synthesis-extensions", label: "推演·扩展" },
  { to: "/synthesis-methods", label: "推演·方法" },
  { to: "/lab", label: "沙盘工坊" },
  { to: "/evolution-loop", label: "进化闭环" },
  { to: "/work-infra-energy", label: "职业·基建·能源" },
  { to: "/risk-geo", label: "地缘与商业" },
  { to: "/net-biz-capital", label: "网·商·资·工" },
  { to: "/national-strategy-opinion", label: "战略·舆情" },
  { to: "/social-responsibility-evolution", label: "社会责任" },
  { to: "/architecture", label: "架构拓扑" },
  { to: "/analysis-hub", label: "分析引擎" },
  { to: "/intelligent-evolution", label: "智能进化" },
  { to: "/smart-overhaul", label: "整体改造" },
  { to: "/evolvable-architecture", label: "可进化架构" },
  { to: "/maintainer-hub", label: "维护导读" },
  { to: "/legacy-all-in-one", label: "单页归档" },
];

export type NavGroup = { title: string | null; items: { to: string; label: string }[] };
export const NAV_GROUPS: NavGroup[] = [
  { title: null, items: [{ to: "/", label: "总览" }] },
  { title: "联结与模型", items: [{ to: "/nexus", label: "立体联结" }, { to: "/edu-nexus", label: "教育纵轴" }, { to: "/evolution-triad", label: "人与AI演进" }, { to: "/model", label: "分层模型" }, { to: "/modules-map", label: "模块图谱" }] },
  { title: "时间与情景", items: [{ to: "/timeline", label: "历史演进" }, { to: "/past-future", label: "廿年视角" }, { to: "/decade", label: "十年展望" }, { to: "/decade-scenes", label: "十年场景" }, { to: "/decade-us", label: "十年之问" }] },
  { title: "推演与沙盘", items: [{ to: "/synthesis", label: "综合推演" }, { to: "/synthesis-extensions", label: "推演·扩展" }, { to: "/synthesis-methods", label: "推演·方法" }, { to: "/lab", label: "沙盘工坊" }, { to: "/evolution-loop", label: "进化闭环" }] },
  { title: "制度与地缘", items: [{ to: "/work-infra-energy", label: "职业·基建·能源" }, { to: "/risk-geo", label: "地缘与商业" }, { to: "/net-biz-capital", label: "网·商·资·工" }, { to: "/national-strategy-opinion", label: "战略·舆情" }, { to: "/social-responsibility-evolution", label: "社会责任" }] },
  { title: "架构与分析", items: [{ to: "/architecture", label: "架构拓扑" }, { to: "/analysis-hub", label: "分析引擎" }, { to: "/intelligent-evolution", label: "智能进化" }, { to: "/smart-overhaul", label: "整体改造" }, { to: "/evolvable-architecture", label: "可进化架构" }] },
  { title: null, items: [{ to: "/maintainer-hub", label: "维护导读" }] },
  { title: null, items: [{ to: "/legacy-all-in-one", label: "单页归档" }] },
];
