# DB 규칙 (MySQL → 추후 Supabase 마이그레이션 고려)

## 네이밍
- 테이블/컬럼: snake_case
- 최소 테이블 4개
  - `devices(id, name, kind, created_at)` — `id`는 `led_1`처럼 짧고 읽기 쉬운 슬러그를
    기본키로 써도 되고 자동증가 정수를 써도 된다(팀이 정한다). 다른 테이블은 전부
    이 `id`를 `device_id`로 참조한다
  - `sensor_readings(id, device_id, value, unit, created_at)`
  - `control_log(id, device_id, action, value, actor, created_at)` — actor는 `'user'` 또는 `'device'`
  - `vision_events(id, event_type, detected, count, confidence, created_at)`

## 경보성 디바이스 원칙
`devices.kind`가 경보성(예: 침입감지)인 디바이스는 트리거 로직이 절대 자동으로 원래
상태로 되돌리지 않는다 — 대시보드에서 사람이 수동으로 해제해야 한다
(`dashboard-ui-design` 스킬의 AlertCard 참고).

## 마이그레이션 호환성
- MySQL 전용 문법(`AUTO_INCREMENT`, `ENUM(...)` 등)을 쓸 때는 주석으로 `-- MySQL-only`
  표시해둔다 (db-migration 스킬에서 Supabase 전환 시 이 주석을 기준으로 변환한다)
- 날짜/시간은 UTC로 저장하고, 타임존 변환은 애플리케이션 레이어에서 처리한다

## 쓰기 경로
- 개발 단계(MySQL): 백엔드가 직접 커넥션을 통해 쓴다
- 배포 단계(Supabase): 백엔드는 `service_role` 키로 RLS를 우회해서 쓴다.
  프론트엔드는 절대 DB에 직접 쓰지 않는다 — 항상 백엔드 API를 거친다
