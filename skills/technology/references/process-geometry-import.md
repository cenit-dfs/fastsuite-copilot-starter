# Process-geometry import decision table

Read [`docs/technology/process-geometry-import.md`](../../../docs/technology/process-geometry-import.md) for the full guide.

| Concern | Owner |
|---|---|
| Parse source rows, convert units/orientation, create points | Process-geometry importer |
| Store values that travel with each point | Process-geometry attributes |
| Expose imported values to operation UI/output | Workmethod `PostWmInitAttributes` + `PostWmSyncPgAttributes` |
| Add built-in events after programming | AutoExecute auxiliary command |
| Emit controller syntax | Downloader, after tree dump confirms the data exists |

Required checks:

1. Document source units and Euler/axis convention.
2. Treat modifier rows as pending state and clear them after the next move.
3. Use `Has_*` flags to distinguish absent values from zero.
4. Guard optional reads before calling typed getters.
5. Define repeated AutoExecute behavior so events are not duplicated accidentally.
6. Tree-dump process geometry, synchronized operations, programmed motions, and inserted events.
