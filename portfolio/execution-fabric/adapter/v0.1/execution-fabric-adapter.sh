#!/usr/bin/env bash
set -euo pipefail

# Execution Fabric Adapter v0.1
#
# Scope: Kestra OSS local runtime lifecycle + execution transport only.
# It MUST NOT own or infer consumer semantics.
#
# Consumers remain independently runnable. Vendoring this file is allowed and
# preferred over introducing a hard runtime dependency on the portfolio repo.

EF_ADAPTER_VERSION="0.1.0"
EF_KESTRA_VERSION="${EF_KESTRA_VERSION:-2.0.5}"
EF_TENANT="${EF_TENANT:-main}"
EF_BASE_URL="${EF_BASE_URL:-http://localhost:8080}"
EF_AUTH_USER="${EF_AUTH_USER:-ci@kestra.io}"
EF_AUTH_PASSWORD="${EF_AUTH_PASSWORD:-Kestra123!}"
EF_RUNTIME_ROOT="${EF_RUNTIME_ROOT:-/tmp/kestra-runtime}"
EF_BIN="${EF_BIN:-/tmp/kestra}"
EF_CONFIG="${EF_CONFIG:-/tmp/kestra-config.yml}"
EF_SERVER_LOG="${EF_SERVER_LOG:-/tmp/kestra-server.log}"
EF_FLOW_CREATE_JSON="${EF_FLOW_CREATE_JSON:-/tmp/kestra-flow-create.json}"
EF_EXECUTION_JSON="${EF_EXECUTION_JSON:-/tmp/kestra-execution.json}"
EF_TASK_OUTPUTS_JSON="${EF_TASK_OUTPUTS_JSON:-/tmp/kestra-task-outputs.json}"
EF_EXECUTION_RECORD="${EF_EXECUTION_RECORD:-/tmp/execution-record.json}"

ef_download_kestra() {
  curl -fL --retry 3     -o "$EF_BIN"     "https://github.com/kestra-io/kestra/releases/download/v${EF_KESTRA_VERSION}/kestra-${EF_KESTRA_VERSION}"
  chmod +x "$EF_BIN"
}

ef_start_kestra() {
  cat >"$EF_CONFIG" <<YAML
kestra:
  server:
    basic-auth:
      username: $EF_AUTH_USER
      password: "$EF_AUTH_PASSWORD"
YAML

  mkdir -p "$EF_RUNTIME_ROOT"
  (
    cd "$EF_RUNTIME_ROOT"
    KESTRA_PLUGINS_AUTO_INSTALL_ENABLED=true       nohup "$EF_BIN" server local --config "$EF_CONFIG"       >"$EF_SERVER_LOG" 2>&1 &
    echo $! >/tmp/kestra.pid
  )

  for _ in $(seq 1 90); do
    if curl -fsS "$EF_BASE_URL/" >/dev/null; then
      return 0
    fi
    sleep 2
  done

  cat "$EF_SERVER_LOG"
  return 1
}

ef_create_flow() {
  local flow_file="$1"

  set -o pipefail
  curl -fsS -u "$EF_AUTH_USER:$EF_AUTH_PASSWORD" -X POST     "$EF_BASE_URL/api/v1/$EF_TENANT/flows"     -H 'Content-Type: application/x-yaml'     --data-binary "@$flow_file"     | tee "$EF_FLOW_CREATE_JSON"
}

ef_execute_flow() {
  local namespace="$1"
  local flow_id="$2"
  local task_id="$3"
  shift 3

  set -o pipefail
  curl -fsS -u "$EF_AUTH_USER:$EF_AUTH_PASSWORD" -X POST     "$EF_BASE_URL/api/v1/$EF_TENANT/executions/$namespace/$flow_id?wait=true"     "$@"     | tee "$EF_EXECUTION_JSON"

  jq -e '.state.current == "SUCCESS"' "$EF_EXECUTION_JSON"

  local execution_id
  local task_run_id
  execution_id="$(jq -r '.id' "$EF_EXECUTION_JSON")"
  task_run_id="$(jq -r --arg task_id "$task_id" '.taskRunList[] | select(.taskId == $task_id) | .id' "$EF_EXECUTION_JSON")"

  test -n "$execution_id"
  test -n "$task_run_id"
  test "$execution_id" != "null"
  test "$task_run_id" != "null"

  curl -fsS -u "$EF_AUTH_USER:$EF_AUTH_PASSWORD"     "$EF_BASE_URL/api/v1/$EF_TENANT/outputs/tasks/$execution_id/$task_run_id"     | tee "$EF_TASK_OUTPUTS_JSON"

  jq -er '.vars.execution_record' "$EF_TASK_OUTPUTS_JSON"     | tee "$EF_EXECUTION_RECORD"
}

ef_assert_execution_envelope() {
  local authority_field="$1"
  local authority_value="$2"

  jq -e     --arg authority_field "$authority_field"     --arg authority_value "$authority_value" '
      .schema_version == 1 and
      .orchestration_state == "KNOWN_SUCCESS" and
      .reason != null and
      (.kestra_execution_id | type == "string" and length > 0) and
      .orchestrator_mutates_evidence == false and
      .[$authority_field] == $authority_value and
      (.artifacts | type == "object")
    ' "$EF_EXECUTION_RECORD"
}

ef_assert_checkout_clean() {
  local repo_root="$1"
  local repo_status
  repo_status="$(git -C "$repo_root" status --porcelain)"
  if [ -n "$repo_status" ]; then
    printf '%s\n' "Repository mutation detected:" "$repo_status"
    return 1
  fi
}

ef_print_identity() {
  printf 'execution-fabric-adapter=%s kestra=%s\n'     "$EF_ADAPTER_VERSION" "$EF_KESTRA_VERSION"
}
