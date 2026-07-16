from python_tsp.distances.data_processing import process_input


def test_1d_array_becomes_2d():
    source = [1.0, -1.0]
    destination = [5.0, -5.0]

    sources_out, destinations_out = process_input(source, destination)

    assert len(sources_out) == 1
    assert len(sources_out[0]) == 2
    assert len(destinations_out) == 1
    assert len(destinations_out[0]) == 2


def test_no_destinations_become_sources():
    sources = [[1.0, -1.0], [2.0, -2.0], [3.0, -3.0], [4.0, -4.0]]

    sources_out, destinations_out = process_input(sources)

    assert sources_out == sources
    assert destinations_out == sources
