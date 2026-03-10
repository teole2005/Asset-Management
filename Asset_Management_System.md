# Asset Management System v1 (SQLite-First)

## Summary
- Build an admin-only internal web app with Django, server-rendered pages, session auth, SQLite, and local file storage for invoices/uploads.
- Keep SQLite for v1 with explicit limits: the app and `db.sqlite3` must run on the same server and local disk; no network-mounted database file and no multi-app-server deployment. If the system later needs heavier concurrent writes, multi-node deployment, or a centralized shared database, migrate to PostgreSQL.
- v1 includes asset CRUD, assignment tracking, repair logs, sale/disposal records, physical audits, CSV/XLSX export, controlled Excel import jobs, dashboard/email alerts, and real backup/restore.

## Key Changes
- SQLite operating model: enable WAL mode for better read/write concurrency, enable `PRAGMA foreign_keys=ON` on every connection, and add a startup health check that fails fast if WAL or foreign-key enforcement is not active.
- Data storage: structured data stays in SQLite; uploaded files stay outside the webroot in a managed `media/` folder; exports are report files only and are not backups.
- Core records: `Asset`, `AssetType`, `StaffMember`, `Department`, `Location`, `Vendor`, `Assignment`, `RepairLog`, `SaleDisposal`, `Attachment`, `PhysicalAudit`, `ImportBatch`, `BackupBundle`, and append-only `AuditEvent`.
- Asset source fields: `legacy_no`, `type`, `owner`, `tracking_code`, `asset_tag`, `brand`, `model`, `serial_no`, `price`, `purchase_date`, `estimate_lifespan_months`, `start_date`, `warranty_expiry_date`, `supplier/vendor`, `invoice_no`, `condition`, `current_location`, `department`, `custodian_it_owner`, `specs_json` for CPU/RAM/Storage or printer/monitor fields, plus created/updated by/date.
- Derived read-only values: `expiry_date`, `used_years`, `replacement_flag`, `current_assignee`, `replacement_due_soon`, `warranty_due_soon`, `audit_due_soon`, `last_audit_at`, and `next_audit_due_at` are computed from source data and history, not stored as editable fields.
- Canonical asset status: `Available`, `Assigned`, `Under Repair`, `Retired`, `Sold`, `Disposed`. `current_holder` comes only from the active assignment record. Legacy spreadsheet `Occupied` imports as `Assigned`.
- Integrity rules: unique `tracking_code`, unique `asset_tag`, unique nonblank `serial_no`, one active assignment per asset, one open repair per asset in v1, nonnegative money fields, positive lifespan, valid date ordering, and no assignment/repair allowed for `Sold` or `Disposed`.
- Delete policy: assets are not hard-deleted in normal use; lifecycle states replace delete. Only failed import rows with no downstream references may be purged by `super_admin`.
- Sale/disposal rule: suggested staff sale price uses straight-line depreciation from purchase price over lifespan with a 10% floor; admin may set a final override price, and both values are logged.
- Import becomes a controlled job: upload CSV/XLSX, map columns, preview normalized values, run dry-run validation, produce duplicate and row-error reports, assign an import batch ID, and commit all rows in one transaction or roll back the whole batch.
- Export supports CSV and XLSX for assets, assignments, repairs, sales/disposals, and audit/activity views; export respects the current filters/search, and `super_admin` alone may export security/auth audit views.
- Backup/restore moves into v1: provide a `Backups` admin page for manual backup, scheduled nightly backups, download/listing, and restore from server-side backup bundles. Backups use SQLite’s online backup API for a live-consistent DB snapshot, then bundle that snapshot with the exact media files referenced by the snapshot and a manifest with timestamps, schema version, and hashes.
- Restore flow: `super_admin` only, maintenance mode required, automatic pre-restore safety backup first, validate manifest/schema/hash, restore DB plus media together, run integrity checks, then bring the app back online.
- Physical audits: record `found/missing`, `verified_location`, `verified_condition`, `audited_by`, `audited_at`, and `follow_up_action`; show “never audited” separately from “audit due”.
- Dashboard/alerts: totals by status, due-for-replacement, due-for-audit, warranty due soon, open repairs, missing invoices, and recent changes; send daily email reminders for due-soon and overdue items.

## Interfaces
- Main routes: `/login`, `/dashboard`, `/assets`, `/assets/new`, `/assets/{id}`, `/assets/{id}/edit`, `/assets/{id}/assign`, `/assets/{id}/repair`, `/assets/{id}/sell`, `/audits`, `/imports`, `/exports`, `/backups`, `/staff`, `/departments`, `/settings`, `/audit-log`.
- Permission matrix: `super_admin` has full access including admin-user management, backup/restore, full security logs, and system settings; `admin` can manage assets, staff, departments, locations, assignments, repairs, sales, imports, uploads, and normal exports, but cannot manage admin accounts, restore backups, or access security-only logs.
- Authorization model: deny by default on every request and action, enforce permissions in middleware plus service-layer checks, and re-check object-level permissions before state changes or file access.
- Session and request security: HTTPS required outside local development, `Secure` + `HttpOnly` + `SameSite=Lax` session cookies, session ID regeneration on login and any privilege change, CSRF protection on every state-changing route, and login throttling with failed-attempt logging.
- Upload security: allowlist `pdf`, `jpg`, `jpeg`, `png`; verify actual file type, rename on upload, cap size at 10 MB per file, keep files outside webroot, restrict download authorization, and run antivirus scanning when available.

## Test Plan
- Verify SQLite startup config sets WAL and `foreign_keys=ON`, and schema constraints reject duplicate keys, invalid dates, and invalid lifecycle states.
- Verify import dry-run catches missing required fields, bad dates/prices, duplicate `tracking_code`/`asset_tag`/`serial_no`, and that failed validation rolls back the batch completely.
- Verify computed fields and flags render correctly from source data and history, including sale price, replacement due soon, warranty due soon, and audit due soon.
- Verify assignment and repair rules prevent two active assignments or two open repairs for one asset, and block actions on `Sold` or `Disposed`.
- Verify backup creates a consistent SQLite snapshot plus matching media bundle during live use, and restore recovers both DB and files together.
- Verify login/logout, failed login, session rotation, CSRF enforcement, deny-by-default authorization, and permission boundaries for every admin route/action.
- Verify file uploads reject disallowed types and oversize files, store randomized filenames, and require authorization for download/delete.
- Verify audit logging captures login/logout, failed login, session events, create/update/state-change actions, import/export, upload/download/delete, backup/restore, and permission-denied attempts.

## Assumptions and Defaults
- Keep Django ORM and migrations PostgreSQL-compatible so the later migration path is straightforward.
- Default backup schedule is nightly with 14 retained daily bundles; manual backups are retained until deleted by `super_admin`.
- Import migration uses `Asset_Search_listing_latest.xlsx` as the primary source; `asset_tag` defaults to `tracking_code` when migrated rows do not have a separate tag.
- Yearly physical audit cadence stays in v1; if an asset has no historical audit, show `Never audited` and set the first due date from the migration date, not from the original purchase date.
- Source references used for these decisions: [SQLite Appropriate Uses](https://www.sqlite.org/whentouse.html), [SQLite WAL](https://sqlite.org/wal.html), [SQLite Backup API](https://sqlite.org/backup.html), [SQLite Foreign Keys](https://www.sqlite.org/foreignkeys.html), [NIST SP 800-128](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-128.pdf), [NIST SP 800-171r3 CM-08](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/800-171r3/NIST.SP.800-171r3.html), [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html), [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html), [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html), and [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html).
