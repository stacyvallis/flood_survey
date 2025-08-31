# Format data
python code/format_surveys.py
python code/format_questions.py
python code/filter_exclusion_criteria.py

# Split data into formats
python code/splitter.py results/filt_surveys.tsv format --df2 conf/questions.xlsx

# Make table1
python code/proportions.py
python code/averages.py
python code/multichoice.py
python code/merge_to_make_table1.py

# Make network
## Run statistical analysis
python code/corr.py results/filt_surveys_format_numeric.tsv -o results/numberscorr.tsv
python code/kruskal.py results/filt_surveys_format_numeric.tsv results/filt_surveys_format_category.tsv -o results/numbers_kruskal.tsv
python code/chisquared.py results/filt_surveys_format_category.tsv -o results/categories_chisq.tsv

## Merge statistics
python code/merge_stats.py

## Get summary of stats
python code/sig_summary.py -i results/edges.tsv -o results/summary.tsv -s qval -c effect

## Final significance filtering
python code/filter.py results/edges.tsv results/edgesfilter.tsv -q 'qval < 0.05' 

## Create and analyze the network
python code/create_network.py --edges results/edgesfilter.tsv --output results/network.graphml

# Make figure1
python code/risk.py

# Plot significant results
python code/regplot.py --input results/filt_surveys.tsv --output results/Q13reg.svg -x Q13 -y Q3 --figsize 2.5,1.5
python code/box.py --input results/filt_surveys.tsv --output results/Q10box.svg -x Q10 -y Q3 --order 'Not Worried,Partly Worried,Worried,Very Worried' --figsize 2.5,1.5
python code/regplot.py --input results/filt_surveys.tsv --output results/Q7reg.svg -x Q13 -y Q7 --figsize 2.5,1.5
python code/box.py --input results/filt_surveys.tsv --output results/Q8box.svg -x Q8 -y Q3 --order 'Yes,No,Unsure' --figsize 2.5,1.5
python code/regplot.py --input results/filt_surveys.tsv --output results/Q12reg.svg -x Q12 -y Q3 --figsize 2.5,1.5
python code/box.py --input results/filt_surveys.tsv --output results/Q5box.svg -x Q5 -y Q3 --order 'Yes,No,Unsure' --figsize 2.5,1.5
python code/box.py --input results/filt_surveys.tsv --output results/Q9box.svg -x Q9 -y Q3 --order 'Yes,No,Unsure' --figsize 2.5,1.5

# Arrange them together
python code/arrange_svgs.py --cols 1 results/Q13reg.svg results/Q10box.svg results/Q7reg.svg results/Q8box.svg -o results/sigplots.svg
python code/arrange_svgs.py --cols 1 results/Q12reg.svg results/Q5box.svg results/Q9box.svg -o results/sigplots2.svg

# Make Supp tables
python code/makesupptable.py
