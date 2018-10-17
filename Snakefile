
##############################################
## Misc
##############################################

# configfile: 'config.yaml'

# Run R with the following options
# do not save workspace after session
# do not restore previously saved objects
# print all information while running the process

run_R = "Rscript --no-save --no-restore --verbose"
run_P = "python"

GRAPHS = ["graph_1", "graph_2"]

##############################################
## Get all input filenames
##############################################


# all: just there to check all jobs are done
rule all:
    input:
        "output/Report.pdf"

rule scrape_ranking:
    input:
        script = "input/code/scrape_ranking.py",
    output:
        "input/raw_data/restaurant_ranking.csv"
    shell:
        "{run_P} {input.script}"

## make_graphs: performs the analysis and outputs the graphs
rule make_graphs:
    input:
        script = "input/code/Analysis.R",
        data = "input/raw_data/restaurant_ranking.csv",
    output:
        expand("output/graphs/{graph}.png", graph=GRAPHS),
        "output/data/corr.tex",
    shell:
        "{run_R} {input.script}"

## make_pdf: makes the final pdf
rule make_pdf:
    input:
        tex = "input/code/Report.tex",
        graphs = expand("output/graphs/{graph}.png", graph=GRAPHS)
    output:
        pdf = "output/Report.pdf"
    run:
        shell("cd input/code && pdflatex -output-directory ../../output Report.tex")
        shell("rm output/Report.aux")
        shell("rm output/Report.log")
        shell("rm output/Report.out")

## clean: removes all a part from folders
rule clean:
    shell:
        "find ./output -type f -delete"


## help: help other users for the bad naming
rule help:
    input:
        "Snakefile"
    shell:
        "sed -n 's/^##//p' {input}"
