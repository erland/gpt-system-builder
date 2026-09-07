# System Builder – Final hygiene and release readiness

SB-40 är den sista granskningen före RC-paketering.

Required gates omfattar:
- runtime/Knowledge contract,
- CI och release workflows,
- fresh distribution builds,
- distribution validation,
- runtime parity,
- tidigare verifierade E2E CREATE/CHANGE/Docker-Coolify,
- repository hygiene,
- blocker state,
- Custom GPT instruction limit.

E2E-resultat får återanvändas från canonical persisted reports när de redan verifierats i föregående steg. Ett avbrutet eller timeoutat omkörningsförsök får aldrig konverteras till PASS.

Beslut:
- READY
- READY_WITH_WARNINGS
- NOT_READY

Live external deployment kan vara en uttrycklig warning/pending gate utan att blockera RC-paketering, så länge inget live PASS fabriceras.
