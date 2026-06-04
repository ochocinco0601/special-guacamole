# Org Hierarchy Redesign — Implementation Transfer Brief

**For:** the implementing AI coding agent (Sonnet 4.6-class), plus the engineer carrying the rationale.
**Source:** a completed, verified reference implementation of this change.
**How to use this:** Read the whole document. Part 1 is the *why* (design). Part 2 is *what to change*. Part 3 is *how to apply and verify* — execute it step by step in the target codebase. Code blocks are **reference from the source implementation — adapt to the target codebase; do not assume identical file names.**

---

## Part 1 — The design (problem · model · why)

### Problem

The `org_hierarchy` reference table (the product organization: **L4 Product Line → L3 Product → L2 Product Area**) had two design weaknesses:

1. **The primary key was an externally-sourced code** (the identifier supplied by the upstream org-data system of record). That value's synthesis is not owned by this application, and it is potentially volatile (reassigned on reorg, or tied to an accounting unit). A volatile, externally-owned value should never be a join key.
2. **The service → org foreign key allowed *any* level.** But the domain rule is firm: **an app is owned by a specific L3**, and each CMDB application id maps to exactly one L4-L3 pair. The "any level" looseness already produced wrong data — every service was anchored at an **L2**, not an L3.

### The model (the decision)

`org_hierarchy` is **current-state reference data**, maintained inside the application (hold-and-edit; humans own the edit), sourced from the upstream org data. No temporal/history modeling. The table keeps its **self-referential adjacency-list** shape (one row per node, `ParentOrgId` self-FK). Four changes:

| # | Change | Rule |
|---|--------|------|
| 1 | `OrgId` → **opaque integer surrogate** (DB-assigned identity) | The key is application-minted and meaningless. The external code is *not* the key. |
| 2 | **`UNIQUE(ParentOrgId, Name)`** | A node name is unique *within its parent*. |
| 3 | **Apps anchor at L3** — the service FK must reference a `Level = 3` node | L4 is derived by walking the parent edge; the L4-L3 pair is never stored. |
| 4 | **Reseed** under the new key scheme | Clean recreate (the prior services were test fixtures, not real). |

### Why — the reasoning

- **Opaque surrogate, not the external code or a "smart" key.** An L3 is only unique *within* its L4, so an L3 *name* is not globally unique — e.g. **the same product name (such as "Cards") can exist under two different Product Lines**. A name key collides; a composite text key like `<line>-<product>` encodes meaning and breaks on rename. An **opaque integer surrogate** gives each "Cards" its own meaningless id (Product Line A's Cards = 47, Product Line B's Cards = 88), and the name collision is handled by the `UNIQUE(ParentOrgId, Name)` constraint — same name allowed under *different* parents, rejected under the *same* parent. This is the standard pattern: surrogate primary key + natural uniqueness as a constraint.
- **Apps anchor at L3, L4 derived.** Storing only the L3 means a reorg that moves an L3 to a different L4 is absorbed by recomputing the rollup — the service FK never has to change. Storing the L4-L3 pair would drift on reorg.
- **Extensible in both directions, by design.** The adjacency list absorbs new tiers as *data, not schema*: a **division tier above L4** (a grouping that contains multiple Product Lines) is just new rows whose children point at them — no schema change. A new descriptive attribute (a cost-center code, an owner email) is an additive nullable column. The only design that would fail this is a smart key or a flattened `(l4,l3,l2)` column table — both rejected.

### Rejected alternatives

| Alternative | Why rejected |
|---|---|
| L3 **name** as key | Not unique — the same name collides across L4s |
| **Smart/composite** text key | Encodes meaning; breaks on rename |
| **External code** as PK | Volatile, externally owned, unknown synthesis |
| **Bitemporal / SCD Type 2** | Over-engineering for human-maintained current-state reference data |
| **Flattened** fixed-depth `(l4,l3,l2)` columns | Not extensible — shatters when a division tier is added above L4 |
| **Numeric *string*** surrogate (`"1001"`) | Type-dishonest; lexicographic sort; app-side id generation. Use a true `int` identity. |

