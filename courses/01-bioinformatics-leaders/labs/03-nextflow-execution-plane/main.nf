nextflow.enable.dsl = 2

params.input = 'data/input.txt'
params.outdir = 'results'

process COUNT_LINES {
    input:
    path infile

    output:
    path 'nlines.txt'

    script:
    """
    wc -l < ${infile} | tr -d ' ' > nlines.txt
    """
}

process WRITE_SUMMARY {
    publishDir params.outdir, mode: 'copy'

    input:
    path nlines
    path infile

    output:
    path 'summary.txt'

    script:
    """
    echo "input=${infile}" > summary.txt
    echo -n "n_lines=" >> summary.txt
    cat ${nlines} >> summary.txt
    echo "runner=nextflow" >> summary.txt
    """
}

workflow {
    ch_in = channel.fromPath(params.input)
    COUNT_LINES(ch_in)
    WRITE_SUMMARY(COUNT_LINES.out, ch_in)
}
