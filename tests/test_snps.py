"""
Copyright (C) 2018 Andrew Riha

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import pandas as pd
import pytest


def create_snp_df(rsid, chrom, pos, genotype):
    df = pd.DataFrame({'rsid': rsid, 'chrom': chrom, 'pos': pos, 'genotype': genotype},
                      columns=['rsid', 'chrom', 'pos', 'genotype'])
    df = df.set_index('rsid')
    return df


@pytest.fixture(scope='module')
def snps_discrepant_pos():
    return create_snp_df(rsid=['rs3094315'], chrom=['1'], pos=[1], genotype=['AA'])


@pytest.fixture(scope='module')
def snps_GRCh38():
    from lineage.snps import SNPs
    return SNPs('tests/input/GRCh38.csv')


@pytest.fixture(scope='module')
def snps():
    from lineage.snps import SNPs
    return SNPs('tests/input/chromosomes.csv')


@pytest.fixture(scope='module')
def snps_none():
    from lineage.snps import SNPs
    return SNPs(None)


def test_assembly_name(snps_GRCh38):
    assert snps_GRCh38.assembly_name == 'GRCh38'


def test_snp_count(snps):
    assert snps.snp_count == 5


def test_chromosomes(snps):
    assert snps.chromosomes == ['1', '2', '3', '5', 'MT']


def test_chromosomes_summary(snps):
    assert snps.chromosomes_summary == '1-3, 5, MT'


def test__read_raw_data(snps_none):
    assert snps_none.snps is None
    assert snps_none.source == ''


def test__lookup_assembly_with_snp_pos_None(snps_discrepant_pos):
    from lineage.snps import detect_assembly
    assert detect_assembly(snps_discrepant_pos) is None


def test_get_assembly_name_None():
    from lineage.snps import get_assembly_name
    assert get_assembly_name(None) is ''