---

## Part 2 — What to change (per layer)

The reference implementation is a .NET / EF Core / SQLite backend + an Angular frontend. **Locate the equivalent in the target codebase; the layers below are the contract, the code is illustration.**

### 2.1 Entity / data model

`OrgId`, `ParentOrgId`, and `Service.OrgId` become integers. The org-node key is a DB-assigned identity.

```csharp
// OrgHierarchy entity
[Key] public int OrgId { get; set; }          // opaque surrogate (was: [Key, MaxLength(20)] string)
public int? ParentOrgId { get; set; }          // self-reference, null for roots (was: string?)

// Service entity
[Required] public int OrgId { get; set; }       // FK to an L3 node (was: [Required, MaxLength(20)] string)
```

### 2.2 EF configuration (model builder)

```csharp
// Unique within parent — same name allowed under multiple L4s, not twice under one
modelBuilder.Entity<OrgHierarchy>()
    .HasIndex(o => new { o.ParentOrgId, o.Name }).IsUnique();

// Service → OrgHierarchy FK, restrict delete
modelBuilder.Entity<Service>()
    .HasOne<OrgHierarchy>().WithMany()
    .HasForeignKey(s => s.OrgId).OnDelete(DeleteBehavior.Restrict);
```

### 2.3 The L3-anchor rule (the key behavioral change)

A cross-row rule (the *referenced* node must be `Level = 3`) can't be a column CHECK — enforce it in the **write path** on create, update, and import:

```csharp
private async Task<ValidationErrorDto?> ValidateL3AnchorAsync(int orgId)
{
    var node = await _db.OrgHierarchy.FirstOrDefaultAsync(o => o.OrgId == orgId);
    if (node != null && node.Level == 3) return null;
    return new ValidationErrorDto { Message = "Service must anchor at an L3 (Product) node",
        Errors = [new FieldErrorDto { Field = "orgId", Rule = "anchor_l3",
            Message = node == null ? $"Org node {orgId} not found"
                                   : $"Org node {orgId} is L{node.Level}; services must anchor at L3" }] };
}
// Call it: create -> BadRequest; update when orgId changes -> BadRequest; import -> UnprocessableEntity.
```

### 2.4 DTOs, controllers, query params

- All `OrgId` / `ParentOrgId` DTO fields → `int` / `int?`.
- `listServices` and readiness `orgId` query params → `int?`.
- `listOrgHierarchy` `parentId` param → `int?`.
- Org-path/breadcrumb resolution that walked `ParentOrgId` as a string → walk it as `int?` (`current.ParentOrgId.HasValue ? …`).

### 2.5 Frontend (Angular)

