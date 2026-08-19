# Freezer temperature log (synthetic)

Teaching SOP for a fictional core facility. Not a real institute document.

## Purpose

Record freezer temperature once per shift so a later audit can see gaps. This note is about *logging*, not about sample contents.

## Procedure

1. Read the display on SYNTH-FREEZER-01.
2. Write timestamp, operator initials, and temperature (°C) into `logs/freezer-YYYY-MM.tsv`.
3. If the reading is outside -70 to -90, page the on-call operator listed on the door card. Do not invent a workaround in chat.

## File naming

`logs/freezer-YYYY-MM.tsv` with header `timestamp\toperator\ttemp_c`.
