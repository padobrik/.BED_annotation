import requests
import json

# get kgXref file
def get_kgxref(output: str):
	ref_link = 'https://genome.ucsc.edu/cgi-bin/hgTables'
	req_body = {
		'hgsid': '1309789803_QZsv668MTZBAeDgcSxj8075rUOsC',
		'jsh_pageVertPos': '0',
		'clade': 'mammal',
		'org':	'Human',
		'db': 'hg19',
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

	with open(output, 'wb') as s:
	    s.write(content)
	    s.close()

def get_chr_data(chr_num):
	
	chr_data = requests.get(f'https://api.genome.ucsc.edu/getData/track?genome=hg19;track=knownGene;chrom=chr{chr_num}').json()

	with open(f'chr{chr_num}_data.json', 'w') as s:
		json.dump(chr_data, s)
		s.close()