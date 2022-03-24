
# get target panel file
from get_files import get_kgxref, get_chr_data, get_sequence
from Bio.Seq import Seq
from Bio.Blast import NCBIWWW, NCBIXML
import json

# input = panel, ref_db
print('Enter target panel file name')
panel_name = input()

panel_data = []
other_data = []

with open(panel_name, 'r') as input_file:
	for line in input_file:
		panel_data.append(line.strip().split()[:3])
		other_data.append(line.strip().split()[3:])

ref_db = other_data[0][4].split('=')[1]

# generate kgXref file:
kgXref = {}
get_kgxref('genes_ref.txt', ref_db)

with open('genes_ref.txt', 'r') as genes_ref:
	for line in genes_ref:
		line_list = line.strip().split('\t')
		kgXref[line_list[0]] = line_list[4]

# extract necessary chromosomes data
# panel_chromosomes = tuple(set([panel_data[i][0].strip('chr') for i in range(1, len(panel_data))]))
# for i in range(len(panel_chromosomes)):
# 	get_chr_data(panel_chromosomes[i], ref_db)

def search_gene(line, chr_num, start, end):
	with open(f'{chr_num}_data.json') as data:
		chr_data = json.load(data)
	for i in range(len(chr_data['knownGene'])):
		gene_exons = {
				'starts': [point for point in chr_data['knownGene'][i]['exonStarts'][:-1].split(',')],
				'ends': [point for point in chr_data['knownGene'][i]['exonEnds'][:-1].split(',')]
					}
		for v in range(len(gene_exons['starts'])):
			if int(start) >= int(gene_exons['starts'][v]) and int(end) <= int(gene_exons['ends'][v]):
				line.append([chr_data['knownGene'][i]['name'], v + 1])
		if i == len(chr_data['knownGene']) - 1 and len(line) == 3: # highlight undefined genes
			line.append('not defined')

def compare_data(line, kgXref_key, kgXref_value):
	if line[3] == 'not defined':
		pass

	for i in range(len(line)):
		if line[i][0] == kgXref_key:
			line[i][0] = kgXref_value

def search_homologue(sequence):
	result_handle = NCBIWWW.qblast('blastn', 'nt', sequence)
	blast_records = NCBIXML.parse(result_handle)
	for b in blast_records:
		for alignment in b.alignments:
			for hsp in alignments.hsp:
				print(alignment.title)
				print(hsp.expect)
				print(hsp.match[0:15] + '...')


print('\n*** PROCESSING ***')
print('Doing Task 1 (T1): Identification of genes and their exons')
# identify gene and exon
for line in panel_data[1:]:
	search_gene(line, line[0], line[1], line[2])
	for key, value in kgXref.items():
		compare_data(line, key, value)
print('T1. Found Genes')
print('T1. Identified Gene Names')

# rewrite data to output file
print('T1. Rewriting genes to panel file. Output file name: "panel_output.bed"')
panel_output1 = []
for line in panel_data[1:]:
	panel_output1.extend([line[:3]])

panel_output2 = []
for line in panel_data[1:]:
	if line[3] == 'not defined':
		panel_output2.append(line[3])
	else:
		temp_line = list(set([tuple(item) for item in line[3:]]))
		new_line = ';'.join(str(i) for i in temp_line)
		panel_output2.append(new_line)

# unite data
for i in range(len(panel_output1)):
	panel_output1[i].append(panel_output2[i])

title = panel_data[0] + other_data[0]
with open('panel_output.bed', 'w') as output_file:
	output_file.write(('\t').join(panel_data[0] + other_data[0]))
	for i in range(1, len(other_data)):
		output_line = panel_output1[i - 1] + other_data[i]
		output_file.write('\t'.join(output_line) + '\n')
	output_file.close()

#### CODE FOR REWRITING DATA TO THE ORIGINAL FILE ####
print('Task 1 done')

print('Doing Task 2 (T2): Search for homologue regions')

#### CODE FOR IDENTIFICATION OF HOMOLOGUE REGIONS AND WRITING THEM TO NEW FILE ####
# do that using BioPython
print('Search may take some time, please wait')
for line in panel_data[1:]:
	sequence = Seq(get_sequence(ref_db, line[0], line[1], line[2])) # Wrapped requested sequence into BioPython object
	output = search_homologue(sequence)
print(output)
