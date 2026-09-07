# Functional Specification – Example Project

## 1. Purpose and goals

Tjänsten ska göra det möjligt för en användare att ladda upp ett lokalt projekt som ZIP och skapa ett nytt repository i sitt GitHub-konto utan manuell filkopiering.

## 2. Scope

### Must

- ladda upp en projekt-ZIP,
- validera att ZIP-filen är säker att packa upp,
- skapa ett nytt GitHub-repository,
- ladda upp projektets filer,
- visa resultatet för användaren.

### Should

- låta användaren välja private/public.

### Could

- föreslå repositorynamn från projektmetadata.

## 3. Actors

- **User** – äger projektet och initierar repository-skapandet.
- **GitHub** – externt system som tar emot repository och filer.

## 4. Main use cases

### UC-001 – Create repository from ZIP

**Primary actor:** User  
**Goal:** Få ett lokalt projekt publicerat som nytt GitHub-repository.

**Main flow**

1. Användaren väljer en projekt-ZIP.
2. Systemet validerar ZIP-filen.
3. Användaren anger repositorynamn och synlighet.
4. Systemet skapar repositoryt.
5. Systemet laddar upp projektfilerna.
6. Systemet visar en länk till repositoryt.

**Important alternatives / exceptions**

- ZIP-filen är ogiltig eller osäker.
- Repositorynamnet finns redan.
- GitHub är tillfälligt otillgängligt.

**Result:** Ett repository finns på GitHub med projektets filer.

## 5. Functional requirements

### FR-001 – Upload project ZIP

**Priority:** Must

Användaren ska kunna välja och ladda upp en ZIP-fil som representerar ett projekt.

### FR-002 – Validate uploaded ZIP

**Priority:** Must

Systemet ska avvisa ZIP-filer med osäkra paths eller poster innan projektinnehåll behandlas.

### FR-003 – Create GitHub repository

**Priority:** Must

En behörig användare ska kunna skapa ett nytt GitHub-repository från den validerade projekt-ZIP:en.

## 6. Business rules

### BR-001

Repositorynamn måste vara giltigt enligt GitHubs regler och får inte kollidera med ett befintligt repository som användaren inte uttryckligen valt att ersätta.

## 7. Information needs

- uppladdad projektfil,
- repositorynamn,
- repository visibility,
- GitHub-identitet,
- resultat-URL.

## 8. Integrations

GitHub används för att skapa repository och lagra projektinnehållet. Vid integrationsfel ska användaren få veta om repositoryt skapades helt, delvis eller inte alls.

## 9. Authorization

Endast autentiserade användare med tillräcklig GitHub-behörighet får skapa repositoryn.

## 10. Errors and exceptional cases

- osäker ZIP avvisas före extraktion,
- namnkonflikt ska inte automatiskt skriva över befintligt repository,
- partiellt misslyckad uppladdning ska rapporteras som sådan.

## 11. Non-functional requirements

### NFR-001 – Safe ZIP handling

**Priority:** Must

ZIP-inspektion och extraktion ska förhindra path traversal och absoluta paths.

## 12. Acceptance criteria

### AC-001

När användaren laddar upp en giltig ZIP, anger ett ledigt repositorynamn och har nödvändig GitHub-behörighet ska ett repository skapas med projektets filer.

**Related requirements:** FR-001, FR-003

### AC-002

När ZIP-filen innehåller en parent-traversal path ska den avvisas och inget repositoryinnehåll skapas från filen.

**Related requirements:** FR-002, NFR-001

## 13. Out of scope

- automatisk deployment av projektet,
- migrering från annan Git-host,
- sammanslagning med ett befintligt repository.

## 14. Open questions

### Blocking

- None.

### Non-blocking

- Om repositorynamn ska kunna föreslås automatiskt i första release.
