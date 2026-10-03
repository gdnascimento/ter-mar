# 01 — Data sources

## Summary

| Source | Contributes | Grain | Access | Required for v1 |
| --- | --- | --- | --- | --- |
| SIH/SUS `RD` (AIH reduzida) | ICU days, death, diagnosis, município of residence and of treatment | One record per AIH per billing month | DATASUS file transfer, `.dbc`, via PySUS | Yes |
| CNES `LT` / `ST` | ICU beds by type; establishment identity | Establishment-month | DATASUS file transfer | Yes |
| IBGE códigos + população | Denominators, names, UF, the 6↔7 digit crosswalk | Município-year | IBGE localidades / SIDRA API | Yes |
| IBGE malhas v3 | Map geometry | Município | `servicodados.ibge.gov.br/api/v3/malhas` | M6 |
| Regiões de Saúde / CIR | The peer grouping | Município | DATASUS auxiliary tables | Yes |
| ANS beneficiários | Private-plan coverage, as a confounder and context strip | Município-month | ANS open data | M5 |
| SIM | Deaths that never reached hospital | Death record | DATASUS file transfer | Phase 2 |

Authoritative field reference: the PCDaS/Fiocruz SIH-SUS *dicionário de
variáveis*. Codings differ between layout versions — check it, do not assume.

## SIH `RD` fields used

### Identity and deduplication
| Field | Use |
| --- | --- |
| `N_AIH` | The chain key. Collapse on this |
| `IDENT` | `1` = AIH normal, `5` = longa permanência / continuation |
| `DT_INTER`, `DT_SAIDA` | Stay bounds after collapse: min and max across the chain |

### Geography
| Field | Use |
| --- | --- |
| `MUNIC_RES` | Residence view key. 6-digit |
| `MUNIC_MOV` | Provider view key. 6-digit |
| `CNES` | Establishment. Used internally for coding-discontinuity checks; never published |

### ICU exposure
| Field | Use |
| --- | --- |
| `UTI_MES_TO` | ICU days billed in the month. Summed across the chain; `> 0` defines ICU exposure |
| `MARCA_UTI` | ICU type. Case-mix covariate and potential stratification |
| `UTI_INT_TO` | Intermediate care days. Not ICU; do not count as exposure |

### Outcome
| Field | Use |
| --- | --- |
| `MORTE` | Death indicator. Taken from the last record in the chain |
| `COBRANCA` | Discharge reason. `41`–`43` are deaths; `31`/`32` are transfers out |

### Case-mix
| Field | Use |
| --- | --- |
| `IDADE` + `COD_IDADE` | Age. `COD_IDADE` gives the unit — days, months or years. Normalise to years |
| `SEXO` | Covariate |
| `DIAG_PRINC` | Primary ICD-10. Mapped to a diagnosis group, not used raw |
| `DIAG_SECUN` | Secondary ICD-10. Use with care: recording completeness varies by hospital |
| `PROC_REA` | Procedure performed |
| `CAR_INT` | Elective vs urgent. A strong predictor; do not omit |
| `COMPLEX`, `ESPEC` | Complexity and bed specialty |
| `DIAS_PERM` | Length of stay. Summed across the chain |

## Known gotchas

1. **Município codes are 6 digits in SIH, 7 in IBGE.** SIH drops the check
   digit. One crosswalk table, built in `transform/crosswalk.py`, used for every
   join. Never join on município name — dozens repeat across states.
2. **`.dbc` is a DATASUS-specific compressed `.dbf`.** It needs `blast-dbf`
   decompression, which PySUS bundles.
3. **Continuation AIHs double-count.** Group by `N_AIH`, sum `UTI_MES_TO` and
   `DIAS_PERM`, take the outcome from the record with the latest `DT_SAIDA`.
4. **Município boundaries move.** New municípios are created and codes change.
   Pin the IBGE vintage in `config.py` and record it in `meta.json`.
5. **`COD_IDADE` is not optional.** An infant recorded as `IDADE = 6`,
   `COD_IDADE = 2` (months) becomes a 6-year-old if you ignore the unit, and
   paediatric ICU case-mix silently corrupts.
6. **DATASUS revises history.** Record the extraction date; never compare two
   runs without it.

## Storage layout

```
data/raw/sih/uf=GO/year=2021/month=01/RDGO2101.parquet
data/raw/cnes/uf=GO/year=2021/month=01/LTGO2101.parquet
data/raw/ibge/municipios-2022.parquet
data/interim/stays/uf=GO/*.parquet        # after collapse
data/interim/casemix/uf=GO/*.parquet      # after case-mix derivation
data/out/municipality_metrics.parquet     # modelled, both views
```

Raw files are written once and never re-downloaded. If a re-ingest is needed,
delete the partition explicitly — the pipeline will not silently overwrite.