- `OrgNode`, `FlatOrgNode`, `ServiceCreate/Update`, `PortfolioReadiness` `orgId` → `number`; `parentOrgId` → `number`.
- **Gotcha — HTML `<select>` yields strings.** Keep the reactive-form control as a string, and convert at the API boundary:
  - on **submit** (create/update): `orgId: Number(form.value.orgId)`
  - on **edit-patch** (prefill the select): `orgId: String(service.orgId)`
  - This avoids the `SelectControlValueAccessor` number/string mismatch (a numeric control value won't match string option values).
- Query param: `httpParams.set('orgId', String(params.orgId))`.

### 2.6 API contract (OpenAPI)

`orgId` and `parentOrgId` schema types and the `orgId` query params → `type: integer`. Update descriptions to "opaque surrogate; FK must reference an L3 node; UNIQUE(parentOrgId, name)."

### 2.7 Reseed

Seed org nodes with explicit integer ids and parent pointers; seed a small number of **demo services anchored at L3** to prove the rule. Example node ids: a Product Line (L4) = 1, a Product (L3) = 2, a Product Area (L2) = 3, … . **For a populated UI** (any service-profile / dashboard view), seed or import at least one service with full four-layer signal data anchored at an L3 — identity-only services render empty profiles.

---

## Part 3 — Apply & verify (execute in the target app)

### Step 0 — Decide the DB strategy ⚠️ ENVIRONMENT-SPECIFIC

The reference app uses `EnsureCreated()` (no migrations), so it applies a schema change by **deleting the dev DB and letting it rebuild from the model + seed**.

- **If the target also uses `EnsureCreated` / a disposable dev DB:** delete the dev database file, then run — it rebuilds with the new schema. Acceptable because the data is test fixtures.
- **If the target uses EF migrations / a database you must preserve:** changing a PK column type is a non-trivial migration (drop/recreate the FK constraints, convert/repopulate keys). Generate a migration; if the data is disposable dev data, a drop-and-recreate migration is simplest. **Do not blindly delete a database that holds anything real — confirm with the engineer first.**

### Step 1 — Apply the layer changes

Work Part 2 in this order (each is one logical commit): entity + EF config + reseed → DTOs + controllers (incl. the L3-anchor validation) → frontend types + select coercion → OpenAPI contract → tests. The backend must compile as one unit (the int PK change ripples through entities/DTOs/controllers together).

### Step 2 — Build

- Backend: build the API project. **Expected: 0 errors.**
- Frontend: build the Angular app. **Expected: clean** (pre-existing warnings only).

### Step 3 — Verify behavior (run against the running app)

Replace ids with the target seed's actual L4/L3/L2 ids. Using `1=L4, 2=L3, 3=L2` as in the reference seed:

| Check | Command (adapt host/port) | Expected |
|-------|---------------------------|----------|
| Int surrogate ids | `GET /reference/org-hierarchy` | `orgId` values are integers; tree intact |
| Create at **L3** | `POST /api/v1/services` with `"orgId": 2` | **201** |
| Reject **L2** | `POST …` with `"orgId": 3` | **400**, `rule: anchor_l3`, "is L2" |
| Reject **L4** | `POST …` with `"orgId": 1` | **400**, "is L4" |
| Reject **missing** | `POST …` with `"orgId": 999` | **400**, "not found" |
| Unique constraint | (DB) `PRAGMA index_list('org_hierarchy')` or equivalent | a unique index on `(ParentOrgId, Name)` exists |
| Breadcrumb | `GET /api/v1/services?orgId=2` | a demo service resolves its full L3→L4 path |

### Step 4 — Run the test suite

Migrate any existing E2E/integration specs that hardcode the old string org id: replace the string value with an **L3 integer** in self-provisioning seeds; any "missing required field" import test that sent `orgId: ""` should send `orgId: 0` (the `OrgId <= 0` required-check still fires). Add a focused spec for the L3-anchor rule (create at L3 → 201; L2/L4/missing → 400 `anchor_l3`). **Expected: full suite green.**

### Troubleshooting

- **Service create returns 400 unexpectedly** → the `orgId` you sent isn't a `Level = 3` node. Check the seed's actual L3 id.
- **Import 400/deserialization error** → an `orgId` is being sent as a JSON *string*; it must be a number.
- **Edit form's org dropdown doesn't preselect** → you patched a number into a `<select>`-bound control; patch `String(orgId)` (see 2.5).
- **Migration fails on PK type change** → drop/recreate dependent FK constraints first, or (dev only) drop-and-recreate the DB.

---

## Reference verification (source implementation, already passing)

Backend + Angular build clean · live HTTP checks pass (L3→201, L2/L4/missing→400 `anchor_l3`) · `PRAGMA` confirms int PK + unique index · **full end-to-end suite green** including new tests for the L3-anchor rule. The full design rationale lives in an Architecture Decision Record (ADR) alongside the source implementation.
