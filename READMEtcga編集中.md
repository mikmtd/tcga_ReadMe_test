# tcga

The Cancer Genome Atlas Program (TCGA) is a program that provides a vast amount of genetic data to investigate genetic mutations, expression patterns, and epigenetic changes in various types of cancer.

## tcga Conversion with RDF-config

### RDF config (senbero)

RDF-config is a tool to generate SPARQL queries, a schema diagram, and files required for [Grasp](https://github.com/dbcls/grasp), [TogoStanza](http://togostanza.org/) and ShEx validator from the simple YAML-based configuration files (see the [specification](./doc/spec.md)).

### SPECIFICATION

* [English version](./doc/spec.md)
* [Japanese version](./doc/spec_ja.md)

## USAGE

### Installation

```
% git clone https://github.com/dbcls/rdf-config.git
% cd rdf-config
% bundle install
```

## Generate RDF or JSON-LD

### Data set for conversion

- convert.yaml
- model.yaml
- prefix.yaml
- endpoint.yaml
- schema.yaml
- sparql.yaml
- stanza.yaml


### Edit convert.yaml

Define rules (procedures) for generating RDF and JSON-LD from CSV and TSV files, and describe them in YAML format.

Tips
- The top-level key (e.g., TcgaFiles:) should be defined as a list item by adding a '-'.
- Indentation should be done with exactly 2 half-width spaces.
- Include - subject and - objects.
- Confirm the path for - source. 

![tcga convert.yaml](./doc/figure/convert.yaml.png)

To generate RDF or JSON-LD from CSV, XML, or JSON files, run rdf-config with the --convert option.

```
% rdf-config --config [directory of the configuration file] --convert [--format output format]
```

To generate Turtle
```
% bundle exec rdf-config --config config/tcga --convert --format turtle > config/tcga/output.ttl
```

To generate JSON-LD
```
% bundle exec rdf-config --config config/tcga --convert --format json-ld > config/tcga/output.json
```

### Generate schema ascii art

```
% bundle exec rdf-config --config config/tcga --senbero
TcgaFiles [tcgaf:TcgaFiles] (tcgaf:1)
    |-- tcgaf:file_id
    |       `-- file_id (tcgaf:a9de4ee0-bf86-482...)
    |-- tcgaf:file_name
    |       `-- file_name ("TCGA_LUSC.eaf3905...")
    |-- tcgaf:file_size
    |       `-- file_size (401704810042)
    |-- tcgaf:data_type
    |       `-- data_type ("Annotated Somatic...")
    |-- tcgaf:data_category
    |       `-- data_category ("Simple Nucleotide...")
    |-- tcgaf:data_format
    |       `-- data_format ("VCF")
    |-- tcgaf:experimental_strategy
    |       `-- experimental_strategy ("WXS")
    |-- tcgaf:platform
    |       `-- platform ("Affymetrix SNP 6.0")
    |-- tcgaf:access
    |       `-- access ("controlled")
    |-- tcgaf:case_id
    |       `-- case_id (tcgaa:dbece124-c042-4ad...)
    `-- tcgaf:project_id
            `-- project_id (tcgap:TCGA-LUSC)
TcgaManifeset [tcgam:TcgaManifest] (tcgam:1)
    |-- tcgam:mani_id
    |       `-- mani_id (tcgam:a9de4ee0-bf86-482...)
    |-- tcgam:mani_filename
    |       `-- mani_filename ("TCGA_LUSC.eaf3905...")
    |-- tcgam:mani_md5
    |       `-- mani_md5 ("d3ee6b811a08c6e3c...")
    |-- tcgam:mani_size
    |       `-- mani_size (401704810042)
    `-- tcgam:mani_state
   ...
(Partial view)

```

### Generate schema diagram

```
% bundle exec rdf-config --config config/tcga --schema > tcga.svg
```

[tcga schema](./doc/figure/tcga.svg)
