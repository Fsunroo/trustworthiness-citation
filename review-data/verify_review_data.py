"""Verify the manuscript's coverage data from the coded report and evaluation inputs."""
from collections import Counter, defaultdict
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parent
CODES = ('Y', 'N', 'NR', 'U', 'UA', 'NA')


def read(filename):
    with (DATA / filename).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def aggregate(evaluations):
    applicable = {row['code'] for row in evaluations if row['applicability'] == 'applicable'}
    unclear = any(row['applicability'] == 'unclear' for row in evaluations)
    if 'Y' in applicable:
        return 'Y', 'applicable'
    if applicable:
        if unclear:
            applicable.add('U')
        return next((code for code in ('U', 'UA', 'NR', 'N') if code in applicable), 'U'), 'applicable'
    return ('U', 'unclear') if unclear else ('NA', 'not_applicable')


def check_coverage(expected, observations):
    states = Counter(code for code, _ in observations)
    applicability = Counter(app for _, app in observations)
    lower = applicability['applicable']
    upper = lower + applicability['unclear']
    computed = dict(total=len(observations), **{code: states[code] for code in CODES},
                    known_applicable=lower, unknown_applicability=applicability['unclear'],
                    denominator_min=lower, denominator_max=upper)
    for key, value in computed.items():
        assert int(expected[key]) == value, (expected['level'], expected['indicator'], key)
    for key, denominator in [
        ('coverage_Y_over_known_applicable', lower),
        ('coverage_lower_bound', upper),
        ('coverage_upper_bound', lower),
    ]:
        expected_value = expected[key]
        if denominator:
            assert float(expected_value) == round(states['Y'] / denominator, 6), (expected, key)
        else:
            assert not expected_value, (expected, key)


def check_geography(article_ids):
    assignments = read('author_affiliation_country_assignments.csv')
    assert {row['article_id'] for row in assignments} == article_ids
    locations = defaultdict(set)
    for row in read('author_affiliation_country_counts.csv'):
        ids = set(row['article_ids'].split(';'))
        assert ids <= article_ids
        assert len(ids) == int(row['reports'])
        assert round(len(ids) / 44 * 100, 2) == float(row['percent_of_44'])
        for article in ids:
            locations[article].add(row['country_or_territory'])
    assert set(locations) == article_ids
    assert all(locations[row["article_id"]] == set(row["countries"].split(";")) for row in assignments)
    assert sum(map(len, locations.values())) == 46
    assert len({loc for group in locations.values() for loc in group}) == 14


def main():
    evaluations = read('evaluation_characteristics.csv')
    primary = {row['experiment_id'] for row in evaluations if row['primary_scope'] == 'True'}
    linked = {row['experiment_id'] for row in evaluations}
    assert len(evaluations) == len(linked) == 150 and len(primary) == 148
    articles = {row['article_id'] for row in read('corpus_characteristics.csv')}
    assert len(articles) == 44 and 'J0176' not in articles
    items = read('item_responses.csv')
    assert len(items) == 6864 and len({(r['article_id'], r['item_id']) for r in items}) == 6864
    assert Counter(r['article_id'] for r in items) == dict.fromkeys(articles, 156)
    assert len(read('descriptive_result_ledger.csv')) == 784
    assert {r['article_id'] for r in read('included_report_funding.csv')} == articles
    assert {r['article_id'] for r in read('table_s1_characteristics.csv')} == articles

    matrix = read('evaluation_indicator_matrix.csv')
    indicators = {row['indicator'] for row in matrix}
    assert len(indicators) == 30 and len(matrix) == 4500
    assert Counter(row['experiment_id'] for row in matrix) == dict.fromkeys(linked, 30)
    report_matrix = read('article_indicator_matrix.csv')
    reports = {(r['article_id'], r['indicator']): (r['code'], r['applicability']) for r in report_matrix}
    assert len(report_matrix) == len(reports) == 1320
    grouped = defaultdict(list)
    for row in matrix:
        indicator = row['indicator']
        family = row['task_family']
        grouped['linked', 'all', indicator].append(row)
        if row['experiment_id'] in primary:
            grouped['primary', 'all', indicator].append(row)
            grouped['primary', family, indicator].append(row)

    for source, filename in [
        ('primary', 'article_coverage.csv'), ('primary', 'experiment_coverage.csv'),
        ('primary', 'task_family_coverage.csv'), ('linked', 'all_linked_coverage.csv'),
    ]:
        for expected in read(filename):
            indicator, family = expected['indicator'], expected['task_family']
            data = grouped[source, family, indicator]
            if expected['level'] == 'article':
                by_report = defaultdict(list)
                for row in data:
                    by_report[row['article_id']].append(row)
                if family == 'all':
                    for article in articles:
                        by_report.setdefault(article, [])
                states = {article: aggregate(rows) for article, rows in by_report.items()}
                if source == 'primary' and family == 'all':
                    assert all(reports[article, indicator] == state for article, state in states.items())
                observations = list(states.values())
            else:
                observations = [(row['code'], row['applicability']) for row in data]
            check_coverage(expected, observations)

    flow_rows = read('figure_1_flow_counts.csv')
    flow = {r['category']: int(r['n']) for r in flow_rows if r['stage'] == 'selection'}
    assert sum(int(r['n']) for r in flow_rows if r['stage'] == 'source_occurrences') == 1864
    assert 1864 + flow['Manually identified'] == flow['Identified records']
    assert flow['Identified records'] - flow['Duplicates removed'] == flow['Records screened']
    assert flow['Records screened'] - flow['Excluded at screening'] == flow['Reports sought']
    assert flow['Reports sought'] - flow['Reports not retrieved'] == flow['Reports assessed']
    assert flow['Reports assessed'] - flow['Full-text exclusions'] == flow['Included reports']
    assert sum(int(r['n']) for r in flow_rows if r['stage'] == 'full_text_exclusion') == flow['Full-text exclusions']
    check_geography(articles)
    print('Verified 44 reports, 150 evaluations, 6,864 checklist responses, 784 estimates, all coverage tables, flow arithmetic, and geographic counts.')


if __name__ == '__main__':
    main()
