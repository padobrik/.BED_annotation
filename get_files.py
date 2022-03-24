import requests
import json

# get kgXref file
def get_kgxref(output: str, db: str):
	ref_link = 'https://genome.ucsc.edu/cgi-bin/hgTables'
	req_body = {
		'hgsid': '1309789803_QZsv668MTZBAeDgcSxj8075rUOsC',
		'jsh_pageVertPos': '0',
		'clade': 'mammal',
		'org':	'Human',
		'db': db,
		'hgta_group': 'genes',
		'hgta_track': 'knownGene',
		'hgta_table': 'kgXref',
		'hgta_fs.check.hg19.kgXref.kgID': 'on',
		'hgta_fs.check.hg19.kgXref.geneSymbol':	'on',
		'position': 'chr1:113,454,470-113,498,975',
		'hgta_regionType': 'genome',
		'hgta_outputType': 'primaryTable',
		'boolshad.sendToGalaxy': '0',
		'boolshad.sendToGreat': '0',
		'hgta_outFileName': 'id_to_symbol.txt',
		'hgta_outSep': 'tab',
		'hgta_compressType': 'none',
		'hgta_doTopSubmit': 'get+output'
		}
	kgXref = requests.post(ref_link, req_body)
	content = kgXref.content

	with open(f'{output}', 'wb') as s:
	    s.write(content)
	    s.close()

# get hg19 chromosome json
def get_chr_data(chr_num, db: str):
	chr_data = requests.get(f'https://api.genome.ucsc.edu/getData/track?genome={db};track=knownGene;chrom=chr{chr_num}').json()

	with open(f'chr{chr_num}_data.json', 'w') as s:
		json.dump(chr_data, s)
		s.close()

def get_sequence(db, chr_num, start, end):
	sequence_data = requests.get(f'https://api.genome.ucsc.edu/getData/sequence?genome={db};chrom={chr_num};start={start};end={end}').json()

	return sequence_data['dna'].upper()