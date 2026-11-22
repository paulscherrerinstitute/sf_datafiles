This is an sfdata session. sfdata is the Python library for reading SwissFEL data files, used mostly in Jupyter notebooks.

- Channel names are in the loaded data: take them from the user's inputs, or have the user list them with `.names` (e.g. `data.names`).
- In the object list, channels show their channel name (`name`), and scans and files their path (`fname`). Data files are under `/sf/<endstation>/data/<pgroup>/raw/`.

SwissFEL has two beamlines, Aramis (hard X-rays) and Athos (soft X-rays), with three endstations each:

- Aramis: 1. Alvra,      2. Bernina, 3. Cristallina
- Athos:  1. Diavolezza, 2. Maloja,  3. Furka

Channel names encode this:
`SAR` is SwissFEL Aramis, `SAT` is SwissFEL Athos, `ES` is endstation.
The first digit after `ES` enumerates the endstation. The second digit enumerates instruments within the respective endstation.
For example, `SARES11-...` belongs to instrument 1 in Alvra and `SATES24-...` to instrument 4 in Maloja.

Other common prefixes, shown for Aramis:

- `SARFE`: the front end, e.g. the gas monitor (`SARFE10-PBPG050`) and the spectrometer (`SARFE10-PSSS059`)
- `SAROP`: the optics, e.g. intensity and position monitors (`SAROP11-PBPS117`) and the arrival time monitor (`SAROP11-PALMK118`)
- `SARUN`: the undulators, e.g. the photon energy (`SARUN03-UIND030:FELPHOTENE`)
- `SLAAR`: the lasers, e.g. delay stages (`SLAAR11-LMOT-M451`) and timing (`SLAAR11-LTIM01-EVR0`)
- `SARCL`, `SARMA`, `SARBD` and `S10`: the electron beam, e.g. beam position monitors (`SARCL02-DBPM110`) and the bunch arrival time (`S10BC01-DBAM070`)

Jungfrau detectors are channels, too, named like `JF02T09V03`.

