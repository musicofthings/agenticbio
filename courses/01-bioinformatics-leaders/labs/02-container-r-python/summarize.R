files <- list.files("/data", full.names = FALSE)
dir.create("/outputs", showWarnings = FALSE)
writeLines(
  paste0("r files=", paste(files, collapse = ","), " count=", length(files)),
  con = "/outputs/r_summary.txt"
)
