# Cantonese-English Parallel Corpus (extracted from the ABC Dictionary)

This project is a Cantonese-English Parallel Corpus extracted from the ABC Cantonese-English Comprehensive Dictionary. It consists of around 14,000 sentences. The aim of this project is to provide high quality parallel data for developing Cantonese-English translation models, in order to facilitate the advancement of Cantonese NLP research.

## Data

Due to copyright issues, the extracted corpus cannot be directly published on GitHub. You can download it through the following two methods.

### Google Drive

The parallel corpus is saved in two files, [`yue.txt`](https://drive.google.com/file/d/1WJ7bWgIhus-geMqwWoyt_POalgrJxuwj/view?usp=sharing) and [`en.txt`](https://drive.google.com/file/d/1XbO6POEbjeiYuIZe_SN9ECv571IRyz2T/view?usp=sharing).

To download the files, simply use the following commands:

```sh
gdown 1WJ7bWgIhus-geMqwWoyt_POalgrJxuwj  # yue.txt
gdown 1XbO6POEbjeiYuIZe_SN9ECv571IRyz2T  # en.txt
```

Additionally, you can also download the title list ([`titles.txt`](https://drive.google.com/file/d/1jGvmg2c-p3WnJg7jUpcmbW0h8XjZoNXm/view?usp=sharing)) and raw data ([`Wenlin+Dictionaries-20221101051901.xml`](https://drive.google.com/file/d/142F7zXUBniB6qnbo3jmLWIVV_UbZbxkZ/view?usp=sharing)), which are the intermediate results of the build process.

### Build from source

This repository provides scripts for building the corpus from source. You can re-run these scripts to obtain the latest version of the corpus. It is worth noting that the new version of the corpus will be different from the one provided above. Therefore, if you are using this corpus in your research, please use the version provided above if possible.

Steps to build the corpus from source:

1. Register an account on the [Wenlin Dictionaries Wiki](https://wenlin.co/);
1. Edit `scrape.py` to add your credentials on the Wenlin Dictionaries Wiki;
1. Run `scrape.py` to get a list of the titles of all pages under the `Jyut` category. The result is written to `titles.txt`;
1. Go to the [export page](https://wenlin.co/wow/Special:Export) to export all the data to an XML file;
1. Run `extract.py` to build the corpus;
1. Manually validate the build results.

## Main difference from the original data

1\. Modification of the selection of Chinese characters

I change the selection of Chinese characters to the modern Hong Kong convention or the [words.hk](https://words.hk/) convention, in order to accurately reflect the generally accepted habit of the selection of Chinese characters of Hong Kong people. For example:

- 床 -> 牀
- 著 -> 着, as in 着衫
- 𡃶 -> 錫, as in 錫佢一啖
- 𧨾 -> 氹, as in 氹阿媽開心
- 𧵳 -> 蝕, as in 生意蝕本
- 杧 -> 芒, as in 芒果
- 𠶧 -> 掂, as in 橫掂

2\. Add full stops at the end of the sentences

The original dictionary does not include a full stop at the end of a declarative sentence, as is the case in both Cantonese and English. This can be confusing because both Cantonese and English use a full stop as a marker at the end of a declarative sentence.

3\. Remove non-informative spaces

I remove all the spaces between Chinese characters and English letters, as well as the spaces between Chinese characters and digits. Spaces between two English words are not removed.

For example, the space in the following sentence is removed:

```
呢場戲NG 咗兩次
```

While the space in this sentence is not:

```
佢積極keep fit，身材好咗好多。
```

This is because the spaces between Chinese characters and English letters and Chinese characters and numbers do not affect the understanding of sentences and can be easily converted to and from each other by rules when needed.

4\. TODO: ...
