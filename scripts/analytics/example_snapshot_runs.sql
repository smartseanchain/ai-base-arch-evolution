-- 最近写入 SQLite 的分析快照历史（列与 scripts/sqlite_store.py · DDL_SNAPSHOT_HISTORY 一致）
SELECT
  run_id,
  repo_revision,
  generated_at,
  stored_at,
  length(snapshot_json) AS snapshot_json_bytes
FROM analysis_snapshot_history
ORDER BY stored_at DESC
LIMIT 20;
